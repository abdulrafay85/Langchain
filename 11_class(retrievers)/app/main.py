## Import necessary modules
## Modules for document compressors, retrievers, and language model integration
from langchain.retrievers.document_compressors import (
    LLMChainFilter, LLMListwiseRerank, LLMChainExtractor, EmbeddingsFilter, DocumentCompressorPipeline
)
import uuid
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.storage import InMemoryByteStore, InMemoryStore
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_transformers import EmbeddingsRedundantFilter, LongContextReorder
from langchain.retrievers import ContextualCompressionRetriever, ParentDocumentRetriever
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers.multi_query import MultiQueryRetriever
from dotenv import load_dotenv
import os

## -------------

## Utility function for printing documents in a readable format
def pretty_print_docs(docs):
    """
    Pretty-print documents for better readability.
    :param docs: List of documents to print
    """
    print(
        f"\n{'-' * 100}\n".join(
            [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
        )
    )

## -------------

## Load environment variables (e.g., API keys) from a .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")  ## Get GEMINI_API_KEY from .env
os.environ["GEMINI_API_KEY"] = gemini_api_key  ## Set globally for the application

## -------------

## Step 1: Initialize the Language Model (LLM)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  ## Model version
    api_key=gemini_api_key,    ## API key for authentication
    temperature=0.2            ## Control response randomness
)

## -------------

## Step 2: Setup Document Compressors
## Compressor that extracts relevant parts of documents
compressor = LLMChainExtractor.from_llm(llm)

## -------------

## Filter-based compressor to keep only specific parts of documents
chain_filter = LLMChainFilter.from_llm(llm)

## -------------

## Reranker to reorder documents based on relevance
listwise_rerank = LLMListwiseRerank.from_llm(llm, top_n=2)

## -------------

## Step 3: Setup Embeddings Model for Similarity Matching
embeddings_model = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004"  ## Embedding model version
)

## -------------

embeddings_filter = EmbeddingsFilter(embeddings=embeddings_model, similarity_threshold=0.5)
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings_model)

## -------------

## Step 4: Load Documents and Split into Chunks
## Load documents from a text file
text_loader = TextLoader("../files/paul_graham_essay.txt")
raw_documents = text_loader.load()

## -------------

## Load additional documents from a PDF
pdf_loader = PyPDFLoader("../files/cocking.pdf")
raw_documents += pdf_loader.load()  ## Combine text and PDF documents

## -------------

## Split documents into smaller chunks for processing
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        ## Maximum chunk size
    chunk_overlap=20,       ## Overlap between chunks
    separators=["\n", "\n\n"]  ## Define split points
)
docs = splitter.split_documents(raw_documents)

## -------------

## Step 5: Create a Vectorstore for Document Retrieval
# Store document embeddings for retrieval
vectorstore = FAISS.from_documents(docs, embeddings_model)

## -------------

## Setup a retriever for vectorstore
retriever = vectorstore.as_retriever()

## -------------

## Retrieve documents using Maximal Marginal Relevance (MMR)
# vector_retriever = vectorstore.as_retriever(search_type="mmr")
# docs = vector_retriever.invoke("Overview of the Five Principles of Prompting?")
# # print(docs)

## -------------

## Setup retriever with similarity score threshold
# retriever = vectorstore.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={"score_threshold": 0.3, "top_k": 1}
# )

## -------------

## Step 6: Multi-Query Retrieval
## Allow multiple interpretations of queries using LLM
# multi_query_retriever = MultiQueryRetriever.from_llm(
#     retriever=retriever, llm=llm
# )
# unique_docs = multi_query_retriever.invoke("Who was the captain in this series?")
# print(unique_docs)

## -------------

# Step 7: Contextual Compression Retrieval
# Example 1: Using LLMChainExtractor as a compressor
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
) ## Step 1: Initialize the Language Model (LLM)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  ## Model version
    api_key=gemini_api_key,    ## API key for authentication
    temperature=0.2            ## Control response randomness
)

## Step 2: Setup Document Compressors
## Compressor that extracts relevant parts of documents
compressor = LLMChainExtractor.from_llm(llm)

## Step 3: Setup Embeddings Model for Similarity Matching
embeddings_model = GoogleGenerativeAIEmbeddings(
    google_api_key=gemini_api_key,
    model="models/text-embedding-004"  ## Embedding model version
)

## Step 4: Load Documents and Split into Chunks
## Load documents from a text file
text_loader = TextLoader("../files/paul_graham_essay.txt")
raw_documents = text_loader.load()

## Step 5: Create a Vectorstore for Document Retrieval
## Store document embeddings for retrieval
# vectorstore = FAISS.from_documents(docs, embeddings_model)

## Step 6: Multi-Query Retrieval
## Allow multiple interpretations of queries using LLM
# multi_query_retriever = MultiQueryRetriever.from_llm(
#     retriever=retriever, llm=llm
# )

## Step 7: Contextual Compression Retrieval
## Example 1: Using LLMChainExtractor as a compressor
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

compressed_docs = compression_retriever.invoke("how to cooked a Kabuli Pulao?")
pretty_print_docs(compressed_docs)


## Step 8: Reorder and Generate Final Response
## Reorder documents to optimize context
# reordering = LongContextReorder()
# reordered_docs = reordering.transform_documents(compressed_docs)

## Define a prompt template for question answering
# prompt_template = """
# Given these texts:
# -----
# {context}
# -----
# Answer this question:
# {query}
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=["context", "query"])

# ## Combine documents using LLM and the defined prompt
# chain = create_stuff_documents_chain(llm, prompt)

# ## Generate a response for a query using the reordered documents
# response = chain.invoke({"context": reordered prompt:\t"})
# compressed_docs = compression_retriever.invoke(user_prompt)
# pretty_print_docs(compressed_docs)

## -------------

## Example 2: Using LLMChainFilter as a compressor
# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=chain_filter,
#     base_retriever=retriever
# )
# compressed_docs = compression_retriever.invoke("how to cooked a Kabuli Pulao?")
# pretty_print_docs(compressed_docs)

## -------------

## Example 3: Using LLMListwiseRerank as a compressor
# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=listwise_rerank,
#     base_retriever=retriever
# )
# compressed_docs = compression_retriever.invoke("how to cooked a Takka Takk?")
# pretty_print_docs(compressed_docs)

## -------------

## Example 4: Using EmbeddingsFilter as a compressor
# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=embeddings_filter,
#     base_retriever=retriever
# )
# compressed_docs = compression_retriever.invoke("how to cooked a Kabuli Pulao?")
# pretty_print_docs(compressed_docs)

## -------------

## Example 5: Using a Pipeline Compressor
# pipeline_compressor = DocumentCompressorPipeline(
#     transformers=[splitter, redundant_filter, embeddings_filter]
# )

# compression_retriever = ContextualCompressionRetriever(
#     base_compressor=pipeline_compressor,
#     base_retriever=retriever
# )

# compressed_docs = compression_retriever.invoke(
#     "how to cooked a Daal Ghosht"
# )

# prompt_template = """
# Given these texts:
# -----
# {context}
# -----
# Answer this question:
# {query}
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=["context", "query"])

# ## Combine documents using LLM and the defined prompt
# chain = create_stuff_documents_chain(llm, prompt)

# ## Generate a response for a query using the reordered documents
# response = chain.invoke({"context": compressed_docs, "query": "translate it into Roman Urdu"})

# ## Display the final response
# pretty_print_docs(response)

## -------------

## Step 8: Reorder and Generate Final Response
## Reorder documents to optimize context
# reordering = LongContextReorder()
# reordered_docs = reordering.transform_documents("""compressed_docs""")

# ## Define a prompt template for question answering
# prompt_template = """
# Given these texts:
# -----
# {context}
# -----
# Answer this question:
# {query}
# """
# prompt = PromptTemplate(template=prompt_template, input_variables=["context", "query"])

# ## Combine documents using LLM and the defined prompt
# chain = create_stuff_documents_chain(llm, prompt)

# ## Generate a response for a query using the reordered documents
# response = chain.invoke({"context": reordered_docs, "query": "how to cooked a Kabuli Pulao?"})

# ## Display the final response
# pretty_print_docs(response)

## -------------

## Multiple vectors per document

# # The storage layer for the parent documents
# store = InMemoryByteStore()
# id_key = "doc_id"

# # The retriever (empty to start)
# multi_vector_retriever = MultiVectorRetriever(
#     vectorstore=vectorstore,
#     byte_store=store,
#     id_key=id_key,
# )

# doc_ids = [str(uuid.uuid4()) for _ in docs]
# # print(doc_ids)

# # The splitter to use to create smaller chunks
# child_text_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

# sub_docs = []
# for i, doc in enumerate(docs):
#     _id = doc_ids[i]
#     _sub_docs = child_text_splitter.split_documents([doc])
#     for _doc in _sub_docs:
#         _doc.metadata[id_key] = _id
#     sub_docs.extend(_sub_docs)


# retriever.vectorstore.add_documents(sub_docs)

# retriever.docstore.mset(list(zip(doc_ids, docs)))

# retriever.vectorstore.similarity_search("justice breyer")[0]

## -------------

# Parent Document Retriever

documents = []

# Load the documents using TextLoader
loaders = [
    TextLoader("../files/paul_graham_essay.txt"),
    TextLoader("../files/state_of_the_union.txt"),
]

parent_docs = []
for loader in loaders:
    parent_docs.extend(loader.load())
# pretty_print_docs(docs)

## -------------

# This text splitter is used to create the child documents
# child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)

## -------------

# Stores
# store = InMemoryStore()

# vectorstore = Chroma(embedding_function=embeddings_model, collection_name="fullDoc", persist_directory="./JohnWick_db_parentsRD")

## -------------

# # Initialize the ParentDocumentRetriever
# parent_document_retriever = ParentDocumentRetriever(
#     vectorstore=vectorstore,
#     docstore=store,
#     child_splitter=child_splitter,
# )
# parent_document_retriever.add_documents(parent_docs, ids=None)

# print(f"Number of parent chunks  is: {len(list(store.yield_keys()))}")

# print(f"Number of child chunks is: {len(parent_document_retriever.vectorstore.get()['ids'])}")

# retrieved_docs = parent_document_retriever.invoke("who is irsham ali")
# pretty_print_docs(retrieved_docs)

## -------------

# Retrieving larger chunks

# # This text splitter is used to create the parent documents
# parent_splitter = RecursiveCharacterTextSplitter(chunk_size=2000)
# # This text splitter is used to create the child documents
# # It should create documents smaller than the parent
# child_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
# # The vectorstore to use to index the child chunks
# vectorstore = Chroma(embedding_function=embeddings_model, collection_name="fullDoc", persist_directory="./JohnWick_db_parentsRD")

# # The storage layer for the parent documents
# store = InMemoryStore()

# retriever = ParentDocumentRetriever(
#     vectorstore=vectorstore,
#     docstore=store,
#     child_splitter=child_splitter,
#     parent_splitter=parent_splitter,
# )

# retriever.add_documents(docs)
# retrieved_docs = retriever.invoke("who is ukasha ?")
# pretty_print_docs(retrieved_docs)
