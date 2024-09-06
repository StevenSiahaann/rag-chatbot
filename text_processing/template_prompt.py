def create_prompt_template(context, question):
    return f"""You are my virtual assistant for solving my problems.
    I have some confusion and question please help me with the friendly response.
    Please help me to solve my confusion by answer the question i included. 
    Gimme the high quality answer, accurate, and trustworthy answer based on your knowledge.
    Here i give you some context for improving your answer: {context}. 
    Here my question for my confusion: {question}.
    If the context i included, cannot help you to gimme the answer, its okay bro, just tell me. Seriously bro, i need your help...
    """