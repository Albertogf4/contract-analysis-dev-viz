import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

from .config import Settings
from .embeddings import OpenAIEmbeddingClient, OpenAILLMClient
from .vectorstore import ChromaVectorStore
from .rag import DocumentIndexer, RAGPipeline
from .graph_builder import KnowledgeGraphBuilder
from .knowledge_graph import KnowledgeGraphStore
from .graph_context import GraphContextRetriever


def create_app() -> Flask:
    app = Flask(__name__)

    # ---------- CORS Configuration ----------
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:3001"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # ---------- Initialize core services ----------
    settings = Settings()

    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.chroma_db_dir, exist_ok=True)
    os.makedirs(settings.graph_dir, exist_ok=True)

    embedding_client = OpenAIEmbeddingClient(settings)
    llm_client = OpenAILLMClient(settings)
    vector_store = ChromaVectorStore(settings, embedding_client)

    graph_store = KnowledgeGraphStore(settings)
    graph_builder = KnowledgeGraphBuilder(settings)
    graph_context_retriever = GraphContextRetriever(  
        settings=settings,
        graph_store=graph_store,
        embedder=embedding_client,
    )

    indexer = DocumentIndexer(settings, vector_store, graph_builder=graph_builder, graph_store=graph_store)
    rag_pipeline = RAGPipeline(settings, vector_store, llm_client, graph_context_retriever=graph_context_retriever)

    # ---------- Routes ----------

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    @app.route("/api/upload", methods=["POST"])
    def upload_document():
        if "file" not in request.files:
            return jsonify({"error": "No file part in the request"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        original_name = secure_filename(file.filename)
        # Use a uuid prefix so we know document_id from filename
        document_id = str(uuid.uuid4())
        saved_filename = f"{document_id}_{original_name}"
        file_path = os.path.join(settings.upload_dir, saved_filename)
        file.save(file_path)

        # Index PDF in vector store
        doc_id_from_indexer = indexer.index_pdf(file_path, document_id=document_id)

        # NOTE: doc_id_from_indexer == document_id if you propagate it
        # from the filename; here the parser generates its own id.
        # To keep them aligned you can pass document_id into parse_pdf_to_document.
        # For now we just return the one from the indexer.
        return jsonify(
            {
                "document_id": doc_id_from_indexer,
                "filename": original_name,
            }
        ), 200

    @app.route("/api/query", methods=["POST"])
    def query_document():
        try:
            data = request.get_json(force=True)
            question = data.get("question")
            document_id = data.get("document_id")

            if not question or not document_id:
                return jsonify({"error": "Missing 'question' or 'document_id'"}), 400

            result = rag_pipeline.answer_question(question, document_id)

            return jsonify(
                {
                    "answer": result.answer,
                    "contexts": [
                        {
                            "chunk_id": c.chunk_id,
                            "document_id": c.document_id,
                            "filename": c.filename,
                            "page_number": c.page_number,
                            "start_char": c.start_char,
                            "end_char": c.end_char,
                            "score": c.score,
                            "text": c.text,
                        }
                        for c in result.context_chunks
                    ],
                }
            ), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/documents/<document_id>/file", methods=["GET"])
    def get_document_file(document_id: str):
        """
        Very simple implementation: scan upload_dir for a file whose
        name starts with document_id + underscore.
        In production: small DB mapping doc_id -> filename.
        """
        for fname in os.listdir(settings.upload_dir):
            if fname.startswith(f"{document_id}_"):
                return send_from_directory(
                    directory=settings.upload_dir,
                    path=fname,
                    as_attachment=True,
                )

        return jsonify({"error": "Document not found"}), 404
    
    # ---------- Knowledge graph endpoints ----------
    @app.route("/api/graph/<document_id>", methods=["GET"])
    def get_full_graph(document_id: str):
        graph = graph_store.load_graph(document_id)
        if graph is None:
            return jsonify({"error": "Graph not found"}), 404
        return jsonify(graph.to_dict()), 200

    @app.route("/api/graph/<document_id>/node/<node_id>", methods=["GET"])
    def get_node_subgraph(document_id: str, node_id: str):
        subgraph = graph_store.get_node_and_neighbors(document_id, node_id)
        if subgraph is None:
            return jsonify({"error": "Node or graph not found"}), 404
        return jsonify(subgraph), 200

    return app
