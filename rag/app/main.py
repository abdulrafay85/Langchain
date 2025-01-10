import streamlit as st
from langchain.prompts import ChatPromptTemplate, PromptTemplate, FewShotPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load the API key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Streamlit interface setup
# st.title("Gemini ChatBot")
# st.text("This interface allows you to interact with the Gemini API using a simple chat interface.")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=gemini_api_key,
    temperature=0.2,
    verbose=False,
)

# Embeddings setup
embeddings_model = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004",
)

# Load the PDF
file_path = "../files/example.txt"
loader = TextLoader(file_path)
my_data = loader.load()
# print(my_data)
documents_text = [doc.page_content for doc in my_data]


# Chunk the text using embeddings
text_splitter = SemanticChunker(
    embeddings_model,  
    breakpoint_threshold_type="percentile",
)
# print()

combined_text = " ".join(documents_text)
docs = text_splitter.create_documents([combined_text])
# print(docs)

# Create a vector store
vectorstore = FAISS.from_documents(docs, embeddings_model)

# Query ko embed karo
query = "what is generative ai ?"
query_vector = embeddings_model.embed_query(query)  # Embed the query to get its vector
docs = vectorstore.similarity_search_by_vector(query_vector)  # Pass the embedded vector here
print(docs[0].page_content)


# # Create the example prompt
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)


# # Example selector using semantic similarity
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vectorstore,
    k=1,
)


# # Dynamic few-shot prompt template
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {input}\nOutput:",
    input_variables=["input"],
)

# # Create the LLM chain using RunnableSequence
llm_chain = RunnableSequence(dynamic_prompt | llm)


res = llm_chain.invoke(
    input={"input": "what is docker ?"},
)

# print(res)

# # # User input
# # user_input = st.text_input("Enter you are Question:", "")

# # if st.button("Send"):
# #     if user_input:
# #         chain_input = {"input": user_input}
# #         # Input for the chain

# #         # Run the chain
# #         chain_output = llm_chain.invoke(chain_input)

# #         # Display the output
# #         st.write("Chatbot Response: ", chain_output.content)
# #     else:
# #         st.warning("koi sawal poochhein.")
