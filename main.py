import numpy as np  # Importing numpy for numerical operations
from PIL import Image  # Importing Image module from PIL to handle image operations
import math  # Importing math for mathematical operations
import os  # Importing os for operating system related operations
from tqdm import tqdm  # Importing tqdm for progress bar
import glob  # Importing glob for file path related operations

def file_to_images(input_folder, output_folder, max_image_size=1000000):  
    # Function to convert files to images
    zip_files = glob.glob(os.path.join(input_folder, '*.zip'))  # Get all zip files in the input folder
    if not zip_files:
        print("No .zip files found in the input directory.")  # If no zip files found, print error and return False
        return False

    file_path = zip_files[0]  # Get the first zip file
    os.makedirs(output_folder, exist_ok=True)  # Create output directory if it doesn't exist

    with open(file_path, "rb") as file, tqdm(desc="Encoding", unit='img') as pbar:  # Open the zip file and initialize progress bar
        i = 0  # Initialize image counter
        while True:
            data = file.read(max_image_size - 8)  # Read data from file
            if not data:
                break  # If no data left, break the loop

            actual_size = len(data)  # Get the actual size of the data
            header = actual_size.to_bytes(4, byteorder='big') + i.to_bytes(4, byteorder='big')  # Create a header with the actual size and image counter
            data_with_header = header + data  # Add the header to the data

            data_length = len(data_with_header)  # Get the length of the data with header
            total_pixels_needed = math.ceil(data_length / 3)  # Calculate the total pixels needed
            width = int(math.sqrt(total_pixels_needed))  # Calculate the width of the image
            height = math.ceil(total_pixels_needed / width)  # Calculate the height of the image

            padded_data = data_with_header.ljust(width * height * 3, b'\0')  # Pad the data with zeros to match the total pixels needed
            img_data = np.frombuffer(padded_data, dtype=np.uint8).reshape((height, width, 3))  # Convert the padded data to a numpy array and reshape it to match the image dimensions
            image = Image.fromarray(img_data, 'RGB')  # Create an image from the numpy array
            image_output_path = os.path.join(output_folder, f'encoded_image_{i}.png')  # Define the output path for the image
            image.save(image_output_path)  # Save the image

            i += 1  # Increment the image counter
            pbar.update(1)  # Update the progress bar

    return True  # Return True when done

def images_to_file(input_folder, output_folder):
    # Function to convert images back to file
    image_files = sorted(glob.glob(os.path.join(input_folder, '*.png')), key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0]))  # Get all image files in the input folder and sort them

    if not image_files:
        print("No image files found in the input directory.")  # If no image files found, print error and return False
        return False

    output_file_path = os.path.join(output_folder, 'output.zip')  # Define the output file path
    os.makedirs(output_folder, exist_ok=True)  # Create output directory if it doesn't exist

    with open(output_file_path, "wb") as output_file, tqdm(total=len(image_files), desc="Decoding", unit='img') as pbar:  # Open the output file and initialize progress bar
        for image_path in image_files:  # For each image file
            image = Image.open(image_path)  # Open the image
            img_data = np.array(image)  # Convert the image to a numpy array

            binary_data = img_data.flatten()  # Flatten the numpy array to a 1D array
            actual_size = int.from_bytes(binary_data[:4], byteorder='big')  # Get the actual size of the data from the header
            output_file.write(binary_data[8:8+actual_size])  # Write the actual data to the output file

            pbar.update(1)  # Update the progress bar

    return True  # Return True when done

def main():
    # Main function
    encoded_input_dir = os.path.join('encoded', 'input')  # Define the input directory for encoding
    encoded_output_dir = os.path.join('encoded', 'output')  # Define the output directory for encoding
    decoded_input_dir = os.path.join('decoded', 'input')  # Define the input directory for decoding
    decoded_output_dir = os.path.join('decoded', 'output')  # Define the output directory for decoding

    for directory in [encoded_input_dir, encoded_output_dir, decoded_input_dir, decoded_output_dir]:  # For each directory
        os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

    choice = input("Enter 1 to Encode, 2 to Decode, or 3 to Exit: ")  # Ask the user for their choice
    if choice == '1':  # If the user chose to encode
        success = file_to_images(encoded_input_dir, encoded_output_dir)  # Call the file_to_images function
        print("Encoding completed successfully." if success else "Encoding failed.")  # Print the result
    elif choice == '2':  # If the user chose to decode
        success = images_to_file(decoded_input_dir, decoded_output_dir)  # Call the images_to_file function
        print("Decoding completed successfully." if success else "Decoding failed.")  # Print the result
    elif choice == '3':  # If the user chose to exit
        print("Exiting the program.")  # Print a message and exit
    else:  # If the user entered an invalid choice
        print("Invalid choice. Please enter 1, 2, or 3.")  # Print an error message

if __name__ == "__main__":
    main()  # Call the main function if the script is run directly
