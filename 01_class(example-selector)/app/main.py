# from langchain_google-genai import GoogleGenerativeAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Accessing the environment variable
gemini_api_key = os.getenv('GEMINI_API_KEY')

os.environ["GEMINI_API_KEY"] = gemini_api_key


# Google Generative AI client ka setup
google_ai = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key="gemini_api_key"
)

google_ai.invoke("hello")

# # Embeddings ka setup
# embeddings = GoogleGenerativeAIEmbeddings(
#     content="what is the mening of life?",
#     # task_type=,
#     title="Embedding of singel string",
#     model="models/text-embedding-004",
# )

# # documents = [
# #     Document(page_content=example['input'], metadata=)
# # ]


# # Sample documents
# documents = [
#     Document(page_content="Aaj ka mausam kaisa hai?"),
#     Document(page_content="Mujhe khaas khana pasand hai."),
# ]

# # FAISS Vector Store ka setup
# faiss_store = FAISS.from_documents(documents, embeddings)

# # Prompt template define karein
# prompt_template = PromptTemplate.from_template(template="Aapka sawal: {question}")

# # LLM chain banayein
# llm_chain = LLMChain(llm=google_ai, prompt=prompt_template)

# # Sawal ka jawab hasil karein
# question = "Aaj ka mausam kaisa hai?"
# response = llm_chain.run(question)
# print("Response:", response)