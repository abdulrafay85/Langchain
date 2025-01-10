from langchain.output_parsers import DatetimeOutputParser, CommaSeparatedListOutputParser, PydanticOutputParser
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

# Load the API key from .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=gemini_api_key,  # Corrected the variable usage
    temperature=0.2,
    verbose=True,
)

# # Example 1
date_time_parser = DatetimeOutputParser()
# print(date_time_parser.get_format_instructions())

# # Example 2
# date_time_parser = CommaSeparatedListOutputParser()
# print(date_time_parser.get_format_instructions())

# # Example 3
# date_time_parser = PydanticOutputParser()

human_template = "{request}\n{format_instruction}"

prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(human_template),
 ])

# print(prompt)

formated_prompt = prompt.format_messages(
    request="what is the current date and time",
    format_instruction=date_time_parser.get_format_instructions(),
)

res = llm.invoke(formated_prompt)
# Example 1
print("Response Content :\t", res.content)

# Example 2
print("Response Content Parse :\t", date_time_parser.parse(
    res.content
))
 

