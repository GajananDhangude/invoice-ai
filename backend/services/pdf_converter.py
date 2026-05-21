from pdf2image import convert_from_path
import os


poppler_path=r"C:/poppler/poppler-25.12.0/Library/bin"
os.makedirs('output_folder', exist_ok=True)  # Create output folder if it doesn't exist

def convert_pdf_to_images(pdf_path):
    # Convert PDF to images
    images = convert_from_path(
        pdf_path,
        poppler_path=poppler_path,  # Specify the path to poppler binaries
        dpi=300,  # Set the resolution (dots per inch)
    )

    # Save images to the output folder
    for i, image in enumerate(images):
        image_path = os.path.join('output_folder', f'page_{i + 1}.png')
        image.save(image_path, 'PNG')


    return f'{image_path}'

# if __name__ == "__main__":
#     pdf_path = './uploads/AMAZON.pdf'  # Replace with your PDF file path
#     path = convert_pdf_to_images(pdf_path)
#     print(path)