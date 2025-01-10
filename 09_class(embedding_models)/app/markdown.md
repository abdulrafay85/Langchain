### **Embedding Models Kya Hote Hain?**

**Embedding Models** ka kaam ye hota hai ke woh kisi bhi text (jaise ek sentence ya ek paragraph) ko numbers ki ek **array** (jo ke **vector** kehlati hai) mein convert karte hain. Iska faida yeh hota hai ke yeh vector us text ka core meaning ko represent karta hai.

Misal ke taur par agar aap do alag texts lein, ek "apple" aur doosra "banana", toh in dono ka meaning food se related hai, isliye jab inka vector banaya jata hai, toh in dono vectors mein kuch similarities hoti hain. Yeh process **semantic meaning** ko capture karta hai, yaani text ka asal ma'ni samajhta hai.

### **Vector Kya Hota Hai?**

Aap vector ko ek **numbers ki list** samajh sakte hain. Jaise agar text ko ek tareeqe se samjha jaye, toh ek sentence ka vector kuch is tarah ka ho sakta hai:

`[0.12, 0.45, -0.76, 0.33, 0.91]`

Har number ka ek specific meaning hota hai, jo ke us text ke words ka ek aspect represent karta hai. In numbers ke zariye aap ye pata kar sakte hain ke text ka meaning kya hai aur woh doosre texts ke sath kitna milta hai.

### **Vector Ko Kyun Banate Hain?**

Vectors banane ka maqsad ye hota hai ke jab text ko is form mein convert kar lete hain, toh aap **mathematical operations** perform kar sakte hain. Misal ke taur par, agar aapko yeh check karna hai ke do texts meaning mein kitne milte julte hain, aap unke vectors ko compare kar sakte hain.

Iska faida yeh hota hai ke:
- **Similar Texts**: Aap easily similar texts ko dhoond sakte hain.
- **Context Retrieval**: Aap kisi query ke liye relevant information nikaal sakte hain.

### **LangChain Mein Embedding Models**

Ab **LangChain** ke framework mein jo `Embeddings` class hoti hai, woh text embedding models ke sath kaam karne ka ek **standard tareeqa** provide karti hai. Chahe aap **OpenAI** ka embedding model use kar rahe ho, ya **Cohere** ka, ya phir koi local model, aap LangChain ka ek hi interface use kar ke sab ke sath kaam kar sakte hain.

### **LangChain Embeddings Class Ke Functions**

LangChain mein jo `Embeddings` class hoti hai, usmein do main methods (functions) hote hain:

#### 1. **embed_documents**
Yeh method **documents** ya multiple texts ko embed karta hai. Iska matlab yeh hota hai ke aap ek se zyada texts le kar, unka vector (numbers ki list) banate hain.

#### 2. **embed_query**
Yeh method ek **query** ko embed karta hai. Query woh hoti hai jo aap search kar rahe hote hain, jaise ek sawal ya search phrase. Iska bhi vector banaya jata hai, jo aapke search ka ma'ni represent karta hai.

**Alag Method Kyun Hote Hain?**
Kuch embedding model providers documents aur queries ke liye alag embedding techniques use karte hain, isliye in do methods ka alag alag hona zaroori hai.

### **Example**

Misal ke taur par, agar aapko apne documents ke andar se koi specific information search karni hai, toh pehle aap documents ka vector banayenge, phir query ka vector banake un dono vectors ko compare karenge. Jo document ka vector query ke vector se zyada match karega, woh document relevant hoga.

Example code kuch is tarah se hoga:

```python
from langchain.embeddings import OpenAIEmbeddings

# Embeddings model ka use karna
embeddings = OpenAIEmbeddings()

# Multiple texts ko embed karna
docs_embedding = embeddings.embed_documents(["Yeh ek sample document hai.", "Yeh doosra document hai."])

# Query ko embed karna
query_embedding = embeddings.embed_query("Is document ka mazmoon kya hai?")
```

Is example mein `embed_documents` ko multiple texts embed karne ke liye use kiya gaya, aur `embed_query` ko ek specific search query ke liye.

### **Kya Kaam Karte Hain Embedding Models?**

1. **Search**: Agar aapko kisi text mein search karna ho, aap texts aur query ka vector banake unko compare karte hain.
2. **Similarity Check**: Agar aapko yeh check karna ho ke do alag texts meaning mein kitne similar hain, aap unke vectors ka comparison kar sakte hain.

### **Summarized Points:**
1. **Embedding Models** text ko numbers ki array (vector) mein convert karte hain jo us text ka ma'ni capture karti hai.
2. Yeh vectors ko compare karke aap relevant information retrieve kar sakte hain, ya similar texts dhoond sakte hain.
3. **LangChain** ek standard interface provide karta hai embedding models ke sath kaam karne ka.
4. Do main methods hote hain: `embed_documents` (documents ko embed karna) aur `embed_query` (query ko embed karna).
</br>
</br>
### **Caching in Embeddings**
**Caching** ka matlab hai temporary data ko store karna taake baar baar computation na karna pade. Jab hum embeddings (text ke vectors) ko **cache** karte hain, toh yeh humare computations ko faster banata hai. Matlab agar ek dafa aapne kisi text ka embedding bana liya, toh next time us text ka embedding direct cache se mil jayega, aur dobara se calculation karne ki zaroorat nahi hogi.

### **CacheBackedEmbeddings**
**CacheBackedEmbeddings** ek aisi cheez hai jo embeddings ko cache karta hai. Iska kaam yeh hota hai ke jab bhi hum kisi text ka embedding banate hain, woh cache mein save hota hai. Is cache ko hum key-value store ki tarah samajh sakte hain, jahan **text** ko hash karke uska embedding **key** banate hain, aur **value** uska vector hoti hai.

### **Kaise Initialize Karte Hain CacheBackedEmbeddings?**

`CacheBackedEmbeddings` ko hum **from_bytes_store** method se initialize karte hain, jisme kuch parameters hotay hain:

1. **underlying_embedder**: Yeh wo main embedder hota hai jo text ka embedding (vector) banata hai. Misal ke taur par OpenAI ka embedder.
2. **document_embedding_cache**: Yeh wo store hota hai jahan hum embeddings ko cache karte hain. Yeh koi bhi `ByteStore` ho sakta hai jo aapke document embeddings ko cache kar sake.
3. **batch_size**: Agar aap ek waqt me kai texts embed karte hain, to yeh bataata hai ke ek batch me kitne texts process karne hain.
4. **namespace**: Yeh ek unique naam hota hai jo aap cache ke sath use karte hain taake koi aur cache isko disturb na kare. Misal ke taur par agar aap different embedding models use karte hain, toh har model ke liye alag namespace set karte hain.

### **Important Cheez: Namespace Set Karna**
Namespace set karna zaroori hai taake agar aap ek hi text ko different embedding models ke sath use karte hain, toh cache ke andar clash na ho. Alag-alag namespace se yeh hoga ke har model ke liye different keys banengi.

### **Example of Caching with FAISS**
Ab hum dekhte hain ke **FAISS** vector store kaise use hota hai embeddings ko store aur retrieve karne ke liye.

1. **LocalFileStore**: Aap local system pe embeddings store karne ke liye `LocalFileStore` use karte hain.
2. **FAISS**: FAISS ek powerful library hai jo embeddings ko efficiently search karne ke liye use hoti hai.

#### **Code Example**:

1. **Dependencies Install karna:**
   Pehle hume kuch libraries install karni hoti hain, jisme FAISS aur LangChain included hote hain:
   ```bash
   %pip install --upgrade --quiet langchain-openai faiss-cpu
   ```

2. **Embedding Model Initialize karna:**
   Aap OpenAI ka embeddings model use karenge, aur embeddings ko store karne ke liye `LocalFileStore` banaenge.
   ```python
   from langchain.storage import LocalFileStore
   from langchain_openai import OpenAIEmbeddings

   underlying_embeddings = OpenAIEmbeddings()  # OpenAI ka embedding model
   store = LocalFileStore("./cache/")  # Local storage for caching
   cached_embedder = CacheBackedEmbeddings.from_bytes_store(
       underlying_embeddings, store, namespace=underlying_embeddings.model
   )
   ```

3. **Documents ko Embed Karna:**
   Document ko text chunks me split kar ke uska embedding banate hain:
   ```python
   raw_documents = TextLoader("state_of_the_union.txt").load()  # Document load karna
   text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
   documents = text_splitter.split_documents(raw_documents)

   db = FAISS.from_documents(documents, cached_embedder)  # FAISS me embeddings store karna
   ```

4. **Faster Search:**
   Ab kyunki cache enabled hai, agar dobara se vector store banaya jaye, toh woh kaafi fast hoga:
   ```python
   db2 = FAISS.from_documents(documents, cached_embedder)
   ```

### **Different ByteStore Use Karna**
Agar aap **persistent storage** (jisme data save rehta hai) ke bajaye **non-persistent storage** (jisme data temporary hota hai) use karna chahte hain, toh aap `InMemoryByteStore` use kar sakte hain. Isse embeddings sirf memory me store hote hain, aur jab aap system close karte hain, toh data erase ho jata hai.

```python
from langchain.storage import InMemoryByteStore

store = InMemoryByteStore()  # Non-persistent store
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)
```

### **Summary:**
1. **Caching** embeddings ka fayda yeh hota hai ke aapko dobara embeddings calculate nahi karne padte, jo time aur computational resources bachaata hai.
2. **CacheBackedEmbeddings** ek wrapper hota hai jo embeddings ko cache karne me help karta hai.
3. **LocalFileStore** ko use karke embeddings ko local system pe store kar sakte hain.
4. Aap alag-alag stores (persistent ya non-persistent) use kar sakte hain, jaise `InMemoryByteStore`.

Agar ab bhi koi confusion hai toh aap pooch sakte hain!