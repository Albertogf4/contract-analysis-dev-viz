# app/embeddings.py
from typing import List, Optional
from openai import OpenAI

from .config import Settings


class OpenAIEmbeddingClient:
    def __init__(self, settings: Settings):
        self.client = OpenAI(api_key=settings.openai_api_key or None)
        self.model = settings.embedding_model

    def embed(self, texts: List[str]) -> List[List[float]]:
        resp = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [d.embedding for d in resp.data]


class OpenAILLMClient:
    def __init__(self, settings: Settings):
        self.client = OpenAI(api_key=settings.openai_api_key or None)
        self.model = settings.llm_model

    def generate_answer(self, question: str, context_blocks: List[str], graph_context: Optional[str] = None,) -> str:
        """
        Basic RAG-style prompt: passes the retrieved chunks as context. + optional graph content
        """
        system_prompt = (
            "You are a helpful assistant that answers questions based only on the provided context. "
            "Use both the document excerpts and the knowledge graph information when it is helpful. "
            "If the answer cannot be found in the context, say that you don't know."
        )

        context_text = "\n\n---\n\n".join(context_blocks)

        graph_section = ""
        if graph_context:
            graph_section = (
                "\n\n[Knowledge Graph]\n"
                "The following is a list of key entities, concepts and relations extracted from the document:\n"
                f"{graph_context}"
            )
        
        user_content = (
            f"Context from the document (text chunks):\n{context_text}"
            f"{graph_section}\n\n"
            f"Question: {question}\n\n"
            "Answer concisely, explaining the reasoning when useful."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return resp.choices[0].message.content.strip()
