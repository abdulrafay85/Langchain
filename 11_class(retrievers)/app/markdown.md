## Using Advanced Retrievers in LangChain ``(https://www.comet.com/site/blog/using-advanced-retrievers-in-langchain/)``

<br/>

### **LangChain** 
- mein retrieval systems ka matlab hai aise systems jo kisi query par documents (ya information) dhoond kar waapas dete hain. Iska use AI applications mein hota hai, jahan log ek sawal poochte hain aur system relevant information ya documents la kar deta hai.

### Key Concepts
1. **Retriever Kya Hai?**
   - Retriever aik aise system ko kehte hain jo natural language mein poochi gayi query (jaise: "Mujhe programming ke notes chahiye") ko samajh kar us se related documents ya information return karta hai.
   - LangChain mein retriever ek aise function ko implement karta hai jo query ko input leta hai aur relevant documents ka result deta hai.

2. **Kya Karta Hai Retriever?**
   - Jab aap retriever ko query dete hain, toh yeh function us query ke mutabiq documents ya results dhoondta hai aur aapko waapas deta hai. Aap simply `retrigger.invoke(query)` likhte hain aur yeh related documents list mein return karta hai.

3. **Common Types of Retrieval Systems**
   - Retrieval systems alag alag types ke hote hain, kuch popular types yeh hain:
     - **Search APIs**: Aise systems jo sirf search results dete hain, bina documents ko store kiye, jaise Wikipedia Search.
     - **Relational Databases**: Yeh databases structured data ke sath kaam karte hain, jaise SQL databases, aur query ko structured query mein convert karte hain.
     - **Lexical Search**: Yeh algorithms words ko match karte hain. Jaise agar aap "Python" search karte hain, toh yeh "Python" kaam se related results dhoondenge.
     - **Vector Stores**: Yeh systems AI ke zariye unstructured data ko store aur retrieve karte hain.

4. **Advanced Features**
   - **Ensemble**: Yeh technique multiple retrieval systems ko ek saath use karti hai takay behtar results mil saken.
   - **Source Document Retention**: Yeh feature original document ko safe rakhta hai jab document ko chhote chunks mein divide karke indexing ki jaye.

### Use Case
Agar aap LangChain use karke ek aisa AI system banana chahte hain jo questions par relevant information ya documents return kare, toh LangChain mein ye retrieval systems aur retrievers kaam aayenge.

### Typse of Retriverse

**Vectorstore retriever** ka kaam yeh hai ke yeh vectorstore mein stored documents ko search karke relevant information retrieve karta hai. Yeh vectorstore ke different search methods ka use karke queries ke answers nikaalta hai. Chaliye is process ko step-by-step samajhte hain:

### 1. **Retriever ko Vectorstore se Banayein (Creating a Retriever from Vectorstore)**

Pehle, humein ek vectorstore banani hoti hai, jo humare text ko vector format mein save kar sake. Is example mein hum **FAISS vectorstore** ka use kar rahe hain. Aaye yeh steps dekhein:

- **Text Loader** se hum documents load karte hain.
- **Text Splitter** ka use karke documents ko chhote chunks mein split karte hain, taake retrieval process aur efficient ho.
- **Embeddings**: Hum documents ko vector format mein convert karte hain embeddings ki madad se. Yahan **OpenAIEmbeddings** ka istemal ho raha hai.

Code example:

```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

# Documents ko load karna
loader = TextLoader("state_of_the_union.txt")
documents = loader.load()

# Text ko chhote chunks mein split karna
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# Embeddings ko vectorstore mein save karna
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(texts, embeddings)
```

### 2. **Retriever Ka Instance Banayein**

Ab hum vectorstore mein `as_retriever` method ko use karke ek retriever bana sakte hain. Yeh ek **VectorStoreRetriever** banayega jo ab query ke jawab dhoond sakta hai.

```python
retriever = vectorstore.as_retriever()
```

Is retriever ko ab hum kisi bhi query pe call kar sakte hain, aur yeh humare documents mein se relevant information nikaal dega:

```python
docs = retriever.invoke("what did the president say about ketanji brown jackson?")
```

### 3. **Similarity Search aur Maximum Marginal Relevance (MMR) Search**

By default, retriever **similarity search** ka use karta hai, jo sirf query aur documents mein similarity ke basis par results deta hai. Lekin agar hum chahte hain ke results diverse aur relevant hoon, toh hum **MMR** (Maximum Marginal Relevance) ko enable kar sakte hain. Yeh similar aur unique results dono ko balance karta hai.

```python
retriever = vectorstore.as_retriever(search_type="mmr")
docs = retriever.invoke("what did the president say about ketanji brown jackson?")
```

### 4. **Additional Search Parameters**

Kuch additional parameters bhi set kar sakte hain jo search ko refine karte hain:

- **Similarity Score Threshold**: Hum yeh define kar sakte hain ke sirf wohi documents wapas aayein jinki score threshold (similarity) ek certain value se zyada ho. Yahan pe score threshold `0.5` rakha hai.

  ```python
  retriever = vectorstore.as_retriever(
      search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5}
  )
  docs = retriever.invoke("what did the president say about ketanji brown jackson?")
  ```

- **Top-k Results**: Top-k ka matlab hai ke sirf top `k` documents (jo sab se relevant hain) wapas aayein. Yahan example mein `k=1` rakha gaya hai, is se sirf ek document wapas aayega.

  ```python
  retriever = vectorstore.as_retriever(search_kwargs={"k": 1})
  docs = retriever.invoke("what did the president say about ketanji brown jackson?")
  ```

</br>
</br>

______

</br>
</br>

### **`as_retriever()`** 
* method ka istemal Vector Store (jaise ke Pinecone, FAISS, ya Elasticsearch) ke saath hota hai taake aap us store se retrieval capabilities ko access kar sakein. Chalo, isay detail mein samjhte hain:

### **1. `vectorstore` Kya Hai?**

- `vectorstore` ek aisa data structure hai jisme aapki documents ya text ko vectors (mathematical representations) ke form mein store kiya jata hai.
- Ye vectors kisi bhi text ko numerical format mein convert karte hain, taake machine learning algorithms unhein samajh sakein.

### **2. `as_retriever()` Method Kya Karta Hai?**

- **Purpose**: Ye method `vectorstore` ko ek retriever mein convert karta hai. Iska matlab hai ke ab aap is vector store ko queries ke liye istemal kar sakte hain.
  
- **Kaise Kaam Karta Hai**:
  - Jab aap `as_retriever()` call karte hain, ye method vector store ke andar documents se related vectors ko dhoondne ka ek mechanism tayar karta hai.
  - Jab aap koi query dete hain, ye method query ko vector mein convert karta hai aur phir us vector ko vector store mein search karta hai taake relevant documents ya information nikaale.

### **3. Kaise Istemal Karein?**

Agar aapko ek example chahiye, toh aap kuch is tarah se `as_retriever()` ka istemal kar sakte hain:

```python
from langchain.vectorstores import SomeVectorStore  # Replace with your actual vector store class

# Vector store ka object banana
vectorstore = SomeVectorStore(...)

# Vector store ko retriever mein convert karna
retriever = vectorstore.as_retriever()

# Ab aap is retriever se relevant documents dhoond sakte hain
results = retriever.retrieve("Aapka query yahaan")  # Aapka sawaal ya query
```

### **4. Summary**

- **`as_retriever()`**: Ye method vector store ko ek retriever mein convert karta hai, taake aap queries ke liye relevant documents nikaal sakein.
- **Kaam**: Ye method aapki query ko vector mein convert karke, vector store se search karta hai aur relevant information laata hai.

Is tarah, `as_retriever()` ka istemal aapko aapki documents ko efficiently dhoondne ki sahulat deta hai.



</br>
</br>

______

</br>
</br>


### `vectorstore.as_retriever()` Kya Karta Hai?

1. **Vector Store**:
   - Socho ke aapke paas ek library hai jisme bahut saari kitaabein hain. In kitaabon ko jab aap read karte hain, toh aap unhein samajhte hain aur yaad rakhte hain.

2. **Retrieval**:
   - Ab agar aapko kisi khaas kitaab ya information ki zaroorat hai, toh aap library mein dhoondte hain. Ye dhoondhna hota hai retrieval.

3. **`as_retriever()` Method**:
   - `as_retriever()` ek method hai jo aapke vector store (jaise library) ko ek aise tool mein tabdeel kar deta hai jo aapko dhoondhne mein madad karta hai. 
   - Jab aap is method ko use karte hain, toh ye aapko ek retriever deta hai. Ye retriever aapko query karne ki salahiyat deta hai, matlab aap kuch puchte hain aur ye aapko relevant information laake deta hai.

### Kaise Kaam Karta Hai?

- Jab aap ye likhte hain: 
  ```python
  retriever = vectorstore.as_retriever()
  ```
  Ye line aapko ek naya retriever object de deti hai. Ab aap is object ka istemal karke kuch bhi padh sakte hain, jaise:
  ```python
  results = retriever.retrieve("Koi specific question")
  ```

### Example:

Agar aapko pata karna hai ke "Python programming kya hai?", toh aap ye karte hain:

```python
results = retriever.retrieve("Python programming kya hai?")
```

Ye retriever aapke vector store (library) mein se relevant information dhoond kar aapko dega.

### Summary:

- **Vector Store**: Aapki data library.
- **as_retriever()**: Isko use karne se aapko dhoondhne ka tool milta hai.
- **Retrieve**: Aap apne questions poochte hain aur ye relevant answers laata hai.

</br>
</br>

1. **Retriever Ko Setup Karna (Banana)**:
   - Sab se pehle aap apne documents ko load karenge aur unko chhoti chhoti parts mein divide karenge (sochte hain ke yeh pages hain jo hum search karenge).
   - Yeh documents phir embeddings ke through vectors mein convert hote hain, jo basically documents ka mathematical form hai, taake hum unhein compare kar saken.
   - Phir yeh vectors aik vector store mein save hote hain. FAISS ek aisa vector store hai jo documents ko similarity ke base par organize karta hai, yani jo cheezein milti-julti hain woh paas paas hoti hain.

2. **Retriever Ko Activate Karna**:
   - Ab, vector store se **retriever** banate hain. Aik simple command `.as_retriever()` likhne se vector store retriever ban jata hai jo aapki queries ka jawab relevant documents se de sakta hai.

3. **Search Type Set Karna**:
   - Default mein ye retriever similarity search use karta hai, jo aapki query ke closest matching documents nikaalta hai.
   - Agar aap **MMR (maximum marginal relevance)** chahte hain, to search type "mmr" set kar sakte hain. Is tarah ye zyada diverse aur unique answers dega.

4. **Search Parameters Set Karna**:
   - **Score Threshold**: Aap ye bhi specify kar sakte hain ke sirf wohi documents dikhayein jinka score threshold (similarity) ek level se zyada ho, jaise ke `0.5`.
   - **Top-K**: Ye limit specify karta hai ke sirf `k` documents (jaise top 1, top 3) wapas ayein.

Ye process kaam ko automate karta hai aur queries ko fast aur relevant banata hai, yani hamesha aapko wohi documents milein jo kaam ke hain.

</br>

_____________

</br>

LangChain mein **vector store retriever** aik aisa tool hai jo query ke mutabiq documents ko search aur retrieve karta hai. Ye retrieval documents ki similarity ya context pe based hota hai, yani agar query aur document ke beech ka meaning match karta hai, toh woh relevant document ko retrieve karega.

### Kaise Kaam Karta Hai Vector Store Retriever

1. **Vector Embeddings Ka Banana**: Pehle, har document ko vector mein convert kiya jata hai, jo aik tarah ka mathematical representation hota hai. Ye vectors represent karte hain ke document mein kya content hai aur ye vector store (jaise FAISS ya Chroma) mein store hote hain.

2. **Retriever Ko Initialize Karna**: Vector store ko retriever mein badalne ke liye `.as_retriever()` method ka use kiya jata hai. Yeh retriever aik interface provide karta hai jo query ke basis pe documents ko search kar sakta hai. For example:
   ```python
   retriever = vectorstore.as_retriever()
   ```

3. **Search Types Set Karna**:
   - **Similarity Search**: Is mein retriever aise documents ko search karta hai jo query ke meaning ke saath sab se closely match karte hain.
   - **Maximum Marginal Relevance (MMR)**: Yeh search method diverse aur unique documents dhoondhne mein madad karta hai, taake aapko har result mein kuch naya milay.

4. **Search Parameters Control Karna**:
   - **Top-k Results**: Aap specify kar sakte hain ke kitne top results chahiyein, jaise top 5 ya top 10.
   - **Threshold Set Karna**: Yeh score limit specify karta hai ke similarity ka minimum score kitna hona chahiye taake woh document retrieve ho.

### Example Usage:
Aap aik query chala sakte hain aur retriever automatically relevant documents wapas bhej dega:
```python
retrieved_docs = retriever.invoke("What is said about AI ethics?")
```

**Vector store retrievers** LangChain mein un applications ke liye useful hain jahan aapko user queries ke against accurate aur contextually relevant information retrieve karni ho. Iska istemaal mostly customer support bots ya document search mein hota hai.

</br>

_____________

</br>

#### **`MultiQueryRetriever`** 
- ka kaam yeh hai ke yeh ek hi query ko multiple angles se generate karta hai, taki aapko **zyada diverse aur accurate** results mil sakein. 

### Kaise Kaam Karta Hai:
1. **Query ko Multiple Versions Mein Convert Karna**: Jab aap koi question puchte ho, toh yeh tool **LLM (Language Model)** ka use karke us question ke multiple versions banata hai. Jaise agar aap poochte ho:
   - "Task decomposition ke approaches kya hain?"
   Toh yeh tool multiple tareeqon se is question ko banata hai, jaise:
     - "Task decomposition ke methods kya hain?"
     - "Task decomposition ko kis tareeqe se kiya jaata hai?"
     - "Task decomposition ke strategies kya hain?"

2. **Documents ko Retrieve Karna**: Har ek generated query se documents ko search kiya jaata hai. Har query ka apna alag result milta hai.

3. **Results ka Union**: Phir sabhi queries se aaye huye results ko combine karke, aapko ek **unique set** milta hai jo aapke original question se zyada relevant documents dikhata hai.

### Parameters:
- **retriever**: Yeh wo retriever hota hai jo documents ko query ke mutabiq retrieve karta hai.
- **llm_chain**: Yeh ek LLM aur output parser ka chain hota hai jo query ke multiple versions generate karta hai.
- **verbose**: Agar yeh `True` ho toh aap generated queries dekh sakte ho.

### Example:
Agar aap kahein "Task decomposition ke approaches kya hain?", toh MultiQueryRetriever is query ko multiple versions mein badal kar search karega aur phir un sab versions ke results ko combine karega, jisse aapko ek **better aur richer** set of documents milta hai.

Yeh method simple retrieval ke mukable mein **zyada diverse aur accurate** answers provide karta hai.

<br/>

________________

<br/>

### `MultiQueryRetriever` 

LangChain me ek retriever hai jo ek hi query ko multiple variations me convert karta hai. Isse hum zyada relevant documents retrieve kar sakte hain, jo sirf ek query se nahi milte.

### Key Methods aur Parameters:

1. **`from_llm`**:
   - **Purpose**: Yeh method `MultiQueryRetriever` ko LLM (language model) se initialize karta hai.
   - **Parameters**:
     - `retriever`: Jo retriever documents ko search karega (usually vector store).
     - `llm`: LLM jo different query versions generate karega.
     - `prompt`: Optional prompt jo query generation ke liye use hota hai.
     - `parser_key`: Yeh specify karta hai ke LLM output ko kaise parse kiya jayega.

2. **`generate_queries`**:
   - **Purpose**: Yeh method ek user query se multiple query variations generate karta hai.
   - **Parameters**:
     - `question`: User ki original query.
   - **Return**: Yeh ek list deta hai jisme multiple queries hoti hain.

3. **`get_relevant_documents`**:
   - **Purpose**: Yeh method query ke base par relevant documents retrieve karta hai.
   - **Parameters**:
     - `query`: Query jise use karna hai.
   
4. **`invoke`**:
   - **Purpose**: Yeh method LLM ke saath sab queries run karta hai aur relevant documents nikalta hai.
   - **Parameters**:
     - `input`: User ki query.

5. **`unique_union`**:
   - **Purpose**: Yeh method ensure karta hai ke jo documents retrieve kiye gaye hain wo unique ho.
   - **Parameters**:
     - `documents`: Jo documents filter karna hain.

### Example:
```python
from langchain.llms import ChatGoogleGenerativeAI
from langchain.retrievers import MultiQueryRetriever

llm = ChatGoogleGenerativeAI(api_key="your_api_key")
retriever = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(), llm=llm)

results = retriever.invoke("AI ke kya faide hain?")
print(results)
```

Yeh retriever multiple query versions generate karta hai, jisse zyada accurate aur diverse results milte hain. Traditional retrievers jo sirf ek query par rely karte hain, wo kabhi kabhi exact matches nahi dikhate. 


<br/>

________________


<br/>


### **Contextual Compression Retriever** 
1. LangChain ka Contextual Compression Retriever ek tool hai jo query-specific document retrieval ke liye kaam karta hai. 
2. Yeh ek standard retriever ko wrap karta hai aur documents ko compress karne ke liye additional logic lagata hai. 
3. Iska kaam hai retrieved documents me se irrelevant parts ko hata kar sirf wo content rakhna jo query ke liye important ho.

<br/>

--- 

<br/>

### **Real-Life Analogy**
Socho ke tumhare paas ek bohot badi kitaab hai, aur tum sirf uska wo hissa dhoondh rahe ho jo tumhare sawaal ka jawab de sakta hai.  
- **Normal Retriever**: Poora chapter laakar dega, chahe usmein irrelevant details bhi ho.  
- **Contextual Compression Retriever**: Sirf wo lines ya paragraphs laayega jo tumhare sawaal ke liye important hain. Baaki sab ignore karega.  


<br/>

---

### **Kaam Kaise Karta Hai?**

1. **Normal Retrieval**: Pehle ek system hota hai jo data ya documents ko retrieve karta hai.  
   - Jaise kisi kitaab ka chapter ya article ke kuch parts.  

2. **Compression Layer**: Phir ek smart system (compressor) us data ko filter ya summarize karta hai.  
   - Sirf wo points ya parts rakhta hai jo query se match karte hain.  

---

### **Practical Example**
Let’s say tumhare system ke paas ye text hai:

> "Ketanji Brown Jackson ka Supreme Court mein hona ek historic moment hai. Uska decision-making style logon ko bohot inspiring lagta hai. Usne 2023 mein ek important case decide kiya jo educational policies pe focus karta tha."

Agar tumhara sawaal hai:  
**"Ketanji Brown Jackson ke achievements kya hain?"**

#### **Without Compression:**
Poora text retrieve hoga, chahe uska sirf thoda part kaam ka ho.  

#### **With Compression:**
System sirf yeh part dega:  
**"Ketanji Brown Jackson ka Supreme Court mein hona ek historic moment hai. Usne 2023 mein ek important case decide kiya."**

---

### **Implementation ko Simple Banate Hain**
Agar tum LangChain mein isko implement karte ho, toh:

#### **Steps:**
1. **Data Prepare Karo:** Pehle apna data ya documents split karo manageable chunks mein.  
2. **Retriever Use Karo:** Ek base retriever lagao jo initial data laayega.  
3. **Compressor Add Karo:** Jo sirf relevant parts ya compressed information dega.  

#### Code Example (Simplified):
```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain.llms import OpenAI

# Step 1: Data setup
documents = ["Yahan apna data ya text daalo."]
retriever = FAISS.from_texts(documents, OpenAIEmbeddings()).as_retriever()

# Step 2: Compressor setup
llm = OpenAI(temperature=0)
compressor = LLMChainExtractor.from_llm(llm)

# Step 3: Contextual Compression Retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
)

# Step 4: Query and get compressed data
query = "Achievements of Ketanji Brown Jackson?"
compressed_docs = compression_retriever.get_relevant_documents(query)
print(compressed_docs)
```

---

### **Asaan Baatein Yad Rakho:**
1. **Purpose:** Sirf relevant aur short data dena.
2. **Use:** Jab tumhare paas bohot saara data ho aur tum precise answers chaho.
3. **LangChain Tools:** Base retriever + Compressor (jaise LLM ya Embedding filters).



### `LLMChainExtractor.from_llm(llm)` 
- ka matlab hai ke ek compressor create karna jo query ke hisaab se documents ke andar se sirf relevant information extract kare. 

- **LLM**: Ek large language model (jaise OpenAI) jo samajh sakta hai context aur text ko summarize kar sakta hai.
- **from_llm(llm)**: Is method se extractor banate hain jo LLM ko use karke documents ka relevant content nikalta hai. 

Yeh compressor aapki query ke liye specific aur concise data provide karega, taake irrelevant text skip ho jaye.

### `Extractor` 
- ek tool ya mechanism hota hai jo kisi bade dataset ya text ke andar se **relevant information** nikalta hai. 

For example:

1. Agar aapke paas ek document hai jisme 1000 words hain, aur aap sirf un 50 words ko chahte ho jo kisi specific topic ya query se related hain, to extractor yeh kaam karega.
2. Yeh query ke hisaab se text ko analyze karega aur sirf woh part dega jo useful hai.

Iska use time aur resources save karne ke liye hota hai, taake sirf zaruri data process ho.



<br/>

_________________

<br/>

`LLMChainFilter` vs `LLMChainExtractor` dono tools hain jo documents se information nikaalne mein madad karte hain, lekin inka kaam thoda different hai.

### **1. LLMChainFilter:**
   - **Kaam**: Yeh document ko filter karta hai. Matlab agar aapke paas bohot saare documents hain, toh yeh decide karega ke kaunsa document aapko chahiye aur kaunsa nahi.
   - **Kaise kaam karta hai**: Agar aapne koi question pucha, toh yeh dekhega ki kaunse documents aapke question ke jawab ke liye relevant hain. Jo documents irrelevant hain, unhe hata dega.
   - **Use Case**: Jab aapko sirf un documents ko chahiye ho jo aapke question se directly related hain, aur baaki ko ignore karna ho.

**Example**: Agar aap puchte ho "President ne Ketanji Brown Jackson ke baare mein kya kaha?", toh yeh filter karega aur sirf unhi documents ko dikhayega jo is sawal ka jawab dete hain.

### **2. LLMChainExtractor:**
   - **Kaam**: Yeh document mein se specific information nikaalta hai. Matlab agar aapko kisi document se ek particular cheez chahiye (jaise naam, date, ya facts), toh yeh woh cheez nikaal lega.
   - **Kaise kaam karta hai**: Jab aap ek question puchte hain, yeh document ko dekh kar aapka specific jawab nikaalta hai. Jaise agar aapne pucha "Ketanji Brown Jackson ke baare mein president ne kya kaha?", toh yeh sirf president ke statement ka relevant hissa nikaal lega.
   - **Use Case**: Jab aapko document mein se ek specific cheez chahiye ho, jaise kisi ka naam, date ya koi aur specific fact.

**Example**: Agar aap puchte ho "President ne Ketanji Brown Jackson ke baare mein kya kaha?", toh yeh extractor sirf uss part ko nikaal lega jahan president ne Ketanji Brown Jackson ka naam liya ho.

### **Main Difference:**
- **LLMChainFilter**: Yeh pura document check karta hai aur decide karta hai kaunsa document aapke question se relevant hai, aur kaunsa nahi.
- **LLMChainExtractor**: Yeh ek specific cheez ya information nikaalta hai document se, jaise kisi ka naam ya fact.

### **Simple Comparison**:
- Agar aapko **poore documents ko select ya reject** karna hai, toh aap **`LLMChainFilter`** use karenge.
- Agar aapko **specific information chahiye** (jaise naam, date, ya koi aur fact), toh aap **`LLMChainExtractor`** use karenge.

I hope ab aapko yeh dono tools ka difference achhe se samajh aa gaya hoga.

<br/>

_________________

<br/>

### **LLMListwiseRerank**

- Yeh ek technique hai jo documents ko **query ke mutabiq arrange** karti hai. Jab tumhare paas bahut saare documents ho aur tumhe sirf wo chahiye jo tumhare sawal se sabse zyada related ho, to yeh method kaam aata hai.  

---

### **Kaise kaam karta hai?**  
1. **Ek sath Analyze:**  
   Yeh puri document list ko aik sath dekhta hai aur judge karta hai kaunsa document query ke liye sabse useful hai.  

2. **Top Results:**  
   Tum bata sakte ho ke sirf kitne top documents chahiye, jaise top 1, top 3, ya top 5.  

3. **LLM ka Use:**  
   Yeh ek powerful language model (jaise GPT-4) use karta hai jo natural language samajhne me expert hai.  

---

### **Example:**  
Maal lo tumhe yeh sawal poochhna hai:  
**"President ne healthcare ke bare me kya kaha?"**  
Aur tumhare paas 5 documents hain.  

LLMListwiseRerank un 5 documents ko dekhega, aur judge karega kaunsa document tumhare sawal se sabse zyada relevant hai. Phir tumhe sirf relevant documents dega aur baaki hata dega.  

---

### **LLMListwiseRerank aur doosri techniques ka fark:**  
1. **LLMChainFilter:**  
   Yeh sirf irrelevant documents ko **filter** karta hai, ranking nahi karta.  

2. **LLMListwiseRerank:**  
   Yeh not only irrelevant ko filter karta hai, lekin relevant ko rank bhi karta hai.  

<br/>

_____________

<br/>


### **DocumentCompressorPipeline** 
- bana rahe hain jo kai steps mein documents ko process karta hai taake sirf relevant aur useful documents mil sakein.

### Steps:
1. **Text Split Karna**:
   Pehle, `CharacterTextSplitter` ka use karke documents ko chhote hisso mein todte hain (300 characters har chunk mein). Is se system ko zyada focused aur manage karna asaan ho jata hai.
   
   ```python
   splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0, separator=". ")
   ```

2. **Redundant Documents Hatana**:
   `EmbeddingsRedundantFilter` ka use kar ke hum un documents ko hata dete hain jo ek jaise ya bohot similar hain. Is se hum time aur resources bachate hain, kyunki duplicate documents ko process nahi kiya jata.
   
   ```python
   redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
   ```

3. **Relevance Filter Lagana**:
   Phir, `EmbeddingsFilter` lagate hain jo sirf un documents ko rakhta hai jo query se relevant hon. Agar unki similarity ek certain threshold (jaise 0.76) se kam ho, to wo documents hata diye jate hain.
   
   ```python
   relevant_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)
   ```

4. **Compressor Pipeline**:
   Ab, jo transformations humne define kiye hain (splitter, redundant filter, aur relevance filter), unko ek saath combine karte hain `DocumentCompressorPipeline` mein. Matlab, pehle documents ko split kiya jata hai, phir redundant documents ko remove kiya jata hai, aur akhir mein sirf relevant documents ko rakha jata hai.
   
   ```python
   pipeline_compressor = DocumentCompressorPipeline(
       transformers=[splitter, redundant_filter, relevant_filter]
   )
   ```

5. **Documents Retrieve Karna**:
   Last step mein, `ContextualCompressionRetriever` ko use karke hum query ke liye relevant documents retrieve karte hain. Ye compression pipeline apply kar ke documents ko refine karta hai.
   
   ```python
   compression_retriever = ContextualCompressionRetriever(
       base_compressor=pipeline_compressor, base_retriever=retriever
   )
   ```

### Result:
Is process ke baad, jo documents retrieve hote hain wo sirf wahi hote hain jo query ke liye relevant hain. Is se unnecessary aur redundant information hat jaati hai aur jo zaroori hai wo aasan se mil jata hai.

<br/>

### `EmbeddingsRedundantFilter` 
- ka kaam redundant (dobara se aane wale) documents ko remove karna hota hai, jismein unke meanings ya content kaafi similar ho. 

### Kaise kaam karta hai:
1. **Embeddings**: Pehle har document ko ek **embedding** mein convert kiya jata hai. Embedding, ek number ka set hota hai jo text ka meaning capture karta hai. Jaise agar do documents same topic par ho, toh unka embedding similar hoga.
  
2. **Similarity Check**: Jab embeddings ban jati hain, toh filter dono documents ke embeddings ko compare karta hai. Agar do documents ka embedding ek doosre ke bohot similar hain, toh unko redundant (duplicate) samajh ke ek ko hata diya jata hai.

3. **Threshold**: Is filter mein ek **similarity threshold** set kiya jata hai, jo decide karta hai ki documents kitni similarity tak ek doosre ke redundant honge. Agar similarity score threshold se upar hai, toh ek document ko remove kar diya jata hai.

### Example:
Maan lo tumhare paas kuch news articles hain, aur kuch articles same event ke baare mein hai. **EmbeddingsRedundantFilter** un articles ke embeddings banata hai aur compare karta hai. Agar do articles ka similarity score zyada hai (jaise 0.76 se zyada), toh ek ko result se hata diya jata hai, taake sirf unique documents dikhaye jayein.

### Code Example:
```python
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
```
Is code mein `embeddings` wo model hai jo document ko embedding mein convert karta hai. Uske baad filter decide karta hai ki kaunse documents redundant hain aur unhe hata deta hai.


<br/>


### `DocumentCompressorPipeline` 
- ek tool hai jo LangChain framework mein use hota hai. Iska kaam documents ko process aur refine karna hota hai, jisse unka size chhota ho jaye aur woh query ke liye zyada relevant ban jayein. Yeh pipeline compressors aur transformers ka ek sequence hota hai jo alag-alag steps perform karta hai.

### **Key Features:**
1. **Multiple Transformers and Compressors:**
   - Pipeline mein tum alag-alag tools ko chain kar sakte ho.
   - Jaise:
     - **TextSplitter**: Bade documents ko chhote chunks mein todta hai.
     - **EmbeddingsRedundantFilter**: Duplicate ya similar documents ko remove karta hai.
     - **EmbeddingsFilter**: Sirf relevant documents ko filter karta hai.

2. **Customizable Process:**
   - Tum apni requirement ke hisaab se alag compressors aur transformers use kar sakte ho. Har step ek specific kaam karta hai.

3. **Improves Efficiency:**
   - Bade data sets mein sirf unhi documents ko process karta hai jo kaam ke hote hain, aur irrelevant information ko hata deta hai.

---

### **Kaise Kaam Karta Hai?**
1. **Input Documents**:
   - Pehle tumhe kuch raw documents provide karne hote hain.

2. **Sequence of Operations**:
   - Documents ek pipeline ke through jate hain. Har step ek operation perform karta hai:
     - Pehle documents split hote hain (agar bade hain).
     - Redundant (duplicate) documents ko remove kiya jata hai.
     - Phir query ke relevant documents ko filter kiya jata hai.

3. **Output**:
   - Tumhe compressed aur refined documents milte hain jo chhote hote hain aur query ke liye zyada useful hote hain.

---

### **Code Example:**
```python
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain_text_splitters import CharacterTextSplitter

# Step 1: Define Transformers and Compressors
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0, separator=". ")
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)
relevant_filter = EmbeddingsFilter(embeddings=embeddings, similarity_threshold=0.76)

# Step 2: Create Pipeline
pipeline_compressor = DocumentCompressorPipeline(
    transformers=[splitter, redundant_filter, relevant_filter]
)

# Step 3: Use the Pipeline
compression_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline_compressor, base_retriever=retriever
)

# Step 4: Retrieve Compressed Documents
compressed_docs = compression_retriever.invoke("What did the president say about healthcare?")
```

---

### **Detailed Steps in Example:**
1. **TextSplitter**:
   - Document ko 300 characters ke chunks mein tod deta hai, taake processing zyada efficient ho.

2. **EmbeddingsRedundantFilter**:
   - Agar koi chunks kaafi similar hain (e.g., ek hi baat bar bar likhi hai), toh unhe hata diya jata hai.

3. **EmbeddingsFilter**:
   - Query ke embeddings ke basis par sirf relevant chunks ko select karta hai.

4. **ContextualCompressionRetriever**:
   - Final compressed documents ko retrieve karta hai.

---

### **Faida:**
1. **Performance Improvement**:
   - Chhote aur refined documents hone ki wajah se query processing zyada fast hoti hai.

2. **Relevance**:
   - Sirf useful documents ko process karta hai, extra ya irrelevant data ko hata deta hai.

3. **Flexibility**:
   - Tum apne use-case ke hisaab se is pipeline ko modify kar sakte ho.


<br/>

_______________


<br/>

### How to reorder retrieved results to mitigate the "lost in the middle" effect

#### Masla Kya Hay?
Jab **bohot saare documents** retrieve karte hain (e.g., 10 ya us se zyada), **beech walay documents ko model ignore kar deta hai**. Isko **"lost in the middle" effect** kehte hain.  

**Example:**  
- Tum query karte ho: *"Celtics ke baare mein batao."*  
- Tumhare paas 10 documents aate hain, jo relevance ke basis pe sorted hain.  
- LLM (AI model) usually **start aur end walay documents pe zyada focus karta hai**, aur beech ke documents miss ho jate hain—even agar wo 
important hain.

---

### Solution: Reordering Documents  
Documents ko arrange karna:  
- Sabse relevant documents **start aur end pe rakho.**  
- Less relevant documents **middle mein daalo.**

---

### Kaise Implement Karna Hay?

#### 1. Documents Retrieve Karo  
Tum ek retriever use karte ho (e.g., vector store retriever) jo tumhare query ke liye sabse relevant documents leke aata hai.  

**Example Code:**
```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

# Embeddings aur text define karte hain
embeddings = OpenAIEmbeddings()
texts = ["Celtics are great", "Larry Bird is iconic", "Basketball is fun", ...]

# Retriever banate hain
retriever = InMemoryVectorStore.from_texts(texts, embedding=embeddings).as_retriever(search_kwargs={"k": 10})
docs = retriever.invoke("Tell me about Celtics")
```

Yahaan pe documents relevance ke hisaab se arrange hain:
1. Celtics are great  
2. Larry Bird is iconic  
3. Basketball is fun  
... **(sabse relevant pehle)**

---

#### 2. Documents Ko Reorder Karo  
**Reordering Algorithm:**  
- Sabse relevant documents start aur end pe chalay jate hain.  
- Beech mein kam relevant documents rakhte hain.  

**Example Code:**
```python
from langchain_community.document_transformers import LongContextReorder

# Reorder transformer lagao
reordering = LongContextReorder()
reordered_docs = reordering.transform_documents(docs)
```

Yeh process ke baad documents kuch is tarah honge:  
1. Celtics are great (start)  
2. Larry Bird is iconic (end)  
3. Less relevant documents (middle)  

---

#### 3. Reordered Documents Ka Use Karo  
Ab in reordered documents ko AI model ke context mein bhejo.  

**Example Code:**
```python
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Prompt aur chain define karte hain
llm = ChatOpenAI(model="gpt-4o-mini")
prompt_template = """
Given these texts:
-----
{context}
-----
Answer this question:
{query}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "query"])
chain = create_stuff_documents_chain(llm, prompt)

# Query ka response generate karo
response = chain.invoke({"context": reordered_docs, "query": "Tell me about Celtics"})
print(response)
```

---

### Fayda Kya Hay?
- **Important info ignore nahi hoti** kyun ke wo start aur end pe hoti hai.  
- **Model zyada accurate answer deta hai.**  
- Beech ke less relevant documents ko background mein dal dete hain.

<br/>

_____________

<br/>

### `InMemoryVectorStore` 
- ek class hai jo LangChain mein use hoti hai documents ko vector format mein store karne ke liye. Yeh vector store documents ko unke embeddings (numerical form) mein store karta hai, jise query ke sath compare karke relevant documents retrieve kiye jaate hain.

### Kaise kaam karta hai:
1. **Embeddings**: Sabse pehle, aap documents ko embeddings mein convert karte hain. Embedding ek tarah ka numerical representation hai jo document ki meaning ko capture karta hai.
  
2. **In-Memory Storage**: Yeh embeddings memory (RAM) mein store hoti hain. Iska matlab hai ki data fast retrieve kiya jaa sakta hai, lekin ismein ek limit hai kyunki yeh sirf RAM mein store hoti hai aur bohot large datasets ke liye suitable nahi hota.

3. **Search and Retrieval**: Jab aap query dete hain, us query ko bhi embedding mein convert kiya jaata hai. Phir yeh embedding vector store mein stored embeddings ke saath compare hoti hai aur sabse relevant documents ko retrieve kiya jaata hai.

### Example:
```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings

# Embedding model initialize karna
embeddings = OpenAIEmbeddings()

# Sample documents
texts = ["Celtics ne game jeeta.", "Basketball ek popular sport hai.", "Larry Bird ek legend hai."]

# Documents ko vectors ke roop mein store karna
vectorstore = InMemoryVectorStore.from_texts(texts, embedding=embeddings)

# Query dena
query = "Celtics ke baare mein batayein"
results = vectorstore.similarity_search(query, k=2)

# Results print karna
for doc in results:
    print(doc.page_content)
```

### Fayde:
- **Fast Retrieval**: Yeh RAM mein data store karta hai, isliye retrieval bahut fast hota hai.
- **Simple Use**: LangChain ka system use karna kaafi asaan hai aur aap directly embeddings aur queries ko handle kar sakte hain.

### Limitation:
- **Scalability**: Bahut zyada data handle nahi kar sakta, kyunki yeh sirf RAM mein store hota hai.
- **Volatility**: Agar app band ho jaye, to data bhi chala jata hai kyunki yeh memory mein hota hai, disk par nahi.

Agar aap small-scale ya prototype projects pe kaam kar rahe ho to yeh kaafi useful hai, lekin agar aapko bohot zyada data handle karna ho, to aapko persistent vector stores ki taraf dekhna padega, jaise FAISS ya Pinecone.


<br/>

______

<br/>

### `LongContextReorder` 
- ek transformer hai jo documents ko reorder karta hai taake zyada relevant documents pehle aur aakhri mein aayein, aur kam relevant documents beech mein hoon. Iska faida yeh hota hai ke jab aap long context (multiple documents) de rahe hote hain ek language model ko, toh model ko important information zyada aasani se milti hai, aur wo middle wale documents ko miss nahi karta.

### Yeh kaise kaam karta hai:

1. **Documents ka list**: Aapke paas pehle se ek documents ka list hota hai jo kisi search ya retrieval se aata hai.
2. **Reordering**: `LongContextReorder()` ek transformer hai jo yeh documents reorder karta hai. Yeh aise karta hai ke zyada relevant documents pehle aur aakhri mein hote hain, aur kam relevant documents beech mein hote hain.
3. **Result**: Is reordering ke baad, model ko zyada important information pehle aur aakhri mein milti hai, jisse wo zyada efficiently response de sakta hai.

### Code ka explanation:

```python
from langchain_community.document_transformers import LongContextReorder

# Reordering transformer ko use kar rahe hain
reordering = LongContextReorder()

# Documents ko reorder karna
reordered_docs = reordering.transform_documents(docs)
```

- **Step 1**: `LongContextReorder` ko import karte hain.
- **Step 2**: `LongContextReorder()` ko ek object banate hain, jo documents ko reorder karega.
- **Step 3**: `transform_documents(docs)` function ko call karte hain jo documents ko reorder karta hai.

### Example:

Maan lo aapke paas kuch documents hain:

1. "The Celtics are my favourite team."
2. "This is a document about the Boston Celtics."
3. "The Boston Celtics won the game by 20 points."
4. "L. Kornet is one of the best Celtics players."

Aur agar aap `LongContextReorder` apply karte hain, toh yeh reorder kar ke unhe is tarah dikhayega:

1. "This is a document about the Boston Celtics."
2. "L. Kornet is one of the best Celtics players."
3. "The Boston Celtics won the game by 20 points."
4. "The Celtics are my favourite team."

Yeh tarika iss liye use hota hai ke model ko relevant documents pehle aur aakhri mein milen, jisse model ko unpe focus karna asaan ho jata hai.

<br/>

_______________

<br/>


### `LongContextReorder` 
LangChain ka ek transformer tool hai jo retrieval-augmented generation (RAG) workflows ke liye document context ko optimize karne ke liye design kiya gaya hai. Ye tool ek unique issue ko solve karta hai jisse "Lost in the Middle" effect kehte hain. Ye issue tab hota hai jab long context window mein LLMs beech wale documents ko ignore karte hain, jo overall performance ko girata hai.

### `LongContextReorder` ka kaam:
1. **Reordering Documents**: Ye retrieved documents ko aise reorder karta hai ki most relevant documents context ke start aur end mein ho jayein, aur least relevant documents ko context ke middle mein daal diya jaye.
2. **Issue Mitigation**: Ye ordering strategy ensure karti hai ki important documents LLM ke focus mein rahein, kyunki models top aur bottom mein zyada dhyan dete hain.

### Key Features aur Parameters:
1. **Method: `transform_documents`**  
   - Is method ko use karke aap ek list of documents ko reorder karte ho.  
   - Input: Retrieved documents.  
   - Output: Reordered documents.

2. **Integration with Retrievers**:  
   - Aap pehle documents ko retriever ke `get_relevant_documents()` method se retrieve karte ho.  
   - Fir `LongContextReorder` ko apply karke reorder karte ho.

3. **Use Case**:  
   - Agar aapke RAG pipeline mein retrieved documents ka number 10+ ho, to ye transformer relevant documents ke order ko optimize karta hai, jisse response generation mein improvement hoti hai.

### Code Example:
```python
from langchain_community.document_transformers import LongContextReorder

# Reordering documents
reordering = LongContextReorder()
reordered_docs = reordering.transform_documents(docs)
```

### Practical Benefits:
- LLM responses ki accuracy improve hoti hai jab relevant information zyada accessible position par hoti hai (top ya bottom).
- Ye approach specially helpful hai agar aap multiple documents ko ek saath process kar rahe ho.

Agar aapke paas bahut saare documents hain aur aap unka relevance optimize karna chahte ho, to `LongContextReorder` ka use zaroori ho sakta hai. Detailed insights ke liye aap [ClusteredBytes](https://clusteredbytes.pages.dev/posts/2023/lost-in-the-middle-langchain/) aur [Hashnode Blog](https://juancolamendy.hashnode.dev/lost-in-the-middle-a-deep-dive-into-rag-and-langchains-solution) par padh sakte hain.


Is code mein `LongContextReorder` transformer ka kaam hai documents ko reorder karna, lekin iske `transform_documents` method ka parameter ek "list of documents" expect karta hai, **retriever nahi**.

### Correct Process:
1. **Retriever** se documents ko retrieve karo.
   ```python
   docs = retriever.get_relevant_documents("your query here")
   ```
   Is step mein retriever query ke basis par documents laata hai.

2. **LongContextReorder** transformer ka use karke retrieved documents ko reorder karo.
   ```python
   reordering = LongContextReorder()
   reordered_docs = reordering.transform_documents(docs)
   ```

### Key Points:
- **Retriever directly transformer ke parameter mein nahi dena hota**. 
   - Aapko retriever se pehle documents retrieve karne hote hain.
   - Retrieve hone ke baad woh documents transformer ke input mein diye jaate hain.

- **Code Adjustment:**
   ```python
   # Retrieve documents using retriever
   docs = retriever.get_relevant_documents("What is Kabuli Pulao?")

   # Reorder the retrieved documents
   reordering = LongContextReorder()
   reordered_docs = reordering.transform_documents(docs)
   ```

### Error Avoidance:
Agar aap retriever ko direct transformer mein pass karenge:
```python
reordering = LongContextReorder()
reordered_docs = reordering.transform_documents(retriever)
```
Toh error aayega, kyunki transformer `retriever` object ko samajhne ke liye nahi banaya gaya hai. Ye sirf documents (list format mein) process karta hai.

In short, pehle retriever ka output lena zaroori hai, fir transformer us output ko reorder karega.

<br/>

________


<br/>


### `create_stuff_documents_chain` 
- ek function hai jo LangChain library mein use hota hai. Iska kaam yeh hai ke yeh ek aise chain banata hai jisme aap documents aur questions ko combine kar sakte ho, taake ek language model (jaise GPT) uss context ke saath question ka jawab de sake.

### Simple Roman Urdu mein samjhaya gaya:

1. **`llm` (Language Model)**:
   - Yeh wo AI model hai jo aapke input ko process karega. Aap yahan OpenAI ka model use kar rahe ho, jaise `gpt-4o-mini`.

2. **`prompt`**:
   - Yeh ek template hai jo aap define karte ho. Isme aap `{context}` aur `{query}` jese placeholders daalte ho. `{context}` wo documents hain jo aap model ko dena chahte ho, aur `{query}` wo sawal hai jo aap puchna chahte ho.

3. **Chain ka kaam**:
   - Jab aap `create_stuff_documents_chain` function ko call karte ho, yeh documents aur query ko ek chain mein combine karta hai. Uske baad, jab aap chain ko invoke karte ho, toh model ko woh context aur query di jaati hai, aur model uss input ke basis pe jawab deta hai.

### Example:
Agar aapke paas kuch documents hain jo "Celtics" ke baare mein hain, aur aapka query hai "Celtics ke baare mein batao", toh chain:
1. Documents aur query ko ek format mein arrange karega.
2. Yeh input model ko dega.
3. Model uss input ke basis pe jawab dega.

### Code ka breakdown:
```python
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Language model define karte hain
llm = ChatOpenAI(model="gpt-4o-mini")

# Prompt template define karte hain
prompt_template = """
Given these texts:
-----
{context}
-----
Answer this question:
{query}
"""

# Prompt object create karte hain
prompt = PromptTemplate(template=prompt_template, input_variables=["context", "query"])

# Chain banate hain model aur prompt ko pass karke
chain = create_stuff_documents_chain(llm, prompt)

# Query ke response ko generate karte hain
response = chain.invoke({"context": reordered_docs, "query": "Celtics ke baare mein batao"})
print(response)
```

### Summary:
- Yeh function ek system banata hai jisme aap multiple documents ko combine kar ke ek query ke saath model ko de sakte ho.
- Model documents aur query ko dekh kar relevant jawab generate karega.


<br/>

___________________

<br/>

### **multiple vectors per document**
**MultiVectorRetriever** ka kaam yeh hota hai ke **ek document ke multiple aspects (yaani document ke mukhtalif pehlu, features, ya points) ko retrieve karne ka tareeqa simplify** karna. Yeh tab kaam aata hai jab aapka data bohot bara ho aur queries specific chhoti information ya context ko target kar rahi ho.

---

### **Yeh kis liye use hota hai?**
1. **Bari documents se relevant parts dhoondhna**: Agar ek document bohot bara hai (jaise ek contract ya research paper), to aap iska relevant part retrieve kar ke full document ke saath return karte ho.
   
2. **User query aur document match karna**: Yeh method queries ko chhoti embeddings (mathematical vectors) ke zariye match karta hai, jisse query ka result accurately retrieve hota hai.

3. **Document ke different angles samajhna**:
   - Ek document ke chhoti chunks ko alag alag treat karke retrieval aur zyada relevant banaya jata hai.
   - Summaries aur hypothetical questions ka use karke **user-specific searches** ko enhance kiya jata hai.

---

### **Isko banane ke tareeqe:**
1. **Smaller Chunks (ParentDocumentRetriever):** Document ko chhoti chhoti parts (chunks) mein tod kar unko embeddings banayi jati hain. Agar user koi specific query kare, to woh relevant chunk milta hai aur pura document bhi return hota hai.

2. **Summary:** Har document ki ek concise summary banayi jati hai, jo queries ke saath match hoti hai. Yeh especially tab kaam aata hai jab document ka bara context summarize karna ho.

3. **Hypothetical Questions:** LLM ke zariye document ke relevant questions generate kiye jate hain. Yeh questions queries ke liye ek structured aur controlled retrieval ka tareeqa dete hain.

4. **Manual Additions:** Agar aap manually kuch specific queries associate karna chahte ho, to woh bhi add ki ja sakti hain.

---

### **Example:**
**Ek Library Application:**
- Maan lo ek library ki bohot sari books indexed hain.
- Ek user "Arbitration Clause in Contract" search karta hai.
- MultiVectorRetriever pehle **book ke chhote parts** (chunks) ko scan karega.
- Phir uske full document ko retrieve karega jo relevant ho.


<br/>

-----

<br/>

### **ParentDocumentRetriever** :

### **Scenario:**

Maan lo tumhare paas bohot saare lambi essays hain aur tumhein un essays ke andar se specific information chahiye. Agar tum directly un essays ko use karte ho, to ye kaafi mushkil ho sakta hai, kyunki:

1. **Large Documents:** Agar document bohot lamba ho, to uski embedding (mathematical representation jo AI use karta hai) kaafi complex ho sakti hai. Isse document ka asli meaning loss ho sakta hai.
2. **Small Chunks:** Agar tum documents ko bohot chhote parts me tod dete ho (taake embeddings accurately represent ho sakein), to context ka loss ho sakta hai, matlab tumhein full information nahi milegi.

### **ParentDocumentRetriever ka Kaam:**
ParentDocumentRetriever ka solution yeh hai ki yeh pehle documents ko chhote chunks me todta hai (jisse embeddings better ho sakti hain) aur jab koi query ki jaati hai, to pehle chhote chunks ko retrieve karta hai. Phir, us chunk ke parent document (ya original document) ko retrieve karta hai taake tumhein poora context mil sake.

Jab **ParentDocumentRetriever** chhote chunks aur unke parent documents ko retrieve karta hai, to yeh **compare nahi karta** dono ko directly. Iska main purpose **context restore karna** hai. 

### Process Explanation:

1. **Chhote Chunks Retrieval:**
   Jab query hoti hai, pehle retriever **chhote chunks** ko retrieve karta hai, jisme query ka relevant part hota hai. In chunks ko vectorstore mein embeddings ke through search karke retrieve kiya jata hai.

2. **Parent Document Retrieval:**
   Chhote chunks ke liye, retriever unke **parent document ko retrieve karta hai**. Yeh parent document wo original document ho sakta hai jisme woh chunk tha. Isse poora context milta hai.

3. **No Direct Comparison:**
   Yeh dono — **chunk** aur **parent document** — ko **compare nahi kiya jata**. Instead, parent document ko use kiya jata hai taake **full context** mil sake. Agar parent document ko retrieve karne ke baad query ka relevant context milta hai, to user ko woh poora document provide kiya jata hai.

### Example:

Maan lo aap ne query ki "Justice Breyer". ParentDocumentRetriever:

- Pehle **chhote chunk** ko retrieve karega, jaise ek chhota hissa "Justice Stephen Breyer—an Army veteran".
- Fir, wo **parent document** ko retrieve karega, jisme yeh chunk tha. Parent document mein poora context aur aur relevant details milengi.

To **chunk aur parent document** ko compare karke kisi cheez ka decision nahi liya jata. Rather, **parent document** use hota hai taake **poora context** diya ja sake.


Child chunks ke saath-saath **parent chunks** bhi iss retriever mein stored hain, lekin unka role alag hota hai. Aaye samajhte hain ke **parent chunks** kaise store aur retrieve hote hain:

---

1. **InMemoryStore:**
   - Parent chunks ko `InMemoryStore` mein store kiya jata hai.
   - Jab parent documents ko `add_documents()` function se add karte hain, to har parent chunk ka metadata aur content `store` mein save hota hai.

2. **Parent-Child Mapping:**
   - Jab child chunks vectorstore mein save hote hain, to har child chunk ke saath **parent chunk ka reference** hota hai.
   - Query ke waqt relevant child chunks retrieve hote hain, aur unke reference se corresponding parent chunks memory (`InMemoryStore`) se fetch hote hain.

3. **Parent Retrieval Ka Process:**
   - Jab query process hoti hai, to child chunks ko match karne ke baad, unke corresponding parent chunks ko retrieve kiya jata hai.
   - `ParentDocumentRetriever` ka kaam hi yeh ensure karna hai ke aapko **contextual parent document** mile, na ke sirf chhote chunks.

---

### Verification:
Parent chunks ka count check karne ke liye:
```python
len(list(store.yield_keys()))
```
Agar ye count > 0 hai, to iska matlab parent chunks memory mein successfully stored hain.

---

### Summary in Roman Urdu:
- **Parent chunks** `InMemoryStore` mein store hote hain.
- Har child chunk ka parent ke saath link hota hai.
- Jab query hoti hai, to relevant child chunks retrieve hote hain aur unke saath associated parent chunk ko memory se fetch kiya jata hai. Is tarah context lose nahi hota.

### **Code Breakdown:**

1. **Documents Load Karna:**
   Tumhare paas raw text files hain, jise tum load karte ho using `TextLoader`:
   ```python
   loaders = [
       TextLoader("paul_graham_essay.txt"),
       TextLoader("state_of_the_union.txt"),
   ]
   docs = []
   for loader in loaders:
       docs.extend(loader.load())
   ```

2. **Text Splitter:**
   Text ko chhote chunks me todne ke liye tum `RecursiveCharacterTextSplitter` ka use karte ho:
   ```python
   child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
   ```
   Yani, har chunk ki maximum size 400 characters hogi.

3. **Vectorstore (Chroma):**
   Chhote chunks ko store karne ke liye tum **Chroma** vectorstore ka use karte ho, jo embeddings ko store karta hai:
   ```python
   vectorstore = Chroma(
       collection_name="full_documents", embedding_function=OpenAIEmbeddings()
   )
   ```

4. **Parent Document Storage (InMemoryStore):**
   Parent documents ko store karne ke liye `InMemoryStore` ka use hota hai:
   ```python
   store = InMemoryStore()
   ```

5. **ParentDocumentRetriever:**
   Ab, tum `ParentDocumentRetriever` ko initialize karte ho. Yeh retriever chhote chunks ko store karta hai, lekin query par wo parent document ko fetch karega, jisme wo chunk asal me tha:
   ```python
   retriever = ParentDocumentRetriever(
       vectorstore=vectorstore,
       docstore=store,
       child_splitter=child_splitter,
   )
   ```

### **Query Process:**

1. **Chhote Chunks Se Search:**
   Jab tum search karte ho, to pehle yeh small chunks ko retrieve karta hai. Maan lo tumne query ki "justice breyer" par:
   ```python
   sub_docs = vectorstore.similarity_search("justice breyer")
   ```

   Output kuch is tarah ka ho sakta hai (small chunk ka content):
   ```text
   Tonight, I’d like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court.
   ```

2. **Parent Document Ko Retrieve Karna:**
   Jab tum `ParentDocumentRetriever` se query karte ho, to yeh pehle small chunks ko fetch karta hai aur phir un chunks ke parent document ko dhundta hai:
   ```python
   retrieved_docs = retriever.invoke("justice breyer")
   ```
   Yahan pe tumhe poora document milega, jisme wo chunk included ho.

   **Example output:**
   ```text
   (38540 characters of full document)
   ```

### **Fayda:**
1. **Accurate Embeddings:** Chhote chunks se tumko accurate embeddings milti hain jo document ke meaning ko achhe se capture karti hain.
2. **Context ka Loss Nahi:** Parent document retrieval ke through tumhe poora context milta hai, even agar tumne document ko chhote parts me tod diya ho.

### **Summing Up:**
- **Small chunks** ensure better embeddings (meaning ko accurately capture karte hain).
- **ParentDocumentRetriever** ensure karta hai ke tumko poora context mile, even agar tumne document ko chhote chunks me tod diya ho. 

Is tarah se tumhare paas dono ka fayda hota hai: **accurate embeddings** aur **complete context**.

<br/>

----

<br/>

### Step 1: **Documents Ko Load Karna**
Aapko sabse pehle apne documents ko load karna padta hai, jise aap `TextLoader` ka use karke karte ho. Jaise aapne `paul_graham_essay.txt` aur `state_of_the_union.txt` ko load kiya tha:

```python
loaders = [
    TextLoader("paul_graham_essay.txt"),
    TextLoader("state_of_the_union.txt"),
]
docs = []
for loader in loaders:
    docs.extend(loader.load())
```

Yahaan pe `docs` mein aapke raw text files ka content store ho jata hai.

### Step 2: **Text ko Chhote Chunks Mein Tohna**
Ab, aapko apne documents ko **chhote chunks mein todna** padta hai. Yeh kaam `RecursiveCharacterTextSplitter` karta hai. Isse aapke documents ko small parts (chunks) mein tod diya jata hai taake unke embeddings (AI ke liye mathematical representation) accurately create ho sakein.

```python
child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
```

Aap har chunk ko 400 characters ka rakhte ho.

### Step 3: **Vectorstore Mein Documents Ko Add Karna**
Ab jab chunks ready ho gaye hain, aap unko **Chroma vectorstore** mein add karte ho. Yeh vectorstore AI ko embeddings store karne mein help karta hai, taake search queries ke liye fast results mil sakein.

```python
vectorstore = Chroma(
    collection_name="full_documents", embedding_function=OpenAIEmbeddings()
)
```

### Step 4: **ParentDocumentRetriever Ko Initialize Karna**
Aap `ParentDocumentRetriever` ko initialize karte ho, jisme `vectorstore` aur `docstore` ko link kiya jata hai. Yahan `docstore` mein aap parent documents ko store kar rahe ho.

```python
store = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
)
```

### Step 5: **Documents Ko Retriever Mein Add Karna**
Ab aap documents ko **retriever** mein add karte ho:

```python
retriever.add_documents(docs, ids=None)
```

Yeh step zaroori hai, kyunki jab tak aap documents ko retriever mein add nahi karte, query ka response nahi milega.

### Step 6: **Query Karna (Retrieval)**
Ab jab aap query karte ho, jaise "justice breyer", retriever pehle small chunks ko search karta hai aur phir un chunks ke **parent document** ko retrieve kar leta hai.

```python
retrieved_docs = retriever.invoke("justice breyer")
```

**Kahaan se data aata hai?**
- Jab aap query karte ho, retriever pehle small chunks ko vectorstore se search karta hai (jisme embeddings stored hote hain).
- Phir, wo chunk ke parent document ko fetch karta hai, jisme wo chunk originally tha.
  
### Key Points:
1. **Documents ko load karke unhe vectorstore mein add karte hain**.
2. **Chhote chunks ko retrieve karke unke parent document ko fetch karte hain**.
3. Agar aap documents ko pehle retriever mein add nahi karte, to query ka response nahi milega.

Is tarah se **retriever** query ko handle karta hai aur documents ko properly retrieve karta hai.


<br/>

------

<br/>


### **Self-querying retrieval** 
- ka concept yeh hai ke jab tum kisi system ko query dete ho, to woh query ko samajh kar **structured form** me todta hai aur phir apni stored information se exact aur relevant jawab nikalta hai. Matlab yeh system khud hi apne query ko analyze kar ke aur samajh kar kaam karta hai.

### **Step by Step:**
1. **Query Input:**
   - Tum ek plain Urdu ya English me query likhte ho, jaise:
     - "Wo articles dikhayo jo 2020 ke baad likhe gaye aur machine learning par hain."
   
2. **LLM Query Samajhta Hai:**
   - System (AI language model) tumhari query ko analyze karta hai.
   - Us query me keywords aur filters nikalta hai, jaise:
     - `date > 2020`
     - `topic = machine learning`

3. **Semantic Search Aur Filters:**
   - System apne database (jo information ka store hai) me search karta hai. Yeh search 2 cheezon par based hoti hai:
     - Semantic similarity (query ka overall meaning).
     - Filters (metadata ke hisaab se query ke rules).

4. **Relevant Results:**
   - System woh results nikalta hai jo tumhari query ke bilkul close hotay hain, jaise wo machine learning ke 2020 ke baad ke articles.

### **Example:**
Maan lo tumhare paas ek database hai books ka, aur har book ke sath yeh details hain:
   - **Metadata:** Author, Genre, Year, Pages.
   - Query: *"2022 me published hui fiction novels batao."*
   - Structured Query: 
     - `Genre = Fiction`
     - `Year = 2022`

System yeh details ko filter karke tumhare liye sirf relevant fiction novels show karega.

### **Key Point:**
- Yeh retriever **natural language** (simple human language) ko **structured query** me convert karta hai.
- Uske baad apne **database** me search karke **precise aur filtered jawab** deta hai.

Agar tum samajhne ke liye code example ya practical implementation chahte ho, batao, main aur detail se samjha doonga.