from django.db import models

class Review(models.Model):
    user = models.ForeignKey('core.User', related_name='reviews')
    proposal = models.ForeignKey('core.Proposal', related_name='reviews')
    reviewed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    #(How skilled is the speaker in the topic?)e
    expertise = models.IntegerField(default=0)

    #(How relevant is the topic to the event?)
    relevance = models.IntegerField(default=0)

    #(How experienced is the speaker at speaking?)
    performance = models.IntegerField(default=0)

    #(How positively will the audience respond?)
    response = models.IntegerField(default=0)

    class Meta:
        app_label = 'core'
        #states are 

    def __str__(self):
        return self.name
