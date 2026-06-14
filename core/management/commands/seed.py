import datetime
from django.core.management.base import BaseCommand
from core.models import Production, CastMember, ProductionVideo, ContactMessage


PRODUCTIONS = [
    {
        'title': 'Threshold',
        'slug': 'threshold',
        'status': 'upcoming',
        'date': datetime.date(2026, 9, 18),
        'venue': 'Factory Theatre, Toronto',
        'duration': '70 minutes, no intermission',
        'ticket_url': 'https://factorytheatre.ca',
        'description': (
            'Threshold is a new work for three performers, built from the question of what the body '
            'carries across borders — physical, emotional, linguistic. The piece unfolds in near-silence, '
            'interrupted by bursts of language that never quite resolve into meaning.\n\n'
            'The work draws on the personal histories of the performers alongside text derived from '
            'immigration documents, letters, and testimonies. It is quiet in the way that only '
            'devastation can be quiet.'
        ),
        'concept': (
            '"We were interested in the idea of the threshold not as a line you cross but as a place '
            'you live in. The work is for everyone who has been caught in that in-between." '
            '— Jaber Ramezani'
        ),
        'cast': [
            ('Jaber Ramezani', 'Choreography & Performance'),
            ('Negar Nemati', 'Performance & Dramaturgy'),
            ('Shirin Raad', 'Performance'),
            ('Amir Kouhestani', 'Lighting Design'),
            ('Sara Fattahi', 'Sound Design'),
        ],
        'videos': [
            ('Threshold — Teaser', 'https://www.youtube.com/embed/dQw4w9WgXcQ'),
        ],
    },
    {
        'title': 'Body / Archive',
        'slug': 'body-archive',
        'status': 'past',
        'date': datetime.date(2025, 3, 22),
        'venue': 'Harbourfront Centre, Toronto',
        'duration': '55 minutes',
        'ticket_url': '',
        'description': (
            'Body / Archive excavates the gap between what the body remembers and what '
            'documentation records. Working with personal objects, recorded voice, and an '
            'accumulative movement vocabulary, the piece asks: whose version of events does '
            'the archive trust?\n\n'
            'Performed across two nights as part of the Harbourfront Centre\'s World Stage program, '
            'the work received its Toronto premiere after a residency at the National Arts Centre.'
        ),
        'concept': (
            '"The archive is not neutral. We wanted to make that visible — to put a body in the room '
            'with the document and let them argue." — Negar Nemati'
        ),
        'cast': [
            ('Jaber Ramezani', 'Choreography & Performance'),
            ('Negar Nemati', 'Choreography & Performance'),
            ('Roxanna Sadeghi', 'Costume Design'),
            ('Amir Kouhestani', 'Lighting Design'),
        ],
        'videos': [
            ('Body / Archive — Full Documentation', 'https://www.youtube.com/embed/dQw4w9WgXcQ'),
            ('Body / Archive — Artist Talk', 'https://www.youtube.com/embed/dQw4w9WgXcQ'),
        ],
    },
    {
        'title': 'Unground',
        'slug': 'unground',
        'status': 'past',
        'date': datetime.date(2024, 6, 14),
        'venue': 'Luminato Festival, Toronto',
        'duration': '40 minutes',
        'ticket_url': '',
        'description': (
            'Unground was The Hole Studio\'s debut work — a site-specific piece created for the '
            'outdoor courtyard of Hearn Generating Station during Luminato 2024.\n\n'
            'Four performers and a sound score built from field recordings and processed breath. '
            'The ground is never where you expect it. The audience stood, moved, or sat as the '
            'piece unfolded around them.'
        ),
        'concept': (
            '"We had no studio, no budget, no track record. We had a question and a space and each other. '
            'Unground came from that — from necessity." — Jaber Ramezani'
        ),
        'cast': [
            ('Jaber Ramezani', 'Choreography & Performance'),
            ('Negar Nemati', 'Performance'),
            ('Leila Moafi', 'Performance'),
            ('Dara Nazari', 'Sound Design'),
        ],
        'videos': [
            ('Unground — Documentation', 'https://www.youtube.com/embed/dQw4w9WgXcQ'),
        ],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with dummy Hole Studio productions'

    def handle(self, *args, **kwargs):
        if Production.objects.exists():
            self.stdout.write(self.style.WARNING('Productions already exist. Run with --flush to reset.'))
            return

        for data in PRODUCTIONS:
            cast = data.pop('cast')
            videos = data.pop('videos')

            prod = Production.objects.create(**data)
            self.stdout.write(f'Created: {prod.title}')

            for i, (name, role) in enumerate(cast):
                CastMember.objects.create(production=prod, name=name, role=role, order=i)

            for i, (title, url) in enumerate(videos):
                ProductionVideo.objects.create(production=prod, title=title, embed_url=url, order=i)

        self.stdout.write(self.style.SUCCESS('\nDone. 3 productions seeded.'))
