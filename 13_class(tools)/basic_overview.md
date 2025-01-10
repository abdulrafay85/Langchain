### Tool calling
Ye concept **tool calling** ka hai, jo AI models ko external systems ke sath interact karne ke liye use hota hai, jaise ke databases, APIs, ya doosri functionalities ke liye. Yahan pe main key points hain jo samajhne zaroori hain:

---

<br/>

![Alt text](https://python.langchain.com/assets/images/tool_calling_concept-552a73031228ff9144c7d59f26dedbbf.png)

<br/>

### **1. Tool Calling Ka Maqsad**
AI models aksar natural language me humans se interact karte hain, lekin kuch scenarios me models ko systems ke sath interact karna hota hai jo ek specific input schema ya format follow karte hain. 
- Example: APIs me ek **payload structure** hoti hai jo model ke liye compatible honi chahiye.
- Tool calling ka istemal isi structure ko match karne aur systems ko interact karne ke liye hota hai.

---


<br/>

![Alt text](https://python.langchain.com/assets/images/tool_calling_components-bef9d2bcb9d3706c2fe58b57bf8ccb60.png)

<br/>

### **2. Key Concepts**

#### **A) Tool Creation**
- Tools banane ke liye `@tool` decorator use hota hai.
- Tool ek function ko ek specific schema ke sath bind karta hai.
- Example:
```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Do numbers ka multiplication karta hai."""
    return a * b
```
Is example me `multiply` ek tool hai jo `a` aur `b` integers ko input leta hai.

---

#### **B) Tool Binding**
- Tools ko AI model ke sath bind karte hain taake model un tools ke baare me aware ho aur unka schema samajh sake.
- Ye kaam `.bind_tools()` method ke zariye hota hai:
```python
tools = [multiply]
llm_with_tools = llm.bind_tools(tools)
```

---

#### **C) Tool Calling**
- Model decide karta hai ke tool call karna hai ya nahi, input ki relevance ke basis par.
- **Example 1 (Natural Language Response)**:
```python
result = llm_with_tools.invoke("Hello world!")
```

<br/>

![Alt text](https://python.langchain.com/assets/images/tool_call_example-2348b869f9a5d0d2a45dfbe614c177a4.png
)

<br/>

Agar input tool ke liye relevant nahi hoga, to model natural language me jawab dega (e.g., "Hello!").

- **Example 2 (Tool Calling)**:
```python
result = llm_with_tools.invoke("What is 2 multiplied by 3?")
```
Agar input relevant hai, to model tool call karega aur output me `.tool_calls` attribute populate karega:
```python
result.tool_calls
# {'name': 'multiply', 'args': {'a': 2, 'b': 3}, 'id': 'xxx', 'type': 'tool_call'}
```

---

#### **D) Tool Execution**
- Tool ka execution manually ya automatically ho sakta hai.
- Example:
```python
tool_result = multiply.invoke({'a': 2, 'b': 3})
print(tool_result)  # Output: 6
```

LangChain frameworks jese ke **LangGraph** pre-built components dete hain (e.g., `ToolNode`) jo tools ko automatically invoke kar sakte hain.

---

### **3. Best Practices**
1. Tools ke **names aur descriptions** clear aur relevant hone chahiye.
2. **Simple aur narrowly scoped** tools zyada effective hote hain.
3. Models better perform karte hain jab tools ke schemas well-defined aur intuitive hote hain.
4. Zyada tools ka selection models ke liye mushkil ho sakta hai; unka number limited rakhein.

---

### **Use Case Example**
Koi model agar kahe:
- Query: "What is 5 multiplied by 7?"
Model:
1. Query ko understand karega.
2. Check karega ke relevant tool hai ya nahi.
3. Tool call karega (e.g., `multiply(a=5, b=7)`).
4. Response generate karega.

Tool calling AI ko systems ke sath effectively interact karne ka tareeqa deta hai, jo complex applications (e.g., APIs ya databases) me zaroori hota hai.