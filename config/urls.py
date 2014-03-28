import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from tastypie.api import Api
from core.api import *

v1_api = Api(api_name='v1')

v1_api.register(UserResource())
v1_api.register(CampaignResource())
v1_api.register(ProposalResource())
v1_api.register(ReviewResource())
v1_api.register(SpeakerBiographyResource())
v1_api.register(TopicResource())

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'core.views.index'),
    url(r'^dashboard/$', 'core.views.dashboard'),

    url(r'^feedback/', include('feedback.urls')),
    url(r'^api/', include(v1_api.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url('^markdown/', include( 'django_markdown.urls')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
