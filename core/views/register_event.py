from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.util import ErrorList
from django.template import loader, Context
from django.db import IntegrityError

from core.helpers import template, send_html_mail
from core.forms import EventRegisterForm
from core.models import SpkrbarUser, SpeakerProfile, EventProfile

email_template = loader.get_template('mail/register.html')

@template('auth/register_event.haml')
def register_event(request):
    if request.method == "POST":
        form = EventRegisterForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            confirm = form.cleaned_data['confirm']
            email = form.cleaned_data['email']

            if password != confirm:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("Password does not match confirmation.")

                return {'form': form}

            try:
                user = SpkrbarUser.objects.create_user(username, email, password)
                user.user_type = SpkrbarUser.USER_TYPE_EVENT
                user.save()
            except IntegrityError as e:
                errors = form._errors.setdefault("password", ErrorList())
                errors.append("That username is taken. Try another.")

                return {'form': form}

            profile = EventProfile()
            profile.user = user
            profile.name = name

            if 'description' in form.cleaned_data:
                profile.description = form.cleaned_data['description']

            profile.save()

            text = """
                Hi there! 
                
                I'm SpkrBot. I want to thank you for joining SpkrBar as a conference organizer. Did you know that with SpkrBar you can:

                <ul>
                    <li>Find and follow your favorite speakers</li>
                    <li>Find great talks</li>
                    <li>Recruit Speakers to speak at your events</li>
                    <li>Get in depth and high quality reviews on speakers that speak at your events</li>
                </ul>

                Oh, and before I forget, we are working on making the site better every day, so if you encounter any problems, have questions, or want to give us any feedback please send me an email and I'll automatically send it on to our developers. We read every email we get.

                Thanks again,
                SpkrBot @ Spkrbar.com
                """

            mes = email_template.render(Context({'message': text}))
            send_html_mail("Welcome to SpkrBar", text, mes, [user.email])

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect(request.user.get_profile().get_absolute_url())
    else:
        form = EventRegisterForm()

    return {'form': form}
