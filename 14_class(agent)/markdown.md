## Agents
LangChain ke agents samajhne ke liye, unhein ek smart assistant samajh lo jo aapke tasks ko perform karne ke liye do cheezein use karta hai: 

1. **Brain (LLM - Large Language Model)**  
   Agent ka main brain hota hai LLM. Yeh user ke sawal ko samajhta hai aur decide karta hai ke kaunsa task kaise karna hai. For example, agar user poochta hai "Mujhe stock market ka latest data batao," to LLM yeh decide karega ke kaunsa tool use karna hai.

2. **Tools (Kaam karne ke instruments)**  
   Tools ka kaam hai agent ko environment ke sath interact karne dena. Ye specific kaam ke liye hotay hain, jaise:
   - **Database query** chalana (e.g., kisi company ka data lana).
   - **Web search** karna (e.g., Google Search se real-time information lana).
   - **API call** karna (e.g., weather data ya financial market se data lana).

3. **Toolkit (Tools ka collection)**  
   Jab ek agent ke paas multiple tools ka group hota hai, usay toolkit kehte hain. Har toolkit ek specific kaam ke liye design hoti hai. For example:
   - **Mathematics Toolkit**: Mathematical operations ke liye.
   - **Research Toolkit**: Web aur document search ke liye.

<br/>

![Alt text](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*Hah4yA9A0rniFn2tEDyNrA.png)

<br/>

### Ek Simple Example:  
Maan lo ek agent hai jo maths problems solve karta hai:
- Iska **brain** (LLM) decide karega ke kya addition karna hai ya multiplication.
- Iske paas tools honge jaise "add," "subtract," aur "multiply."
- Jab user kehta hai "5 aur 7 ka sum batao," agent ka brain (LLM) "add" tool use karega aur jawab dega.

LangChain agents ki khas baat yeh hai ke aap apne tasks ke liye custom agents bana sakte ho. For example:
- **Customer Support Agent**: Jo customers ke sawalon ka jawab de aur data fetch kare.
- **Health Data Agent**: Patient ke records ko analyze kare aur report generate kare.

Agents kaafi flexible hote hain aur inka future AI automation mein bohot promising hai. Agar aur examples chahiye ya kisi part mein confusion ho, batao! 😊

------

### Why Chose LangGraph ?


---

**LangGraph** ek powerful Python library hai jo applications banane mein madad karti hai jahan multiple actors, jaise humans, AI models (LLMs), aur tools, ek saath kaam karte hain. Yeh stateful applications ko handle karne ke liye design ki gayi hai, jo apne workflow ke har step ki state ya data ko yaad rakhti hain.

---

### Key Features of LangGraph:

1. **Multiple Actors:**
   - **LLMs (AI Models):** Data ko process karte hain aur intelligent decisions dete hain.
   - **Humans:** Complex decisions lete hain ya manual input dete hain.
   - **Tools:** APIs ko call karna, databases ko access karna, etc.

2. **Stateful Applications:**
   - LangGraph applications apne data ko har step ke baad yaad rakhti hain.
   - Example: Agar ek user chat kar raha hai, toh system uski purani baatein yaad rakhta hai aur unhi ke mutabiq response karta hai.

---

### **Core Techniques: Cycles & Branching**

1. **Cycles (Loops):**
   - **Definition:** Ek task ko tab tak repeat karna jab tak correct outcome na mil jaye.
   - **Example Use Case:** Agar agent email draft kar raha hai lekin draft acceptable nahi hai, toh woh task repeat hoga jab tak sahi draft na ban jaye.
   - **Process:** Task execute → Validate output → Re-execute if validation fails.

2. **Branching (Conditionals):**
   - **Definition:** Decision-making logic ko workflow mein include karna, jaise "if-else" ya "switch-case".
   - **Example Use Case:** Workflow me har step ke baad check karna ke agla step kya hona chahiye based on conditions.
   - **Process:** User input ya agent output ke basis par next step decide karna.

3. **Combining Cycles & Branching:**
   - Yeh dono techniques ko combine kar ke zyada flexible aur efficient workflows banaye ja sakte hain.
   - **Example Flow:** Document summarization → Validation → Cycle (agar validation fail ho) → Revise summary.

---

### **Persistence:**
LangGraph ka **persistence** feature automatically system ki state ko har step ke baad save kar leta hai, jo aapko kisi bhi point par process ko pause karne aur resume karne ki suvidha deta hai. Yeh feature especially **human-in-the-loop** workflows me useful hai, jahan kisi step pe human input ya error recovery ki zarurat hoti hai.

- **Example:** Agar system kisi computation ko pause kar raha hai, toh uska state save ho jata hai, aur aap baad mein wahi se resume kar sakte hain.

---

### **Human-in-the-Loop:**
Human-in-the-loop (HIL) ka matlab hai kisi process ke dauran human input lena. LangGraph mein yeh feature **interrupt** ke through implement hota hai.

1. **Execution Rukna:**
   - Jab system kuch execute kar raha ho, aap manually execution ko rok sakte ho. Yeh useful hota hai jab aapko lagta hai ke koi step galat ja raha hai ya validation zaroori hai.
  
2. **State Save Karna:**
   - Interrupt hone par system us waqt ki state ko save kar leta hai, jisse process dobara se nahi karna padta.
  
3. **Resume with Options:**
   - **Normal Resume:** Execution wahi se resume hota hai.
   - **New Input:** Aap naye input ke saath execution ko start kar sakte hain.
   - **No Action:** Agar koi action na lo, toh system wahi ruk jata hai.

**Example:** Agar input ka format galat ho, toh system us node ko pause kar dega aur human approval lega.

---

### **Streaming Support:**
LangGraph ka **streaming support** feature aapko har node ke output ko real-time stream karne ka option deta hai, jo especially **token-by-token output** ke liye helpful hai.

1. **Token Streaming:**
   - Jab LLM response de raha hota hai, har token ko process hone par stream kiya jata hai. Yeh OpenAI aur other services ke APIs ke saath kaam karta hai.

2. **Real-Time Output:**
   - Har node ka output turant visible hota hai jab node execute hota hai.
   - Yeh real-time feedback aur dynamic user engagement ke liye best hai, jaise chatbots aur dashboards me.

---

### **Integration with LangChain & LangSmith:**
LangGraph ko **LangChain** aur **LangSmith** ke saath integrate karna bohot asaan hai, lekin unka hona optional hai. Agar aap in tools ko use karte hain, toh aapke workflows aur bhi efficient ho sakte hain.

1. **LangChain:**  
   Yeh ek framework hai jo LLMs aur APIs ko manage karta hai.
  
2. **LangSmith:**  
   Yeh debugging aur testing tool hai jo LLM-based systems ko debug aur track karne me madad karta hai.

**Example:** Agar aap ek chatbot bana rahe ho, toh LangChain ka agent system aapko help karega user inputs handle karne mein, aur LangGraph ka graph structure is process ko organize karega.

---

Is tarah se LangGraph ek powerful tool hai jo complex workflows, multi-actor interactions, aur stateful applications ko efficiently handle karta hai.

---

<br/>

---

### **Exampel 2:**

Sorted and clarified explanation:

---

### **Cycle and Branching:**
- **Cycle:** Workflow ke andar repeated processes ko manage karta hai. Agar system kisi specific task ko multiple times execute karna chahta hai, to woh cycle ke zariye hota hai.
  - Example: Agar tumhe "Point C" par kuch validate karna hai aur woh galat hai, to system wapas "Point B" par jayega aur cycle tab tak repeat karega jab tak task sahi na ho jaye.
  
- **Branching:** Workflow me decision-making allow karta hai. Har step par system check karta hai ke agla step kya hona chahiye, jo current conditions par depend karta hai.
  - Example: Agar input sahi hai, "Point B" par bheja jaye. Agar galat hai, "Point C" par.

- **Combination:** System branching aur looping ka mix use kar ke dynamic workflows create karta hai. Ek loop ke andar branches ho sakti hain, jahan condition ke basis par decision liya jata hai.

---

### **Persistence:**
- Persistence ka matlab hai system apne state (information) ko har step par save karta hai aur usse maintain karta hai.
  - **State:** Key-value pairs ki form me data ko define karta hai, jaise dictionary me hota hai.
  - **Features:**
    1. Workflow ke har node par data save hota hai.
    2. Agar system pause ho jaye, to wapas wahi se shuru ho sakta hai jahan state save hui thi.
    3. Har iteration ke baad checkpoints save kar ke consistency maintain karta hai.

- **Use Case:** System me data ko backend (database) par save karne ke liye har loop aur node ke baad state share aur manage karta hai.

---

### **Human-in-the-Loop:**
- Iska matlab hai workflow ke andar kisi step par human intervention involve karna.
  - **Example:** Agar ek student ko "Quarter 1" me enroll karna hai, to final approval human se liya ja sakta hai.
    - Approve: Workflow continue karega.
    - Reject: Workflow stop ho jayega.

- **Key Features:**
  1. Human kisi bhi node ya edge par decision-making me involve ho sakta hai.
  2. LangSmith ki madad se history aur actions backend par save ho jate hain.
  3. Workflow critical points par human input ko allow karta hai, jaise approvals ya sensitive decisions.

---

Yeh version concise aur easily readable hai. Agar aur improvement chahiye, to zaroor batao! 😊

---