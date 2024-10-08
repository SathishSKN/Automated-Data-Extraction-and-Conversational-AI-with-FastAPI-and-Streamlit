# Importing Dependencies
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from dotenv import load_dotenv                      # NVIDIA_API_KEY stored in a .env file
from wiki import extract_wikipedia_data
from vecdb import instruct_llm, nv_embeddings, splitter
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()
api_key = os.getenv("NVIDIA_API_KEY")               # Importing the NVIDIA_API_KEY

if not api_key:
    logging.error("API key not found. Please set NVIDIA_API_KEY in your environment.")
    exit(1)

# Initialize FastAPI app
app = FastAPI()

# Initialize Weaviate client and VectorStorecls
try:
    """
    Ensure you are running the weaviate server in your docker

    """
    # Connecting to the local weaviate server 
    weaviate_client = weaviate.connect_to_local()
    # Creating a Weaviate Vecto Database
    vecdb = WeaviateVectorStore.from_documents([], nv_embeddings, client=weaviate_client)
except Exception as e:
    logging.error(f"Failed to connect to Weaviate: {e}")
    exit(1)

# Request Classes
class URLRequest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    question: str

# Endpoint to welcome users
@app.get("/")
async def welcome():
    return {"message": "Welcome to Wikipedia Q&A RAG"}


# Endpoint to load data
@app.post("/load")
async def load_data(request: URLRequest):
    url = request.url
    if not url.startswith("https://en.wikipedia.org/"):
        raise HTTPException(status_code=400, detail="Only Wikipedia URLs are supported.")
    
    data = extract_wikipedia_data(url)
    if data is None:
        raise HTTPException(status_code=400, detail="Failed to extract data from the provided URL.")
    
    data_chunks = splitter(data)
    if not data_chunks:
        raise HTTPException(status_code=400, detail="No valid data to load from the provided URL.")
    
    vecdb.add_documents(data_chunks)
    return {"message": "Data loaded successfully"}

# Assigning the retriever
retriever = vecdb.as_retriever(search_type="mmr")

# Endpoint to query data
@app.post("/query")
async def query_data(request: QueryRequest):
    question = request.question
    try:
        chain = RetrievalQAWithSourcesChain.from_chain_type(
            instruct_llm,
            chain_type="stuff", 
            retriever=retriever
        )
        template = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use five sentences maximum and keep the answer concise.
        Question: {question}
        Context: {context}
        Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)
        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | instruct_llm
            | StrOutputParser()
        )
        answer = rag_chain.invoke(question)
        return {"answer": answer}
    except Exception as e:
        logging.error(f"Error querying data: {e}")
        raise HTTPException(status_code=500, detail="Failed to query data.")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
