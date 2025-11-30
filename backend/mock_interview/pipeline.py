import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Tuple
from backend.mock_interview.question_generation.QuestionsAndAnswersGenerator import generate_questions_and_answers

from constants import LLM_ONLY, VECTOR_DB

mock_interview_topic = "RAG"

from logging_config import setup_logging
import logging

setup_logging()

# 1. Generate questions and answers 

generate_questions_and_answers(mock_interview_topic)

# 2. Evaluate answers entered by users and generate appropriate feedbacks

# 3. Grade the answer against each generated answer for the question

# 4. Suggest learning resources for each question 


# TODO
#
# Continue till max_num of retries
# check for hallucination in the end
    


