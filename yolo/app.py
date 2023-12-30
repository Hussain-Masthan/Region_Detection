from ultralytics import YOLO
from PIL import Image
import cv2

model = YOLO("yolov8n.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
# results = model.predict(source="1")
# results = model.predict(source="folder", show=True) # Display preds. Accepts all YOLO predict arguments

# from PIL
# im1 = Image.open("C:/Users/VR Della/Desktop/yolov8_mask/datasets/coco128/images/train2017/000000000474.jpg")
# results = model.predict(source=im1, save=True)  # save plotted images

# from ndarray
im2 = cv2.imread("C:/Users/VR Della/Desktop/yolov8_mask/datasets/coco128/images/train2017/000000000474.jpg")
results = model.predict(source=im2, save=True, save_txt=True)  # save predictions as labels

# View results
for class_data in results:
    for box in class_data.boxes:
        cords = box.xyxy[0].tolist()
        class_id = box.cls[0].item()
        conf = box.conf[0].item()
        print("Object type:", class_id)
        print("Coordinates:", cords)
        print("Probability:", conf)



# from list of PIL/ndarray
# results = model.predict(source=[im1, im2])



# Run inference on 'bus.jpg' with arguments
# model.predict('bus.jpg', save=True, imgsz=320, conf=0.5)




# import cv2
# import sys
# import os
# from ultralytics import YOLO
#
# model = YOLO("yolov8n.pt")  # path to model file
# cap = cv2.VideoCapture(0)  # path to video file or webcam
# crop_filename = "crop"  # set the crop file name
# crop_count = 0
#
# if not cap.isOpened():
#     print("Error reading video file")
#     sys.exit()
#
# if not os.path.exists("crop"):
#     os.mkdir("crop")
#
# while cap.isOpened():
#
#     success, frame = cap.read()
#     if success:
#         results = model.predict(frame, verbose=False)
#         boxes = results[0].boxes.xyxy.cpu()
#         for box in boxes:
#             crop_count += 1
#             crop_object = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
#             cv2.imwrite(os.path.join("crop", crop_filename+ f"_{crop_count}.png"), crop_object)
#
#         cv2.imshow("YOLOv8 Detection", frame)
#         if cv2.waitKey(1) & 0xFF == ord("q"):
#             break
#     else:
#         break
#
# cap.release()
# cv2.destroyAllWindows()