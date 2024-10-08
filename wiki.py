# Importing Dependencies
import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract Wikipedia data
def extract_wikipedia_data(url):
    """
    Extracts paragraph data from a given Wikipedia page URL.

    Args:
        url (str): The URL of the Wikipedia page.

    Returns:
        list: A list of dictionaries containing paragraphs and their metadata,
               or an empty list if an error occurs.
    """
    try:
        # Check if the URL is a Wikipedia page
        if not url.startswith("https://en.wikipedia.org/"):
            raise ValueError("Only Wikipedia pages links are supported.")

        # Make a request with timeout
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an error for bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')

        if not paragraphs:
            raise ValueError("No paragraphs found in the provided Wikipedia page.")

        return [{"paragraph": para.text.strip(), "metadata": {"source": url}} for para in paragraphs]

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except ValueError as val_err:
        logging.error(f"Value error: {val_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

    return []  # Return an empty list if an error occurred

# Example usage
data = extract_wikipedia_data("https://en.wikipedia.org/wiki/Retrieval-augmented_generation")
# print(data)
