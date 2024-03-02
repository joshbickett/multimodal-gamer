import os
from gamer.config import Config
from datetime import datetime
from PIL import Image, ImageDraw


# Load configuration
config = Config()


def get_text_element(result, search_text, image_path):
    """
    Searches for a text element in the OCR results and returns its index. Also draws bounding boxes on the image.
    Args:
        result (list): The list of results returned by EasyOCR.
        search_text (str): The text to search for in the OCR results.
        image_path (str): Path to the original image.

    Returns:
        int: The index of the element containing the search text.

    Raises:
        Exception: If the text element is not found in the results.
    """
    if config.verbose:
        print("[get_text_element]")
        print("[get_text_element] search_text", search_text)
        # Create /ocr directory if it doesn't exist
        ocr_dir = "ocr"
        if not os.path.exists(ocr_dir):
            os.makedirs(ocr_dir)

        # Open the original image
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)

    lowest_index = None
    max_y_value = -1
    for index, element in enumerate(result):
        text = element[1]
        box = element[
            0
        ]  # Box is a list of tuples [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]

        if config.verbose:
            draw.polygon([tuple(point) for point in box], outline="blue")

        if search_text in text:
            # Calculate the average Y value of the bottom points of the bounding box
            bottom_y_average = (box[2][1] + box[3][1]) / 2
            if bottom_y_average > max_y_value:
                lowest_index = index
                max_y_value = bottom_y_average
            if config.verbose:
                print("[get_text_element][loop] found search_text, index:", index)

    if lowest_index is not None:
        if config.verbose:
            box = result[lowest_index][0]
            draw.polygon([tuple(point) for point in box], outline="red")
            datetime_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            ocr_image_path = os.path.join(ocr_dir, f"ocr_image_{datetime_str}.png")
            image.save(ocr_image_path)
            print("[get_text_element] OCR image saved at:", ocr_image_path)
        return lowest_index

    raise Exception("The text element was not found in the image")


def get_text_coordinates(result, index, image_path):
    """
    Gets the coordinates of the text element at the specified index as a percentage of screen width and height.
    Args:
        result (list): The list of results returned by EasyOCR.
        index (int): The index of the text element in the results list.
        image_path (str): Path to the screenshot image.

    Returns:
        dict: A dictionary containing the 'x' and 'y' coordinates as percentages of the screen width and height.
    """
    if index >= len(result):
        raise Exception("Index out of range in OCR results")

    # Get the bounding box of the text element
    bounding_box = result[index][0]

    # Calculate the center of the bounding box
    min_x = min([coord[0] for coord in bounding_box])
    max_x = max([coord[0] for coord in bounding_box])
    min_y = min([coord[1] for coord in bounding_box])
    max_y = max([coord[1] for coord in bounding_box])

    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2

    # Get image dimensions
    with Image.open(image_path) as img:
        width, height = img.size

    # Convert to percentages
    percent_x = round((center_x / width), 3)
    percent_y = round((center_y / height), 3)

    return {"x": percent_x, "y": percent_y}
