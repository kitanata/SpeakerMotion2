from django.db import models

class SpeakerBiography(models.Model):
    user = models.ForeignKey('core.User', related_name='biographies')
    biography = models.TextField()
    photo = models.ImageField(upload_to="photo", blank=True)

    class Meta:
        app_label = 'core'
        #states are 

    def __str__(self):
        return self.name
