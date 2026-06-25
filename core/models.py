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


class HomePage(models.Model):
    logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Nav logo image. Leave blank to use text.')
    hero_eyebrow = models.CharField(max_length=200, default='Contemporary Dance & Theatre · Toronto, Canada')
    hero_tagline = models.CharField(max_length=300, blank=True, default='Work that lives in the body.\nQuestions the archive refuses.')
    dark_band_heading = models.CharField(max_length=200, default='Work that refuses to settle')
    dark_band_body = models.TextField(blank=True, default='the– hOle –studio is an independent dance, performance, and film company founded by Iranian artists Jaber Ramezan and Negar Nemati, based in Toronto. Building on more than fifteen years of practice, the studio develops original works that move between disciplines, cultures, and performance traditions.\n\nThe studio is available for presentations, co-productions, and residencies. If you\'re a festival, presenter, or venue — we\'d like to hear from you.')

    class Meta:
        verbose_name = 'Home Page'
        verbose_name_plural = 'Home Page'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Home Page'


class AboutPage(models.Model):
    # Header
    header_quote = models.CharField(max_length=300, default='"We believe that every project demands its own form."')
    header_intro = models.TextField(blank=True, default='the– hOle –studio is an independent dance, performance, and film company founded by Iranian artists Jaber Ramezan and Negar Nemati, based in Toronto. The studio develops original works that move between disciplines, cultures, and performance traditions.')

    # Stats
    stat1_num   = models.CharField(max_length=20, default='15+')
    stat1_label = models.CharField(max_length=100, default='Years of Practice')
    stat2_num   = models.CharField(max_length=20, default='3')
    stat2_label = models.CharField(max_length=100, default='Productions')
    stat3_num   = models.CharField(max_length=20, default='3')
    stat3_label = models.CharField(max_length=100, default='Countries')

    # Story
    story_body = models.TextField(blank=True, default='the– hOle –studio is an independent dance, performance, and film company founded by Iranian artists Jaber Ramezan and Negar Nemati. Building on more than fifteen years of artistic practice across theatre, dance, film, and design, the studio develops original works that move between disciplines, cultures, and performance traditions.\n\nRooted in the experimental spirit of Tehran\'s independent arts scene and shaped by international collaborations across Europe and North America, the company brings together artists, performers, filmmakers, and designers to create contemporary works for stage and screen.\n\nLed by Artistic Director Jaber Ramezan, the studio is driven by a search for new forms of performance and storytelling. Its projects emerge through research, collaboration, and experimentation, often crossing the boundaries between theatre, choreography, cinema, and visual design.')

    # Land acknowledgement
    land_acknowledgement = models.TextField(blank=True, default='the– hOle –studio acknowledges that our work takes place on the traditional territories of many Indigenous Nations, including the Wendat, the Anishinaabeg, the Mississaugas of the Credit First Nation, and the Haudenosaunee Confederacy. We recognize their enduring presence, stewardship, and relationships to this land, and we are committed to ongoing learning, respect, and meaningful dialogue.')

    # Values
    value1_label = models.CharField(max_length=100, default='Form First')
    value1_text  = models.TextField(blank=True, default='We believe that every project demands its own form. Rather than working within fixed genres or disciplines, we approach creation as a process of research and discovery.')
    value2_label = models.CharField(max_length=100, default='Memory & the Body')
    value2_text  = models.TextField(blank=True, default='Influenced by contemporary performance, choreography, cinema, and documentary practices, we are interested in memory, spectatorship, the body, and the ways personal experience intersects with larger social and political realities.')
    value3_label = models.CharField(max_length=100, default='International Exchange')
    value3_text  = models.TextField(blank=True, default='Through performances, films, workshops, and artistic laboratories, the studio creates spaces for encounter, exchange, and creative risk-taking, connecting contemporary artistic voices across different geographies, disciplines, and communities.')

    # CTA
    cta_heading = models.CharField(max_length=200, default='Interested in presenting our work?')

    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Page'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'About Page'


class HomePhoto(models.Model):
    home_page = models.ForeignKey('HomePage', on_delete=models.CASCADE, related_name='photos', default=1)
    image = models.ImageField(upload_to='home/strip/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption or f'Photo {self.order + 1}'


class Founder(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.ImageField(upload_to='founders/', blank=True, null=True)
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ContactPage(models.Model):
    intro_text = models.TextField(blank=True, default="We're interested in hearing from presenters, festivals, venues, and press. Fill out the form and we'll get back to you shortly.")
    booking_desc = models.TextField(blank=True, default="Festivals, venues, and presenters interested in hosting a production or commissioning new work.")
    press_desc = models.TextField(blank=True, default="Media inquiries, interviews, and press accreditation for upcoming performances.")
    general_desc = models.TextField(blank=True, default="Collaborations, residencies, and anything in between.")
    location = models.CharField(max_length=200, blank=True, default="Toronto, Canada")

    class Meta:
        verbose_name = 'Contact Page'
        verbose_name_plural = 'Contact Page'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Contact Page'


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
