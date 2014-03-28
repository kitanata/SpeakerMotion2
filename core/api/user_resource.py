import json
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
from core.models import User
from core.tastypie import actionurls, action

from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as djlogout
from django.shortcuts import redirect

class UserObjectsAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(is_active=True)

    def read_detail(self, object_list, bundle):
        return bundle.obj.is_active

    def create_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no creations.")

    def create_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no creations.")

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj == bundle.request.user and obj.is_active:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user and bundle.obj.is_active

    def delete_list(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        if bundle.obj == bundle.request.user:
            bundle.obj.is_active = False
        else:
            raise Unauthorized("Sorry, no deletes.")


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = UserObjectsAuthorization()

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
