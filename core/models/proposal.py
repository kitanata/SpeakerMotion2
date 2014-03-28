from django.db import models

class Proposal(models.Model):
    user = models.ForeignKey('core.User', related_name='proposals')
    campaign = models.ForeignKey('core.Campaign', related_name='proposals')

    name = models.CharField(max_length=400)
    abstract = models.TextField()
    topics = models.ManyToManyField('core.Topic', related_name='proposals')
    biography = models.ForeignKey('core.SpeakerBiography', related_name='proposals')

    accepted = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'core'
        #states are 

    def __str__(self):
        return self.name
