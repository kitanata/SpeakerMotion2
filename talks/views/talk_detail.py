from datetime import datetime

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from events.models import Event
from core.models import SpkrbarUser
from core.helpers import template

from talks.models import Talk
from talks.forms import TalkRatingForm, TalkLinkForm

@template('talks/talk_detail.haml')
def talk_detail(request, talk_id):
    talk = get_object_or_404(Talk, pk=talk_id)

    engagements = talk.engagements.all()

    upcoming = engagements.filter(date__gt=datetime.today())
    past = engagements.filter(date__lt=datetime.today())

    user_endorsed = False
    user_rated = False
    will_have_links = False

    if not request.user.is_anonymous():
        user_endorsed = (request.user in talk.endorsements.all())
        user_rated = (request.user in [x.rater for x in talk.ratings.all()])

        will_have_links = True

    photos = talk.talkphoto_set.all()

    photo_col = []
    for photo in photos:
        width = photo.width
        height = photo.height
        aspect = width / height if height != 0 else 0
        width = min(width, 200)
        photo_col.append((photo.photo, width, width * aspect))

    events = Event.objects.all()

    rating_form = TalkRatingForm()
    link_form = TalkLinkForm()

    return {
        'last': talk.get_absolute_url(),
        'talk': talk,
        'photos': photo_col,
        'upcoming': upcoming,
        'past': past,
        'user_endorsed': user_endorsed,
        'user_rated': user_rated,
        'will_have_links': will_have_links,
        'events': events,
        'rating_form': rating_form,
        'link_form': link_form,
        }
