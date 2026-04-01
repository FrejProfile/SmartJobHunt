from django.db import models

class Visited(models.Model):
    url        = models.URLField(unique=True)
    first_seen = models.DateTimeField(auto_now_add=True)

class Job(models.Model):
    STATUS_CHOICES = [
        ('potential', 'Potential'),
        ('applied', 'Applied'),
        ('ranked', 'Ranked'),
    ]
    visited    = models.OneToOneField(Visited, on_delete=models.CASCADE)
    employer   = models.CharField(max_length=255, blank=True)
    title      = models.CharField(max_length=255, blank=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='potential')
    snippet    = models.TextField(blank=True)
    employer_url = models.URLField(blank=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

class RankedJob(models.Model):
    job        = models.OneToOneField(Job, on_delete=models.CASCADE)
    score      = models.IntegerField()
    html       = models.TextField()
    scored_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['score'])]