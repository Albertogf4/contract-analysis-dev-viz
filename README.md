# 📄 Contract Analysis - Document Q&A with Knowledge Graphs

An AI-powered document analysis platform for contract analysis that enables searchable, traceable document querying with structured knowledge extraction and interactive visualization.

## 🎯 Overview

This project provides a comprehensive pipeline for:

- **PDF Document Ingestion & Parsing**: Upload contracts/documents and automatically extract text
- **Vector-based Semantic Search**: Using embeddings and ChromaDB for efficient retrieval
- **Knowledge Graph Generation**: Automatic extraction of entities and relationships from documents
- **Interactive Graph Visualization**: Explore document structure through an interactive knowledge graph drawer
- **RAG-powered Q&A**: Ask natural language questions and get answers with citations
- **Custom Embedding Adapter Training**: Fine-tune embedding models for domain-specific retrieval

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Next.js Frontend                         │
│  (Document Upload, Chat Interface, Knowledge Graph Viewer)   │
└──────────────────────────┬──────────────────────────────────┘
                           │ REST API
┌──────────────────────────▼──────────────────────────────────┐
│                    Flask Backend API                         │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────┐   │
│  │ PDF Parser  │  │ RAG Pipeline│  │ Knowledge Graph    │   │
│  │ (PyPDF2)    │  │ (OpenAI)    │  │ Builder (LangChain)│   │
│  └─────────────┘  └─────────────┘  └────────────────────┘   │
│                          │                                   │
│              ┌───────────▼──────────┐                       │
│              │   ChromaDB Vector    │                       │
│              │       Store          │                       │
│              └──────────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
contract-analysis-dev-viz/
├── backend/                    # Flask Backend API
│   ├── main.py                 # Application entry point
│   └── app/
│       ├── api.py              # REST API endpoints
│       ├── config.py           # Settings and configuration
│       ├── models.py           # Pydantic data models
│       ├── preprocessing.py    # PDF parsing (PyPDF2)
│       ├── chunking.py         # Text chunking logic
│       ├── embeddings.py       # OpenAI embedding client
│       ├── vectorstore.py      # ChromaDB integration
│       ├── rag.py              # RAG pipeline & document indexer
│       ├── graph_builder.py    # LLM-based knowledge graph extraction
│       └── knowledge_graph.py  # Graph data structures & storage
│
├── document-q-and-a-ui/        # Next.js Frontend
│   ├── app/
│   │   ├── page.tsx            # Main page
│   │   ├── layout.tsx          # App layout
│   │   └── api/                # API routes (proxy to backend)
│   │       ├── upload/         # File upload endpoint
│   │       ├── query/          # Q&A endpoint
│   │       └── graph/          # Knowledge graph endpoints
│   │           └── [documentId]/
│   │               ├── route.ts        # Full graph endpoint
│   │               └── node/[nodeId]/  # Node details endpoint
│   ├── components/
│   │   └── document-qa/        # Main UI components
│   │       ├── document-qa-app.tsx
│   │       ├── chat-panel.tsx
│   │       ├── document-panel.tsx
│   │       ├── knowledge-graph-view.tsx    # Interactive graph SVG
│   │       ├── knowledge-graph-drawer.tsx  # Resizable side drawer
│   │       ├── knowledge-graph-button.tsx  # Toggle button
│   │       └── node-details.tsx            # Node info panel
│   ├── hooks/
│   │   └── use-knowledge-graph.ts  # Graph data fetching hook
│   └── lib/types/
│       └── knowledge-graph.ts      # TypeScript interfaces
│
├── train/                      # Embedding Adapter Training
│   ├── adapters/               # Trained adapter checkpoints
│   └── emb_adapter/
│       ├── config.py           # Training configuration
│       ├── models/
│       │   ├── base_encoder.py # SentenceTransformer wrapper
│       │   └── linear_adapter.py # Query-only linear adapter
│       ├── data/
│       │   ├── loaders.py      # PDF chunking utilities
│       │   ├── datasets.py     # TripletDataset for training
│       │   └── synthetic_labels.py # LLM-based question generation
│       ├── training/
│       │   ├── trainer.py      # Training loop with triplet loss
│       │   └── scheduler.py    # Learning rate scheduling
│       ├── retrieval/
│       │   ├── vectordb.py     # ChromaDB manager
│       │   └── evaluator.py    # Evaluation metrics
│       └── scripts/
│           ├── build_index.py  # Index creation & synthetic data
│           ├── train_adapter.py # Adapter training script
│           └── eval_adapter.py # Evaluation script
│
├── chroma_db/                  # Vector database storage
├── graphs/                     # Knowledge graph JSON files
├── uploads/                    # Uploaded PDF documents
└── data/                       # Sample documents & training data
    ├── Documento_Financiacion_Modelo.pdf  # Example financing contract
    ├── train.json
    └── validation.json
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- pnpm (recommended) or npm
- OpenAI API Key

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables:**
   ```bash
   export OPENAI_API_KEY="your-api-key"
   export EMBEDDING_MODEL="text-embedding-3-small"  # optional
   export LLM_MODEL="gpt-5-mini"                   # optional
   export PORT=5328                                  
   ```

3. **Run the backend:**
   ```bash
   python backend/main.py
   ```
   The API will be available at `http://localhost:5328`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd document-q-and-a-ui
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Access the application:**
   Open [http://localhost:3000](http://localhost:3000)

---

## 📖 Usage Example: Analyzing a Financing Contract

This example demonstrates how to use the platform with the included sample document `data/Documento_Financiacion_Modelo.pdf` (a Spanish fake financing contract template).

### Step 1: Upload the Document

1. Open the application at `http://localhost:3000`
2. Click on **"Choose File"** or drag & drop the PDF into the upload zone
3. Select `data/Documento_Financiacion_Modelo.pdf`
4. Wait for the status to change from "Processing" to **"Ready"**

### Step 2: Ask Questions

Once the document is ready, you can ask questions in Spanish (or any language). Here are example questions for the financing contract:

| Example Question | What it Retrieves |
|------------------|-------------------|
| `¿Cuál es el importe del préstamo?` | The loan amount specified in the contract is 7,5 MM EUR|
| `¿Cuál es el tipo de interés aplicable?` | The applicable interest rate is EURIBOR +  3,25% |
| `¿Cuáles son las condiciones de amortización?` | Repayment terms and schedule |
| `¿Qué garantías se exigen en el contrato?` | Required guarantees/collateral |
| `¿Cuáles son las causas de vencimiento anticipado?` | Early termination clauses |

### Step 3: Explore the Knowledge Graph

1. Click the **Network icon** (🔗) in the header to open the Knowledge Graph drawer
2. The graph displays extracted entities and their relationships:
   - **Nodes**: Key concepts like "Prestatario" (Borrower), "Prestamista" (Lender), "Tipo de Interés" (Interest Rate)
   - **Edges**: Relationships like "firma", "establece", "requiere"
3. Click on any node to see its details and connected entities
4. Resize the drawer by dragging the left edge

### Example API Interaction

You can also interact directly with the API:

```bash
# Upload a document
curl -X POST http://localhost:5328/api/upload \
  -F "file=@data/Documento_Financiacion_Modelo.pdf"

# Response:
# {"document_id": "abc123-...", "filename": "Documento_Financiacion_Modelo.pdf"}

# Ask a question
curl -X POST http://localhost:5328/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "¿Cuál es el importe del préstamo?",
    "document_id": "abc123-..."
  }'

# Get the knowledge graph
curl http://localhost:5328/api/graph/abc123-...
```

### Example Response

```json
{
  "answer": "El importe del préstamo es de [AMOUNT] euros, según se establece en la cláusula primera del contrato de financiación...",
  "contexts": [
    {
      "chunk_id": "chunk-uuid",
      "document_id": "abc123-...",
      "filename": "Documento_Financiacion_Modelo.pdf",
      "page_number": 1,
      "start_char": 150,
      "end_char": 1150,
      "score": 0.23,
      "text": "PRIMERA. IMPORTE Y DESTINO DEL PRÉSTAMO..."
    }
  ]
}
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/upload` | Upload a PDF document |
| `POST` | `/api/query` | Ask a question about a document |
| `GET` | `/api/documents/<id>/file` | Download document file |
| `GET` | `/api/graph/<document_id>` | Get full knowledge graph |
| `GET` | `/api/graph/<document_id>/node/<node_id>` | Get node with 1-hop neighbors |

### Knowledge Graph Response Structure

```json
{
  "document_id": "uuid",
  "nodes": [
    {
      "id": "prestatario",
      "label": "Prestatario",
      "type": "entity",
      "description": "Persona física o jurídica que recibe el préstamo"
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "prestatario",
      "target": "contrato",
      "relation": "firma"
    }
  ]
}
```

---

## 🧠 Embedding Adapter Training

The project includes a training pipeline for fine-tuning embedding models using a query-only linear adapter approach with triplet loss.

### Training Workflow

1. **Build Index & Generate Synthetic Data:**
   ```bash
   python -m train.emb_adapter.scripts.build_index \
     --pdf ./data/Documento_Financiacion_Modelo.pdf \
     --collection financing_collection \
     --db_path ./chroma_db \
     --reset
   ```

2. **Train the Adapter:**
   ```bash
   python -m train.emb_adapter.scripts.train_adapter \
     --train_json ./data/train.json \
     --negatives_pdf ./data/nvidia_10k.pdf \
     --out ./train/adapters/adapter.pth \
     --epochs 30 --batch_size 32 --lr 3e-3 --margin 1.0
   ```

3. **Evaluate Performance:**
   ```bash
   # Baseline (without adapter)
   python -m train.emb_adapter.scripts.eval_adapter \
     --val_json ./data/validation.json \
     --db_path ./chroma_db \
     --collection financing_collection \
     --k 10

   # With trained adapter
   python -m train.emb_adapter.scripts.eval_adapter \
     --val_json ./data/validation.json \
     --db_path ./chroma_db \
     --collection financing_collection \
     --k 10 \
     --adapter ./train/adapters/adapter.pth
   ```

### Key Training Features

- **Triplet Loss**: Uses anchor (query), positive (relevant chunk), and negative (random chunk) samples
- **Linear Adapter**: Lightweight query-only transformation layer (R^D → R^D)
- **Synthetic Data Generation**: LLM-generated questions for each document chunk
- **Evaluation Metrics**: Hit Rate@K and Mean Reciprocal Rank (MRR)

---

## ⚙️ Configuration

### Backend Configuration (`backend/app/config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `embedding_model` | `text-embedding-3-small` | OpenAI embedding model |
| `llm_model` | `gpt-5-mini` | OpenAI chat model |
| `top_k` | `4` | Number of chunks to retrieve |
| `chunk_size` | `1000` | Characters per chunk |
| `chunk_overlap` | `200` | Overlap between chunks |
| `graph_max_chars` | `12000` | Max chars for graph extraction |

### Training Configuration (`train/emb_adapter/config.py`)

| Setting | Default | Description |
|---------|---------|-------------|
| `base_encoder_name` | `all-MiniLM-L6-v2` | Base SentenceTransformer (384-dim) |
| `num_epochs` | `10` | Training epochs |
| `batch_size` | `32` | Batch size |
| `learning_rate` | `3e-3` | Learning rate |
| `margin` | `1.0` | Triplet loss margin |

---

## 🛠️ Tech Stack

### Backend
- **Flask** - REST API framework with CORS support
- **LangChain** - LLM orchestration for graph building
- **OpenAI API** - Embeddings (text-embedding-3-small) & chat completions (gpt-4.1-mini)
- **ChromaDB** - Persistent vector database with cosine similarity
- **PyPDF2** - PDF text extraction
- **Pydantic** - Data validation with dataclasses

### Frontend
- **Next.js 16** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS v4** - Styling
- **Radix UI** - Accessible component primitives
- **React Dropzone** - File uploads
- **Framer Motion** - Animations
- **Lucide React** - Icons

### Training
- **PyTorch** - Deep learning framework
- **SentenceTransformers** - Embedding models
- **LangChain** - Synthetic data generation with GPT

---

## 🎯 Project Objectives

This project was developed to:

1. Build an ingestion + parsing + chunking pipeline for contracts
2. Extract structured data (knowledge graphs) from contracts using LLMs
3. Create a hybrid knowledge base (graph + vector store)
4. Implement a RAG system for contract Q&A
5. Fine-tune embedding models for the financial domain
6. Provide an intuitive chat interface with visualization capabilities

