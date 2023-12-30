"""==========================================
 Title:  Assignment - Python - ObjectDetection
 Author: Hussain Masthan
 Date:   Jan - 2024
=========================================="""

import os
import datetime
import logging
import time

import cv2
import numpy as np

from yolo.ultralytics import YOLO
from src.utils_files.config_reader import ConfigReader
from src.utils_files import util

_logger = logging.getLogger(__name__)


class RegionExtractor:
    """Class for extracting regions from an image using YOLOv8 Model."""

    def __init__(self, image_path):
        self.image_path = image_path
        self.config_mgr = ConfigReader().config_reader()
        predefined_model = self.config_mgr.get("YOLO", "MODEL")
        self.yolo_model = YOLO(f"yolo/{predefined_model}")
        self.save_images = self.config_mgr.get("OUTPUT", "SAVE_IMAGES")
        self.confidence_threshold = self.config_mgr.getfloat("YOLO", "CONFIDENCE")
        self.labels = self.config_mgr.get("YOLO", "LABELS")[1:-1].split(', ')
        self.data_path = self.config_mgr.get("OUTPUT", "IMAGES_PATH")

    def extract_regions(self):
        """Extracts regions from the image using YOLOv8 Model."""
        regions_list, merged_coordinates = {}, {}
        try:
            # Log File Creation Process
            log_file = util.setup_root_logger("Python-Assignment")
            _logger.info("--------------------------------------------")
            _logger.info("Log file is writing to : %s" % log_file)
            _logger.info("--------------------------------------------")

            # Start time
            start_time = time.time()
            app_name = "Assignment - Region Extraction Using YoloV8 Model"
            _logger.info(f'{app_name} has started at {format(start_time)}')
            _logger.info(f"Beginning {app_name} process, log is: {log_file}")
            _logger.info("Region Extraction API post process is started...")
            _logger.info(f"FileName: {self.image_path}")

            # Region identification process
            _logger.info("Region Identification process is started...")
            regions_list = self.__identify_regions()
            _logger.info("Region Identification process is completed...")

            # Coordinates overlapping process
            _logger.info("Coordinates Overlapping process is started...")
            merged_coordinates = self.__merge_overlapping_coordinates(regions_list)
            _logger.info("Coordinates Overlapping process is completed...")

            # Logging and saving progress images
            if self.save_images == 'True':
                _logger.info("Output Progress Image is started...")
                self.__write_merged_overlap_image(merged_coordinates)
                self.__write_white_mask_image(regions_list)
                self.__write_mask_image_with_original(regions_list)
                _logger.info("Output Progress Image is completed...")

            # Logging region fields
            _logger.info(f"Region Fields: {regions_list}")
            _logger.info("----------------------------------")
            _logger.info(f"Execution of {app_name} process is Successfully Completed")
            _logger.info("----------------------------------")
            _logger.info(f"Elapsed time: {time.time() - start_time}")
            _logger.info(f'{app_name} has completed at {format(datetime.datetime.now())}')
            _logger.info("----------------------------------")

        except Exception as e:
            _logger.error(f"Region Extraction API failed! {repr(e)}")

        return regions_list, merged_coordinates

    # @classmethod
    def __identify_regions(self):
        """This is a private method intended for internal use within the class."""
        """Identifies regions in the image using YOLOv8 Model."""
        regions_list = []

        try:
            # Read the image as an array
            image_array = cv2.imread(self.image_path)
            # Use YOLOv8 model to predict regions in the image
            results = self.yolo_model.predict(source=image_array, save=True, save_txt=True,
                                              conf=self.confidence_threshold)

            # Iterate through the results to extract relevant information
            for class_data in results:
                for box in class_data.boxes:
                    coordinates = box.xyxy[0].tolist()
                    class_id = box.cls[0].item()
                    confidence = box.conf[0].item()
                    class_name = class_data.names[class_id]

                    print("Object type:", class_id)
                    print("Coordinates:", coordinates)
                    print("Probability:", confidence)
                    print("ClassNames:", class_name)

                    # Check if the detected class is among the specified labels
                    if class_name in self.labels:
                        region_dict = {'xmin': int(coordinates[0]), 'ymin': int(coordinates[1]),
                                       'xmax': int(coordinates[2]), 'ymax': int(coordinates[3]),
                                       'confidence': round(confidence, 2), 'class_id': class_id,
                                       'class_name': class_name}
                        regions_list.append(region_dict)

            _logger.info("Identify Region Process has been completed successfully...")

        except Exception as e:
            # Log an error message if the region identification process fails
            _logger.error(f"Region Identification Process failed! {repr(e)}")

        return regions_list

    def __write_white_mask_image(self, regions_list):
        """Writes an image with a white mask based on identified regions."""
        try:
            original_image = cv2.imread(self.image_path)
            white_mask_image = np.zeros_like(original_image)
            self.__write_images(regions_list, white_mask_image, 'white_mask')
        except Exception as e:
            _logger.error(f"Image Mask Creation Process failed! {repr(e)}")

    def __write_mask_image_with_original(self, regions_list):
        """Writes an image with a mask overlay on the original image."""
        try:
            original_image_copy = ''
            original_image = cv2.imread(self.image_path)
            original_image_copy = original_image.copy()
            self.__write_images(regions_list, original_image_copy, 'white_mask_original')
        except Exception as e:
            _logger.error(f"Image Mask Overlay Process failed! {repr(e)}")

    def __write_merged_overlap_image(self, merged_coordinates_list):
        """Writes an image with merged overlapping regions."""
        try:
            original_image_copy = ''
            original_image = cv2.imread(self.image_path)
            original_image_copy = original_image.copy()
            self.__write_images(merged_coordinates_list, original_image_copy, 'merged_overlap')
        except Exception as e:
            _logger.error(f"Merged Overlapping Image Writing Process failed! {repr(e)}")

    def __merge_overlapping_coordinates(self, regions_list):
        """Merges overlapping coordinates in a list of regions."""
        merged_boxes = []
        try:
            # Convert regions to a list of tuples for easy manipulation
            coordinates_tuples = [(region['xmin'], region['ymin'],
                                   region['xmax'], region['ymax']) for region in regions_list]

            # Sort bounding boxes based on Xmin
            sorted_boxes = sorted(coordinates_tuples, key=lambda box: box[0])
            merged_boxes = []
            current_box = sorted_boxes[0]

            for next_box in sorted_boxes[1:]:
                # Check if the boxes overlap
                if current_box[0] + current_box[2] >= next_box[0]:
                    # Merge overlapping boxes
                    current_box = (
                        min(current_box[0], next_box[0]),
                        min(current_box[1], next_box[1]),
                        max(current_box[2], next_box[2]),
                        max(current_box[3], next_box[3])
                    )
                else:
                    # No overlap, add the current merged box to the result
                    if current_box:
                        merged_boxes.append({'xmin': current_box[0], 'ymin': current_box[1],
                                            'xmax': current_box[2], 'ymax': current_box[3]})
                        current_box = next_box

            # Add the last merged box
            if current_box:
                merged_boxes.append({'xmin': current_box[0], 'ymin': current_box[1],
                                    'xmax': current_box[2], 'ymax': current_box[3]})

        except Exception as e:
            _logger.error(f"Merged Overlapping Coordinates Process failed! {repr(e)}")

        return merged_boxes

    def __write_images(self, coordinates_list, image_data, image_name):
        """Writes images with specified names and overlays."""
        try:
            for idx, region in enumerate(coordinates_list):
                x_min, y_min = region['xmin'], region['ymin']
                x_max, y_max = region['xmax'], region['ymax']
                cv2.rectangle(image_data, (x_min, y_min), (x_max, y_max), (255, 255, 255), thickness=cv2.FILLED)
                # image_data[yMin:yMax, xMin:xMax, :] = (255, 255, 255)
            if self.save_images == "True":
                cv2.imwrite(f"{self.data_path}/{image_name}.jpg", image_data)
        except Exception as e:
            _logger.error(f"Image Writing Process failed! {repr(e)}")
