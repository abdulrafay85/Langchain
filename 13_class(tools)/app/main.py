from typing_extensions import Annotated, TypedDict
from langchain_core.messages import HumanMessage
from langchain_core.tools import ToolException
from langchain_core.tools import Tool
from langchain_community.tools import WikipediaQueryRun, BraveSearch
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field   
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from typing import Annotated, Lista
from langchain_core.tools import StructuredTool
from typing import List, Tuple
from dotenv import load_dotenv
import random
import os

## Load environment variables from .env file (e.g., API keys)
load_dotenv()

## Load the API key from the .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")

## Set the API key to the environment variable for use in the model
os.environ["GEMINI_API_KEY"] = gemini_api_key

# Use OpenAI GPT Model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # Make sure this model name is correct and supported
    api_key=gemini_api_key,
    temperature=0.2  # Lower temperature for more deterministic responses
)

# @tool
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b


# Let's inspect some of the attributes associated with the tool.
# print(multiply.name)
# print(multiply.description)
# print(multiply.args)

# result = multiply.invoke({"a": 5, "b": 3})
# print(result)  # Output: 8 (addition ka result)

## ----------

# @tool
# def multiply_by_max(
#     a: Annotated[str, "scale factor"],
#     b: Annotated[List[int], "list of ints over which to take maximum"],
# ) -> int:
#     """Multiply a by the maximum of b."""
#     return a * max(b)

# print(multiply_by_max.args_schema.schema())

## ----------

# class CalculatorInput(BaseModel):
#     a: int = Field(description="first number")
#     b: int = Field(description="second number")

# @tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b


# Let's inspect some of the attributes associated with the tool.
# print(multiply.name)
# print(multiply.description)
# print(multiply.args)
# print(multiply.args_schema.schema())

# ans = multiply.invoke({"a":4, "b":4})
# print(ans)

## ----------

# @tool(parse_docstring=True)
# def foo(bar: str, baz: int) -> str:
#     """The foo.

#     Args:
#         bar: The bar.
#         baz: The baz.
#     """
#     return bar


# print(foo.args_schema.schema())

## ----------

# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b    


# async def amultiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b


# calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

# print(calculator.invoke({"a": 2, "b": 3}))
# # print(await calculator.ainvoke({"a": 2, "b": 5}))

## ----------

# class CalculatorInput(BaseModel):
#     a: int = Field(description="first number")
#     b: int = Field(description="second number")


# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b


# calculator = StructuredTool.from_function(
#     func=multiply,
#     name="Calculator",
#     description="multiply numbers",
#     args_schema=CalculatorInput,
#     return_direct=True,
#     # coroutine= ... <- you can specify an async method if desired as well
# )

# print(calculator.invoke({"a": 2, "b": 3}))
# print(calculator.name)
# print(calculator.description)
# print(calculator.args)

# ------------

# Creating tools from Runnables

# # Define the prompt
# prompt = ChatPromptTemplate.from_messages(
#     [("human", "Hello. Please respond in the style of {answer_style}.")]
# )

# # Combine the prompt, LLM, and parser into a runnable chain
# chain = prompt | llm | StrOutputParser()

# # Convert the chain into a tool
# as_tool = chain.as_tool(
#     name="Style Responder",
#     description="Responds to a message in a specific style.",
# )

# # Invoke the tool
# response = as_tool.invoke({"answer_style": "formal"})
# print(response)  # Output: "Good evening, how can I assist you?"


# -----------

# Handling Tool Errors

# def get_weather(city: str) -> int:
#     """Get weather for the given city."""
#     raise ToolException(f"Error: There is no city by the name of {city}.")

# get_weather_tool = StructuredTool.from_function(
#     func=get_weather,
#     handle_tool_error=True,
# )

# res = get_weather_tool.invoke({"city": "foobar"})
# print(res)

# -----------

# Returning artifacts of Tool execution

# @tool(response_format="content_and_artifact")
# def generate_random_ints(min: int, max: int, size: int) -> Tuple[str, List[int]]:
#     """Generate random integers."""
#     array = [random.randint(min, max) for _ in range(size)]  # Random numbers list
#     content = f"Successfully generated {size} numbers between {min} and {max}."  
#     return content, array  # Ek model ke liye, dusra future ke liye

# print(generate_random_ints.invoke({
#     "name": "generate_random_ints",
#     "args": {"min": 0, "max": 9, "size": 5},
#     "id": "123",
#     "type": "tool_call",
# }))

# # -------



# class GenerateRandomFloats(BaseTool):
#     name: str = "generate_random_floats"
#     description: str = "Generate size random floats in the range [min, max]."
#     response_format: str = "content_and_artifact"

#     ndigits: int = 2

#     def _run(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
#         range_ = max - min
#         array = [
#             round(min + (range_ * random.random()), ndigits=self.ndigits)
#             for _ in range(size)
#         ]
#         content = f"Generated {size} floats in [{min}, {max}], rounded to {self.ndigits} decimals."
#         return content, array

    # Optionally define an equivalent async method

    # async def _arun(self, min: float, max: float, size: int) -> Tuple[str, List[float]]:
    #     ...

# rand_gen = GenerateRandomFloats(ndigits=4)

# rand_gen.invoke(
#     {
#         "name": "generate_random_floats",
#         "args": {"min": 0.1, "max": 3.3333, "size": 3},
#         "id": "123",
#         "type": "tool_call",
#     }
# )

## ---------

# Wikipedia Tools

# api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
# tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# # print(tool.invoke({"query": "langchain"}))
# print(f"Name: {tool.name}")
# print(f"Description: {tool.description}")
# print(f"args schema: {tool.args}")
# print(f"returns directly?: {tool.return_direct}")

## --------------

# Customizing Default Tools

# class WikiInputs(BaseModel):
#     """Inputs to the wikipedia tool."""

#     query: str = Field(
#         description="query to look up in Wikipedia, should be 3 or less words"
#     )


# api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)

# tool = WikipediaQueryRun(
#     name="wiki-tool",
#     description="look up things in wikipedia",
#     args_schema=WikiInputs,
#     api_wrapper=api_wrapper,
#     return_direct=True,
# )

# print(tool.run("langchain"))

# print(f"Name: {tool.name}")
# print(f"Description: {tool.description}")
# print(f"args schema: {tool.args}")
# print(f"returns directly?: {tool.return_direct}")


# class add(TypedDict):
#     """Add two integers."""

#     # Annotations must have the type and can optionally include a default value and description (in that order).
#     a: Annotated[int, ..., "First integer"]
#     b: Annotated[int, ..., "Second integer"]


# class multiply(TypedDict):
#     """Multiply two integers."""

#     a: Annotated[int, ..., "First integer"]
#     b: Annotated[int, ..., "Second integer"]

# ----------------------


# class CalculatorInput(BaseModel):
#     a: int = Field(description="first number")
#     b: int = Field(description="second number")



# @tool("addition-tool", args_schema=CalculatorInput, return_direct=True)
# def add(a: int, b: int) -> int:
#     """Add two numbers."""
#     return a + b

# @tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
# def multiply(a: int, b: int) -> int:
#     """Multiply two numbers."""
#     return a * b

# # Bind tools to LLM
# tools = [add, multiply]
# llm_with_tools = llm.bind_tools(tools)



# Invoke the bound tools
# response = llm_with_tools.invoke("What is 5 + 3?")
# print(response.content)

# ------------------

# class CalculatorInput(BaseModel):
#     a: int = Field(..., description="First number")
#     b: int = Field(..., description="Second number")

# @tool("addition-tool", args_schema=CalculatorInput, return_direct=True)
# def add(a: int, b: int) -> int:
#     """Add two integers."""
#     return a + b

# @tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
# def multiply(a: int, b: int) -> int:
#     """Multiply two integers."""
#     return a * b

# tools = [add, multiply]
# # # print(tools)

# llm_with_tools = llm.bind_tools(tools)

# # print(llm_with_tools)

# query = "What is 3 * 12?"


# response = llm_with_tools.invoke(query)

# # Process tool calls to get the results
# for tool_call in response.tool_calls:
#     # Get the result from the tool call (this can vary based on the setup)
#     result = tool_call.get('result', 'No result found')
#     print(f"Result from tool {tool_call['name']}: {result}")    

# -------------

class CalculatorInput(BaseModel):
    a: int = Field(..., description="First number")
    b: int = Field(..., description="Second number")

@tool("addition-tool", args_schema=CalculatorInput, return_direct=True)
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b

tools = [add, multiply]
# # print(tools)

llm_with_tools = llm.bind_tools(tools)
# print(llm_with_tools)

query = "What is 3 * 12?"

messages = [HumanMessage(query)]

ai_msg = llm_with_tools.invoke(messages)

print(ai_msg)

for tool_call in ai_msg.tool_calls:
    # print("tool_call", tool_call)
    # Corrected dictionary to match tool names
    selected_tool = {"addition-tool": add, "multiplication-tool": multiply}[tool_call["name"].lower()]
    # print("selected_tool", selected_tool)

    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

# print("messages",messages)


final_response = llm_with_tools.invoke(messages)
print(final_response.content)

