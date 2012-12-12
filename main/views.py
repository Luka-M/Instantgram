from django.http import HttpResponse
from django.shortcuts import render_to_response
from main.qqFileUploader import qqFileUploader
from instantgram import settings
from django.views.decorators.csrf import csrf_exempt
import sys
from main.models import Image
from django.utils import timezone
import os
import main

def index(request):
    return render_to_response("main/tagcloud.html")

def tag(request, tagtext):
    return render_to_response('main/images.html', {"tag":tagtext})

def upload(request, tagtext):
    return render_to_response('main/upload.html', {"tag":tagtext})

@csrf_exempt
def upload2(request, tagtext):
    #print >>sys.stderr, ':::::::::::::::::::::::::::::::::::::::'
    allowedExtension = [".jpg", ".png"]
    sizeLimit = 10024000
    uploader = qqFileUploader(allowedExtension, sizeLimit)
    filename = request.read.im_self.META["HTTP_X_FILE_NAME"]
    im = Image(title='random', url= '/static/' + filename, pub_date=timezone.now(), geolocation='', tag=tagtext)
    im.save()
	
    return HttpResponse(uploader.handleUpload(request, os.path.join(os.path.dirname(main.__file__), 'static') ))