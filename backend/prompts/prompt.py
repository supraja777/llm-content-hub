from langchain_core.prompts import PromptTemplate
from constants import VECTOR_DB, LLM_ONLY

summarize_content_prompt = PromptTemplate(
        input_variables = ["content"],
        template = """
        Given the content. Summarize the information.

        Content: {content}
        Bullet points : 

        """
    )

question_generator_prompt = PromptTemplate(
        input_variables = ["content"],
        template = """
        Generate interview style questions using the following content. 
        The questions should be one liner and there should be 1 easy question,
        1 medium level question and 1 hard questions.

        For each question tag its difficulty level - Easy, Medium, Hard

        Output MUST be a JSON array of tuples, like:
        [["Question 1 text", "Easy"], ["Question 2 text", "Medium"], ... ]

        Content: {content}
        questions: 

        """
    )


router_prompt = PromptTemplate(
        input_variables = ["question"],
        template = """
        Based on the question decide whether the LLM can answer the question on its own,
        or if it needs a vector search to be performed. 

        if only LLM can answer the question output - {{LLM_ONLY}}
        if a vector search is required to answer output - {{VECTOR_DB}}

        Give appropriate explanation for the above selection. The explaination should be at max 2 lines

        question: {question}
        questions: 

        """
    )

retrieval_evaluator_prompt = PromptTemplate(
        input_variables = ["query", "document"],
        template = """
        On a scale from 0 to 1, how relevant is the following document to the query? 

        Query: {query}
        Document: {document}

        Relevance score: 

        """
    )

knowledge_refinment_prompt = PromptTemplate(
        input_variables = ["document"],
        template = """ Extract the key information from the following in bullet points: \n 
        {document}
        key points: 
        """
    )

generate_response_prompt = PromptTemplate(
        input_variables = ["query", "knowledge", "sources"],
        template = "Based on the following knowledge, " \
        "answer the query. Include the sources with their links (if available)" \
        "at the end of your answer : Query : {query} " \
        "Knowledge: {knowledge}" \
        "Answer: "
    )

generate_answer_prompt = PromptTemplate(
        input_variables = ["query"],
        template = "" \
        "Answer the following query. Include the sources with their links (if available)" \
        "at the end of your answer : Query : {query} " \
        "Answer: "
    )