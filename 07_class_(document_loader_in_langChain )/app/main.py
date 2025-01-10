# Import necessary libraries
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader, BSHTMLLoader, WebBaseLoader
from langchain_unstructured import UnstructuredLoader
from unstructured.partition.pdf import partition_pdf
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load the API key from the environment variable
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Initialize the ChatGoogleGenerativeAI model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Specify the model to use
    api_key=gemini_api_key,     # Set the API key for authentication
    temperature=0.2,             # Control the randomness of the output
    verbose=True,                # Enable verbose output for debugging
)

# Example 1: Load data from a text file
file_path = "../files/example.txt"  # Path to the text file
loader = TextLoader(file_path)       # Create a loader for the text file
my_data = loader.load()               # Load the data
my_context = my_data[0].page_content   # Extract the content from the loaded data

# Uncomment the below examples to load data from other file formats

# Example 2: Load data from a PDF file
# file_path = "../files/Prompt Engineering for Generative AI Future-Proof Inputs for Reliable AI Outputs (James Phoenix, Mike Taylor).pdf"
# loader = PyPDFLoader(file_path)
# my_data = loader.load()
# print(my_data)  # Inspect the loaded data

# Example 3: Load data from a CSV file
# file_path = "../files/business-financial-data-june-2024-quarter-csv.csv"
# loader = CSVLoader(file_path)
# my_data = loader.load()
# print("My Data:\t", my_data[0])  # Inspect the first entry of the loaded data

# Example 4: Load data from an HTML file
# file_path = "../files/example.html"
# loader = BSHTMLLoader(file_path)
# my_data = loader.load()
# print("My Data:\t", my_data[0].page_content)  # Inspect the first entry of the loaded data

# Example 5: Load data from a URL
# page_url = "https://en.wikipedia.org/wiki/Imran_Khan"
# loader = WebBaseLoader(web_paths=[page_url])
# my_data = loader.load()
# print(my_data)

# Example 6: Load data from a URL With the help of UnstructuredLoader
# page_url = "https://en.wikipedia.org/wiki/Babar_Azam"
# loader = UnstructuredLoader(web_url=page_url)
# my_data = loader.load()
# print(my_data)

## Example 7: Load data from a PDFs w/ tables and Multi-Modal (text + images) With the help of UnstructuredLoader

# page_path = "Prompt Engineering for Generative AI Future-Proof Inputs for Reliable Al Outputs (James Phoenix, Mike Taylor).pdf"

# raw_pdf_elements = partition_pdf(
#     filename="page_path",
#     extract_images_in_pdf=True,
#     infer_table_structure=True,
#     chunking_strategy="by_title",
#     max_characters=4000,
#     new_after_n_chars=3800,
#     combine_text_under_n_chars=2000
# )

# print(type(raw_pdf_elements))

# Define the template for the human input
human_template = "{quistion}\n{docment_content}"

# Create a prompt template from the human message
prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(human_template)
])

# Get a question from the user
dynamic_input = input("Enter your question:\t")

# Format the prompt with the user's question and document content
formated_prompt = prompt.format_messages(
    quistion=dynamic_input,
    docment_content=my_context,
)

# Invoke the LLM with the formatted prompt and print the response
res = llm.invoke(formated_prompt)
print(res.content)
