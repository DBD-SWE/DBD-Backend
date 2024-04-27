from django.db import IntegrityError
from django.shortcuts import render
from .models import Image
from rest_framework.decorators import api_view
from rest_framework.response import Response

# We need to recieve upload images
# in single, or in bulk
# through multipart/form-data

@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('image') or request.FILES.getlist('images')
            details = []
            for file in files:
                if not file.content_type.startswith('image/'):
                    return Response({'message': "Invalid file type, expected an image"}, status=400)

                original_name = request.POST.get('name', file.name)
                description = request.POST.get('description')

                image = Image.objects.create(image=file, name=original_name, description=description)
                image_details = {'image_id': image.id, 'image_name': image.name, 'image_url':  request.build_absolute_uri(image.image.url), 'created_at': image.created_at}
                details.append(image_details)

            if len(details) == 1:
                response_message = {'message': "Image uploaded successfully", **details[0]}
            else:
                response_message = {'message': "Images uploaded successfully", 'images': details}

            return Response(response_message, status=201)
        except Exception as e:
            return Response({'message': "An error occurred: " + str(e)}, status=400)