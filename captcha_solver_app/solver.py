from typing import NamedTuple 

import cv2
from cv2.typing import MatLike
import numpy as np


Box = tuple[int, int, int, int]


class SolvedImage(NamedTuple):
    image: MatLike
    objects_count: int


def get_solved_image(image_to_process: MatLike, look_for: str) -> SolvedImage:
    """
    recognition and determination of the coordinates of objects on the image
    :param image_to_process: original image
    :param look_for: objects to detect user input
    :return: image with marked objects and captions to them
    """
    # Loading YOLO scales from files and setting up the network
    RESOURCES_PATH = 'captcha_solver_app/resources'
    net = cv2.dnn.readNetFromDarknet(
            f'{RESOURCES_PATH}/yolov4-tiny.cfg',
            f'{RESOURCES_PATH}/yolov4-tiny.weights',)
    layer_names = net.getLayerNames()
    out_layers_indexes = net.getUnconnectedOutLayers()
    out_layers = [layer_names[index - 1] for index in out_layers_indexes]

    # Loading from a file of object classes that YOLO can detect
    with open(f'{RESOURCES_PATH}/coco.names.txt') as file:
        classes = file.read().split("\n")

    # Remove spaces and case sensitivity
    list_look_for: list[str] = []
    for look in look_for.split(','):
        list_look_for.append(look.strip().lower())

    classes_to_look_for = list_look_for

    height, width, _ = image_to_process.shape
    blob = cv2.dnn.blobFromImage(image_to_process, 1 / 255, (608, 608),
                                 (0, 0, 0), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(out_layers)
    class_indexes: list[np.intp]
    boxes: list[Box]
    class_indexes, class_scores, boxes = ([] for _ in range(3))
    objects_count = 0

    # Starting a search for objects in an image
    for out in outs:
        for obj in out:
            scores = obj[5:]
            class_index = np.argmax(scores)
            class_score = scores[class_index]
            if class_score > 0:
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                obj_width = int(obj[2] * width)
                obj_height = int(obj[3] * height)
                box = (center_x - obj_width // 2, center_y - obj_height // 2,
                       obj_width, obj_height)
                boxes.append(box)
                class_indexes.append(class_index)
                class_scores.append(float(class_score))

    # Selection
    chosen_boxes = cv2.dnn.NMSBoxes(boxes, class_scores, 0.0, 0.4)
    for box_index in chosen_boxes:
        box_index = box_index
        box = boxes[box_index]
        class_index = class_indexes[box_index]

        # For debugging, we draw objects included in the desired classes
        if classes[class_index] in classes_to_look_for:
            objects_count += 1
            image_to_process = draw_object_bounding_box(
                    image_to_process, class_index, box, classes)

    return SolvedImage(image=image_to_process, objects_count=objects_count)


def draw_object_bounding_box(image_to_process: MatLike, index: np.intp,
                             box: Box, classes: list[str]) -> MatLike:
    """
    Drawing object borders with captions
    :param image_to_process: original image
    :param index: index of object class defined with YOLO
    :param box: coordinates of the area around the object
    :return: image with marked objects
    """
    height, width, _ = image_to_process.shape
    x, y, w, h = box
    start = (x, y)
    end = (x + w, y + h)
    color = (0, 255, 0)

    # Adjust thickness of rectangle and text size based on image dimensions
    rect_thickness = max(1, int(min(height, width) * 0.002))  # Rectangle thickness
    font_size = min(height, width) * 0.0015  # Font size based on image size
    font = cv2.FONT_HERSHEY_SIMPLEX

    final_image = cv2.rectangle(image_to_process, start, end, color, rect_thickness)

    # Calculate position for text slightly above the rectangle
    text_start = (x, max(0, y - 10))

    # Adjust text thickness
    text_thickness = max(1, int(rect_thickness / 2))

    # Get the class name to display
    text = classes[index]
    final_image = cv2.putText(final_image, text, text_start, font, font_size, color, text_thickness, cv2.LINE_AA)

    return final_image

