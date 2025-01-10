# Import necessary modules for prompts, Google Generative AI (Gemini), and loading environment variables
from langchain.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

import os

# Load environment variables from a .env file
load_dotenv()

# Fetch the Gemini API key from environment variables
gemini_api_key = os.getenv('GEMINI_API_KEY')
# Set the fetched API key into the environment variables (for compatibility with libraries)
os.environ['GEMINI_API_KEY'] = gemini_api_key

# Initialize the Google Generative AI (Gemini) chat model
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',  # Specify the model version of Gemini to use
    api_key=gemini_api_key,    # Pass the API key for authentication
    temperature=0.2,           # Set temperature for response variability (lower means more deterministic)
)

# Define the few-shot examples (input-output pairs) to guide the model
examples = [
   {"input": "2 🦜 2", "output": "4"},  # Example where input involves a custom operation and the output is its result
   {"input": "2 🦜 3", "output": "5"},  # Another example for the same operation to guide the model's understanding
]

# Define a few-shot prompt template with these examples
few_shot_prompt = FewShotChatMessagePromptTemplate(
    input_variables=["input"],  # Define the input variable that will be passed
    examples=examples,          # Pass the list of examples defined above
    example_prompt=ChatPromptTemplate.from_messages(
        [("human", "{input}"),  # Format: Human input as message
         ("ai", "{output}")]    # Format: AI response as message
    ),
)

# Combine everything into a final prompt template for the model
final_prompt = ChatPromptTemplate.from_messages(
   [
       ("system", "You are a wondrous wizard of math."),  # A system message setting the context or behavior of the model
       few_shot_prompt,  # Include the few-shot examples defined earlier
       ("human", "{input}"),  # Define the input from the user, which will be filled in at runtime
   ]
)

# Invoke the model with a new input (what is 4 🦜 3?) and print the response
# print(final_prompt.invoke({"input":"What's 4 🦜 3?"}))  # The model should now be able to deduce the pattern based on the examples
# print(f"final_prompt, {final_prompt}")