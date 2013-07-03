from datetime import datetime

from django.db import models

class Notification(models.Model):
    user = models.ForeignKey('core.SpkrbarUser')
    message = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.now())

    class Meta:
        app_label = 'core'

    @classmethod
    def create(klass, profile, message):
        note = klass()
        note.profile = profile
        note.message = message
        note.save()

        return note