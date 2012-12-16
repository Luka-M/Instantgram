from django.http import HttpResponse
from django.shortcuts import render_to_response
from main.qqFileUploader import qqFileUploader
from instantgram import settings
from django.views.decorators.csrf import csrf_exempt
from main.models import Image, Tag
from django.utils import timezone
import os
import base64
import md5


def index(request):
    return render_to_response("main/tagcloud.html", {"datetime" : timezone.now()})

def tag(request, tagtext):
    return render_to_response('main/images.html', {"tag":tagtext})

def upload(request):
    return render_to_response('main/upload.html')

@csrf_exempt
def upload2(request):
    """Get uploaded file from form."""
    uploaded = request.read
    fileSize = int(uploaded.im_self.META["CONTENT_LENGTH"])
    fileName = uploaded.im_self.META["HTTP_X_FILE_NAME"]    
    fileContent = uploaded(fileSize)
    
    """Write image to disk."""
    fn, ext = os.path.splitext(fileName)
    name = fn + timezone.now().strftime("%Y_%m_%d_%H_%M_%S_%f") + base64.urlsafe_b64encode(os.urandom(settings.SALT_LENGHT)) + ext
    fileHandler = open(settings.MEDIA_ROOT + "images/" + name, "wb")
    fileHandler.write(fileContent)
    fileHandler.close()
    
    """Create md5hash digest for image."""
    base64string = base64.b64encode(fileContent)
    mdfive = md5.new(base64string).hexdigest()
    
    """Write image data to db."""
    latitude = request.GET.get('lat')
    longitude = request.GET.get('lon')
    tags = request.GET.get('tags').split(' ')

    image = Image(title = name, md5hash = mdfive, pub_date = timezone.now(), lat = latitude, lon = longitude)
    image.save()

    for tagtext in tags:
        if Tag.objects.filter(name=tagtext).exists():
            t = Tag.objects.get(name=tagtext)
        else:
            t = Tag(name = tagtext)
            t.save()
        image.tags.add(t)
        image.save()

    return HttpResponse('{"success": true}')

def embed(request, tagtext):
    return render_to_response('main/embed.html', {"tag":tagtext})

def embedtest(request):
    return render_to_response('main/embedtest.html')
