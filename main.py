import os
import requests
from PIL import Image
from io import BytesIO

def download_image_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        image_bytes = BytesIO(response.content)
        return Image.open(image_bytes)
    else:
        raise Exception(f"Failed to download image from URL: {url}")

def slice_and_scale_image(input_image, output_folder, target_height):
    # Calculate the aspect ratio
    aspect_ratio = input_image.width / input_image.height

    # Calculate the target width based on the target height and aspect ratio
    target_width = int(target_height * aspect_ratio)

    # Resize the image while maintaining aspect ratio
    resized_image = input_image.resize((target_width, target_height), Image.LANCZOS)

    # Calculate the number of slices needed
    num_slices = target_width // target_height

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for i in range(num_slices + 1):  # Include the last slice
        # Calculate slice positions
        left = i * target_height
        right = min((i + 1) * target_height, target_width)

        # Crop the slice from the resized image
        slice_image = resized_image.crop((left, 0, right, target_height))

        # Create a transparent canvas to adjust for non-perfect aspect ratios
        canvas = Image.new('RGBA', (target_height, target_height), (0, 0, 0, 0))

        # Calculate the paste position for the last slice
        paste_position = (0, 0) if i == num_slices else ((target_height - slice_image.width), 0)

        canvas.paste(slice_image, paste_position)

        # Save the sliced image
        output_path = os.path.join(output_folder, f'slice_{i}.png')
        canvas.save(output_path)

if __name__ == "__main__":
    image_url = input("Enter the URL of the image: ")
    try:
        input_image = download_image_from_url(image_url)
        slice_and_scale_image(input_image, "output", 128)
        print(f"Image processing completed, output has been saved in {os.path.abspath('output')}")
    except Exception as e:
        print(f"An error occurred: {e}")
