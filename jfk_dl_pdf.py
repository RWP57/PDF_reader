import os
import PyPDF2
import re
import requests
from datetime import datetime
from collections import defaultdict

# Define the directory where documents are stored
DOCS_URL_2025 = "https://www.archives.gov/files/research/jfk/releases/2025/0318/"
DOCS_URL_2023 = "https://www.archives.gov/files/research/jfk/releases/2023/"

DOCS_URL = DOCS_URL_2023
DOCS_DIR = "c:\\Users\\Robbo\\Downloads\\jfk"
SORTED_DIR ="C:\\Users\\Robbo\\Downloads\\jfk\\sorted_documents"
KEYWORDS = ["CIA", "FBI", "Oswald", "assassination", "Dallas", "conspiracy", "classified", "TOP SECRET", "Insight Global", "Optical Prescription", "intimate relationship"]

# Function to create list of pdf for download
def list_pdf():
    file1 = open(DOCS_DIR + "\\xx.txt", 'r')
    lines = file1.readlines()
    file1.close()
    file_list = []
    for line in lines:
        filename = line.split(" ")
        result = "{}{}".format(DOCS_URL,filename[0])
        file_list.append(result)
    return(file_list)

# Function to download PDFs from URLs
def download_jfk_pdfs(url_list):
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
    for url1 in url_list:
        url = url1.rstrip('\n')
        filename = os.path.join(DOCS_DIR, url.split("/")[-1])
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Downloaded: {filename}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

# Function to extract text from PDFs
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""


# Function to categorize documents based on keywords
def categorize_document(text, filename):
    categories = set()
    if len(text) == 0:
        categories.add("No_Text")
    for keyword in KEYWORDS:
        if re.search(rf"\b{keyword}\b", text, re.IGNORECASE):
            categories.add(keyword)
    return categories if categories else {"Uncategorized"}


# Function to sort and organize documents
def sort_documents():
    if not os.path.exists(SORTED_DIR):
        os.makedirs(SORTED_DIR)

    document_categories = defaultdict(list)

    for file in os.listdir(DOCS_DIR):
        if file.endswith(".pdf"):
            file_path = os.path.join(DOCS_DIR, file)
            text = extract_text_from_pdf(file_path)
            #print(f"TEXT: XX{len(text)}XX")

            categories = categorize_document(text, file)

            for category in categories:
                category_dir = os.path.join(SORTED_DIR, category)
                if not os.path.exists(category_dir):
                    os.makedirs(category_dir)
                os.rename(file_path, os.path.join(category_dir, file))
                document_categories[category].append(file)

    print("Sorting complete. Documents have been categorized.")
    return document_categories

if __name__ == "__main__":
    jfk_pdf_urls = list_pdf()
    print(f'download start: {datetime.now()}')
    download_jfk_pdfs(jfk_pdf_urls)
    print(f'download end: {datetime.now()}')
    print(f"Documents listed: {len(jfk_pdf_urls)}")
    print(f'Sort start: {datetime.now()}')
    sorted_docs = sort_documents()
    for category, files in sorted_docs.items():
        print(f"{category}: {len(files)} documents")
    print(f'Sort End: {datetime.now()}')
