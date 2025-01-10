# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.prompts import PromptTemplate
# from langchain_community.cache import InMemoryCache

# from dotenv import load_dotenv
# import os

# load_dotenv()

# # Load the API key from .env file
# gemini_api_key = os.getenv("GEMINI_API_KEY")
# os.environ["GEMINI_API_KEY"] = gemini_api_key

# # Cache setup
# cache = InMemoryCache()

# # Initialize the LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     api_key=gemini_api_key,
#     temperature=0.2,
#     verbose=True,
# )

# # Create the prompt template
# prompt_template = PromptTemplate(
#     input_variables=["input"],  # Only need input here
#     template="Input: {input}\nOutput:",
# )

# # LLM Chain setup with cache
# llm_chain = LLMChain(
#     prompt=prompt_template,
#     llm=llm,
# )

# save_memory = llm_chain.set_llm_cache(cache)
# print(save_memory)

# # User input
# dynamic_prompt = input("Enter a prompt to generate a response:\t")

# # Invoke the LLM chain
# res = llm_chain.invoke(
#     input=dynamic_prompt,
# )

# print(res)
