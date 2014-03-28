from django.db import models

class Campaign(models.Model):
    name = models.CharField(max_length=140)
    code = models.CharField(max_length=32, default="")

    manager = models.ForeignKey('core.User', related_name='campaigns_i_manage')
    reviewers = models.ManyToManyField('core.User', related_name='campaigns_i_review')
    speakers = models.ManyToManyField('core.User', related_name='campaigns_applied_to')
    published = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'core'
        #states are 

    def __str__(self):
        return self.name
