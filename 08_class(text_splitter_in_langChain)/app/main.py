## Import necessary libraries and modules
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language, CharacterTextSplitter
from dotenv import load_dotenv
import os

## Load environment variables from .env file (e.g., API keys)
load_dotenv()

## Load the API key from the .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

## Set the API key to the environment variable for use in the model
os.environ["GEMINI_API_KEY"] = gemini_api_key

## Initialize the Google Generative AI model (ensure the model name is correct)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Make sure this model name is correct and supported
    api_key=gemini_api_key,
    temperature=0.2  # Lower temperature for more deterministic responses
)

## Initialize the Google Generative AI Embeddings model 
embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004",
)

# # Specify the file path for the document loader
# file_path = "../sample.txt"

# # Create a new instance of the TextLoader to load text documents
# loader = TextLoader(file_path)
# my_document = loader.load()
# data = my_document[0].page_content

# # Create a new instance of the CharacterTextSplitter
# text_splitter = CharacterTextSplitter(
#     chunk_size=300,
#     chunk_overlap=20,
#     separators="\n\n",  # Use separators 
# )

# my_data = text_splitter.create_documents([data])
# print("my_data\t:", my_data)

# # Specify the file path for the document loader
# file_path = "../sample.txt"

# # Create a new instance of the TextLoader to load text documents
# loader = TextLoader(file_path)
# my_document = loader.load()
# data = my_document[0].page_content

# # Create a new instance of the RecursiveCharacterTextSplitter
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=300,
#     chunk_overlap=20,
#     separators=["\n\n", "\n", " ", ""],  # Use separators instead of separator
# )

# my_data = text_splitter.create_documents([data])
# print("my_data\t:", my_data)

# # Specify the file path for the document loader
# file_path = "../sample.txt"

# # Example 1 --> Create a new instance of the TextLoader to load text documents
# loader = TextLoader(file_path)
# my_document = loader.load()  # Load the content of the document
# data = my_document[0].page_content  # Extract the text content from the first page

# # Example of splitting text into chunks using RecursiveCharacterTextSplitter

# # Define a sample JavaScript code as a string
# JS_CODE = """
# function helloWorld() {
#   console.log("Hello, World!");
# }

# // Call the function
# helloWorld();
# """

# ## Initialize a RecursiveCharacterTextSplitter for JavaScript
# js_splitter = RecursiveCharacterTextSplitter.from_language(
#     language=Language.JS,  # Specify the language as JavaScript
#     chunk_size=100,         # Set chunk size to 60 characters
#     chunk_overlap=0        # No overlap between chunks
# )

# ## Split the JavaScript code into chunks
# js_docs = js_splitter.create_documents([JS_CODE])
# js_code = js_docs[0].page_content
# Specify the file path for the document loader
file_path = "../sample.txt"

# Create a new instance of the TextLoader to load text documents
loader = TextLoader(file_path)
my_document = loader.load()
data = my_document[0].page_content

# Semantic Chunker
text_splitter = SemanticChunker(
    embeddings,  # Use the embeddings instance created earlier
    breakpoint_threshold_type="percentile",
)
docs = text_splitter.create_documents([data])
print(docs)


# ## Define a template string for the prompt
# human_template = "{text}\n{docment_content}"

# ## Create a new instance of the ChatPromptTemplate using the template string
# prompt_template = PromptTemplate.from_template(
#     template=human_template,  # The template structure
# )

# dynamic_prompt = input("Enter you are prompt :\t")

# ## Format the prompt by inserting the text and document content
# formatted_prompt = prompt_template.format(
#     text=dynamic_prompt,
#     docment_content=js_code,  # Use the chunks of JavaScript code
# )

# ## Print the formatted prompt
# # print(formatted_prompt)

# ## Optionally, use the Google Generative AI model to generate a response
# res = llm.invoke(formatted_prompt)
# print(res.content)
