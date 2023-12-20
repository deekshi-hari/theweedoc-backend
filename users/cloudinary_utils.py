import cloudinary
from cloudinary.uploader import upload
from django.conf import settings

# def upload_files(file, folder_name, _type):
#     cloudinary.config(
#         cloud_name=settings.CLOUDINARY['cloud_name'],
#         api_key=settings.CLOUDINARY['api_key'],
#         api_secret=settings.CLOUDINARY['api_secret']
#     )
#     if _type == 'video':
#         result = upload(file, folder=folder_name, resource_type=_type)
#         duration = result.get("duration")
#         return [result['secure_url'], duration]
        
#     else:
#         result = upload(file, folder=folder_name)
#         return result['secure_url']

from cloudinary.uploader import upload_large

# def upload_files(file, folder_name, _type):
#     cloudinary.config(
#         cloud_name=settings.CLOUDINARY['cloud_name'],
#         api_key=settings.CLOUDINARY['api_key'],
#         api_secret=settings.CLOUDINARY['api_secret']
#     )
    
#     if _type == 'video':
#         # Use upload_large for video files
#         for chunk in file:
#                 result = upload_large(
#                     chunk,
#                     folder=folder_name,
#                     resource_type='video',
#                     chunk_size=1024 * 1024  # Set your preferred chunk size in bytes
#                 )
#         # result = upload_large(file, 
#         #                       folder=folder_name, 
#         #                       resource_type=_type, 
#         #                       chunk_size=10 * 1024 * 1024)
#         duration = result.get("duration")
#         return [result['secure_url'], duration]
#     else:
#         # Use regular upload for other file types
#         result = upload(file, folder=folder_name)
#         return result['secure_url']


import tempfile

def upload_files(file, folder_name, _type):
    cloudinary.config(
        cloud_name=settings.CLOUDINARY['cloud_name'],
        api_key=settings.CLOUDINARY['api_key'],
        api_secret=settings.CLOUDINARY['api_secret']
    )

    if _type == 'video':
        # Use upload_large for video files
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in file:
                temp_file.write(chunk)

            result = upload_large(
                temp_file.name,
                folder=folder_name,
                resource_type='video',
                chunk_size=6 * 1024 * 1024  # Set your preferred chunk size in bytes
            )

        duration = result.get("duration")
        return [result['secure_url'], duration]
    else:
        # Use regular upload for other file types
        result = upload(file, folder=folder_name)
        return result['secure_url']
