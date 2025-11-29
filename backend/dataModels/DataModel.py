from pydantic import BaseModel, Field
from typing import List, Tuple
from constants import VECTOR_DB, LLM_ONLY

class ContentSummarizerOutput(BaseModel):
    summary: str = Field(description = "Content summary of the data")

class QuestionGeneratorOutput(BaseModel):
    questions: List[Tuple[str, str]] = Field(
        description="The list of interview style question generated for the selected topic. " \
    "Each question will be one liner.")

class RouterOutput(BaseModel):
    decision: str = Field(description=f"The LLM will decide whether to use vector DB or not. " \
    "If only LLM is sufficient to answer the question output '{LLM_ONLY}' else if vector call is required" \
    "output '{VECTOR_DB}'")
    explanation: str = Field(description = "Explanation for the above decision - "
    "'{LLM_ONLY}' or '{VECTOR_DB}' is given in at max 2 lines")

class RetrievalEvaluatorInput(BaseModel):
    relevance_score: float = Field(description="The relevance score of the document to the query. " \
    "The score should be between 0 and 1")

class KnowledgeRefinementInput(BaseModel):
    key_points: str = Field(description = "The document to extract key information from.")