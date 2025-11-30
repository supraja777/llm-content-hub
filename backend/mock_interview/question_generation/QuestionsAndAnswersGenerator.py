import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from websearch import *

selected_topic = "RAG"

from llm_ini import *
from llm_chains.llm_chains import question_generator_chain
from router.router import get_router_decision
from constants import PATH, LLM_ONLY, VECTOR_DB
from CRAG.crag import crag_process
from llm_chains.llm_chains import generate_answer
from vectorstore import load_vector_db
from embedder import embeddings

faiss_index = load_vector_db(embeddings, path = PATH)

def question_generator(content: str):
    """
       Using the retrieved information - 
       Generate interview style questions of easy - 1, medium - 1 and hard level - 1
    """

    print("Generating question")
    
    return question_generator_chain(content)


def generate_questions(query: str):
    """
        DuckDuckGoSearch for the selected topic -  
        to get the important information regarding the selected topic
    """

    print("Original " + query)

    web_knowledge = perform_web_search(query)

    result = question_generator(web_knowledge)

    return result

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
           
        elif decision == VECTOR_DB:
            logging.info("Decision is VECTOR DB")
            question, answer = crag_process(question, faiss_index)
            
        result.append({
            "question": question,
            "answer": answer
        })

    return result



