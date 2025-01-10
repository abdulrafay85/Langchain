from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
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

# 2. Document ko load karo aur split karo
raw_documents = TextLoader("../example.txt").load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# 3. FAISS index me documents ko store karo with cached embeddings
db = FAISS.from_documents(documents, embeddings_model)

# Query ko embed karo
query = "What sparked your interest in astronomy and the study of stars and galaxies?"
query_vector = embeddings_model.embed_query(query)  # Embed the query to get its vector

# Vector ke zariye similarity search karo
docs = db.similarity_search_by_vector(query_vector)  # Pass the embedded vector here
# print(docs)
