"""
Optional synthetic label generator. Requires OpenAI key in env (OPENAI_API_KEY).
Not used by training scripts unless you call it explicitly.
"""
from typing import List, Dict
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
import getpass
from pydantic import BaseModel, Field


LABEL_TMPL = """
You are an AI assistant tasked with generating a single, realistic question-answer pair based on a given document. The question should be something a user might naturally ask when seeking information contained in the document.

Given: {chunk}

Instructions:
1. Analyze the key topics, facts, and concepts in the given document, choose one to focus on.
2. Generate twenty similar questions that a user might ask to find the information in this document that does NOT contain any company name.
3. Use natural language and occasionally include typos or colloquialisms to mimic real user behavior in the question.
4. Ensure the question is semantically related to the document content WITHOUT directly copying phrases.
5. Make sure that all of the questions are similar to eachother. I.E. All asking about a similar topic/requesting the same information.


Be creative, think like a curious user, and generate your {questions_per_chunk} similar questions that would naturally lead to the given document in a semantic search. Ensure your response is a valid JSON object containing only the questions.


"""

class Question(BaseModel):
    question: str = Field(..., description="Generated question text")

class QuestionsOutput(BaseModel):
    questions: List[Question] = Field(..., description="List of generated questions")

def build_questions_chain(
    model: str = "gpt-5-nano",
    temperature: float = 1.0,
):
    if "OPENAI_API_KEY" not in os.environ:
        raise RuntimeError("OPENAI_API_KEY not set")

    llm = ChatOpenAI(temperature=temperature, model=model)
    prompt = ChatPromptTemplate.from_template(LABEL_TMPL)
    structured_llm = llm.with_structured_output(QuestionsOutput)
    chain = prompt | structured_llm
    return chain

# Ya no lo uso
def generate_questions_for_chunk(
        chunk: str, 
        model: str = "gpt-5-nano", 
        temperature: float = 1.0, 
        questions_per_chunk: int = 10
    ) -> List[str]:

    if "OPENAI_API_KEY" not in os.environ:
        raise RuntimeError("OPENAI_API_KEY not set")
    
    llm = ChatOpenAI(temperature=temperature, model=model)
    prompt = ChatPromptTemplate.from_template(LABEL_TMPL)
    structured_llm = llm.with_structured_output(QuestionsOutput)
    chain = prompt | structured_llm
    result = chain.invoke({
        "chunk": chunk,
        "questions_per_chunk": questions_per_chunk
    })
    questions = [q.question for q in result.questions]
    
    return questions

def build_supervision(
    chunks: List[str],
    questions_per_chunk: int = 10,
    model: str = "gpt-5-nano",
    temperature: float = 1.0,
    max_concurrency: int = 8,
) -> List[Dict[str, str]]:
    """Batch version: processes all chunks in parallel under the hood."""
    # Build chain once
    chain = build_questions_chain(model=model, temperature=temperature)

    # Prepare inputs for batch
    inputs = [
        {
            "chunk": ch,
            "questions_per_chunk": questions_per_chunk,
        }
        for ch in chunks
    ]

    # Run all in parallel (up to max_concurrency)
    results: List[QuestionsOutput] = chain.batch(
        inputs,
        config={"max_concurrency": max_concurrency},
    )

    # Flatten into [{"question": ..., "chunk": ...}, ...]
    pairs: List[Dict[str, str]] = []
    for ch, res in zip(chunks, results):
        for q in res.questions:
            pairs.append(
                {
                    "question": q.question, 
                    "chunk": ch,
                }
            )

    return pairs

def build_supervision_en_serie(chunks: List[str], questions_per_chunk: int = 10) -> List[Dict[str, str]]:
    pairs: List[Dict[str, str]] = []
    for ch in chunks:
        for q in generate_questions_for_chunk(ch, questions_per_chunk=questions_per_chunk):
            pairs.append({"question": q, "chunk": ch})
    return pairs

#Test code
if __name__ == "__main__":


    chunks = [
        """As we begin our 26th year, I've never been more energized or inspired. Salesforce just delivered the strongest 
year in our history—$37.9 billion in revenue, record operating margin and cash flow, and our first-ever $10 billion 
quarter. But this is more than a financial milestone — it's a moment of transformation.
In just a few months, we've seen our addressable market grow from hundreds of billions to a multi-trillion-dollar 
opportunity. Why? Because we're pioneering a new kind of workforce—a new model for business — with the 
launch of Agentforce, the first digital labor platform for enterprises. This is not just a technology shift — it's 
a revolution in how work gets done.
I'm especially proud that we're achieving this incredible success by staying true to our values: trust, customer 
success, innovation, equality, and sustainability. For over 26 years, we've proven that our values create value and 
that business is the greatest platform for change. To date, Salesforce has given nearly $800 million in grants and 
our employees have performed almost 10 million service hours, while more than 60,000 nonprofits and higher-
ed customers use our software for free. And nearly 20,000 other companies have followed our lead through 
Pledge 1% and adopted our 1-1-1 model.""",
        """Accelerating ethical, responsible, and sustainable AI
As the world's #1 AI CRM, we have a responsibility to lead with trust, mitigate bias, and ensure that the 
technologies we develop are safe and inclusive for everyone. With the launch of Agentforce in FY25, 
we set out to empower businesses with agentic AI while advancing trust in AI and upholding the highest ethical 
standards.
At Salesforce, we believe that the intentional design, responsible development, and accessible use of technology 
are integral to preventing harm and unlocking human potential for all. Our Office of Ethical and Humane Use 
guides the responsible development and deployment of AI in our products through best practices, tools, and 
frameworks. We prioritize AI safety measures with our Trust Layer, model testing, and detection of bias and 
toxicity to advance ethical AI. We have also invested in a series of initiatives geared towards managing and 
mitigating the environmental impact of AI models and data centers, as well as directing some of our investments 
and philanthropic focus to ensure our technology is developed in a way 
that supports a sustainable future.""",
        """Across our company and in our communities, we remain committed to our longstanding core value of 
equality — equal opportunities for all, equal pay for equal work, and the dignity of every person. This 
commitment is the driving force behind our efforts to expand equitable access to trusted generative AI.
With Trailhead, we announced our AI for All program — a more than $50 million investment in skilling up the 
workforce and addressing the growing AI skills gap. The program includes AI training spaces around the world and 
free AI courses and AI certifications through the end of 2025.
In FY25, we provided nearly $36 million in education grants, supporting 37 organizations globally. In total, 
these grants reached over 676,000 educators and more than 14 million students and young people, expanding AI 
access and literacy so teachers and the next generation of students are prepared for the future of work.
Leveraging our 1-1-1 model to close the AI access gap
Our Salesforce Accelerator — AI for Impact continues to help purpose-driven organizations gain equitable access to 
trusted generative AI technologies. By providing flexible funding, pro-bono expertise, and technology to purpose-
driven organizations, we're empowering nonprofits to accelerate generative AI-based solutions to help them meet 
their missions. Recognizing the urgent need to close a widening AI access gap, we committed resources to support 
three nonprofit cohorts, resulting in $6 million in new funding for organizations to harness the power of agents for 
climate, education, and other key impact areas.
Leading on nature restoration at scale
Sustainability is a core value at Salesforce that is operationalized across the business. We believe the health 
of nature and business are inextricably linked, which is why we are committed to improving nature 
restoration at scale."""
    ]

    pairs = build_supervision(
        chunks=chunks,
        questions_per_chunk=3,
        model="gpt-5-nano",
        temperature=1,
        max_concurrency=3,
    )

    print("\nGenerated supervision pairs:\n")
    for i, p in enumerate(pairs, start=1):
        print(f"{i}. Q: {p['question']}")
        print(f"   From chunk: {p['chunk'][:80]}...")
        print("-" * 80)


    