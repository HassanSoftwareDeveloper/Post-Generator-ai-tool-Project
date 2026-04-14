from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure GROQ_API_KEY is found
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please add it to your .env file.")

# Initialize LLM
llm = ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile")

# Test the LLM
if __name__ == "__main__":
    prompt = "Title, Summary, Description and tags of Infinix Hot 11 play"
    response = llm.invoke(prompt)
    print(response.content)