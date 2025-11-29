import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from pydantic import BaseModel, Field
from langchain_community.tools import DuckDuckGoSearchRun
from typing import List, Dict, Any, Tuple
from langchain_core.prompts import PromptTemplate
from llm_chains.llm_chains import knowledge_refinment_chain
from llm_ini import *
import json

search = DuckDuckGoSearchRun()

from logging_config import setup_logging
import logging

setup_logging()

# Knowledge Refinement

def knowledge_refinment(document: str) -> List[str]:
    logging.info("Performing knowledge refinment")
  
    result = knowledge_refinment_chain(document)

    return [point.strip() for point in result.split('\n') if point.strip()]
    
def perform_web_search(query: str) -> Tuple[List[str], List[Tuple[str, str]]]:
    print("Performing web search")
    """
    Perform a web search based on a query.

    Args:
        query (str): The query string to search for.

    Returns:
        Tuple[List[str], List[Tuple[str, str]]]: 
            - A list of refined knowledge obtained from the web search.
            - A list of tuples containing titles and links of the sources.
    """

    rewritten_query = query
    web_results = search.run(rewritten_query)
    web_knowledge = knowledge_refinment(web_results)
    # sources = parse_search_results(web_results)
    return web_knowledge