import os
import io
import zipfile
from PIL import Image 
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.conf import settings
from django.templatetags.static import static

def compress(image_path):
    # Load the image using PIL
    image = Image.open(image_path)

    # Perform compression operations on the image
    # Here, we resize the image to 50% of its original size
    compressed_image = image.resize((int(image.width * 0.5), int(image.height * 0.5)))

    return compressed_image
def index(request):
    return render(request, 'image_compress/index.html')

def compress_images(request):
    if request.method == 'POST':
        # Get the selected images from the request
        images = request.FILES.getlist('images')
        compressed_images = []

        # Create an in-memory zip file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for image in images:
                # Save the uploaded image temporarily
                with open(image.name, 'wb') as file:
                    file.write(image.read())
                image_path = os.path.join(settings.BASE_DIR, image.name)
                
                # Compress each image and add it to the zip file
                compressed_image = compress(image_path)
                compressed_image.save(image_path)  # Overwrite the original image with the compressed version
                zip_file.write(image_path, os.path.basename(image_path))  # Add the compressed image to the zip file
                compressed_images.append(image_path)

                # Delete the temporary image file
                os.remove(image_path)

        # Set the appropriate response headers
        response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="compressed_images.zip"'
        return response

    return render(request, 'image_compress/result.html')
def result(request):
    zip_url = r'C:\Users\bvnku\image_compression\compressed_images.zip' 
    return render(request, 'image_compress/result.html', {'zip_url': zip_url})