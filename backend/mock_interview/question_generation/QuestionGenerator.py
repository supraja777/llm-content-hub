import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from websearch import *

selected_topic = "RAG"

from llm_ini import *
from llm_chains.llm_chains import question_generator_chain

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



