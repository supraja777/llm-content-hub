import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from llm_ini import *
from dataModels.DataModel import (ContentSummarizerOutput, RetrievalEvaluatorInput, 
                                  RouterOutput, QuestionGeneratorOutput, KnowledgeRefinementInput)
from prompts.prompt import (summarize_content_prompt, 
                            retrieval_evaluator_prompt,router_prompt, 
                            question_generator_prompt, knowledge_refinment_prompt,
                            generate_response_prompt, generate_answer_prompt)

def summarize_content_chain(content: str):
    
    chain = summarize_content_prompt | llm.with_structured_output(ContentSummarizerOutput)
    input_variables = {"content": content}
    result = chain.invoke(input_variables).summary
    return result

def retrieval_evaluator_chain(query: str, document: str) -> float:
  
    chain = retrieval_evaluator_prompt | llm.with_structured_output(RetrievalEvaluatorInput)
    input_variables = {"query" : query, "document": document}
    result = chain.invoke(input_variables).relevance_score
    return result

def router_chain(question: str):

    chain = router_prompt | llm.with_structured_output(RouterOutput)
    input_variables = {"question": question}
    result = chain.invoke(input_variables)
    return result.decision, result.explanation

def question_generator_chain(content: str):
       
    chain = question_generator_prompt | llm.with_structured_output(QuestionGeneratorOutput)
    input_variables = {"content": content}
    result = chain.invoke(input_variables).questions
    return result

def knowledge_refinment_chain(document: str):

    chain = knowledge_refinment_prompt | llm.with_structured_output(KnowledgeRefinementInput)
    input_variables = {"document" : document}
    result = chain.invoke(input_variables).key_points
    return result

def generate_response_chain(query: str, knowledge: str):

    """
    Generate a response to a query using knowledge.

    Args:
        query (str): The query string.
        knowledge (str): The refined knowledge to use in the response.
       
    Returns:
        str: The generated response.
    """

    response_chain = generate_response_prompt | llm
    input_variables = {
        "query": query,
        "knowledge": knowledge,
    }
    return response_chain.invoke(input_variables).content


def generate_answer(query: str):
    generate_answer_chain = generate_answer_prompt | llm
    input_variables = {
        "query": query,
    }
    return generate_answer_chain.invoke(input_variables).content