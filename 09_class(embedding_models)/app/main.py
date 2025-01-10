from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.storage import LocalFileStore
from langchain_community.vectorstores import FAISS
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from dotenv import load_dotenv
import os

load_dotenv()

# Load the API key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=gemini_api_key,
    temperature=0.2,
    verbose=True,
)

# Embeddings setup
embeddings_model = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004",
)

## Exmample 1 --> Embed list of texts --> Use .embed_documents to embed a list of strings, recovering a list of embeddings
# embeddings = embeddings_model.embed_documents(
#     [
#         "Hi there!",
#         "Oh, hello!",
#         "What's your name?",
#         "My friends call me World",
#         "Hello World!"
#     ]
# )

# print(embeddings[0])


## Embed single query --> Use .embed_query to embed a single piece of text (e.g., for the purpose of comparing to other embedded pieces of texts).
# embedded_query = embeddings_model.embed_query("What was the name mentioned in the conversation?")
# print(embedded_query)


# Example 2 --> GoogleGenerativeAI ka embedding model
store = LocalFileStore("./cache/")  # Local storage for caching
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    embeddings_model, 
    store, 
    namespace=embeddings_model.model
)

# 2. Document ko load karo aur split karo
raw_documents = TextLoader("../state_of_the_union.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# 3. FAISS index me documents ko store karo with cached embeddings
db = FAISS.from_documents(documents, cached_embedder)

# query = "I enjoy hiking in the mountains a lot."
# docs = db.similarity_search(query)
# print(docs[0].page_content)



