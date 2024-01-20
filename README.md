# motoes-zip-to-image

`motoes-zip-to-image` is a Python tool designed to encode `.zip` files into a series of images and then decode these images back into the original `.zip` file. This project provides an innovative approach to circumvent file type restrictions and upload size limits on various platforms.

## Features

- **Encode Zip Files**: Convert `.zip` files into a sequence of images, efficiently handling large files by splitting them into chunks.
- **Decode Images to Zip**: Reassemble the original `.zip` file from the sequence of images, ensuring data integrity and order.
- **Progress Tracking**: Visual progress bars for both encoding and decoding processes.
- **User-Friendly**: Simple CLI for easy operation.

## Installation

Clone the repository:

```bash
git clone https://github.com/motoemoto47ark123/motoes-zip-to-image.git
cd motoes-zip-to-image
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with:

```bash
python main.py
```

Follow the CLI prompts:

1. **Encode**: Place a `.zip` file in the `encoded/input` directory and choose the encode option.
2. **Decode**: Place encoded images in the `decoded/input` directory and choose the decode option.

## Contributing

Contributions to `motoes-zip-to-image` are welcome! Please feel free to submit pull requests, or open issues to suggest features or report bugs.
