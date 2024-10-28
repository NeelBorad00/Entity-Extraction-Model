import os
import requests
import pandas as pd
from tqdm import tqdm
from pathlib import Path
import time
from PIL import Image

# Create a placeholder image if download fails
def create_placeholder_image(image_save_path):
    try:
        placeholder_image = Image.new('RGB', (100, 100), color='black')
        placeholder_image.save(image_save_path)
        print(f"Created placeholder image at: {image_save_path}")
    except Exception as e:
        print(f"Error creating placeholder image: {e}")

# Download individual image
def download_image(image_link, save_folder, retries=3, delay=3):
    if not isinstance(image_link, str):
        return

    filename = Path(image_link).name
    image_save_path = os.path.join(save_folder, filename)

    # Check if image is already downloaded
    if os.path.exists(image_save_path):
        print(f"Image already exists: {image_save_path}")
        return

    headers = {'User-Agent': 'Mozilla/5.0'}

    # Attempt downloading the image
    for attempt in range(retries):
        try:
            response = requests.get(image_link, headers=headers, timeout=5)
            if response.status_code == 200:
                with open(image_save_path, 'wb') as f:
                    f.write(response.content)
                print(f"Image downloaded and saved at: {image_save_path}")
                return
            else:
                print(f"Failed to download image {image_link}. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error downloading image {image_link}: {e}")
            time.sleep(delay)

    # Create a placeholder image if download fails
    create_placeholder_image(image_save_path)

# Function to download all images from a dataset
def download_images(image_links, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for image_link in tqdm(image_links, total=len(image_links)):
        download_image(image_link, download_folder)

# Main function to load CSV and download images
def main():
    download_folder = 'images_train'  # Folder to save the images
    csv_path = 'train.csv'  # Path to your dataset (replace with actual CSV file)
    
    # Load the dataset
    df = pd.read_csv(csv_path)
    
    # Extract image links from the dataset
    image_links = df['image_link'].tolist()
    
    # Download the images
    download_images(image_links, download_folder)

if __name__ == "__main__":
    main()
