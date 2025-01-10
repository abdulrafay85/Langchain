from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# Load the API key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
langchain_api_key=os.getenv("LANGCHAIN_API_KEY")
langchain_tracing_v2 = os.getenv("LANGCHAIN_TRACING_V2")

os.environ["GEMINI_API_KEY"] = gemini_api_key
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_TRACING_V2"]= True

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=gemini_api_key,
    temperature=0.3
)

res = llm.invoke("hello world")
print(res)