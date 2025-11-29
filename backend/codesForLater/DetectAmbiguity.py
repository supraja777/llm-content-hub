from typing import Tuple, List
import streamlit as st
from llm_ini import *
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field


class DetectAmbiguityOutput(BaseModel):
    ambiguous: bool = Field("True if the topic is ambiguous and False if the topic is not ambiguous")
    contexts : List[str] = Field(description="The list of possible contexts")


def detect_ambiguity(topic):
    prompt = PromptTemplate(
        input_variables = ["topic"],
        template = """
        Detect if the topic is ambiguous or not.

        If the topic is ambiguos say True and give a list of possible context that the topic 
        can be related to.

        if topic is ambiguous then say:
            "ambiguous" : true
            "contexts" : ["context1", "context2", "context3", ..........]
        
        if topic is not ambiguous then say:
            "ambiguous" : false
            "contexts" : []

        Topic: {topic}

        """
    )

    chain = prompt | llm.with_structured_output(DetectAmbiguityOutput)
    input_variables = {"topic": topic}
    result = chain.invoke(input_variables)
    return result