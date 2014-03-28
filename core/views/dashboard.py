from core.helpers import template
from django.shortcuts import redirect

@template('dashboard.haml')
def dashboard(request):
    if request.user.is_anonymous():
        return redirect('/')

    return {}
