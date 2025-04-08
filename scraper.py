import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to download an image
def download_image(image_url, folder_path):
    # Get the image content
    img_data = requests.get(image_url).content
    # Extract image name from URL
    img_name = os.path.basename(image_url)
    # Create the full path for saving the image
    img_path = os.path.join(folder_path, img_name)
    
    # Save the image to the folder
    with open(img_path, 'wb') as img_file:
        img_file.write(img_data)
    print(f"Downloaded {img_name}")

# Function to scrape and download images
def scrape_images(url, folder_path):
    # Make a request to the website
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return

    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all <img> tags in the page
    img_tags = soup.find_all('img')
    
    if not img_tags:
        print("No images found on this page.")
        return
    
    # Make folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Loop through all the image tags and download them
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            # Resolve relative URLs
            img_url = urljoin(url, img_url)
            try:
                download_image(img_url, folder_path)
            except Exception as e:
                print(f"Failed to download {img_url}. Error: {e}")

# Main function
if __name__ == "__main__":
    # URL of the website you want to scrape
   # website_url = 'https://example.com'  # Replace with your desired URL
    website_url = 'https://weather.com'
    download_folder = 'downloaded_images'  # Folder to save the images

    # Call the scraping function
    scrape_images(website_url, download_folder)

