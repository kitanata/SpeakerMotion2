from django.contrib import admin
from core.models import *

admin.site.register(SpkrbarUser, admin.ModelAdmin)
admin.site.register(Event, admin.ModelAdmin)
admin.site.register(Proposal, admin.ModelAdmin)
admin.site.register(Review, admin.ModelAdmin)
admin.site.register(SpeakerBiography, admin.ModelAdmin)
admin.site.register(Topic, admin.ModelAdmin)
