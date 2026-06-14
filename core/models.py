from django.db import models
from django.utils.text import slugify


class Production(models.Model):
    STATUS_CHOICES = [('upcoming', 'Upcoming'), ('past', 'Past')]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True)
    concept = models.TextField(blank=True, help_text="Artist statement / concept note")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=300, blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. 75 minutes")
    ticket_url = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to='productions/covers/', blank=True, null=True)
    poster_image = models.ImageField(upload_to='productions/posters/', blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CastMember(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='cast')
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='cast/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ProductionPhoto(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='productions/photos/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Photo {self.id} — {self.production.title}"


class ProductionVideo(models.Model):
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    embed_url = models.URLField(help_text="YouTube or Vimeo embed URL")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


SUBJECT_CHOICES = [
    ('general', 'General'),
    ('booking', 'Booking'),
    ('press', 'Press'),
]


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=10, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_subject_display()}) — {self.created_at.strftime('%Y-%m-%d')}"
