import streamlit as st
from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector,  MaxMarginalRelevanceExampleSelector
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableSequence

from dotenv import load_dotenv
import os

load_dotenv()

# Load the API key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Streamlit interface setup
st.title("Gemini ChatBot")
st.text("This interface allows you to interact with the Gemini API using a simple chat interface.")

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=gemini_api_key,  # Corrected the variable usage
    temperature=0.2,
    # verbose=True,
)

# Examples for few-shot prompting
examples = [
    {"input": "What is the capital of France?", "output": "The capital of France is Paris."},
    {"input": "Who wrote the play 'Romeo and Juliet'?", "output": "William Shakespeare wrote 'Romeo and Juliet'."},
    {"input": "What is the boiling point of water in Celsius?", "output": "The boiling point of water is 100°C."},
    {"input": "Who is the current CEO of Tesla?", "output": "Elon Musk is the current CEO of Tesla."}
]

# Embeddings setup
embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004",
)

# Documents to store in vector database
documents = [Document(page_content=example['input'], metadata={"input": example["input"], "output": example["output"]})
             for example in examples]

# print(documents)

# Create a vector store using FAISS
vector_store = FAISS.from_documents(documents, embeddings)

# Example selector using SemanticSimilarityExampleSelector
example_selector = SemanticSimilarityExampleSelector(
    vectorstore=vector_store,  
    k=2,
)

# Example selector using MaxMarginalRelevanceExampleSelector
# example_selector = MaxMarginalRelevanceExampleSelector(
#     vectorstore=vector_store,  
#     k=2,
# )

# Create the prompt template
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)

# Dynamic few-shot prompt template
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {input}\nOutput:",
    input_variables=["input"],
    # verbose=True,
)

print(dynamic_prompt.invoke(
    {
        "input": "What is the capital of Islamabad?"
    }
))

# # Create the LLMChain
# # Example code using RunnableSequence
# llm_chain = RunnableSequence(dynamic_prompt | llm)

# # User input
# user_input = st.text_input("Enter you are Question:", "")

# if st.button("Send"):
#     if user_input:
#         chain_input = {"input": user_input}
#         # Input for the chain

#         # Run the chain
#         chain_output = llm_chain.invoke(chain_input)

#         # Display the output
#         st.write("Chatbot Response: ", chain_output.content)
#     else:
#         st.warning("koi sawal poochhein.")



# # Run the chain with an example input
# chain_input = {"input": "who is the CEO  of Google?"}

# chain_output = llm_chain.invoke(chain_input)

# # Print the output of the LLMChain
# print(chain_output.content)
