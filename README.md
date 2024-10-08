# Wikipedia RAG Chatbot
This project implements a Retrieval-Augmented Generation (RAG) chatbot that extracts data from Wikipedia, stores it in a vector database, and uses a generative AI model to answer user queries.


Tools & Technologies
- Programming Language: Python
- Web Scraping: BeautifulSoup
- Vector Database: Weaviate (your preference)
- Generative AI Model: NVIDIA AI model
- API Framework: FastAPI
- Frontend: Streamlit (for user interaction)


Project Structure

bash

/wikipedia-rag-chatbot
│
├── /wiki.py             # Data extraction from Wikipedia
├── /vecdb.py            # Vector database interactions and processing
├── /api.py              # FastAPI application with endpoints
├── /streamlit_app.py     # Streamlit frontend
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
