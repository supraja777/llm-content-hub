from constants import LLM_ONLY, VECTOR_DB

from logging_config import setup_logging
import logging

setup_logging()

def generate_answers(router_results):
    """
        Generates answers based on router decision
        1 If the decision is LLM_ONLY then direct call is made to the router 
        2 If the decision is VECTOR_DB then relevant chunks and queried and 
        CRAG is implemented
    """

    for router_result in router_results:
        decision = router_result[0]
        print(decision)

        if decision == LLM_ONLY:
            logging.info("Making call directly to LLM")
        elif decision == VECTOR_DB:
            logging.info("Fectching information from vector DB")
            # Utilizing CRAG here
            crag_process()