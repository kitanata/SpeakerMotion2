from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=400)
    deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'core'
        #states are 

    def __str__(self):
        return self.name
