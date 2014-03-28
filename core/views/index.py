from core.helpers import template
from django.shortcuts import redirect

@template('index.haml')
def index(request):
    if not request.user.is_anonymous():
        return redirect('/dashboard')
    return {}
