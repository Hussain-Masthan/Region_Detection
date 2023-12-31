import os
import requests

from src.utils_files.config_reader import ConfigReader

# Load configuration from config.ini
config_mgr = ConfigReader().config_reader()

# Directory to store uploaded files
UPLOAD_DIR = config_mgr.get("OUTPUT", "IMAGES_PATH")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(file, destination):
    """ Save the Uploaded Image to the specified location """
    with open(destination, "wb") as dest_file:
        dest_file.write(file.file.read())


def save_image_from_server(url, local_path):
    """
    Save an image from a given URL to the local path.

    Parameters:
    - url: URL of the image.
    - local_path: Local path to save the image.

    Returns:
    - str: Path to the saved image.
    """
    image_path = local_path + '/input.jpg'
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Image saved to {image_path}")
    else:
        image_path = ''
        print(f"Failed to download image. Status code: {response.status_code}")

    return image_path
