import requests
import datetime
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from core.models import Event, Artist, Photo, Video

ARTISTS = [
    ('Kian Sadeghi',    'Visual Artist',      'Kian works with projection and generative visuals, crafting real-time environments that respond to sound.'),
    ('Roya Mohebbi',    'Sound Designer / DJ','Roya builds sonic landscapes that blur the line between club music and experimental composition.'),
    ('Dara Nazari',     'Light Installation', 'Dara constructs light structures that transform architectural space into an instrument of perception.'),
    ('Shirin Hosseini', 'DJ / Producer',      'Shirin curates extended sets that move through ambient, techno, and everything in between.'),
]

# Mixed portrait and landscape seeds for visual variety in masonry
PHOTO_SEEDS = [
    ('seed/feedback1/800/1100',  'portrait'),
    ('seed/feedback2/1100/800',  'landscape'),
    ('seed/feedback3/900/900',   'square'),
    ('seed/feedback4/800/1150',  'portrait'),
    ('seed/feedback5/1100/750',  'landscape'),
    ('seed/feedback6/850/1100',  'portrait'),
    ('seed/feedback7/1000/800',  'landscape'),
    ('seed/feedback8/800/1000',  'portrait'),
    ('seed/feedback9/1100/820',  'landscape'),
    ('seed/feedback10/820/1100', 'portrait'),
    ('seed/feedback11/900/750',  'landscape'),
    ('seed/feedback12/800/1050', 'portrait'),
]


class Command(BaseCommand):
    help = 'Seed the database with dummy Feedback event content'

    def handle(self, *args, **kwargs):
        if Event.objects.exists():
            self.stdout.write(self.style.WARNING('Event already exists. Delete it first to re-seed.'))
            return

        self.stdout.write('Creating Feedback event...')
        event = Event.objects.create(
            name='Feedback',
            tagline='A convergence of light, sound, and space',
            description=(
                'Feedback was a one-night multidisciplinary event bringing together light designers, '
                'visual artists, sound designers, and DJs to transform an industrial space into a living, '
                'breathing environment. Every element — the architecture, the sound, the light — was designed '
                'to interact. The result was something that resisted easy categorization: not quite a concert, '
                'not quite an exhibition, but a shared experience of all senses at once.'
            ),
            date=datetime.date(2024, 11, 15),
            location='Tehran, Iran',
        )

        self.stdout.write('Creating artists...')
        for i, (name, role, bio) in enumerate(ARTISTS):
            Artist.objects.create(event=event, name=name, role=role, bio=bio, order=i)

        self.stdout.write('Downloading and uploading photos to Cloudinary...')
        for i, (path, _) in enumerate(PHOTO_SEEDS):
            url = f'https://picsum.photos/{path}'
            try:
                res = requests.get(url, timeout=15)
                res.raise_for_status()
                photo = Photo(event=event, order=i)
                photo.image.save(f'feedback_{i+1}.jpg', ContentFile(res.content), save=True)
                self.stdout.write(f'  ✓ Photo {i+1}/{len(PHOTO_SEEDS)}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ Photo {i+1} failed: {e}'))

        self.stdout.write('Creating placeholder videos...')
        Video.objects.create(
            event=event,
            title='Feedback — Highlights',
            embed_url='https://www.youtube.com/embed/jfKfPfyJRdk',
            order=0,
        )
        Video.objects.create(
            event=event,
            title='Feedback — Aftermovie',
            embed_url='https://www.youtube.com/embed/jfKfPfyJRdk',
            order=1,
        )

        self.stdout.write(self.style.SUCCESS('\nDone. Feedback event seeded successfully.'))
