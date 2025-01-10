# Import necessary libraries
from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
from dotenv import load_dotenv
import uvicorn
import os

# Load environment variables from .env file
load_dotenv()

# Accessing the environment variable for the Gemini API key
gemini_api_key = os.getenv('GEMINI_API_KEY')

# Set the environment variable for the API key
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Initialize the FastAPI application
app = FastAPI(
    title="Langchain Server",  # Title of the API
    version="1.0",              # Version of the API
    description="A Simple API Server"  # Description of the API
)

# Create an instance of ChatGoogleGenerativeAI with specified model and parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Specify the model to be used
    api_key=gemini_api_key,    # Use the loaded API key for authentication
    temperature=0.3,           # Set temperature for response variability (0.0 to 1.0)
)

# Add routes to the FastAPI application for Google Generative AI
add_routes(
    app,
    llm,  # Instance of ChatGoogleGenerativeAI to handle requests
    path="/gen_ai"             # Path for accessing the generative AI functionality
)

# Define a chat prompt template for generating text based on a topic
prompt_1 = ChatPromptTemplate.from_template(
    "Write me an easy about {topic} with 100 words"  # Template for generating text prompts
)

add_routes(
    app,
    prompt_1 | llm,
    path="/essay"
)

if __name__=="__main__":
    uvicorn.run(app,host="localhost", port=8000)