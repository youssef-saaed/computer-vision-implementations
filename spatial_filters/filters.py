from .utils import * 

def negative_filter(image_path: str, output_path: str) -> None:
    image = get_image(image_path)
    transformed_image = 255 - image
    save_image(transformed_image, output_path)
    