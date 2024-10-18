# Importing Dependencies
import os
import re
from dotenv import load_dotenv
api_key = os.environ["NVIDIA_API_KEY"] 
import logging
from wiki import data  # Ensure data is imported correctly from wiki.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_nvidia_ai_endpoints import ChatNVIDIA, NVIDIAEmbeddings
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import warnings
warnings.filterwarnings("ignore")


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Load environment variables
load_dotenv()
# Get the API key from environment variables
api_key = os.getenv("NVIDIA_API_KEY")

# Check if the API key is missing
if not api_key:
    # Log an error message if the API key is not found
    logging.error("API key not found. Please set NVIDIA_API_KEY in your environment.")
    # Exit the program with an error status
    exit(1)

# Initialize models
try:
    """
    Specifying models to use GPU by setting device="cuda"

    """
    instruct_llm = ChatNVIDIA(model_name="meta-llama/llama-3-8b-instruct", temperature=0, device="cuda")
    nv_embeddings = NVIDIAEmbeddings(model_name="nvidia/nv-embed-v2", truncate="END", device="cuda")
except Exception as e:
    logging.error(f"Failed to initialize models: {e}")
    exit(1)


# Function to preprocess and split data
def splitter(data):
    try:
        # Validate data
        if not isinstance(data, list):
            raise ValueError("Data must be a list.")
        if not all("paragraph" in item and "metadata" in item for item in data):
            raise ValueError("Each item in the list must contain 'paragraph' and 'metadata'.")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100,
            separators=["\n\n", "\n", ".", ";", ",", " "],
        )

        # Remove citation markers like [1], [2], etc.
        for item in data:
            item["paragraph"] = re.sub(r'\[\d+\]', '', item["paragraph"])

        # Storing the paragraph
        documents = [Document(page_content=item["paragraph"], metadata=item["metadata"]) for item in data]

        # Document Chunking
        data_chunks = text_splitter.split_documents(documents)
        return data_chunks

    except Exception as e:
        logging.error(f"Error in splitter function: {e}")
        return []

# Use the splitter function
data_chunks = splitter(data)
# print(data_chunks)


# Loading Data into Weaviate Vector Database
weaviate_client = weaviate.connect_to_local()

# Creating a Vector Database
vecdb = WeaviateVectorStore.from_documents(data_chunks, nv_embeddings, client=weaviate_client)

# Assigning the retriever
retriever = vecdb.as_retriever(search_type="mmr")

# Creating a chain
chain = RetrievalQAWithSourcesChain.from_chain_type(
    instruct_llm,
    chain_type="stuff", 
    retriever=retriever
)

# chain(
#     {"question": "What is rag?"},
#     return_only_outputs=True,
# )

# Template for instruct_llm model
template = """You are an AI assistant for question-answering tasks for the provided wikipedia URL.
Use the following pieces of retrieved context to answer the question. 
ONLY use information from the provided context. DO NOT use any outside knowledge.
If you don't know the answer, just say "Hmm, I'm not sure." Don't try to make up an answer.
If the question is not about the provided context, politely inform them that you are tuned to only answer questions about provided wikipedia URL.
Do NOT infer any answers not directly available in the provided context. 

Question: {question}
Context: {context}
Answer:
"""
prompt = ChatPromptTemplate.from_template(template)

# print(prompt)

# Creating a RunnablePassthrough
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | instruct_llm
    | StrOutputParser()
)

# answer = rag_chain.invoke("What did you mean by RAG?")

# print(answer)