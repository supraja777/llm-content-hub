# 1 Based on the question the LLM will decide if it has to do a retreieve from vector db
# Else if it has to perform a web query or can give an answer on its own
from logging_config import setup_logging
import logging

setup_logging()

from prompts.prompt import router_prompt
from dataModels.DataModel import RouterOutput
from llm_ini import llm
from constants import LLM_ONLY, VECTOR_DB
from llm_chains.llm_chains import router_chain

def get_router_decision(question: str):
    """
       Based on the question the router will decide if LLM is sufficient 
       or if a vector db call is required
    """

    logging.info("Calling router LLM")
    
    return router_chain(question)