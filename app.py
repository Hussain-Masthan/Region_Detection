"""==========================================
 Title:  Python Assignment
 Author: Hussain Masthan
 Date:   Jan - 2023
=========================================="""

# Import Necessary Modules
import os

from src.utils_files.config_reader import ConfigReader

import uvicorn

from fastapi import FastAPI, File, UploadFile, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from service.region_detection_service.object_detection_processor import RegionExtractor

# Load configuration from config.ini
config_mgr = ConfigReader().config_reader()

# Create a FastAPI instance
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this list based on your specific requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store uploaded files
UPLOAD_DIR = config_mgr.get("OUTPUT", "IMAGES_PATH")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(file, destination):
    """ Save the Uploaded Image to the specified location """
    with open(destination, "wb") as dest_file:
        dest_file.write(file.file.read())
        
        
@app.post("/detect_regions_from_uploaded_image/")
async def detect_regions_from_uploaded_images(image_file: UploadFile = File(...)):
    """
    Endpoint Description:
    - Endpoint for multi-object region detection from a User-uploaded image file.

    Parameters:
    - image_file: User-uploaded image file.

    Returns:
    - JSONResponse with region data.
    """
    try:
        # Validate the input parameter
        if not image_file:
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # Validate content type to ensure it's an image
        if not image_file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Only image files are allowed.")

        # Save the Uploaded Image file from Users
        image_path = os.path.join(UPLOAD_DIR, image_file.filename)
        save_uploaded_file(image_file, image_path)

        # Perform Region detection on the uploaded image
        region_fields, merged_coordinates = RegionExtractor(image_path).extract_regions()
        # Return the result as JSON response
        return JSONResponse(content={"status": "success", "status_code": status.HTTP_200_OK,
                                     "region_data": region_fields, "merged_coordinates": merged_coordinates},
                            status_code=status.HTTP_200_OK)

    except HTTPException as e:
        # Handle client errors and return an error response
        return JSONResponse(content={"status": "error", "status_code": e.status_code,
                                     "message": str(e.detail)}, status_code=e.status_code)

    except Exception as e:
        # Handle server errors and return an error response
        return JSONResponse(content={"status": "error", "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     "message": f"Internal server error: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.post("/detect_regions_from_image_link/")
async def detect_regions_from_image_link(doc_file_name: str):
    """
    Endpoint Description:
    - Endpoint to detect regions from an image link on the server.

    Parameters:
    - image_link: URL of the image file on the server.

    Returns:
    - JSONResponse with region data.
    """
    try:
        # Validate the input parameter
        if not doc_file_name:
            raise HTTPException(status_code=400, detail="Invalid document file name.")
        # Perform Region Detection
        region_fields, merged_coordinates = RegionExtractor(doc_file_name).extract_regions()
        # Return the result as JSON response
        return JSONResponse(content={"status": "success", "status_code": status.HTTP_200_OK,
                                     "region_data": region_fields, "merged_coordinates": merged_coordinates},
                            status_code=status.HTTP_200_OK)

    except Exception as e:
        # Handle Unexpected errors and return an error response
        return JSONResponse(content={"status": "error", "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                                     "message": f"Internal server error: {str(e)}"},
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


if __name__ == "__main__":
    # Get the port number from the configuration file
    port = config_mgr.getint("SERVER_CONFIG", "PORT")
    # Get the Host number from the configuration file
    host = config_mgr.get("SERVER_CONFIG", "HOST")
    # Run the application using Uvicorn
    uvicorn.run(app, host=host, port=port)
