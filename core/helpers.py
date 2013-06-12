import uuid
import os
from config.settings import MEDIA_ROOT

from django.shortcuts import render_to_response
from django.template import RequestContext

def save_photo_with_uuid(photo):
    photo_ext = photo.name.split('.')[-1]
    photo_root_name = str(uuid.uuid4()) + '.' + photo_ext
    photo_name = os.path.join('photo', photo_root_name)
    photo_storage = os.path.join(MEDIA_ROOT, 'photo', photo_root_name)

    with open(photo_storage, 'wb+') as destination:
        for chunk in photo.chunks():
            destination.write(chunk)

    return photo_name


def render_to(request, template, js=None, context=None):

    if js and context:
        context['js'] = js
    elif js:
        context = dict(js=js)

    return render_to_response(template, context, 
            context_instance=RequestContext(request))