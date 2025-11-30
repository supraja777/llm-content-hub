import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Tuple
from mock_interview.question_generation.QuestionGenerator import generate_questions
from router.router import get_router_decision
from constants import LLM_ONLY, VECTOR_DB
from vectorstore import load_vector_db
from embedder import embeddings
from constants import PATH
from CRAG.crag import crag_process
from llm_chains.llm_chains import generate_answer

mock_interview_topic = "RAG"

from logging_config import setup_logging
import logging

setup_logging()

faiss_index = load_vector_db(embeddings, path = PATH)

def generate_questions_and_answers(mock_interview_topic: str):
    # 1 Generate set of questions
    questions = generate_questions(mock_interview_topic) 

    # 2 Generate answers for each question
    #   2.a First the RAG will decide if we need to access vetor db 
    #   2.b If RAG will be able to answer it on its own then no need of vector db

    router_results =  [(get_router_decision(question), question) for question in questions]

    # 3 Generate answers - If LLM_ONLY - then use LLM only otherwise - CRAG (VectorDB + WebSearch)

    result = []

    for router_result in router_results:
        decision = router_result[0][0]
        explanation = router_result[0][1]
        question = router_result[1][0]

        if decision == LLM_ONLY:
            logging.info("Decision is LLM only")
            answer = generate_answer(question)
            result.append((question, answer))
        elif decision == VECTOR_DB:
            logging.info("Decision is VECTOR DB")
            question, answer = crag_process(question, faiss_index)
            result.append((question, answer))

        result.append({
            "question": question,
            "answer": answer
        })
    return result


generate_questions_and_answers(mock_interview_topic)

# TODO
# For each answer generated - grade it, 
# if grade is below a threshold then generate again, check if websearch is required
# Continue till max_num of retries
# check for hallucination in the end
    


