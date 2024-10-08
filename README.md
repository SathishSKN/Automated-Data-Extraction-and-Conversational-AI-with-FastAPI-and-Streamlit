# Wikipedia RAG Chatbot Documentation

## Overview
This project implements a Retrieval-Augmented Generation (RAG) chatbot that extracts data from Wikipedia, stores it in a vector database, and uses a generative AI model to answer user queries.

## Objectives
- Extract data from a Wikipedia page.
- Load the extracted data into a vector database.
- Use a generative AI model to answer questions based on the loaded data.
- Develop a FastAPI application with two endpoints: one for loading data and another for querying.

## Tools & Technologies
- **Programming Language**: Python
- **Web Scraping**: BeautifulSoup
- **Vector Database**: Weaviate (or Milvus, if preferred)
- **Generative AI Model**: NVIDIA AI model
- **API Framework**: FastAPI
- **Frontend**: Streamlit
- **Containerization**: Docker

## Project Structure


      /wikipedia-rag-chatbot
      │
      ├── /wiki.py             # Data extraction from Wikipedia
      ├── /vecdb.py            # Vector database interactions and processing
      ├── /main.py             # FastAPI application with endpoints
      ├── /chatbot.py          # Streamlit frontend
      ├── requirements.txt     # Python dependencies
      ├── Dockerfile           # Docker configuration 
      └── README.md            # Project documentation



## Installation

### Using Docker

1. **Build the Docker Image**:
   In the project directory, run:
   ```bash
   docker build -t wikipedia-rag-chatbot .

2. Run the Docker Container:
   ```bash
   docker run -p 8080:8080 wikipedia-rag-chatbot
   
The API will be accessible at `http://localhost:8000`.


### Without Docker

1. Clone the repository:
```bash   
git clone https://github.com/SathishSKN/Wikipedia-RAG-Chatbot
cd wikipedia-rag-chatbot
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (if needed):
```bash
export NVIDIA_API_KEY='your_api_key_here'  # For NVIDIA models
```

## Usage
### Running the FastAPI Server

1. Start the FastAPI Server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 / uvicorn main:app --reload
```

2. The API will be accessible at `http://localhost:8000` or at `localhost`

## FastAPI Endpoints

1. **Load Data**
- **Endpoint:** `/load`
- **Method:** POST
- **Request Body:**
```json
{
"url": "https://en.wikipedia.org/wiki/Your_Article_Name"
}
```

- **Description:** Accepts a Wikipedia page URL, extracts the data, processes it, and loads it into the vector database.

- **Response:**
       - **Success:** `{"message": "Data loaded successfully"}`
       - **Error:** `{"detail": "Error message"}`

2. **Query Data**

- **Endpoint:** `/query`

- **Method:** POST

- **Request Body:**
```json
{
"question": "Your question here"
}
```

- **Description:** Accepts a user query, retrieves relevant data from the vector database, and generates an answer using the generative AI model.

- **Response:**
       - **Success:** `{"answer": "Your answer here"}`
       - **Error:** `{"detail": "Error message"}`


## Running the Streamlit App

1. Start the Streamlit app:
```bash
streamlit run chatbot.py
```

2. Access the app at `http://localhost:8501`.


## Error Handling

- Each API endpoint includes error handling for common issues, such as invalid URLs or failed data extraction.


## Additional Notes

- Ensure your environment is set up with the necessary API keys and dependencies.
- Refer to the code comments for detailed explanations of functions and logic.


## License

This project is a prototype and is not licensed under any specific terms. Use it for educational purposes only.

```
### Dockerfile Example

If you don't already have a `Dockerfile`, here's a simple example you can include in your project:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8080

# Define environment variable
ENV NVIDIA_API_KEY='your_api_key_here'

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"] / [uvicorn main:app --reload]
```



