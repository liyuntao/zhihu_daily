from django.db import models

class News(models.Model):
    id = models.IntegerField('id', primary_key=True)
    title = models.CharField(max_length=200)
    share_url = models.CharField(max_length=200)
    api_url = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    image_source = models.CharField(max_length=100)
    date = models.CharField(max_length=10)
    seq = models.IntegerField()
    def __unicode__(self):
        return self.title
