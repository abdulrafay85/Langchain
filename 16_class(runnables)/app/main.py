# # How to chain runnables

# # --------

# # Importing necessary libraries from LangChain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# # Loading environment variables (API key for Gemini model)
load_dotenv()

# # Fetching the API key for Gemini from the environment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")

# # Setting the API key for use in the environment
os.environ["GEMINI_API_KEY"] = gemini_api_key

# # Initializing the Google Generative AI model with required parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Specifying the model to use
    api_key=gemini_api_key,    # Providing the API key
    temperature=0.3            # Setting the temperature for response creativity (0.3 is more deterministic)
)

# Embeddings setup
embeddings_model = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004",
)

# # Creating a prompt template for generating a joke about a given topic
# prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")

# # Creating a chain where the prompt is passed to the model and the output is parsed into a string
# chain = prompt | llm | StrOutputParser()

# # Creating a prompt template for analyzing if the joke is funny or not
# analysis_prompt = ChatPromptTemplate.from_template("is this a funny joke? {joke}")

# # Composing the full chain of operations:
# # 1. Generate a joke using the 'joke' chain
# # 2. Analyze if the joke is funny using the 'analysis_prompt' chain
# composed_chain = {"joke": chain} | analysis_prompt | llm | StrOutputParser()

# # Running the composed chain with the input topic "bears"
# res = composed_chain.invoke({"topic": "bears"})

# # Printing the result, which will include the analysis of the joke's funniness
# print(res)

# --------

# How to invoke runnables in parallel


vectorstore = FAISS.from_texts(
    ["ukasha ek larki hay or is ka school ka name starskise education hay."], embedding=embeddings_model
)
retriever = vectorstore.as_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""

# The prompt expects input with keys for "context" and "question"
prompt = ChatPromptTemplate.from_template(template)

retrieval_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

res = retrieval_chain.invoke("who is ukasha?")

print(res)