# app/embeddings.py
from typing import List
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

    def generate_answer(self, question: str, context_blocks: List[str]) -> str:
        """
        Basic RAG-style prompt: passes the retrieved chunks as context.
        """
        system_prompt = (
            "You are a helpful assistant that answers questions based only on the provided context. "
            "If the answer cannot be found in the context, say that you don't know."
        )

        context_text = "\n\n---\n\n".join(context_blocks)

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Context:\n{context_text}\n\n"
                    f"Question: {question}\n\n"
                    "Answer concisely and cite the relevant sections by page number if possible."
                ),
            },
        ]

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return resp.choices[0].message.content.strip()
