# Python Assignment - Object Detection with FastAPI

## Overview

This Python assignment demonstrates the implementation of an Object Detection API using FastAPI, coupled with YOLOv8 for region extraction. The application allows users to detect regions from both an image link and user-uploaded images, utilizing the YOLOv8 model for accurate and efficient region identification.

Develop a robust API endpoint, leveraging YOLOv8 on the CPU, for precise identification of furniture items and generation of masks. Special emphasis on addressing overlapping bounding boxes to ensure accurate results.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [Configuration](#configuration)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)

## Installation

Clone the repository:

```bash
git clone https://github.com/Hussain-Masthan/Region_Detection.git
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Please run the Swagger page once the server is started: 
```bash
http://localhost:8080/docs/
```


## Usage

The Object Detection API provides two main endpoints:

1. ### Detect Regions from User Uploaded Image:

	Endpoint: `/detect_regions_from_uploaded_image/`

	Method: `POST`

	Parameters:

	* `image_file`: User-uploaded image file.
	
	Example:

	```bash
	curl -X POST -H "Content-Type: multipart/form-data" -F "image_file=@example.jpg" http://localhost:8000/detect_regions_from_uploaded_image/
	```


2. ### Detect Regions from Image Link:

	Endpoint: /detect_regions_from_image_link/

	Method: POST

	Parameters:

	* `doc_file_name`: The name of the document file containing the image link.
	
	Example:

	```bash
	curl -X POST -H "Content-Type: application/json" -d '{"doc_file_name": "example.jpg"}' http://localhost:8000/detect_regions_from_image_link/
	```


## Endpoints

* `/detect_regions_from_uploaded_image/`: Multi-object region detection from a user-uploaded image file.

* `/detect_regions_from_image_link/`: Detects regions from an image link on the server.


## Saving Processed Images

* All processed images are saved in the `/data/` directory.


## Output Responses

The API response includes the following parameters:

- **Status Code**: An HTTP status code indicating the success or failure of the request.
- **Status**: Success or error.
- **Message**: A descriptive message providing additional context about the status of the request.
- **region_data**: Details about the regions detected in the given image. only this four labels(chair, couch, bed, dining table)
- **merged_coordinates**: Coordinates of regions that have been merged to eliminate overlaps.

#### Example Response

```json
{
  "status": "success",
  "status_code": 200,
  "status_message": "Region Data found Successfully.",
  "region_data": [
    {
      "xmin": 801,
      "ymin": 538,
      "xmax": 1999,
      "ymax": 1353,
      "confidence": 0.92,
      "class_id": 57,
      "class_name": "dining table"
    },
	    {
      "xmin": 0,
      "ymin": 625,
      "xmax": 263,
      "ymax": 1170,
      "confidence": 0.7,
      "class_id": 56,
      "class_name": "chair"
    },
    // ... additional region entries ...
  ],
  "merged_overlapping_coordinates": [
    {
      "xmin": 0,
      "ymin": 538,
      "xmax": 2000,
      "ymax": 1998
    }
  ]
}
```


## Configuration
* Configuration settings are stored in the config.ini file.

* Adjust the configuration parameters in config.ini based on your requirements.

## Logging
* Application logs are stored in the `logs` directory.
* Log level and formatting can be configured in the `logging.config` file.

## Contributing
* Contributions are welcome! Please follow the `CONTRIBUTING.md` guidelines.


## Example Rectangle

To visually represent a rectangle, The rectangle is defined by the following coordinates:

- `xmin`: The x-coordinate of the bottom-left corner of the rectangle.
- `ymin`: The y-coordinate of the bottom-left corner of the rectangle.
- `xmax`: The x-coordinate of the top-right corner of the rectangle.
- `ymax`: The y-coordinate of the top-right corner of the rectangle.

Here's a sample representation:

<!-- Example Rectangle -->


<div style="border: 2px solid #000; width: 200px; height: 100px; padding: 10px; text-align: center; position: relative; margin: auto;">
    <p style="margin: 0; position: absolute; left: -35px; top: 30px;">xmin</p>
    <p style="margin: 0; position: absolute; left: 70px; bottom: 100px;">ymin</p>
    <p style="margin: 0; position: absolute; right: -40px; top: 30px;">xmax</p>
    <p style="margin: 0; position: absolute; right: 90px; bottom: -23px;">ymax</p>
</div>




