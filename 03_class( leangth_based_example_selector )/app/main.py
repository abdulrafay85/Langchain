from langchain_core.prompts import ChatPromptTemplate, FewShotPromptTemplate, PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

# Load the API key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Initialize the LLM (ensure the model name is correct and supported)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Make sure this is correct
    api_key=gemini_api_key,
    temperature=0.2
)

# Examples for few-shot prompting
examples = [
    {"input": "happy", "output": "sad"},
    {"input": "tall", "output": "short"},
    {"input": "energetic", "output": "lethargic"},
    {"input": "sunny", "output": "gloomy"},
    {"input": "windy", "output": "calm"},
]

# Embeddings setup (Ensure the model name is correct and supported by Google API)
embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004"  # This is a valid embedding model (adjust as needed)
)

# Documents to store in vector database
documents = [
    Document(page_content=example['input'], metadata={"input": example["input"], "output": example["output"]})
    for example in examples
]

# Create a vector store using FAISS
vector_store = FAISS.from_documents(documents, embeddings)

# print(vector_store)

# Create the prompt template
example_prompt = PromptTemplate(
    input_variables=["input", "output"],
    template="Input: {input}\nOutput: {output}",
)

# print(example_prompt.invoke({"input": "hello", "output": "desired_output_value"}))


# Example selector using LengthBasedExampleSelector
# Assuming 'vector_store' and 'example_prompt' are defined above
example_selector = LengthBasedExampleSelector(
    examples=examples,  # Yeh line add karo, jo examples ko provide karega
    # vector_store=vector_store,
    example_prompt=example_prompt,
    # max_length=30,  # Adjust as needed
)

# # Debug print to verify the selector
# print(example_selector)

# # Create the dynamic few-shot prompt template
dynamic_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Give the antonym of every input",
    suffix="Input: {input}\nOutput:",
    input_variables=["input"],
)

# Invoke the prompt with an example input
print(dynamic_prompt.invoke({"input": "hello", "output": "desired_output_value"}))

# formated_prompt = dynamic_prompt.format(
#     input="Hi"
# )
# res = llm.invoke(formated_prompt)
# print(res.content)
