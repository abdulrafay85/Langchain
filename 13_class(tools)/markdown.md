# Tools

LangChain mein **tools** ek abstraction hain jo Python functions ko ek schema ke sath associate karte hain. Tools ka kaam hota hai models ke sath interact karna aur specific tasks perform karna. Isko asan tareeqe se samajhne ke liye detail mein breakdown karte hain:

---

### **Tool Abstraction Kya Hai?**
1. **Definition**:
   - Ek tool ek Python function hota hai jo ek schema ke sath define hota hai.
   - Schema mein function ka **naam**, **description**, aur **expected arguments** hotay hain.
   
2. **Purpose**:
   - Tools ko **chat models** ke sath integrate karte hain, taki model ek function ko specific inputs ke sath execute kar sake.

---

### **Key Concepts**
1. **Encapsulation**:
   - Tools ek function ko aur uske metadata (schema) ko encapsulate karte hain.
   - Metadata define karta hai ki function ka naam aur kaam kya hai.

2. **Tool Creation**:
   - Tools ko banane ke liye **@tool decorator** ka use hota hai.
   - Ye process ko simplify karta hai aur function ke naam, description, aur arguments ko automatically infer karta hai.

3. **Return Artifacts**:
   - Tools aise outputs bhi return kar sakte hain jo **artifacts** hain, jaise images, dataframes, ya complex data.

4. **Injected Arguments**:
   - Agar kisi argument ko model ke liye chhupana ho, to **injected arguments** ka use hota hai.

---

### **Tool Interface**
LangChain tools ka interface **BaseTool class** ke zariye define hota hai, jo **Runnable Interface** ka subclass hai. Tools ke kuch important attributes aur methods:

1. **Attributes**:
   - **name**: Tool ka naam.
   - **description**: Tool ka kaam batata hai.
   - **args**: Tool ke arguments ka JSON schema.

2. **Methods**:
   - **invoke**: Tool ko arguments ke sath invoke karna.
   - **ainvoke**: Asynchronous execution ke liye.

---

### **Tool Banane Ka Tareeqa**
Tools banane ka recommended tareeqa **@tool decorator** ka use karna hai. Is decorator ka kaam:
   - Function ko simplify karna.
   - Metadata automatically generate karna.

Example:
```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
   """Do numbers ko multiply kare."""
   return a * b
```

---

### **Tool Ka Direct Use**
Tool ko directly use karna bahut asaan hai:
```python
result = multiply.invoke({"a": 2, "b": 3})
print(result)  # Output: 6
```
- `invoke` method function ko dictionary format mein arguments ke sath call karta hai.

---

### **Other Methods for Tool Creation**
Agar **@tool decorator** ka use na ho, to:
1. **BaseTool Class**:
   - Direct sub-classing se tools create hote hain.
   
2. **StructuredTool**:
   - Zyada complex ya structured tools ke liye use hota hai.

---

## **Tool Inspection**
Tools ko inspect karne ke liye, aap in attributes ka use kar sakte hain:

1. **name**: Tool ka naam batata hai.
2. **description**: Tool kya kaam karta hai uska overview deta hai.
3. **args**: Tool ke input arguments ka JSON schema deta hai.

Example:
```python
print(multiply.name)  # Output: multiply
print(multiply.description)  # Output: Multiply two numbers.
print(multiply.args)
# Output:
# {
#   'type': 'object',
#   'properties': {
#       'a': {'type': 'integer'},
#       'b': {'type': 'integer'}
#   },
#   'required': ['a', 'b']
# }
```

### **Best Use Case**
- Ye features debugging aur testing ke liye helpful hain.
- Agar aap custom workflows bana rahe hain, to directly tools ke sath kaam karna zaruri ho sakta hai.

---

## **Configuring Schema**
`@tool` decorator ke options ke zariye aap tool ke schema ko customize kar sakte hain:
1. **Name** aur **Description** ko modify karna.
2. **Doc-string parsing** ka use karna, jo function ki description se schema infer karta hai.

Example:
```python
@tool(name="my_tool", description="My custom tool")
def some_tool(a: int, b: int) -> int:
    """Do numbers ko add kare."""
    return a + b
```

---

## **Tool Artifacts**
Tools ka output kabhi kabhi ek artifact hota hai, jaise:
- **Images**
- **DataFrames**
- **Custom Objects**

Artifacts ko models ke liye expose kiye bina chain ke dusre components ko accessible banaya ja sakta hai.

Example:
```python
@tool(response_format="content_and_artifact")
def some_tool(...) -> Tuple[str, Any]:
    """Ek kaam karne wala tool."""
    return "Message for model", some_artifact
```

- **content**: Model ke liye visible message.
- **artifact**: Internal use ke liye.

---

## **Special Type Annotations**
LangChain mein kuch special type annotations hain jo tool ki schema aur behavior ko modify karte hain:

### 1. **InjectedToolArg**
- Kuch arguments ko runtime par inject karna hota hai, jo model ko visible nahi hote.
- Example:
  ```python
  from langchain_core.tools import tool, InjectedToolArg

  @tool
  def user_specific_tool(input_data: str, user_id: InjectedToolArg) -> str:
      """User-specific data process karta hai."""
      return f"User {user_id} processed {input_data}"
  ```

### 2. **RunnableConfig**
- **RunnableConfig** se runtime values tools ko pass karne ka option milta hai.
- Example:
  ```python
  from langchain_core.runnables import RunnableConfig

  @tool
  async def some_func(..., config: RunnableConfig) -> ...:
      """Ek kaam karne wala tool."""
      ...
  await some_func.ainvoke(..., config={"configurable": {"value": "kuch_value"}})
  ```

### 3. **InjectedState**
- LangGraph graph ka overall state pass karne ke liye use hota hai.
- Documentation refer karein for more details.

### 4. **InjectedStore**
- LangGraph store object ko tool ke function mein pass karne ke liye use hota hai.

---

## **Best Practices for Tool Design**
1. **Naming**:
   - Tools ko meaningful aur simple naam dein.
   - Example: `add_numbers` instead of `tool1`.

2. **Documentation**:
   - Function ke kaam ko explain karne ke liye acha doc-string likhein.

3. **Type-Hinting**:
   - Inputs aur outputs ko properly define karna models ke liye zaruri hai.

4. **Scope**:
   - Ek tool ek single task ke liye design karein.

5. **Integration with Models**:
   - Models ke sath aise chat models use karein jo tool-calling APIs ko support karte ho.

---

LangChain mein **toolkits** ka concept ek abstraction provide karta hai jo ek group of tools ko saath laata hai. Ye tools ek specific task ya domain ke liye banaye gaye hote hain aur ek saath kaam karte hain. Toolkit ka primary purpose hai tools ko organize karna aur unka reuse easy banana.

---

### **Toolkit Interface**
Toolkit ek simple method provide karta hai **`get_tools()`**, jo un tools ki list return karta hai jo toolkit mein defined hain.

#### **Example**
```python
# Toolkit initialize karte hain
toolkit = ExampleToolkit(...)

# Toolkit ke tools ki list get karte hain
tools = toolkit.get_tools()
```

### **Key Concepts**
1. **Grouping Tools**: 
   - Ek toolkit mein aise tools include hote hain jo ek hi type ka kaam karte hain ya ek hi task ke liye helpful hote hain.
   - Example: File processing tools, database interaction tools, etc.

2. **Reuse and Modularity**:
   - Toolkits ek modular structure provide karte hain jo reusable aur manageable hote hain.
   - Agar ek hi toolkit ke tools use karne ho, to unhe ek group ke through manage kar sakte hain.

3. **Use with Models**:
   - Toolkits ke tools ko LLMs (chat models) ke sath integrate karna easy hota hai, kyun ke ye ek predefined structure mein hote hain.

---

### **Example Toolkits in LangChain**
1. **SQL Toolkit**: 
   - SQL databases ke saath kaam karne ke liye tools provide karta hai.
   - Example: Queries ko execute karna, schemas ko explore karna.

2. **Python Toolkit**:
   - Python code execution ke tools ko group karta hai.

3. **Math Toolkit**:
   - Mathematical calculations ke liye tools ko group karta hai.

---

### **Benefits of Using Toolkits**
- **Organized Structure**: Specific tools ko ek jagah organized rakhta hai.
- **Simplified Code**: Ek hi method `get_tools()` se tools ki access milti hai.
- **Scalability**: Naye tools add karna ya purane modify karna easy hota hai.

---

### **Summary**
LangChain toolkits tools ka ek logical group provide karte hain jo specific tasks ke liye design kiye gaye hote hain. Inka use karne se workflows streamline hote hain aur development process efficient ho jata hai. `get_tools()` method toolkit ke andar defined tools ko access karne ka standard way hai.


### **Use Case**
Agar aapka chatbot koi task perform karna chahta hai, jaise numbers multiply karna ya weather fetch karna, to tools ka use:
- **Direct execution** ke liye.
- **Model se dynamic interaction** ke liye hota hai.

LangChain tools aapke workflows ko automate aur streamline karne ke liye ek powerful abstraction hai.

<br/>

---------

<br/>

---------

<br/>

### Overview
LangChain me tools ka kaam ye hai ke yeh AI model ko external systems, jaise APIs ya databases, ke saath interact karne ki ability dete hain. Yani, AI sirf text generate nahi karta, balki wo systems ke saath kaam bhi karta hai jahan se wo data le sakta hai ya kuch calculations kar sakta hai.

Ye tools kaise kaam karte hain:

1. **Tool Creation**: Pehle, aap custom tools bana sakte hain jo specific tasks perform karte hain. Jaise ek tool jo numbers ko multiply kare ya kisi external system se data fetch kare.

2. **Tool Usage**: Jab tool ban jaata hai, model usko use kar sakta hai. Tool ko inputs milte hain, wo kaam karta hai aur result de deta hai. Jaise agar model ko kisi multiplication ka jawab chahiye ho, to wo multiplication tool ko call karega.

3. **Chains**: Agar multiple tools ka use karna ho ek ke baad ek, to aap chain bana sakte hain. Yeh tab kaam aata hai jab ek complex task ko solve karna ho.

4. **Tool Calling with LLMs**: LangChain models ko yeh tools automatically call karne ka feature dete hain, jo AI workflows ko aur flexible banaata hai.

In tools ka use aap OpenAI, Anthropic, ya Google ke models ke saath kar sakte hain. Is tarah se AI sirf baatein nahi karta, balki wo actual tasks bhi perform karta hai jo data ya APIs ke through ho sakte hain.

------------

### Key concepts
LangChain me tools ka use ek function ko define karke usko AI model tak pass karne ke liye hota hai. Tools ko banane ka kaafi asaan tareeqa hai, jo `@tool` decorator ka use karta hai. Yeh decorator tools ko create karne me madad karta hai, aur kuch key features provide karta hai:

### 1. **Tool Creation with `@tool` decorator**:
   Jab aap `@tool` decorator ka use karte hain, to LangChain automatically tool ka **naam**, **description**, aur **expected arguments** ko infer kar leta hai. Matlab aapko manually yeh sab define karne ki zarurat nahi padti, lekin agar chahen to customize bhi kar sakte hain.

   Example:
   ```python
   @tool
   def multiply(a: int, b: int) -> int:
       return a * b
   ```
   Is example mein `multiply` ek tool ban gaya hai jo do integers ko multiply karta hai. LangChain is tool ka naam aur description automatically samajh lega.

### 2. **Defining Tools that Return Artifacts**:
   Tools ko aap aise bhi define kar sakte hain jo kisi artifact ko return karte hain, jaise images ya dataframes. Yeh feature useful hota hai jab aapko complex outputs chahiye hotay hain jo sirf text nahi hote.

   Example:
   ```python
   @tool
   def generate_image(text: str) -> Image:
       # Code to generate an image from text
       return image
   ```
   Is tool mein, AI model text ko input ke roop mein leta hai aur usse ek image generate karke return karta hai.

### 3. **Hiding Input Arguments from the Schema**:
   Kabhi kabhi aap chahte hain ke kisi input argument ko tool ke schema mein nahi dikhaya jaye. Yeh kaam karte waqt `injected tool arguments` ka use hota hai, jisme aap internal inputs ko chhupaa sakte hain jo model ko directly nahi dikhne chahiye.

   Example:
   ```python
   @tool
   def internal_processing(data: str, secret: str = "hidden") -> str:
       # secret is hidden from the schema
       return f"Processed: {data}"
   ```

### 4. **Tool ka Integration in AI Model**:
   Jab tools ban jaate hain, aap unhe AI model ke saath integrate kar sakte hain. Yeh tools model ke paas ek function ki tarah pahunchtay hain aur model un tools ko call kar sakta hai. Tools ka use AI ko external systems ya specific functionalities ke saath interact karne mein madad deta hai.

### Conclusion:
LangChain tools ka use external tasks ko AI model ke saath seamlessly integrate karne ke liye hota hai. Tools ko create karne ka tareeqa simple hai, aur unka behavior customizable hai. Isse aap complex operations ko model ke liye accessible bana sakte hain.

------------

### Tool interface

---

### **Tool Interface Ka Maqsad**
LangChain me tools ka kaam hai ek **function** ko is tarah package karna ke wo AI model ko samajh aa sake. Har tool ke paas apna naam, kaam (description), aur arguments ka structure hota hai.

**BaseTool Class** iska base hota hai, aur ye 2 kaam karta hai:
1. **Tool ka Metadata Define Karna**:
   - Naam kya hai (`name`)
   - Kya karta hai (`description`)
   - Konse inputs chahiye (`args`)
2. **Tool Chalana**:
   - Synchronous tareeqe se (`invoke`)
   - Ya asynchronous tareeqe se (`ainvoke`)

---

### **Key Concepts**

1. **Tool Schema Attributes**
   Har tool ke kaam ko define karne ke liye 3 main attributes hain:
   - **`name`**:  
     Tool ka ek unique naam, jo AI ko batata hai ke kis kaam ke liye ye tool use karna hai.  
     _Example_: `"calculator_tool"`

   - **`description`**:  
     Tool kis cheez ke liye bana hai, ye batata hai.  
     _Example_: `"Ye tool basic mathematical calculations karta hai."`

   - **`args`**:  
     Ye batata hai ke tool ko chalane ke liye konsa input (arguments) chahiye. Iska format **JSON schema** me hota hai.
     ```json
     {
       "type": "object",
       "properties": {
         "num1": {"type": "number"},
         "num2": {"type": "number"}
       },
       "required": ["num1", "num2"]
     }
     ```
     _Example_: Agar aap calculator tool chalana chahte hain, to arguments `"num1": 5` aur `"num2": 10` honge.

---

2. **Execution Methods**
   Jab ek tool kaam karta hai, to uske liye 2 methods hain:
   - **`invoke`**:  
     Normal tareeqe se kaam karta hai. Ek kaam khatam hota hai, tab agla start hota hai.  
     _Example_:  
     ```python
     result = calculator_tool.invoke({"num1": 5, "num2": 3})
     print(result)  # Output: 8 (addition ka result)
     ```

   - **`ainvoke`**:  
     Agar aapko ek saath multiple tasks chalane hain, to asynchronous method use hota hai. Ye zyada efficient hai.
     _Example_:
     ```python
     async def main():
         result = await calculator_tool.ainvoke({"num1": 7, "num2": 2})
         print(result)  # Output: 9
     ```

---

### **Kya Faydah Hai?**
1. Tools ke metadata aur execution ke liye ek fixed framework milta hai.
2. Tools AI ko samajhne me madad karte hain ke konse task ke liye konsa tool use hoga.
3. Asynchronous methods (like `ainvoke`) tasks ko fast aur efficient banate hain.

Aap ise AI ko **tasks automate karne aur efficiently kaam karne** ke liye use kar sakte hain.


----------

## Creating tools from functions
- ### ``@tool decorator``
LangChain me **@tool decorator** ka use karke aap apne functions ko tools me convert kar sakte hain, jise AI models use kar sakein. Is decorator ka fayda ye hai ke aap easily function ko tool bana sakte hain bina kisi complex setup ke. 

### **@tool Decorator Ki Samajh:**

1. **Function Ko Tool Me Convert Karna:**
   Jab aap kisi function ke upar `@tool` decorator apply karte hain, to wo function ek tool me convert ho jata hai jo AI model ke saath interact kar sakta hai.

2. **Tool Name Aur Description:**
   - **Naam**: By default, tool ka naam function ka naam hota hai. Agar aap chahein to tool ka naam manually define kar sakte hain.
   - **Description**: Function ka **docstring** (jo description function ke andar likhi hoti hai) ko tool ka description bana diya jata hai.

### **Example:**

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""  # Ye docstring tool ka description banega
    return a * b
```

### **Attributes:**

- **`multiply.name`**: Ye aapko function ka naam dega jo tool ka naam banega. By default, ye function ka naam hoga (`multiply`).
- **`multiply.description`**: Ye function ke docstring ko tool ki description me convert karega. Is example me, `"Multiply two numbers."`
- **`multiply.args`**: Ye function ke arguments ka schema bataega, jisme inputs ki types aur unki requirements hongi.

### **Code Output:**

```python
print(multiply.name)        # Output: multiply
print(multiply.description) # Output: Multiply two numbers.
print(multiply.args)        # Output: JSON schema of arguments, e.g., {'a': {'type': 'integer'}, 'b': {'type': 'integer'}}
```

### **Summary:**
- **@tool** decorator ke through, function ko ek tool banaya jaata hai.
- **Naam** aur **description** ko automatic ya manually define kiya jaa sakta hai.
- Ye tools AI models ko input arguments aur relevant actions ke liye clearly define karte hain, taki models efficiently kaam kar sakein.

Is tarah se aap apne functions ko easily tools mein convert kar sakte hain aur unhe AI tasks ke liye use kar sakte hain.

<br/>

------

<br/>

LangChain me `@tool` decorator ka use aapko custom tools banane ke liye hota hai. Ye tools kisi bhi function ko ek specific format mein convert karte hain, jise aap LangChain model ke saath use kar sakte hain. 

### **Basic Explanation:**
Jab aap `@tool` decorator ka use karte hain, to aap ek function ko ek special tool mein convert karte hain, jo kisi bhi AI model ke through easily call ho sakta hai. Aap is tool ko specific input dete hain, aur ye ek result generate karta hai.

### **1. Basic Tool Example:**
```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

Yahaan, humne ek function `multiply` banaya hai jo do numbers ko multiply karta hai. `@tool` decorator is function ko LangChain ke tool format mein convert kar dega. Is tool ka naam automatically `multiply` ho jayega, aur function ka description bhi uski docstring se liya jayega.

- **Name**: Multiply (ye function ka naam hai).
- **Description**: "Multiply two numbers." (ye function ki docstring hai).

### **2. Async Tool Example:**
Jab aapko koi function asynchronous chahiye hota hai, jaise time-consuming tasks, to aap usse `async` bana sakte hain.

```python
@tool
async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers asynchronously."""
    return a * b
```

Ye function ab asynchronously execute hoga. Matlab, agar koi time-lag ya delay ho, to system ko block nahi karega.

### **3. Arguments and Schema:**
Agar aap function arguments ko bhi explain karna chahte hain, to `@tool` decorator schema ko use karta hai. Jaise, agar aapko ek list of numbers ka maximum multiply karna ho:

```python
from typing import Annotated, List

@tool
def multiply_by_max(
    a: Annotated[str, "scale factor"],
    b: Annotated[List[int], "list of ints over which to take maximum"],
) -> int:
    """Multiply a by the maximum of b."""
    return a * max(b)
```

Yahaan, `a` ek string hai jo scale factor ko represent karta hai, aur `b` ek list hai jisme maximum number ko find karke `a` se multiply kiya jata hai.

### **4. Tool Schema:**
Jab aap tool banate hain, to aap arguments ka schema generate kar sakte hain jo ye define karta hai ki inputs kis type ke hone chahiye. Jaise:

```python
multiply_by_max.args_schema.schema()
```

Ye aapko ek schema deta hai jisme:
- `a` ka type string hai,
- `b` ka type list of integers hai.

### **Summary:**
- `@tool` decorator functions ko tools me convert karta hai jo LangChain AI models ke saath kaam karte hain.
- Aap synchronous aur asynchronous tools bana sakte hain.
- Function arguments ko define karne ke liye schema ka use hota hai.

Isse aap apne custom functions ko easily integrate kar sakte hain aur unhe models ke through efficiently use kar sakte hain.

----------

<br/>


## Explanation:
### Basic Use:
- ``Annotated`` aapko type annotations ke sath additional information dene ki facility deta hai. Matlab, aap variable ya function argument ka type specify karte hue uske baare mein aur zyada description ya metadata provide kar sakte hain.

Syntax:
```python
Annotated[Type, Info]
```

- ``Type`` : Yeh variable ya argument ka type specify karta hai (jaise str, int, float, etc.).
- ``Info`` : Yeh extra metadata hota hai jo aapke type ke sath associated hota hai (for example, description, valid range, etc.).

<br/>

---------

<br/>

Is code mein `@tool` decorator ka use karke ek custom tool create kiya gaya hai jo do numbers ko multiply karta hai. Code ko samajhne ke liye har part ko break karte hain:

### Code Breakdown:

1. **`@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)`**
   - **`@tool`**: Yeh LangChain ka decorator hai jo function ko ek tool mein convert kar deta hai. Aap is tool ko LangChain ke ecosystem mein kisi bhi model ya pipeline ke saath integrate kar sakte hain.
   - **`"multiplication-tool"`**: Yeh custom tool ka naam hai. Jab aap is tool ko call karenge, to yeh name use hoga.
   - **`args_schema=CalculatorInput`**: Iska matlab hai ke function ke arguments ko `CalculatorInput` schema ke hisaab se validate kiya jayega. `CalculatorInput` ek **Pydantic BaseModel** hai jo input arguments ka structure define karta hai.
     - **`CalculatorInput` class** mein **`a` aur `b`** do integer variables hain jo tool ko pass kiye jayenge.
     - **`args_schema`** LangChain ko bataata hai ke input data ka format kya hoga.
   - **`return_direct=True`**: Yeh specify karta hai ke function direct result return karega, bina kisi additional processing ke. Agar `False` hota, to LangChain kuch extra steps perform karta.

2. **Function Definition:**
   ```python
   def multiply(a: int, b: int) -> int:
       """Multiply two numbers."""
       return a * b
   ```
   - **`def multiply(a: int, b: int) -> int:`**: Yeh function define karta hai jo **`a`** aur **`b`** ko parameters ke roop mein leta hai. Dono parameters integer type ke hain.
   - **`"""Multiply two numbers."""`**: Yeh docstring hai, jo tool ke description ke roop mein use hota hai. Isse tool ko samajhne mein madad milti hai ke yeh kya karta hai.
   - **`return a * b`**: Yeh function do numbers ko multiply karta hai aur result return karta hai.

3. **Function ko Tool Mein Convert Karna:**
   - Jab **`@tool`** decorator use hota hai, to yeh function ko ek reusable tool bana deta hai. Iska matlab hai ke yeh function LangChain ke tools ke roop mein integrate ho sakta hai, aur isse aap apne models ya workflows ke andar use kar sakte hain.

### Key Points:
- **Tool Naming**: Aap tool ko custom naam de sakte hain. Is case mein `"multiplication-tool"` diya gaya hai.
- **Schema Validation**: Tool ke input arguments ko **`args_schema=CalculatorInput`** ke zariye validate kiya jaata hai. `CalculatorInput` ek Pydantic model hai jo ensure karta hai ke input arguments sahi type aur format mein ho.
- **Direct Result**: `return_direct=True` ka matlab hai ke function ka result directly return hoga, bina kisi intermediate step ke.

### Example:
Is tool ko use karte waqt aapko inputs dene honge jo **`CalculatorInput`** ke according honge, jaise:
```python
multiply({"a": 5, "b": 3})
```
Is case mein, result **`5 * 3 = 15`** hoga.

### Summary:
- **Tool Creation**: Aap `@tool` decorator ke zariye ek simple function ko reusable tool mein convert kar sakte hain.
- **Schema Validation**: Input validation `args_schema` ke zariye define ki jaati hai.
- **Direct Output**: Agar `return_direct=True` diya jaye, to tool direct result return karega bina kisi extra processing ke.

<br/>

--------

<br/>

### Docstring parsing
### **`parse_docstring=True` ka kya matlab hai?**

Jab aap `@tool(parse_docstring=True)` use karte hain, to LangChain **automatic** aapke function ke **docstring** ko padhta hai aur usse **arguments ka schema** banata hai. Docstring wo chhoti si description hoti hai jo function ke niche likhi jaati hai, jisme aap batate hain ki function kaise kaam karta hai aur uske inputs kya hain.

### Example:

```python
@tool(parse_docstring=True)
def foo(bar: str, baz: int) -> str:
    """The foo.

    Args:
        bar: The bar.
        baz: The baz.
    """
    return bar
```

#### Is code mein kya ho raha hai?
1. **Docstring** mein aapne function ke inputs `bar` aur `baz` ke baare mein likha hai.
2. **LangChain** is docstring ko padhta hai aur **schema** create karta hai jo us function ke arguments (inputs) ko explain kare.
   
#### Result:
LangChain is docstring ko read karke **schema banata hai**, jo kuch is tarah dikhega:

```python
foo.args_schema.schema()

{
    'description': 'The foo.',
    'properties': {
        'bar': {'description': 'The bar.', 'title': 'Bar', 'type': 'string'},
        'baz': {'description': 'The baz.', 'title': 'Baz', 'type': 'integer'}
    },
    'required': ['bar', 'baz'],
    'title': 'fooSchema',
    'type': 'object'
}
```

### **Key Points**:
- Aapko function ke arguments ko manually explain karne ki zarurat nahi, kyunki LangChain **docstring ko samajh kar** un arguments ke baare mein schema banata hai.
- Agar aapke docstring mein **`Args:`** section hota hai, to LangChain usko use karta hai.
- **`bar` aur `baz`** ke baare mein descriptions ko **`properties`** ke andar daal diya jata hai.

### **Faydah**:
- Isse **time bachata** hai, kyunki aapko schema ko manually likhne ki zaroorat nahi padti.
- Aapke code mein **clarity** bhi hoti hai, kyunki arguments ka description direct docstring se milta hai.


<br/>

-----------

<br/>

### StructuredTool
**`StructuredTool`** ka use aapko apne functions ko **tools me convert** karne ke liye kiya jata hai. Yeh aapko flexibility deta hai, aur aap asaani se **synchronous aur asynchronous functions** ko ek hi tool me handle kar sakte ho.

### **Asan Tarike se Samajhna:**

1. **Normal Function (`multiply`)**:
   - Yeh ek function hai jo do numbers ko multiply karta hai.

2. **Asynchronous Function (`amultiply`)**:
   - Yeh wahi kaam karta hai, lekin **asynchronously** (matlab isme time lag sakta hai, jaise network ya database se data lena ho).

3. **`StructuredTool.from_function`**:
   - Iska kaam hai apne function ko ek **tool** me convert karna. 
   - Aap dono functions (normal aur async) ko ek saath ek tool me convert kar sakte hain.

4. **`invoke` aur `ainvoke`**:
   - **`invoke`** function ko normal tareeqe se chalata hai.
   - **`ainvoke`** asynchronous function ko chalata hai, aur aapko **`await`** ka use karna padta hai.

### Example:
- **`invoke`** se aap 2 aur 3 ko multiply kar ke **6** result lete ho.
- **`ainvoke`** se aap 2 aur 5 ko multiply kar ke **10** result lete ho.

### Fayda:
- Aap apne functions ko zyada **customizable** aur **configurable** bana sakte hain.
- Yeh tool ko asynchronous aur synchronous functions dono ko support karta hai.

Aise, **`StructuredTool`** aapke liye ek aise cheez hai jisse aap easily apne existing functions ko **tools** me convert kar sakte ho.

### **StructuredTool Example 1 with Code**

```python
from langchain_core.tools import StructuredTool

# Normal function to multiply two numbers
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Asynchronous function to multiply two numbers
async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers asynchronously."""
    return a * b

# Create a StructuredTool using both functions
calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

# Using invoke to call the normal function
print(calculator.invoke({"a": 2, "b": 3}))  # Output: 6

# Using ainvoke to call the async function
import asyncio
async def run_async():
    result = await calculator.ainvoke({"a": 2, "b": 5})
    print(result)  # Output: 10

# Running the async function
asyncio.run(run_async())
```

### **Explanation in Simple Roman Urdu**:
1. **`multiply(a, b)`** ek simple function hai jo 2 numbers ko multiply karta hai.
2. **`amultiply(a, b)`** ek async function hai jo waise hi kaam karta hai, lekin isme aapko **`await`** use karna padta hai, jo asynchronous execution ke liye hai.
3. **`StructuredTool.from_function(func=multiply, coroutine=amultiply)`**: Yeh tool banata hai jisme aap dono types (synchronous aur asynchronous) functions ko ek saath handle kar sakte hain.
4. **`invoke`**: Yeh normal function ko call karta hai.
5. **`ainvoke`**: Yeh asynchronous function ko call karta hai.

Is tarah, **`StructuredTool`** ka use aapko multiple functions ko easily tool me convert karne aur execute karne me madad karta hai, chahe wo synchronous ho ya asynchronous.

#### Example 2

**LangChain Structured Tool ki Explanatio**

### 1. **Schema Banana (CalculatorInput Class)**:
Pehle humne `Pydantic` ka use kiya hai `CalculatorInput` class banane ke liye jo input arguments ko define karta hai:

```python
class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")
```

- **`a` aur `b`**: Yeh dono integers hain jo hum input me denge (numbers jo multiply karna hain).
- **`Field`**: Yeh input arguments ke liye descriptions deta hai, jo tool ko help karta hai inputs ko samajhne me.

### 2. **Function (multiply)**:
Phir humne `multiply` function banaya hai jo input numbers ko multiply karta hai:

```python
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

- **`multiply` function**: Yeh 2 numbers ko multiply karke unka result return karta hai.

### 3. **StructuredTool Banana (Using from_function)**:
Ab humne `StructuredTool.from_function()` ka use kiya jo function ko LangChain ka tool banata hai. Isme humne function ke saath saath schema bhi specify kiya hai:

```python
calculator = StructuredTool.from_function(
    func=multiply,
    name="Calculator",
    description="multiply numbers",
    args_schema=CalculatorInput,
    return_direct=True,
)
```

- **`func=multiply`**: Yeh `multiply` function ko tool banata hai.
- **`name="Calculator"`**: Tool ka naam "Calculator" rakha gaya hai.
- **`description="multiply numbers"`**: Yeh batata hai ke tool kis kaam ka hai, yeh numbers ko multiply karta hai.
- **`args_schema=CalculatorInput`**: Yeh schema batata hai ke tool ko kaunse inputs chahiye, yani `a` aur `b`.
- **`return_direct=True`**: Yeh specify karta hai ke function ka direct result return ho.

### 4. **Tool ka Use (Invoke and Inspect)**:
Ab humne tool ko call (invoke) kiya hai aur kuch attributes ko print kiya hai:

```python
print(calculator.invoke({"a": 2, "b": 3}))  # Multiply 2 and 3
print(calculator.name)  # Tool ka naam
print(calculator.description)  # Tool ka description
print(calculator.args)  # Arguments ka schema
```

- **`invoke({"a": 2, "b": 3})`**: Yeh function `a=2` aur `b=3` ke saath run hota hai aur output 6 deta hai (multiply hone ke baad).
- **`name`**: Tool ka naam print hota hai, jo `"Calculator"` hai.
- **`description`**: Tool ka description print hota hai, jo `"multiply numbers"` hai.
- **`args`**: Yeh tool ke input arguments (schema) ko describe karta hai, yani `a` aur `b` ki types aur unke descriptions.

### **Summary**:
Is tarah se **`StructuredTool`** ka use karke hum apne simple functions ko LangChain tools me convert kar sakte hain. Yeh tool inputs ko validate karta hai, tool ko ek naam aur description deta hai, aur aasan tareeqe se functions ko LangChain ke workflow me integrate karne me madad karta hai.

<br/>

--------

<br/>

### Creating tools from Runnables
**LangChain** mein **Runnables** ek tareeqa hai jo aapke functions ko ek structured tool mein convert karta hai. Jaise aap ek tool bana rahe ho, us tool ka kaam ek specific task perform karna hota hai. Hum **`as_tool()`** method se kisi bhi chain ko tool mein convert kar sakte hain.

### Example Samajhne ki Koshish karte hain:

1. **Prompt Template**: Pehle, hum ek **prompt** create karte hain jo user se kuch input lega. Is case mein, yeh prompt user se **`answer_style`** ka input lega.

   ```python
   prompt = ChatPromptTemplate.from_messages(
       [("human", "Hello. Please respond in the style of {answer_style}.")]
   )
   ```

   Isme **`answer_style`** ek placeholder hai jisme user input karega.

2. **Fake Language Model (LLM)**: Yeh ek placeholder model hai jo test karne ke liye use hota hai, jisme hum predefined response set karte hain. Yani jab input milta hai, yeh uska jawab generate karega.

   ```python
   llm = GenericFakeChatModel(messages=iter(["hello matey"]))
   ```

3. **Output Parser**: Hum ek parser use karte hain jo output ko readable string mein convert kar dega.

   ```python
   chain = prompt | llm | StrOutputParser()
   ```

4. **Converting to a Tool**: Jab hum chaahte hain ke yeh chain ek tool ke roop mein kaam kare, toh hum `as_tool()` method use karte hain. Iske zariye, hum tool ka naam, description, aur input arguments define kar sakte hain.

   ```python
   as_tool = chain.as_tool(
       name="Style responder", description="Description of when to use tool."
   )
   ```

   Yeh tool ab ek **name** aur **description** ke saath kaam karega.

### Output:

Jab hum `as_tool.args` ko print karte hain, toh hum tool ka schema dekh sakte hain, jo bata raha hota hai ki tool kis input ko expect karta hai.

```python
{'answer_style': {'title': 'Answer Style', 'type': 'string'}}
```

Yahaan, **`answer_style`** ek input argument hai jiska **title** "Answer Style" hai aur **type** "string" hai.

### Key Concept:
- **`as_tool()`** method kisi bhi **chain** ko ek **tool** mein convert kar deta hai.
- Hum tool ka **name** aur **description** set kar sakte hain.
- Aur **args** ko define kar sakte hain, jisme tool ka expected input aur uska type bataya jata hai.

### Simple Example:
Agar aap ke paas ek simple function ho jo do numbers ko multiply karta ho, toh aap is function ko tool mein convert kar sakte hain jisme aap **arguments** aur **description** specify karte hain. Is se aap apne function ko ek reusable tool bana sakte hain jo ek specific task ko perform karega.

Mujhe ummed hai ab aapko concept thoda clearer ho gaya hoga. Agar aur koi confusion ho toh zaroor poochein!

<br/>

-----------------

<br/>

### How to create async tools
LangChain mein tools ko async (asynchronous) ya sync (synchronous) banaya ja sakta hai, aur yeh depend karta hai ke aapka kaam kis tarah ka hai. **Async tools** zyada useful hote hain jab aapko lambi operations (jaise network requests ya complex calculations) ko efficiently handle karna ho bina dusre tasks ko block kiye.

### **Key Concepts**:
1. **Runnable Interface**:  
   LangChain mein tools **Runnable** interface ko implement karte hain, jo do important methods provide karta hai:
   - **`invoke`**: Yeh synchronous (sync) execution ke liye hota hai.
   - **`ainvoke`**: Yeh asynchronous (async) execution ke liye hota hai.
   
   - **Synchronous tools** woh hote hain jo jaldi se execute ho jaate hain aur dusre kaam ko block nahi karte.
   - **Asynchronous tools** jab aapko background mein koi lamba kaam karna ho, jaise database queries ya API calls, tab use kiye jaate hain. Yeh dusre tasks ko block nahi karte.

2. **Async tools ka use**:
   Agar aap async codebase mein kaam kar rahe hain, toh **async tools** ka use karna zyada efficient hota hai. Async tools ko use karte waqt, LangChain background mein operations ko handle karta hai bina main task ko rok ke. Agar aap synchronous tool use karte hain, toh LangChain thoda extra overhead dalta hai, kyunki yeh operation ko thread mein execute karta hai.

3. **Sync aur Async Tool Difference**:
   - Agar aap **sync** tool use karte hain aur `ainvoke()` call karte hain, toh LangChain automatically async version ko handle karta hai lekin thoda overhead dalta hai.
   - Agar aap **async** tool provide karte hain, toh aapko sirf `ainvoke()` use karna chahiye, `invoke()` se nahi chalana.

### **Code Breakdown**:

#### Example 1: Sync Tool with Async Overhead
```python
from langchain_core.tools import StructuredTool

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

calculator = StructuredTool.from_function(func=multiply)

print(calculator.invoke({"a": 2, "b": 3}))  # Sync call
print(await calculator.ainvoke({"a": 2, "b": 5}))  # Async call with some overhead
```
- **`multiply`** ek sync function hai. Jab aap `.ainvoke()` use karte hain, LangChain usay async tarike se run karta hai, lekin thoda extra overhead hota hai.

#### Example 2: Async Tool Without Overhead
```python
from langchain_core.tools import StructuredTool

async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers asynchronously."""
    return a * b

calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)

print(calculator.invoke({"a": 2, "b": 3}))  # Sync call
print(await calculator.ainvoke({"a": 2, "b": 5}))  # Direct async call without overhead
```
- **`amultiply`** ek async function hai. Jab aap `.ainvoke()` use karte hain, yeh directly async function ko use karta hai bina extra overhead ke.

#### Example 3: Error While Using `invoke` with Async Function
```python
@tool
async def multiply(a: int, b: int) -> int:
    """Multiply two numbers asynchronously."""
    return a * b

try:
    multiply.invoke({"a": 2, "b": 3})
except NotImplementedError:
    print("Raised not implemented error. You should not be doing this.")
```
- Agar aap **async function** use kar rahe hain aur **`invoke()`** use karne ki koshish karte hain, toh **NotImplementedError** milega, kyunki async functions ko sirf `.ainvoke()` se hi call karna chahiye.

### **Kab Sync aur Async Tools Use Karein**:
- **Async tools** tab use karein jab aapko lambi operations (jaise data fetch karna ya APIs call karna) ko handle karna ho bina dusre tasks ko block kiye.
- **Sync tools** tab use karein jab kaam fast ho aur async ka overhead unnecessary ho.

### **Summary**:
- Agar aap **async codebase** mein kaam kar rahe hain, toh **async tools** use karna chahiye.
- **Sync tools** ka use tab karein jab kaam jaldi ho aur aapko async ka overhead nahi chahiye.
- **Async function** ka use karte waqt, **`ainvoke()`** use karna zaroori hai, **`invoke()`** nahi.

Agar aapko aur clarification chahiye ho toh bataiye!

<br/>

---------

<br/>

### Handling Tool Errors

LangChain mein error handling ek zaroori feature hai jab aap tools ko use karte hain, especially jab aapke code mein koi issue ho jaye, aur aap chahte hain ke tool apne aap se handle kare aur process ko rukne na de. 

### **ToolException**:
Jab aapka tool kisi reason ki wajah se fail hota hai, jaise invalid data, aap **ToolException** raise karte hain. Yeh ek special error type hai jo LangChain mein use hota hai.

### **handle_tool_error**:
Jab aap **handle_tool_error** ko `True` ya kuch aur set karte hain, toh LangChain tool ke andar error ko handle karta hai. Iska matlab hai, agar koi error hota hai, toh LangChain apne aap usko catch karke user ko ek suitable message dega.

### **Example 1: Default Error Handling**:
Agar aap **handle_tool_error=True** set karte hain, toh jab tool error throw karega, LangChain us error ko apne default method se handle karega aur ek error message return karega.

```python
def get_weather(city: str) -> int:
    """Get weather for the given city."""
    raise ToolException(f"Error: There is no city by the name of {city}.")

get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=True,  # Tool error ko handle karne ke liye True set kar rahe hain
)

print(get_weather_tool.invoke({"city": "foobar"}))
```

**Output**: `'Error: There is no city by the name of foobar.'`

Yahan, **ToolException** raise hota hai aur LangChain is error ko handle kar leta hai.

### **Example 2: Custom Error Message**:
Agar aap chahte hain ke tool koi specific error message return kare jab koi issue ho, toh aap **handle_tool_error** ko string mein set kar sakte hain.

```python
get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error="There is no such city, but it's probably above 0K there!",  # Custom message
)

print(get_weather_tool.invoke({"city": "foobar"}))
```

**Output**: `'There is no such city, but it's probably above 0K there!'`

Is case mein, jab tool error raise karega, toh aapka predefined message return hoga.

### **Example 3: Handling Error with a Function**:
Agar aap chahein ke error ko ek specific function ke through handle kiya jaye, toh aap apna function define kar sakte hain. Yeh function **ToolException** ko handle karega aur aapka desired output return karega.

```python
def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"

get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=_handle_error,  # Custom function jo error ko handle kare
)

print(get_weather_tool.invoke({"city": "foobar"}))
```

**Output**: `'The following errors occurred during tool execution: `Error: There is no city by the name of foobar.`'`

### **Summary**:
1. **ToolException** ko raise karke aap errors handle karte hain jab tool execute nahi kar pata.
2. **handle_tool_error** ko `True`, ek string, ya ek function se set kar ke aap tool ke error handling ko control karte hain.
3. Agar aap **True** set karte hain, toh LangChain default message return karega.
4. Agar aap string set karte hain, toh custom message hamesha return hota hai.
5. Agar aap function set karte hain, toh aap zyada control paa sakte hain aur custom logic apply kar sakte hain.

Is system ka use agents mein error handling ke liye hota hai, taki jab error aaye, agent ko pata ho aur wo apne kaam ko rukne na de.

Agar aapko is baare mein aur questions hain ya koi specific part samajhna hai, toh bataiye!

-------------------

LangChain mein error handling ek zaroori feature hai jab aap tools ko use karte hain, especially jab aapke code mein koi issue ho jaye, aur aap chahte hain ke tool apne aap se handle kare aur process ko rukne na de. 

### **ToolException**:
Jab aapka tool kisi reason ki wajah se fail hota hai, jaise invalid data, aap **ToolException** raise karte hain. Yeh ek special error type hai jo LangChain mein use hota hai.

### **handle_tool_error**:
Jab aap **handle_tool_error** ko `True` ya kuch aur set karte hain, toh LangChain tool ke andar error ko handle karta hai. Iska matlab hai, agar koi error hota hai, toh LangChain apne aap usko catch karke user ko ek suitable message dega.

### **Example 1: Default Error Handling**:
Agar aap **handle_tool_error=True** set karte hain, toh jab tool error throw karega, LangChain us error ko apne default method se handle karega aur ek error message return karega.

```python
def get_weather(city: str) -> int:
    """Get weather for the given city."""
    raise ToolException(f"Error: There is no city by the name of {city}.")

get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=True,  # Tool error ko handle karne ke liye True set kar rahe hain
)

print(get_weather_tool.invoke({"city": "foobar"}))
```

**Output**: `'Error: There is no city by the name of foobar.'`

Yahan, **ToolException** raise hota hai aur LangChain is error ko handle kar leta hai.

### **Example 2: Custom Error Message**:
Agar aap chahte hain ke tool koi specific error message return kare jab koi issue ho, toh aap **handle_tool_error** ko string mein set kar sakte hain.

```python
get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error="There is no such city, but it's probably above 0K there!",  # Custom message
)

print(get_weather_tool.invoke({"city": "foobar"}))
```

**Output**: `'There is no such city, but it's probably above 0K there!'`

Is case mein, jab tool error raise karega, toh aapka predefined message return hoga.

### **Example 3: Handling Error with a Function**:
Agar aap chahein ke error ko ek specific function ke through handle kiya jaye, toh aap apna function define kar sakte hain. Yeh function **ToolException** ko handle karega aur aapka desired output return karega.

```python
def _handle_error(error: ToolException) -> str:
    return f"The following errors occurred during tool execution: `{error.args[0]}`"

get_weather_tool = StructuredTool.from_function(
    func=get_weather,
    handle_tool_error=_handle_error,  # Custom function jo error ko handle kare
)

print(get_weather_tool.invoke({"city": "foobar"}))
```

**Output**: `'The following errors occurred during tool execution: `Error: There is no city by the name of foobar.`'`

### **Summary**:
1. **ToolException** ko raise karke aap errors handle karte hain jab tool execute nahi kar pata.
2. **handle_tool_error** ko `True`, ek string, ya ek function se set kar ke aap tool ke error handling ko control karte hain.
3. Agar aap **True** set karte hain, toh LangChain default message return karega.
4. Agar aap string set karte hain, toh custom message hamesha return hota hai.
5. Agar aap function set karte hain, toh aap zyada control paa sakte hain aur custom logic apply kar sakte hain.

Is system ka use agents mein error handling ke liye hota hai, taki jab error aaye, agent ko pata ho aur wo apne kaam ko rukne na de.

Agar aapko is baare mein aur questions hain ya koi specific part samajhna hai, toh bataiye!

<br/>

-------

<br/>

###  Handling Tool Errors

```python
raise ToolException(f"Error: There is no city by the name of {city}.")
```

Yeh line ek **exception raise** karti hai jab koi unexpected ya invalid input detect hota hai. Specific taur par, yeh **ToolException** ko trigger karti hai, jo LangChain mein ek special type ki error hoti hai.

### **Breakdown**:

1. **`raise` Keyword**:
   - Yeh Python ka command hai jo explicitly ek exception (error) throw karne ke liye use hota hai.
   - Jab `raise` call hoti hai, program execution turant ruk jata hai aur woh exception trigger hoti hai.

2. **`ToolException`**:
   - LangChain mein ek custom exception hai.
   - Iska use tools ke errors ko handle karne ke liye hota hai.
   - Isko raise karne ka matlab hai ke tool ke andar kuch galat hua aur iska output error ki form mein hoga.

3. **Error Message**:
   - `f"Error: There is no city by the name of {city}."`
   - Yeh ek formatted string hai jo error ka specific message dene ke liye use hoti hai. `{city}` placeholder mein input value aa jati hai jo user ne provide ki hoti hai.
   - Example:
     Agar `city = "Atlantis"`, toh error message banega:
     ```
     Error: There is no city by the name of Atlantis.
     ```

### **Kya karta hai yeh?**

Agar user tool ko kisi invalid input ke sath call kare, toh yeh exception raise karega aur LangChain ya agent ko signal dega ke kuch galat ho gaya hai.

### **Example**:

```python
def get_weather(city: str) -> int:
    """Get weather for the given city."""
    # Agar city ka naam invalid hai toh ToolException raise karo
    raise ToolException(f"Error: There is no city by the name of {city}.")

# Invalid input ke sath tool ko call karte hain
try:
    get_weather("Atlantis")
except ToolException as e:
    print(e)
```

**Output**:
```
Error: There is no city by the name of Atlantis.
```

### **Why Use This?**

1. **Error Handling**:
   - Agar tool ke andar kuch problem ho, toh ye tool se bahar ek clear message bhejta hai.
   - Agents ya LangChain system ko pata chal jata hai ke tool fail hua hai aur wo uska solution dhoondh sakte hain.

2. **Custom Messages**:
   - Error ke sath ek specific aur meaningful message bhejne ke liye.

3. **Workflow Continuation**:
   - Agar system ko pata ho ke error kahan aur kyun ho rahi hai, toh wo recovery steps le sakta hai aur apna kaam continue kar sakta hai.

Agar aapko isme aur clarification chahiye, bataiye!

<br/>

---------

<br/>

### **3 primary methods for createing tools in langchian**:

---

### 1. **@tool Decorator**
   - **Istemaal:** Ye decorator code ko ek simple tool me badalne ke liye use hota hai.
   - **Asaan aur Seedha Tarika:** Kam code likhna hota hai.
   - **Example:**
     ```python
     from langchain_core.tools import tool

     @tool
     def multiply(a: int, b: int) -> int:
         """Multiply two numbers."""
         return a * b

     print(multiply.invoke({"a": 2, "b": 3}))  # Output: 6
     ```
   - **Khasiyat:**
     - Function directly tool ban jata hai.
     - Documentation (docstring) ko use karke arguments aur details define karta hai.

---

### 2. **StructuredTool.from_function**
   - **Istemaal:** Ye tab use hota hai jab tool ko zyada control aur customizability deni ho.
   - **Advanced Control:** Arguments aur async methods ka support.
   - **Example:**
     ```python
     from langchain_core.tools import StructuredTool

     def multiply(a: int, b: int) -> int:
         """Multiply two numbers."""
         return a * b

     calculator = StructuredTool.from_function(
         func=multiply,
         name="Calculator",
         description="Multiplies numbers.",
     )

     print(calculator.invoke({"a": 2, "b": 3}))  # Output: 6
     ```
   - **Khasiyat:**
     - **Async Implementation:** Agar aap async environment me kaam kar rahe hain.
     - Zyada customization ke liye acha hai.

---

### 3. **Subclassing BaseTool**
   - **Istemaal:** Jab aapko ek complex aur custom tool banana ho, jo default behavior ke upar ho.
   - **Maximal Control:** Aap har cheez customize kar sakte hain.
   - **Example:**
     ```python
     from langchain_core.tools import BaseTool
     from pydantic import BaseModel, Field

     class CalculatorInput(BaseModel):
         a: int = Field(description="First number")
         b: int = Field(description="Second number")

     class CustomCalculatorTool(BaseTool):
         name = "Calculator"
         description = "Multiply numbers"
         args_schema = CalculatorInput

         def _run(self, a: int, b: int):
             return a * b

     multiply = CustomCalculatorTool()
     print(multiply.invoke({"a": 2, "b": 3}))  # Output: 6
     ```
   - **Khasiyat:**
     - Pura control `_run` aur `_arun` (async) methods ka hota hai.
     - Advanced use-cases ke liye best.

---

### **Comparison Table:**

| Method                  | Complexity Level | Async Support | Customization | Use Case                                    |
|-------------------------|------------------|---------------|---------------|--------------------------------------------|
| **@tool Decorator**     | Low              | Limited       | Basic         | Simple tools with minimal configuration.   |
| **StructuredTool**      | Medium           | Yes           | Moderate      | Tools with more customization and async.   |
| **BaseTool Subclassing**| High             | Yes           | Maximal       | Complex tools with complete customization. |

Agar aapko kisi ek approach par zyada details ya implementation chahiye, to bataiye!

<br/>

----------

<br/>

### Returning artifacts of Tool execution

---

### Artifacts Kya Hain?

LangChain mein **artifacts** ek tarah ka structured output hota hai jo ek tool ya function ke execute hone ke baad banta hai. Yeh ek **technical ya detailed result** ho sakta hai jo kisi aur process ke liye zaroori hote hain, jaise machine learning models ya downstream systems.

---

### Tools aur Artifacts ka Rishta

1. **Content**: 
   - Yeh ek **simple output** hota hai jo human-readable ho, jaise ek message ya summary.
   - Example: `"Aapke numbers generate ho gaye hain"`

2. **Artifact**:
   - Yeh ek **detailed technical output** hota hai jo models ya processes ko use karne ke liye hota hai.
   - Example: `[3, 6, 1, 9, 4]` (randomly generated numbers ki list).

---

### Example Code Samajhna
Aapke code mein, do cheezein return ho rahi hain:
1. **Content**: Ek success message jo LLM ke liye hai.
2. **Artifact**: Ek list of numbers jo kisi aur process mein reuse ki ja sakti hai.

Code:
```python
@tool(response_format="content_and_artifact")
def generate_random_ints(min: int, max: int, size: int) -> Tuple[str, List[int]]:
    array = [random.randint(min, max) for _ in range(size)]  # Random numbers list
    content = f"Successfully generated {size} numbers between {min} and {max}."  
    return content, array
```

---

### Iska Use Kya Hai?
1. **Content**:
   - Chatbot ya user-friendly systems ko ek simple message dena.
   - Example: `"5 numbers generated successfully."`

2. **Artifact**:
   - Agar aapko numbers ka analysis karna ho ya kisi aur system ko pass karna ho.
   - Example: AI model ko ek random dataset dena.

---

Artifacts LangChain ke workflows ko **modular aur efficient** banate hain. Tools ke output ko samajhne aur use karne ke liye artifacts important role play karte hain.


</br>

----------

<br/>

### ``Note`` : Tools in LangChain

Ye paragraph LangChain ke tools aur unke integration ke baray mein hai, aur is baat ko emphasize karta hai ke agar aap **third-party tools** use karte hain, to unke functionalities aur security aspects ko samajhna zaroori hai. Detail mein samajhte hain:

---

### **Tools in LangChain**
LangChain ke tools wo utilities hain jo **agents** ke sath kaam karte hain. Ye tools kisi specific kaam ko solve karte hain, jaise:
- Data ko fetch karna (e.g., API calls, database queries).
- Data ko process karna (e.g., summarization, translation).
- External services ke saath interaction (e.g., Google Drive, Email services).

**Third-party tools** wo tools hain jo kisi aur developer ya company ne banaye hain, aur aap unhe LangChain ke agents ke saath use kar sakte hain.

---

### **LangChain Tool Integrations**
LangChain me kai third-party integrations hain jo aapko alag-alag tasks me madad dete hain, jaise:
1. **Google Drive/Sheets Integration** – Data ko access aur manage karna.
2. **API Tools** – OpenAI ya HuggingFace models ka use karna.
3. **Web Scraping Tools** – Websites se data nikalna.
4. **Cloud Storage Tools** – S3 buckets se interact karna.

LangChain ke documentation me ek [Tool Integrations](https://docs.langchain.com/integrations/tools/) section hai jisme available tools ka list aur unka use case diya gaya hai.

---

### **Why Security and Permissions Matter?**
Jab aap third-party tools use karte hain, to unka secure hona aur unki permissions samajhna bohot zaroori hai:
1. **Sensitive Data**:
   Agar tool sensitive data ke sath kaam kar raha hai (e.g., customer details, payment info), to ensure karo ki tool properly secure hai.

2. **Permissions**:
   - Ye check karo ki tool ko kis level ka access chahiye? (e.g., files, APIs, personal information)
   - Kahi tool extra unnecessary permissions to nahi le raha?

3. **Documentation**:
   Har tool ke sath ek documentation hoti hai jisme likha hota hai:
   - Tool kaise setup karein.
   - Kya dependencies ya API keys chahiye.

4. **Security Risks**:
   - Kahi tool malicious ya compromised to nahi hai?
   - Agar tool data store karta hai, to uska encryption setup samjho.

---

### **Security Guidelines for LangChain**
LangChain recommend karta hai ki har tool ko **security guidelines** ke sath use karo:
- **Check Source**: Ensure karo ki tool reliable source se liya gaya hai.
- **Audit Tools**: Agar tool ke outputs unexpected lagte hain, to tool ki puri audit karo.
- **Update Tools**: Hamesha tools ka updated version use karo.

---

### **Example**
Agar aap Google Sheets integration use karte hain, to:
1. **Permissions**:
   Tool ko Google account ka access chahiye. Ensure karo ki yeh sirf required permissions tak limited ho.
2. **Security**:
   - API token secure jagah rakho.
   - Data ko share karte waqt check karo ki unauthorized access na ho.
3. **Documentation**:
   Set up ke instructions ko samjho aur step-by-step follow karo.

---

### **Key Takeaway**
LangChain ke third-party tools ka faida tabhi ho sakta hai jab:
1. Aapko unka kaam achi tarah samajh aaye.
2. Aap unka secure aur responsible tareeke se use karein.


<br/>

---------------

<br/>

### Wikipedia integration
Ye code example LangChain ke Wikipedia integration ko use karke Wikipedia se information fetch kar raha hai. Chalo step by step samajhte hain:

---

### **1. Required Setup**
```python
!pip install -qU langchain-community wikipedia
```
Yeh command **`langchain-community`** aur **`wikipedia`** library ko install karta hai jo Wikipedia integration ke liye zaroori hai. Iske bina tool kaam nahi karega.

---

### **2. Import Statements**
```python
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
```
- **WikipediaQueryRun**: Yeh ek LangChain ka tool hai jo Wikipedia se queries run karta hai.
- **WikipediaAPIWrapper**: Yeh backend pe Wikipedia ke API ke sath interaction karta hai.

---

### **3. API Wrapper Configuration**
```python
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
```
Yahaan APIWrapper ko customize kiya gaya hai:
- **`top_k_results=1`**: Sirf top 1 result ko fetch karega.
- **`doc_content_chars_max=100`**: Sirf 100 characters tak ka content return karega.

---

### **4. Tool Initialization**
```python
tool = WikipediaQueryRun(api_wrapper=api_wrapper)
```
- **WikipediaQueryRun** ko initialize kiya gaya hai jo **api_wrapper** ka use karega.
- Yeh tool ko ready karta hai taake aap search queries ko run kar sako.

---

### **5. Query Execution**
```python
print(tool.invoke({"query": "langchain"}))
```
- **`invoke()`** method ko call karke query "langchain" ke liye Wikipedia data fetch karta hai.
- Example Output:
  ```
  Page: LangChain
  Summary: LangChain is a framework designed to simplify the creation of applications
  ```
  Yahaan result me:
  - **Page**: Wikipedia page ka naam.
  - **Summary**: Page ka ek chhota sa summary jo `doc_content_chars_max=100` ki limit tak hai.

---

### **6. Tool's Default Properties**
```python
print(f"Name: {tool.name}")
print(f"Description: {tool.description}")
print(f"args schema: {tool.args}")
print(f"returns directly?: {tool.return_direct}")
```
Is code se tool ke **default properties** print hoti hain:
- **`tool.name`**: Tool ka naam `wikipedia` hai.
- **`tool.description`**: Tool ka use-case batata hai:
  ```
  A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects.
  ```
- **`tool.args`**: Query ka schema (yani input data structure) deta hai:
  ```
  {'query': {'description': 'query to look up on wikipedia', 'title': 'Query', 'type': 'string'}}
  ```
- **`tool.return_direct`**: Agar `True` hota to raw response directly return hoti, lekin yahaan `False` hai.

---

### **Summary**
Ye example Wikipedia integration ka ek simple demonstration hai jo:
1. Wikipedia ke API se ek custom wrapper banata hai.
2. Queries ka result fetch karta hai.
3. Tool ki properties jaise name, description, args schema ko explore karta hai.

Agar query ko modify karna hai, bas `invoke({"query": "<your_query>"})` me query change karo aur nayi information fetch ho jayegi! 

<br/>

--------

<br/>

## Customizing Default Tools


Is code snippet me **LangChain** ka Wikipedia tool customize karna sikha gaya hai. Aap tool ke **name**, **description**, aur **JSON schema** ko modify kar sakte ho, jab tak input parameters function ke input se match karein. Yahan detail explanation di gai hai:

---

### **Step-by-Step Explanation**

#### **1. Customize Name and Description**
- **`name`**: Tool ka naam customize kiya gaya hai. Default name ki jagah hum **`wiki-tool`** use kar rahe hain.
- **`description`**: Tool ka kaam define karne ke liye custom description likhi gayi hai. Is example me:
  ```python
  description="look up things in wikipedia"
  ```

---

#### **2. JSON Schema for Arguments**
- Aap **JSON schema** ke zariye input arguments ka structure aur description customize kar sakte ho.
- Example me, **`WikiInputs`** ek custom class hai jo arguments ka structure define kar rahi hai.

  ```python
  class WikiInputs(BaseModel):
      """Inputs to the wikipedia tool."""
      query: str = Field(
          description="query to look up in Wikipedia, should be 3 or less words"
      )
  ```

  - **BaseModel**: Pydantic ka ek model jo input validation aur schema generation ke liye use hota hai.
  - **Field**: Aap har input parameter ka description de sakte ho. Yahan kaha gaya hai ke query maximum 3 words ki honi chahiye.

---

#### **3. Initialize Customized Tool**
- Aap customized schema aur parameters ko pass karke tool initialize karte ho:
  ```python
  tool = WikipediaQueryRun(
      name="wiki-tool",
      description="look up things in wikipedia",
      args_schema=WikiInputs,  # Custom JSON schema
      api_wrapper=api_wrapper,  # Existing API wrapper
      return_direct=True,       # Output ko directly return kare
  )
  ```

  - **`args_schema`**: Custom schema jo humne define ki hai (`WikiInputs`).
  - **`return_direct=True`**: Tool ka output directly return kare bina kisi additional processing ke.

---

#### **4. Running the Tool**
- **`tool.run("langchain")`**:
  Yahan tool ko ek query "langchain" pass ki gayi hai, jo Wikipedia me search karega aur result return karega.

---

### **Output Example**
Agar query "langchain" pass ki gayi hai, to expected output kuch is tarah hoga:

```plaintext
Page: LangChain
Summary: LangChain is a framework designed to simplify the creation of applications.
```

---

### **Core Concepts**
1. **Customizing Inputs**:
   JSON schema ke zariye aap har input field ka validation aur description define karte ho.
   
2. **Customizing Tool Behavior**:
   Aap tool ke name aur description ko modify kar ke uska functionality ka context define karte ho.

3. **Return Directly**:
   Tool ka result directly return karwana.

---

Yeh approach tab useful hoti hai jab aap tool ko specific use-case ke liye tailor karna chahte ho. 😊

<br/>

--------

<br/>

**Wikipedia tool ke schema ko customize karne ki zarurat is liye hoti hai taake tool ko apne specific use-case ke liye better tailor kiya ja sake.** Agar hum default settings use karein, to tool general-purpose rehta hai, jo har situation me best fit nahi karta. Customization ka kaam hota hai tool ko context-specific banana aur uske inputs/outputs ko properly manage karna.

### **Customization ki Zarurat kahan hoti hai?**

1. **Input Validation aur Restriction:**
   - Default schema me inputs generalized hote hain, jaise "query" field. Lekin aap kuch specific constraints dalna chahte ho, jaise:
     - Query me sirf 3 words allowed ho.
     - Query ka format specific ho, jaise alphanumeric ya kuch aur pattern.

   **Example:**
   Agar aapko ensure karna ho ke query me sirf short phrases ho, to aap input validation ke liye schema customize karoge.

---

2. **Readable Description for Input Fields:**
   - Default description har user ke liye asan samajh nahi hoti. Custom descriptions dal kar aap schema ko human-readable aur user-friendly bana sakte ho.
   - Jaise:
     ```python
     query: str = Field(
         description="Enter a Wikipedia search query of maximum 3 words"
     )
     ```
   Yahan ek clean aur understandable description add ki gayi hai.

---

3. **Custom Tool Name aur Purpose:**
   - Agar aap multiple tools use kar rahe ho (jaise Wikipedia aur Google Search), to har tool ka name aur description specific hona chahiye taake clarity rahe.
   - Example:
     - Wikipedia tool ke liye: "Look up things in Wikipedia."
     - Google tool ke liye: "Search the web using Google."

---

4. **Control Over Outputs:**
   - Default tool output ko directly return karta hai. Agar aapko output me customization chahiye, jaise sirf content ya kuch metadata add karna, to schema useful hai.

---

5. **Specific Use-Case Applications:**
   - Agar aapka application ek limited domain me kaam karta hai (e.g., history, science, etc.), to aap schema customize karke tool ko domain-specific bana sakte ho.
   - Example:
     Query field ke description me mention karo: "Search only historical events."

---

### **Benefits of Customization**
1. **User Experience Better Hoti Hai**:
   Custom schema se tool ko use karna asaan aur effective hota hai.
   
2. **Error Handling Improve Hoti Hai**:
   Input constraints lagane se galat input pass hone ki probability kam ho jati hai.

3. **Multiple Tools Ke Sath Integration Smooth Hoti Hai**:
   Har tool ka unique name aur description hone se conflicts avoid hote hain.

4. **Automation Aur Scaling Me Madad Milti Hai**:
   Customized tools application workflows ke liye zyada compatible hote hain.

---

**Aapke Application Ke Hisab Se Customization Ki Zarurat Hogi.** Agar tool general-purpose hai, to default settings kaafi hain. Lekin specific workflows ya user scenarios ke liye customize karna must hota hai.

<br/>

-------------

<br/>

### How to use built-in toolkits

**LangChain toolkits** asaan aur predefined tools ka collection hain jo ek saath kaam karte hain specific tasks solve karne ke liye. Ye tools kaam ko asaan banate hain aur directly use karne ki facility dete hain. Chalo isko ek example ke zariye simple karte hain:

---

### **Toolkit Ka Matlab**
Toolkits ek tarah ka **"toolbox"** hain jo multiple tools ka collection hota hai. Aapko alag-alag tools configure karne ki zarurat nahi hoti; sab kuch ek jagah se ready mil jata hai.

---

### **Toolkits Kaise Kaam Karte Hain?**

1. **Toolkit Initialize Karna:**  
   Har toolkit ko start karne ke liye initialize karna padta hai. Agar kisi tool ko API ya setting ki zarurat hai, wo yahin set hota hai.  
   Example: Wikipedia ke tools load karna.
   ```python
   from langchain_community.toolkits import WikipediaToolkit
   toolkit = WikipediaToolkit()
   ```

2. **Tools Ki List Lena:**  
   Toolkit ke andar ke tools ko `get_tools()` method se access karte hain.  
   ```python
   tools = toolkit.get_tools()
   print(tools)  # Ye toolkit ke tools ki list dikhayega
   ```

3. **Tool Run Karna:**  
   Ek specific tool run karne ke liye `run()` method use karte hain.  
   ```python
   result = tools[0].run("LangChain")
   print(result)  # Ye "LangChain" ka Wikipedia se summary dega.
   ```

---

### **Example**

Wikipedia se search karna ek task hai, jisme toolkit ka use hota hai:

```python
from langchain_community.toolkits import WikipediaToolkit

# Step 1: Initialize toolkit
toolkit = WikipediaToolkit()

# Step 2: Get tools from the toolkit
tools = toolkit.get_tools()

# Step 3: Use the first tool for Wikipedia search
result = tools[0].run("Artificial Intelligence")
print(result)
```

**Output:**  
Wikipedia se "Artificial Intelligence" ka short summary aayega.

---

### **Toolkits Ka Fayda**
1. **Easy to Use:** Aapko har tool alag se configure karne ki zarurat nahi hoti.
2. **Predefined Tools:** Pehle se banaye gaye tools ka collection hota hai.
3. **Efficient Workflow:** Multiple tools ek hi jagah use karne ka option milta hai.
4. **Automated Agents:** Ye agents ke sath easily integrate hote hain.

---

**Summary:** Toolkits aapke kaam ko fast aur asaan banate hain. Agar ek specific task ke liye ready-made tools chahiye, to LangChain toolkits best solution hain.

<br/>

----------

<br/>

### What problem is the toolkit solving?

LangChain toolkit ek important concept hai jo kuch specific problems ko efficiently solve karta hai. Ye problems ko simplify karta hai, aur alag alag tools ko ek organized aur coordinated framework mein laata hai. Yahan par kuch key problems aur unka solution explain kiya gaya hai:

---

### **1. Tools Ko Manage Karna**
- **Problem**: Alag alag tools ka use karna mushkil ho jata hai, specially jab unka kaam ek doosre se related ho.
- **Solution**: Toolkit ek group provide karta hai jo saare related tools ko ek saath organize karta hai. Iska matlab ek hi jagah se saare tools ko call aur manage kiya ja sakta hai.

**Example**: Agar aapko search, database query, aur PDF parsing karna hai, toh alag alag tools ko manually handle karna mushkil ho sakta hai. Toolkit in saare tools ko ek hi interface ke through access deta hai.

---

### **2. Model aur Tools ka Coordination**
- **Problem**: LLMs (Language Models) ko properly guide karna mushkil hota hai ke kaunsa tool kab aur kaise use karna hai.
- **Solution**: Toolkit ke saath LLM easily samajh leta hai ke kis kaam ke liye kaunsa tool use karna hai, kyun ke toolkit ek schema define karta hai jo LLM ke liye compatible hota hai.

**Example**: Search toolkit automatically model ko samjha deta hai ke search ka query kaise handle karni hai.

---

### **3. Reusability aur Scalability**
- **Problem**: Custom tools bar bar har project ke liye banane padte hain, jo time aur resources waste karta hai.
- **Solution**: Toolkits reusable aur scalable design provide karte hain. Aap ek hi toolkit multiple agents ke saath use kar sakte ho, aur future me usko expand kar sakte ho.

---

### **4. Debugging aur Testing**
- **Problem**: Agar tools alag alag hain, toh debugging karna aur issues identify karna time-consuming ho jata hai.
- **Solution**: Toolkit centralized access aur logs provide karta hai, jo debugging aur testing ko easy banata hai.

---

### **5. Custom Workflows Ka Design**
- **Problem**: Har application ka use-case alag hota hai, toh tools ke workflows manually design karna mushkil ho jata hai.
- **Solution**: Toolkits workflows ko automate aur customize karne ke options dete hain, jo application development ko faster banata hai.

---

### **Practical Example**
Agar aapko ek multi-step task perform karna hai, jaise:
1. Web se data fetch karna,
2. Uska sentiment analysis karna,
3. Aur result database me save karna,

Toh aapko alag alag libraries aur frameworks handle karni padti hain. Toolkit is workflow ko ek hi interface se efficiently solve karta hai.

---

### **Summary**
Toolkit ka main kaam hai:
- Tools ko ek group mein laana.
- Tools aur LLM ke beech coordination improve karna.
- Development ko fast aur reliable banana.

Ye problems solve karne ke baad aap apne application ko zyada efficiently develop aur deploy kar sakte ho.

<br/>

----------

<br/>

### How to use chat models to call tools
### 1. **Tools kya hote hain?**
Tools woh functions hote hain jo specific kaam karte hain. Jaise agar aapko do numbers ko add karna ho ya multiply karna ho, to aap un tasks ko perform karne ke liye ek tool bana sakte hain. 

Example:
- **add** tool: 2 numbers ko add karne ka function
- **multiply** tool: 2 numbers ko multiply karne ka function

<br/>

![Alt text](https://python.langchain.com/assets/images/tool_call-8d4a8b18e90cacd03f62e94071eceace.png)


<br/>

### 2. **Model ke saath tools ko connect karna**
Aap jab ek LLM (Language Model) ko tools ke saath kaam karne dena chahte hain, to aap un tools ko **model ke saath bind karte ho**. Iska matlab hai ke model ko yeh pata hota hai ke yeh tools available hain, aur jab zarurat ho to unhe use kar sakta hai.

Example:
```python
tools = [add, multiply]  # Ye tools define karte hain jo hum use karenge
llm_with_tools = llm.bind_tools(tools)  # Model ko tools ke saath bind karna
```

### 3. **Model kaam kaise karta hai?**
Jab aap model se koi question poochte ho, for example *"5 + 3 kya hai?"*, to model yeh samajhta hai ke aapko addition chahiye. Toh model apne aap se yeh decide karta hai ke **add** tool ko call karna hai. Model sirf **arguments** generate karta hai, jisme woh numbers hote hain jo add hone hain (jaise 5 aur 3).

Model ka kaam yeh hota hai ke woh tools ko "call" karne ka suggestion deta hai, lekin tools ko actually chalana aapka kaam hota hai.

Example:
```python
response = llm_with_tools.invoke("What is 5 + 3?")  # Model ko yeh question diya
print(response.content)  # Model ka jawab
```

### 4. **Tool calling ka example**
Agar aap yeh question *"5 + 3 kya hai?"* model se poochte ho, to model apne response me aapko yeh suggest karega ke aap **add** tool ko use karein. Lekin actual calculation model nahi karega, woh sirf bataega ke kaun sa tool use karna hai.

Model ki taraf se aapko yeh output mil sakta hai:
```
The available tools lack the functionality to perform this calculation. I need a tool that can perform addition.
```
Iska matlab hai ke model ne tools ko dekh liya hai, aur addition karne ke liye ek tool ki zarurat thi.

### 5. **Tool ko run karna**
Jab model tool calling karta hai, to uska matlab yeh hota hai ke woh aapko **arguments de raha hai** jise aap tool ko denge. Tool ko chalana aapke upar hota hai, model ne sirf input diya hai.

---

**Final Summary**:  
- **Tool calling** ka matlab hai ke model tools ko use karne ka plan banata hai, lekin woh tools ko **run nahi karta**. Model sirf **arguments** deta hai jo aapko tools ko dene hote hain.
- Aapko apne **tools** ko **model ke saath bind** karna padta hai taake model ko unka pata ho jab zarurat ho.
- Jab aap model se question poochte ho, to model **argument generate karta hai** jo tool ko dene hote hain.
---

### Tool Calling Kyun Zaruri Hai?

1. **Updated Information**:
   - Jo baat model ko nahi pata ya jo real-time ka data hai, wo tools se mil sakta hai. 
   Misal: Weather data, latest news, etc.

2. **Reliable Answers**:
   - Tools se correct aur verified information milti hai.

3. **Customization**:
   - Aap apne custom tools integrate kar sakte hain, jese apni database ya APIs.

---

### Misal Workflow:

1. Input: "New York ka weather batao?"
2. Model Suggestion: "Weather API tool use karo."
3. Arguments: `{"city": "New York", "date": "today"}`
4. Tool Result: "New York me aaj weather 25°C aur sunny hai."

---

### Aam Tools Jo Use Ho Sakte Hain:
- **Search Tools**: Brave ya Wikipedia Search.
- **Data Extraction Tools**: Documents ya PDFs se information nikalna.
- **API Tools**: Custom services ke liye.

Agar aapko iska practical use banana hai, to ek chatbot setup kar ke tools bind karen aur unko integrate karen. Misal, Brave Search API ka use karke search queries handle karna.


<br/>

--------------

<br/>

### Defining tool schemas
Tool schemas ka matlab hota hai ek **structure** ya **definition** jo tool ke kaam aur uske arguments ko describe karta hai. Agar aap ek chat model ko tools call karwana chahte hain, to pehle un tools ki schemas define karni padti hain. Ye schema model ko batata hai ke tool kya karta hai aur usko chalane ke liye kaunsa input chahiye.

---

### Python Functions se Tool Schemas Define Karna

Aap Python functions ka use karke tool schema define karte hain. **Function ka naam**, **type hints**, aur **docstring** hi us tool ka schema banata hai. Ye schema model ke liye ek **guide** hoti hai jo samajhne me madad karti hai ke tool ka input aur output kya hoga.

---

#### Example:

```python
# Pehla tool: Add karne ke liye
def add(a: int, b: int) -> int:
    """Add two integers.

    Args:
        a: Pehla integer
        b: Dusra integer
    """
    return a + b

# Dusra tool: Multiply karne ke liye
def multiply(a: int, b: int) -> int:
    """Multiply two integers.

    Args:
        a: Pehla integer
        b: Dusra integer
    """
    return a * b
```

**Explanation**:
1. **Function name**:
   - `add` aur `multiply` functions ke naam hi batate hain ke tools kya kaam karenge.

2. **Type Hints**:
   - `a: int` aur `b: int` se samajh aata hai ke dono inputs integers hone chahiye.

3. **Docstring**:
   - Ye ek explanation hai jo tool ke kaam ko briefly describe karti hai.

---

### Bind Tools to Model

Aap in functions ko model ke saath bind karte hain taake model ko pata chale ke kaunsa tool kab use karna hai. Ye process **tool calling** kehlaata hai.

```python
from langchain.chat_models import ChatOpenAI

# Chat Model initialize karte hain
model = ChatOpenAI(temperature=0)

# Tools ko bind karte hain
model = model.bind_tools([add, multiply])
```

---

### Model ka Behavior

1. **Input**: User ka sawaal: `"5 aur 3 ko add karo aur multiply karo 2 se"`
2. **Model Decision**: Model samajhta hai ke `add` aur `multiply` tools use karne hain.
3. **Tool Call**: Model `add(5, 3)` call karega aur result ko store karega.
4. **Output**: Result ko process karne ke baad user ko reply milega.

---

### Practical Benefits

1. **Automation**:
   - Tools ko bind karne se repetitive tasks automate ho jaate hain.

2. **Modularity**:
   - Har function ek independent tool hota hai, jise aap alag se bhi use kar sakte hain.

3. **User Customization**:
   - Aap apne custom tools define kar sakte hain jese database queries, API calls, etc.

4. **Error Reduction**:
   - Model ko tools ke clear schemas milte hain, jo galtiyon ke chances kam karte hain.

---

### Final Note
Tool schemas ek **bridge** hai model aur tools ke beech, jo unko sahi tareeke se collaborate karne me madad karta hai. Har tool ka schema jitna descriptive aur clear hoga, model ka output utna hi reliable hoga.


<br/>

--------------

<br/>

### TypedDict class
Yeh concept **TypedDict classes** ke through tools ke schemas ko define karna dikhata hai. Is method ka faida hai ke aap har argument ka data type aur description clearly likh saktay hain, aur schema modular hota hai.

---

### **TypedDict ka Role**

1. **TypedDict** ek Python ka feature hai (jo `typing_extensions` library ka hissa hai), jo dictionaries ka structure define karta hai:
   - Har field ka type.
   - Optional description (using `Annotated`).

2. TypedDict ke schema ko LangChain tools ke liye use kiya jata hai, jahan chat model ko yeh samjhana hota hai ke tool ka input kaisa hoga.

---

### **Example: Adding and Multiplying**

```python
from typing_extensions import Annotated, TypedDict

# Add karne ke liye schema
class add(TypedDict):
    """Add two integers."""  # Tool ka kaam explain karta hai
    a: Annotated[int, ..., "First integer"]  # Pehla argument
    b: Annotated[int, ..., "Second integer"]  # Dusra argument

# Multiply karne ke liye schema
class multiply(TypedDict):
    """Multiply two integers."""  # Tool ka kaam explain karta hai
    a: Annotated[int, ..., "First integer"]  # Pehla argument
    b: Annotated[int, ..., "Second integer"]  # Dusra argument

# Tools ki list
tools = [add, multiply]
```

---

### **Explanation**

1. **TypedDict Class**:
   - Yeh ek schema define karta hai jisme keys aur unke types mentioned hote hain.

2. **Annotations (`Annotated`)**:
   - Har field ke sath `Annotated` use hota hai jisme:
     - Type (e.g., `int`).
     - Default value (`...` ka matlab required field).
     - Description (e.g., `"First integer"`).

3. **Docstring**:
   - `"""Add two integers."""` yeh tool ka kaam describe karta hai.

4. **Tools List**:
   - Sab TypedDict schemas ko ek list me rakha jata hai, jo baad me chat model ke sath bind hoti hai.

---

### **Binding Tools to Model**

Tools ko schema bind karne ke liye `.bind_tools()` method use hoti hai. Is method se schema ko LangChain ke models ke format me convert kiya jata hai.

#### **Example Binding**:
```python
from langchain.chat_models import ChatOpenAI

# Model initialize karna
model = ChatOpenAI(temperature=0)

# Tools bind karna
model = model.bind_tools(tools)

# Chat model invoke karna
response = model("Add 10 and 5, then multiply by 3")
print(response)
```

---

### **Advantages of TypedDict**:

1. **Clear Structure**:
   - Har field ka type aur purpose clearly likha hota hai.

2. **Validation**:
   - Agar galat input ho, to error aayega, jo debugging me help karega.

3. **Reusable**:
   - Aap ek schema ko multiple tools ke liye use kar saktay hain.

4. **Modular Design**:
   - Yeh approach modular hai, aur har tool ke liye separate schema maintain kar sakte hain.

---

### **Practical Example: Financial Calculator**

Agar ek tool banate hain jo **simple interest** calculate karta hai:
```python
class CalculateInterest(TypedDict):
    """Calculate simple interest."""
    principal: Annotated[float, ..., "Principal amount"]
    rate: Annotated[float, ..., "Rate of interest in percentage"]
    time: Annotated[int, ..., "Time period in years"]
```

Bind karne ke baad:
```python
response = model("Calculate interest for principal 1000, rate 5%, and time 2 years")
```

---

### **Conclusion**

TypedDict ek flexible aur clean way hai tools ke schemas banane ka. Yeh method:
- **Chat models ko input samjhata hai**.
- **Developers ke liye debugging aur modularity improve karta hai**.

<br/>

------------

<br/>

### **`llm_with_tools = llm.bind_tools(tools)` Ka Kaam Kya Hai?**

Yeh line LangChain framework ka ek core feature hai, jo chat-based language models ko tools ke sath integrate karta hai. Iska kaam hai **LLM (Language Model)** ko tools ke sath **bind karna**, taki language model tools ke schemas ko samajh sake aur unko effectively call kar

### **`llm.bind_tools(tools)` Ka Basic Kaam**
Jab tum ek **language model (LLM)** ko kisi tool ke sath "bind" karte ho, iska matlab hota hai:
1. **Tools ko define karna**: Tumhare paas kuch predefined tools hain, jaise `add`, `multiply`, ya Brave Search, jinhe tum define karte ho.
2. **LLM ko tools ke bare mein batana**: LLM ko yeh samjhana hota hai ki kaunse tools hain aur unka kya kaam hai (e.g., `add` ka kaam hai do numbers ko add karna).
3. **LLM ko tools ka use sikhana**: Ab language model jab tumse koi input lega, woh samajh jayega ki kab kaunsa tool call karna hai.

### **Example**
Suppose tumne `add` aur `multiply` tools define kiye hain. Jab tum **`bind_tools`** function ka use karte ho, LLM yeh samajhne lagta hai:
- Agar user bole "Add 3 and 5", toh LLM **`add`** tool call karega.
- Agar user bole "Multiply 4 and 6", toh LLM **`multiply`** tool call karega.

### **Code Example**
```python
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool

# Tools define karte hain
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

tools = [
    Tool(name="add", func=add, description="Add two numbers"),
    Tool(name="multiply", func=multiply, description="Multiply two numbers")
]

# LLM ko tools ke sath bind karte hain
llm = ChatOpenAI()
llm_with_tools = llm.bind_tools(tools)

# Ab LLM ko input do
response = llm_with_tools("What is 5 + 3?")
print(response)
```

### **Binding Tools Ka Benefit**
1. Tum easily multiple tools ko ek hi LLM ke sath integrate kar sakte ho.
2. LLM automatically tool ke logic ko samajhkar uska use karega.
3. Tumhare chat-based applications intelligent aur dynamic ban jati hain.

Agar koi confusion ho, toh pucho! 😊


<br/>

---------------

<br/>

Bilkul sahi baat hai ke **LLM** khud decision le raha hai ke konsa tool use karna hai, aur yeh kaam ek agent bhi karta hai. Lekin **LangGraph** aur LangChain agents ke beech kuch distinct differences aur specific use-cases hain. 

### **LLM + Tools vs LangGraph Agents:**

#### 1. **LLM Bind Tools (Jaise Aapka Code):**
   - **Simple Flow**: Aap tools ko directly LLM ke saath bind karte hain, aur LLM input ke basis par decide karta hai ke kaunsa tool call karna hai.
   - **Limited Complexity**: 
     - Yeh structure tab kaam karta hai jab aapke tools simple aur independent tasks handle karte hain (e.g., `add`, `multiply`).
     - Complex decision-making, chaining, ya multi-step workflows ke liye limited hai.
   - **Usage**: 
     - Straightforward applications jaise calculator, weather checker, ya API queries.

#### 2. **LangGraph (or LangChain Agents):**
   - **Advanced Reasoning**: LangGraph ek **agent-based framework** hai jo multi-step reasoning aur task execution ke liye optimized hai.
     - Agents not only decide tools but also chain multiple tools together.
     - Example: Agar ek query me "Summarize this article and translate it to Spanish" ho, agent yeh workflow aise handle karega:
       1. Summarize tool call.
       2. Translate tool call.
       3. Aggregate result.
   - **Dynamic Memory Management**: Agents dynamically memory aur state manage karte hain.
   - **Plugins/Tools Interaction**: LangGraph agents complex plugins aur APIs ko seamlessly interact karte hain.

---

### **When to Use Which?**

| Feature                    | **LLM + Tools**                                  | **LangGraph/Agents**                            |
|----------------------------|--------------------------------------------------|------------------------------------------------|
| **Complexity**             | Suitable for simple tasks (single-step).         | Handles complex workflows (multi-step).        |
| **Tool Chaining**          | Limited, manual chaining needed.                 | Automatic, supports dynamic tool invocation.   |
| **Memory Requirements**    | Stateless, doesn't track intermediate steps.     | State-based, tracks progress/context.          |
| **Error Handling**         | Basic (errors need to be manually managed).      | Better error handling via retries and context. |
| **Ease of Implementation** | Easy for small, single-task workflows.           | Best for sophisticated, large-scale systems.   |

---

### **Example Scenarios:**
1. **LLM + Tools**: 
   - `"What is 5 + 6?"`  
     Simple tool selection and execution.
   - `"Get me today's weather in Lahore."`  

2. **LangGraph/Agents**:
   - `"Fetch data from this API, analyze it, and send the report."`
   - `"Plan my day based on my calendar and current weather conditions."`

---

### **Conclusion**
Agar aapka use-case **simple tool selection aur single-step execution** hai, to LLM + tools kaafi hai. Agar aapko **complex workflows** ya **multi-step decisions** handle karne hain, to LangGraph ya LangChain agents use karna zaroori hai. Dono ka apni jagah kaam hai, aur complexity par depend karta hai. 

Agar aapke paas koi specific use-case hai, to share karein, aur main guide karunga ke kahan LLM + tools theek hai aur kahan LangGraph better rahega! 😊

<br/>

-----

<br/>

### Tool calls

LangChain me jab hum kisi tool (jaise function ya API) ko call karte hain, to wo call `tool_calls` naam ke list me store ho jati hai. Ye list har tool ke call ki details rakhti hai, jisme kuch important cheezein hoti hain:

1. **Name**: Yeh tool ka naam hota hai (for example, `add` ya `multiply`).
2. **Args**: Yeh wo values hoti hain jo tool ko diye ja rahe hote hain. Jaise agar aap `multiply` function call karte ho, to usme aapko numbers dene padte hain, jaise `{a: 3, b: 12}`.
3. **ID**: Har tool call ka ek unique identifier hota hai jo us tool call ko identify karta hai.
4. **Type**: Yeh hamesha `tool_call` hota hai, jo batata hai ke yeh tool ko call kiya gaya hai.

Agar model multiple tools ko ek hi time pe call karta hai, to ye tool calls ek list me store ho jati hain. Example:

```json
[
  {
    'name': 'multiply',
    'args': {'a': 3, 'b': 12},
    'id': 'call_1fyhJAbJHuKQe6n0PacubGsL',
    'type': 'tool_call'
  },
  {
    'name': 'add',
    'args': {'a': 11, 'b': 49},
    'id': 'call_fc2jVkKzwuPWyU7kS9qn1hyG',
    'type': 'tool_call'
  }
]
```

Is example me, model ne `multiply` aur `add` dono tools ko call kiya hai. Har tool call ke saath `args` diye gaye hain, jo ki wo values hain jo function ko pass ki gayi hain (jaise `a: 3, b: 12`).

**Agar koi tool call galat ho jaye** (for example, agar arguments galat format mein ho), to wo call `invalid_tool_calls` mein chala jata hai, jahan uske sath error message bhi hota hai.

**Summary**: `tool_calls` track karta hai kaunsa tool call kiya gaya, uske arguments kya the, aur uska unique ID kya hai. Agar tool call galat ho jaye, to wo `invalid_tool_calls` mein record ho jata hai.


<br/>

-------------

<br/>

###  How to pass tool outputs to chat models
