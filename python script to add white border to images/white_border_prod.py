import os
from PIL import Image, ExifTags

def add_border(input_folder, output_folder, border_size, border_color="white"):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # Loop through all the files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".png"):
            try:
                # Open the image
                image_path = os.path.join(input_folder, filename)
                image = Image.open(image_path)

                # Rotate the image based on EXIF orientation data
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = image._getexif()
                if exif is not None:
                    orientation = exif.get(orientation)
                    if orientation == 3:
                        image = image.rotate(180, expand=True)
                    elif orientation == 6:
                        image = image.rotate(270, expand=True)
                    elif orientation == 8:
                        image = image.rotate(90, expand=True)

                # Get the original image dimensions
                width, height = image.size

                # Calculate the new dimensions with the border
                new_width = width + border_size * 2
                new_height = height + border_size * 2

                # Create a new image with the specified border color
                new_image = Image.new("RGB", (new_width, new_height), border_color)

                # Calculate the position to paste the original image
                left = top = border_size
                right = left + width
                bottom = top + height

                # Paste the original image onto the new image
                new_image.paste(image, (left, top, right, bottom))

                # Save the new image with the border
                output_path = os.path.join(output_folder, filename)
                new_image.save(output_path)

                print(f"Added border to {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
        else:
            print(f"Skipping file {filename} (not an image)")

# Specify the input and output folders
input_folder = "input folder"
output_folder = "output folder"

# Specify the border size (in pixels) and color
border_size = 500  # Adjust this value to match the border size you want
border_color = "white"

# Call the function to add borders to the images
add_border(input_folder, output_folder, border_size, border_color)