from tastypie.resources import ModelResource
from core.models import User
from core.tastypie import actionurls, action

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'post', 'put', 'delete']

    def prepend_urls(self):
        return actionurls(self)

    @action(name='login', allowed=['post'], static=True)
    def user_login(self, request, **kwargs):
        pass

    @action(allowed=['get'], require_loggedin=True)
    def logout(self, request, **kwargs):
        pass

    @action(allowed=['post'], static=True)
    def register(self, request, **kwargs):
        pass

    @action(allowed=['post'], require_loggedin=True)
    def changepassword(self, request, **kargs):
        pass

    @action(allowed=['post'], static=True)
    def forgotpassword(self, request, **kwargs):
        pass
