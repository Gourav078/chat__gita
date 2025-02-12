# import os
# import time

# import uvicorn
# from crewai import Agent, Crew, Process, Task
# from crewai_tools import PDFSearchTool
# from dotenv import load_dotenv
# from fastapi import FastAPI, HTTPException
# from langchain_openai import ChatOpenAI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware


# load_dotenv()

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# pdf_search_tool = PDFSearchTool(
#     pdf="backend/bhagwat gita.pdf",
#     config=dict(
#         llm=dict(provider="groq", config=dict(model="groq/llama-3.1-8b-instant")),
#         embedder=dict(provider="huggingface", config=dict(model="all-MiniLM-L6-v2")),
#     ),
# )


# # llm = ChatOpenAI(
# #     model="ollama/llama3.2",
# #     openai_api_key="NA",
# #     base_url="http://localhost:11434/v1",
# #     temperature=0.1,
# #     max_tokens=8000,
# # )

# llm = ChatOpenAI(
#     openai_api_base="https://api.groq.com/openai/v1",
#     openai_api_key=os.environ['GROQ_API_KEY'],
#     model_name="groq/llama-3.1-8b-instant",
#     temperature=0.1,
#     max_tokens=1000,
# )

# research_agent = Agent(
#     role="Gita Knowledge Expert",
#     goal="Provide insights and solutions based on the Bhagavad Gita.",
#     allow_delegation=False,
#     verbose=True,
#     backstory=(
#         """
#         The Gita Knowledge Expert has profound knowledge of the Bhagavad Gita and can
#         extract relevant teachings and provide interpretations in multiple languages.
#         It is designed to help users solve their problems with Gita-based wisdom.
#         """
#     ),
#     tools=[pdf_search_tool],
#     llm=llm,
# )


# answer_user_query_task = Task(
#     description=(
#         """
#         Analyze the user's question, search the Bhagavad Gita for relevant teachings, and provide a structured response:
        
#         - **Relevant Slokas**: Include Sanskrit verse(s) with chapter and verse number.
#         - **Translation**: Provide translations in English and Hindi.
#         - **Explanation**: Explain the verse(s) in detail.
#         - **Stories or Analogies**: Use examples or analogies from the Gita or related teachings.
#         - **Practical Guidance**: Suggest actionable steps based on the teachings of the Gita.
        
#         User's question:
#         {user_question}
#         """
#     ),
#     expected_output=(
#         """
#         - Sanskrit Verse (Sloka) with reference.
#         - Translation in English and Hindi.
#         - Detailed explanation.
#         - Supporting examples, stories, or analogies.
#         - Practical steps to apply the wisdom.
        
#           **IMPORTANT**: Use the following format for your final answer:
#         Final Answer: <your best complete final answer to the task>
#         """
#     ),
#     tools=[pdf_search_tool],
#     agent=research_agent,
#     llm=llm,
# )


# crew = Crew(
#     tasks=[answer_user_query_task],
#     agents=[research_agent],
#     process=Process.sequential,
# )


# class QueryRequest(BaseModel):
#     user_question: str

# def retry_with_backoff(func, *args, max_retries=3, initial_wait=1, **kwargs):
#     retries = 0
#     while retries < max_retries:
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             if "rate_limit_exceeded" in str(e):
#                 wait_time = initial_wait * (2 ** retries)
#                 print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
#                 time.sleep(wait_time)
#                 retries += 1
#             else:
#                 raise e
#     raise Exception("Max retries exceeded.")

# @app.post("/ask")
# def ask_gita(query: QueryRequest):
#     try:
#         user_question = query.user_question.strip().lower()  
#         if not user_question:
#             raise HTTPException(status_code=400, detail="User question cannot be empty.")
        
        
#         if user_question in ["hi", "hello"]:
#             return {"message": "Hello! I am your chat assistant. I will provide enlightened knowledge from the Bhagavad Gita."}
        
        
#         search_input = {"query": user_question}
#         result = retry_with_backoff(crew.kickoff, inputs={"user_question": search_input})
        
#         # if isinstance(result, dict):
#         #     if "message" in result:
#         #         final_answer = result["message"]
#         #     elif "task_results" in result:
#         #         final_answer = result["task_results"][0]["output"]
#         #     else:
#         #         final_answer = str(result)
#         # else:
#         #     final_answer = str(result)
        
#         final_answer = result[0]["output"]
        
#         ref_message = final_answer.replace("**", "").replace("\n\n", "\n").strip()
#         return {"message": ref_message}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     uvicorn.run(app, host="localhost", port=8000)

import os
import time

import uvicorn
from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust based on frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PDF search tool setup
pdf_search_tool = PDFSearchTool(
    pdf="backend/bhagwat_gita.pdf",
    config=dict(
        llm=dict(provider="groq", config=dict(model="groq/llama-3.3-70b-versatile")),
        embedder=dict(provider="huggingface", config=dict(model="all-MiniLM-L6-v2")),
    ),
)


llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="groq/llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=1000,
)


research_agent = Agent(
    role="Gita Knowledge Expert",
    goal="Provide insights and solutions based on the Bhagavad Gita.",
    allow_delegation=False,
    verbose=True,
    backstory=(
        """
        The Gita Knowledge Expert has profound knowledge of the Bhagavad Gita and can
        extract relevant teachings and provide interpretations in multiple languages.
        It is designed to help users solve their problems with Gita-based wisdom.
        """
    ),
    tools=[pdf_search_tool],
    llm=llm,
)


answer_user_query_task = Task(
    description=(
        """
        Analyze the user's question, search the Bhagavad Gita for relevant teachings, and provide a structured response:
        
        - **Relevant Slokas**: Include Sanskrit verse(s) with chapter and verse number.
        - **Translation**: Provide translations in English and Hindi.
        - **Explanation**: Explain the verse(s) in detail.
        - Stories or analogies: Use examples or analogies from the Gita or related teachings.
        - Practical guidance: Suggest actionable steps based on the teachings of the Gita.
        
        User's question:
        {user_question}
        """
    ),
    expected_output=(
        """
        - Sanskrit Verse (Sloka) with reference.
        - Translation in English and Hindi.
        - Detailed explanation.
        - Supporting examples, stories, or analogies.
        - Practical steps to apply the wisdom.
        """
    ),
    tools=[pdf_search_tool],
    agent=research_agent,
    llm=llm,
)


crew = Crew(
    tasks=[answer_user_query_task],
    agents=[research_agent],
    process=Process.sequential,
)

class QueryRequest(BaseModel):
    user_question: str


def retry_with_backoff(func, *args, max_retries=3, initial_wait=1, **kwargs):
    retries = 0
    while retries < max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "rate_limit_exceeded" in str(e):
                wait_time = initial_wait * (2 ** retries)
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                raise e
    raise Exception("Max retries exceeded.")

@app.post("/ask")
def ask_gita(query: QueryRequest):
    try:
        user_question = query.user_question.strip().lower()
        if not user_question:
            raise HTTPException(status_code=400, detail="User question cannot be empty.")

        if user_question in ["hi", "hello"]:
            return {"message": "Hello! I am your chat assistant. I will provide enlightened knowledge from the Bhagavad Gita."}

        search_input = {"query": user_question}
        result = retry_with_backoff(crew.kickoff, inputs={"user_question": search_input})

        # Extract the final answer
        # final_answer = result[0]["output"] if result else "Sorry, I couldn't process your query."
        if isinstance(result, dict):
            if "message" in result:
                final_answer = result["message"]
            elif "task_results" in result:
                final_answer = result["task_results"][0]["output"]
            else:
                final_answer = str(result)
        else:
            final_answer = str(result)

        ref_message = final_answer.replace("**", "").replace("\n\n", "\n").strip()
        return {"message": ref_message}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
