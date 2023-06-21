import cloudinary
from cloudinary.uploader import upload
from django.conf import settings

def upload_files(image, folder_name, _type):
    cloudinary.config(
        cloud_name=settings.CLOUDINARY['cloud_name'],
        api_key=settings.CLOUDINARY['api_key'],
        api_secret=settings.CLOUDINARY['api_secret']
    )
    if _type == 'video':
        result = upload(image, folder=folder_name, resource_type=_type)
    result = upload(image, folder=folder_name)
    return result['secure_url']