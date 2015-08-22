from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255, default='')
    timestamp = models.DateTimeField(blank=True, db_index=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        db_table = 'hackathon_event'