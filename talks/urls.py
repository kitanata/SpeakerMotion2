from django.conf.urls import patterns, url

from views import TalkDetail, TalkTagList, TalkTagDetail
from views import TalkLinkList, TalkLinkDetail, TalkSlideDeckDetail
from views import TalkVideoDetail

urlpatterns = patterns('',

    url(r'^rest/talk_tag/(?P<pk>\d+)$', TalkTagDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/talk_tag$', TalkTagDetail.as_view(
        actions={'post': 'create'})),
    url(r'^rest/talk_tags$', TalkTagList.as_view()),

    url(r'^rest/talk_link/(?P<pk>\d+)$', TalkLinkDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/talk_link$', TalkLinkDetail.as_view(
        actions={'post': 'create'})),
    url(r'^rest/talk_links$', TalkLinkList.as_view()),

    url(r'^rest/talk_slide/(?P<pk>\d+)$', TalkSlideDeckDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/talk_slide$', TalkSlideDeckDetail.as_view(
        actions={'post': 'create'})),

    url(r'^rest/talk_video/(?P<pk>\d+)$', TalkVideoDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),
    url(r'^rest/talk_video$', TalkVideoDetail.as_view(
        actions={'post': 'create'})),

    url(r'^rest/talk/(?P<pk>\d*)$', TalkDetail.as_view(
        actions={'get': 'retrieve', 'put': 'update', 'delete':'destroy'})),

    url(r'^talk/new$', 'talks.views.talk_new'),
    url(r'^talk/(?P<talk_id>\d+)$', 'talks.views.talk_detail'),
    url(r'^talk/(?P<talk_id>\d+)/edit$', 'talks.views.talk_edit'),
    url(r'^talk/(?P<talk_id>\d+)/delete$', 'talks.views.talk_delete'),

    url(r'^talk/(?P<talk_id>\d+)/comment/new$', 'talks.views.talk_comment_new'),
    url(r'^talk/(?P<talk_id>\d+)/rate$', 'talks.views.talk_rate_new'),
    url(r'^talk/(?P<talk_id>\d+)/endorse$', 'talks.views.talk_endorsement_new'),

    url(r'^talk/(?P<talk_id>\d+)/slides/new$', 'talks.views.talk_slides_new'),
    url(r'^talk/(?P<talk_id>\d+)/video/new$', 'talks.views.talk_video_new'),
)
