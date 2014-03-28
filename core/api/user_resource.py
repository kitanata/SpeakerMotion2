import json
from tastypie.resources import ModelResource
from core.models import User
from core.tastypie import actionurls, action

from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as djlogout
from django.shortcuts import redirect

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']

    def prepend_urls(self):
        return actionurls(self)

    @action(name='login', allowed=['post'], static=True)
    def user_login(self, request, **kwargs):
        data = json.loads(request.body)

        email = data['email'].lower()
        password = data['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponse(json.dumps({'ok': True}), 
                    content_type="application/json", status=200)
            else:
                return HttpResponse(
                    json.dumps({'error': "account_disabled"}),
                    content_type="application/json", status=400)

        return HttpResponse(
            json.dumps({'error': "auth_failed"}),
            content_type="application/json", status=400)

    @action(allowed=['get'], static=True, require_loggedin=True)
    def logout(self, request, **kwargs):
        djlogout(request)

        return redirect('/')

    @action(allowed=['post'], static=True)
    def register(self, request, **kwargs):
        data = json.loads(request.body)

        email = data['email'].lower()
        full_name = data['full_name']

        password = data['password']
        confirm = data['confirm']

        if password != confirm:
            return HttpResponse(
                json.dumps({'error': "password_match"}),
                content_type="application/json", status=400)
        try:
            user = User.objects.create_user(email, password)
            user.full_name = full_name
            user.save()
        except IntegrityError:
            return HttpResponse(
                json.dumps({'error': "email_taken"}),
                content_type="application/json", status=400)

        return HttpResponse(json.dumps({'ok': True}), 
            content_type="application/json", status=200)


    @action(allowed=['post'], require_loggedin=True)
    def changepassword(self, request, **kargs):
        pass

    @action(allowed=['post'], static=True)
    def forgotpassword(self, request, **kwargs):
        pass
