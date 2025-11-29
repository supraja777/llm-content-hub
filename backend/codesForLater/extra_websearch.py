class QueryRewriterInput(BaseModel):
    query: str = Field(description = "The query to rewrite")

def rewrite_query(query: str) -> str:
    print("Rewriting query")
    prompt = PromptTemplate(
        input_variables = ["query"],
        template = """Rewrite the following query to make it more suitable for a web search: 
        {query} rewritten query: 
        """
    )

    chain = prompt | llm.with_structured_output(QueryRewriterInput)
    input_variables = {"query" : query}
    return chain.invoke(input_variables).query.strip()


def parse_search_results(results_string: str) -> List[Tuple[str, str]]:
    print("Result String == ", results_string)
    print("Parsing search results")
    try:
        # Attempt to parse json string
        results = json.loads(results_string)

        # Extract and return the title and link from each result
        return [(result.get('title', 'Untitled'), result.get('link', '')) for result in results]
    except json.JSONDecodeError:
        # Handle JSON decoding errors by returning an empty list
        print("Error parsing search results. Returning empty list")
        return []
    
