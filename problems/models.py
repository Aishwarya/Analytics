from django.db import models

class Submission(models.Model):
    status = models.CharField(choices=(), max_length=50, db_index=True)
    timestamp = models.DateTimeField(blank=True, db_index=True)

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        db_table = 'hackathon_submission'