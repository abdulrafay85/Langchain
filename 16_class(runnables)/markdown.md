LangChain me *Chains* aur *Runnables* ka kaafi important role hota hai, lekin dono mein kuch key differences hote hain.

1. **Chains**:
   - Chains LangChain mein ek process hoti hai jo multiple steps ko sequence mein connect karti hai. 
   - Jaise ek chain mein ek input diya jata hai, aur har step apni output generate karta hai, jo next step ko input ke roop mein diya jata hai.
   - Example: Agar apko ek product ka name generate karna ho, aur phir us product ke liye description likhna ho, to aap ek *Sequential Chain* use karenge jisme ek chain se output next chain ko input ke roop mein diya jata hai.

2. **Runnables**:
   - Runnables ek function ya method hote hain jo ek specific task ko perform karte hain, jaise API se data lena ya kisi tool ko call karna.
   - Runnables ko *chain* kar sakte hain, jisme ek runnable ka output dusre runnable ko input ban jata hai. Is process ko *RunnableSequence* kaha jata hai.
   - Runnables ko zyada flexible banaya gaya hai, jisme inhe directly invoke ya stream bhi kiya ja sakta hai.

**Key Difference**:
- *Chains* zyada focused hote hain structured workflows aur sequential operations par, jabki *Runnables* zyada modular hote hain aur ek task ko perform karte hain. Runnables ko aap ek sequence mein chain kar sakte hain jisme unka output next runnable ko pass hota hai. 

Aap chains ko specific data flows ke liye use karte hain, jabke runnables ko tasks ko execute karne ke liye use kiya jata hai.


<br/>

----

<br/>

# How to chain runnables

LangChain mein *runnables* ko chain karna ek powerful feature hai jo aapko multiple tasks ko sequence mein efficiently execute karne ka mauka deta hai. Is process mein, ek runnable ka output directly doosre runnable ko input ke roop mein diya jata hai, jisse ek streamlined aur automated workflow banta hai.

### Step-by-Step Explanation:

1. **LangChain Expression Language (LCEL)**:
   LangChain ka Expression Language (LCEL) ek powerful tool hai jo runnables ko chain karne mein madad karta hai. Aap do runnables ko ek sequence mein chain kar sakte hain.

2. **Using Pipe Operator (|)**:
   Aap chain karne ke liye do tarike use kar sakte hain:
   - **Pipe Operator (|)**: Yeh operator runnables ko connect karne ka shorthand method hai. Jab aap is operator ko use karte hain, to pehle runnable ka output automatically next runnable ko input ban jata hai.
   - **.pipe() Method**: Yeh method zyada explicit aur readable hai. Aap is method ko use karke runnables ko chain karte hain, jisme output ko manually pass kiya jata hai.

   **Example**:
   ```python
   result = first_runnable | second_runnable
   ```
   Ya aap is tarah bhi likh sakte hain:
   ```python
   result = first_runnable.pipe(second_runnable)
   ```

3. **RunnableSequence**:
   Jab aap multiple runnables ko chain karte hain, to jo sequence banta hai, woh bhi ek runnable ke roop mein treat hota hai. Iska matlab hai ki aap is sequence ko directly invoke, stream, ya aur zyada chain kar sakte hain, jaise kisi normal runnable ko karte hain.

4. **Advantages of Chaining Runnables**:
   - **Efficient Streaming**: Agar aap ek sequence create karte hain, to jab bhi ek output available hota hai, wo immediately stream hota hai. Isse real-time processing aur faster results milte hain.
   - **Debugging & Tracing**: LangChain ka *LangSmith* tool debugging aur tracing ko simple banata hai. Aap easily dekh sakte hain ke har step mein kya ho raha hai aur kahin pe koi error toh nahi aa rahi.

### Simple Example:

Maan lo aapko ek text ko process karna hai:
1. Pehla task: Text ko clean karna.
2. Dusra task: Cleaned text ko analyze karna.

Aap in runnables ko chain kar ke ek sequence bana sakte hain:
```python
clean_text = text_cleaner.pipe(text_analyzer)
```

### Key Benefits:
- **Faster Execution**: Runnables ko chain karke aap ek streamlined aur faster execution process create karte hain.
- **Reusable**: Runnables ko alag alag tasks ke liye reuse kiya ja sakta hai, jo code maintainability ko improve karta hai.
- **Customization**: Chaining allows full flexibility in designing complex tasks with specific input-output requirements.

<br/>

----

<br/>

# How to invoke runnables in parallel

`RunnableParallels` LangChain mein ek aisi technique hai jo kaafi tasks ko parallel chalane ke liye use hoti hai. Iska fayda yeh hai ke aap ek hi input par kai tasks ko ek sath chalane ke liye bhej sakte ho, aur phir un tasks ke results ko merge karke final output bana sakte ho. 

Misaal ke taur par agar aapko koi question answer karna ho, aur aapko pehle context chahiye aur phir question ko process karna hai, toh `RunnableParallel` aapko yeh dono tasks parallel mein karne ki suhulat deta hai. 

Pehle input ko do branches mein divide kiya jata hai, ek retriever ko context ke liye aur doosra branch question ko process karta hai. Jab dono tasks complete ho jaate hain, unke results ko ek final output mein combine kiya jata hai.

Is tarah ka system use karna tasks ko zyada efficiently parallel process karne mein madad karta hai.


```markdown

    Input  
     /  \  
    /    \  
Branch1 Branch2  
    \    /  
     \  /  
   Combine 

```

<br/>

 ### **RunnablePassthrough** 
 Agar **question** ko `RunnablePassthrough` ke through bypass karna tha, toh usay directly pass bhi kiya jaa sakta tha. Lekin yahan isko **`{"context": retriever, "question": RunnablePassthrough()}`** is tarah likhne ka reason yeh hai ke yeh ek **dictionary** ke format mein hai, jisme context aur question ko specify kiya jaa raha hai.

### Detailed Explanation:
1. **{"context": retriever, "question": RunnablePassthrough()}**:
   - Yeh dictionary define karti hai ke **context** kahan se aayega (yani retriever se) aur **question** kis tarah handle hoga (yahan `RunnablePassthrough()` ke zariye).
   
2. **`RunnablePassthrough()`**:
   - Yeh ek pass-through mechanism hai, jo **question** ko bina kisi badlav ke aage bhejta hai. Matlab, **question** ko koi transformation nahi hoti, bas yeh directly usko aage ke steps (jaise **prompt** aur **model**) tak bhej deta hai.
   
3. **Usage in the Chain**:
   - Jab yeh dictionary use hoti hai, toh **context** ko retriever se fetch kiya jaata hai, aur **question** ko bypass karke `RunnablePassthrough()` ke through directly next step tak bheja jaata hai.
   - Is tarah se, aap question ko **pass-through** kar rahe ho bina usko modify kiye.

Agar directly **question** ko bypass karna tha, toh aap simply **question** ko `RunnablePassthrough()` se connect kar sakte the, lekin yahan dono ko dictionary format mein rakha gaya hai taake dono cheezon ko alag-alag specify kiya ja sake: ek ko retriever se fetch karna hai (context), aur dusre ko pass-through karna hai (question).

### Simple Example:
Agar aap **context** aur **question** ko alag-alag handle karna chahte ho, toh yeh ek tarika hota hai. Isse aap ko flexibility milti hai aur easily manage kar sakte ho ke kis cheez ko kahan se laana hai aur kis cheez ko pass-through karna hai.