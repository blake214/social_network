from celery import shared_task
from .models import *
from PIL import Image as img
import io
from django.core.files.uploadedfile import SimpleUploadedFile

@shared_task
def make_gallery_thumbnail(record_pk):
    '''make_gallery_thumbnail
    A task listener. Creates a gallery thumbnail when a gallery_image is created

    Paramiters:
    pk: Is the user_gallery PK

    returns: Nothing
    '''
    record = UserGalleries.objects.get(pk=record_pk)
    image = img.open('images/'+str(record.gallery_image))
    x_scale_factor = image.size[0]/100
    thumbnail = image.resize((100, int(image.size[1]/x_scale_factor)))
    byteArr = io.BytesIO()
    thumbnail.save(byteArr, format='jpeg')
    file = SimpleUploadedFile("thumb_"+str(record.gallery_image), byteArr.getvalue())
    record.gallery_image_thumb = file
    record.save()

@shared_task
def make_profile_thumbnail(record_pk):
    '''make_profile_thumbnail
    A task listener. Creates a profile image thumbnail when a profile_image is created

    Paramiters:
    pk: Is the user_details PK

    returns: Nothing
    '''
    record = UserDetails.objects.get(pk=record_pk)
    image = img.open('images/'+str(record.profile_image))
    x_scale_factor = image.size[0]/100
    thumbnail = image.resize((100, int(image.size[1]/x_scale_factor)))
    byteArr = io.BytesIO()
    thumbnail.save(byteArr, format='jpeg')
    file = SimpleUploadedFile("thumb_"+str(record.profile_image), byteArr.getvalue())
    record.profile_image_thumb = file
    record.save()