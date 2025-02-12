import os
import time
import uvicorn
from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

# Load environment variables
load_dotenv()

app = FastAPI()

# --- PDF Search Tool ---
pdf_search_tool = PDFSearchTool(
    pdf="backend/bhagwat gita.pdf",
    config=dict(
        llm=dict(provider="groq", config=dict(model="groq/Llama3-8b-8192")),
        embedder=dict(provider="huggingface", config=dict(model="all-MiniLM-L6-v2")),
    ),
)

# --- LLM Integration ---
llm = ChatOpenAI(
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=os.environ['GROQ_API_KEY'],
    model_name="groq/llama3-8b-8192",
    temperature=0.1,
    max_tokens=1000,
)

# --- Agent ---
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
    llm=llm
)

# --- Task ---
answer_user_query_task = Task(
    description=(
        """
        Analyze the user's question or problem, and identify its essence. Search the Bhagavad Gita for relevant teachings,
        particularly verses spoken by Lord Krishna, and provide a comprehensive response. The response should be delivered
        in English, Hindi, and Sanskrit, incorporating the following elements:
        
        - Relevant Slokas: Include the Sanskrit verse(s) from the Bhagavad Gita that align with the user's question.
        - Translation: Provide the translation of the verse(s) in both English and Hindi.
        - Explanation: Offer a detailed explanation of the verse(s) and their connection to the user's question.
        - Stories or Analogies: Use supporting stories, examples, or analogies from the Gita or related teachings.
        - Practical Solutions: Suggest actionable steps for the user to apply the wisdom of the Gita in real life.
        
        User's question/problem:
        {user_question}
        """
    ),
    expected_output=(
        """
        A structured, detailed response addressing the user's question or problem, which includes:
        
        1. Sanskrit Verse (Sloka): The relevant verse(s) from the Bhagavad Gita, with chapter and verse number.
        2. Translation: Word-to-word and contextual translation in both English and Hindi.
        3. Explanation: A thorough explanation of the verse(s) and their relevance to the user's query.
        4. Stories or Analogies: Supporting examples, stories, or analogies to clarify and enhance understanding.
        5. Practical Guidance: Actionable steps rooted in the teachings of the Gita to help the user implement the wisdom in their life.
        """
    ),
    tools=[pdf_search_tool],
    agent=research_agent,
    llm=llm
)

# --- Crew ---
crew = Crew(
    tasks=[answer_user_query_task],
    agents=[research_agent],
    process=Process.sequential,
)

# Request model
class QueryRequest(BaseModel):
    user_question: str

# Retry mechanism for rate limiting
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

# API Endpoint
@app.post("/ask")
def ask_gita(query: QueryRequest):
    try:
        # Validate and sanitize input
        user_question = query.user_question.strip()
        if not user_question:
            raise ValueError("User question cannot be empty.")

        # Execute the task with retry mechanism
        result = retry_with_backoff(crew.kickoff, inputs={"user_question": user_question})
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)