import datetime
from django.core.management.base import BaseCommand
from core.models import Production, CastMember, ProductionVideo, Founder


FOUNDERS = [
    {
        'name': 'Negar Nemati',
        'role': 'Co-Founder & Costume Designer',
        'bio': (
            'Negar Nemati is an award-winning Iranian-Canadian costume designer working across film, '
            'theatre, and performance. With more than seventeen years of international experience, she '
            'has collaborated with some of the most acclaimed voices in contemporary cinema and theatre, '
            'including Asghar Farhadi, Mani Haghighi, Matthew Rankin, and Amir Reza Koohestani.\n\n'
            'Her work is distinguished by a strong visual language, meticulous attention to detail, and '
            'a deep understanding of character, atmosphere, and storytelling. Nemati received the 2025 '
            'Canadian Screen Award for Achievement in Costume Design and the 2025 CAFTCAD Award for her '
            'work on Universal Language.\n\n'
            'As co-founder of the– hOle –studio, Nemati brings a multidisciplinary approach to '
            'performance-making, combining visual design, dramaturgical thinking, and international '
            'collaboration to develop new contemporary works for stage and screen.'
        ),
        'website': 'https://negarnemati.com/',
        'order': 0,
    },
    {
        'name': 'Jaber Ramezan',
        'role': 'Co-Founder & Artistic Director',
        'bio': (
            'Jaber Ramezan is an Iranian-born playwright, director, and choreographer whose work explores '
            'the intersection of the personal and political through contemporary performance. Working across '
            'theatre, dance, and film, he investigates new dramaturgies and interdisciplinary approaches '
            'that blur the boundaries between narrative, movement, and visual composition.\n\n'
            'Over the past fifteen years, his productions have been presented internationally across Iran, '
            'Europe, and Canada, including Swim Team at SummerWorks in Toronto and Boundaries of Bodies '
            'at Theatre de la Ville in Paris. A laureate of the Institut Francais x Cite internationale '
            'des arts residency in Paris, Ramezan also participated in Transmission Impossible, a '
            'choreographic research program at the 79th Festival d\'Avignon.\n\n'
            'He is the Co-Founder and Artistic Director of the– hOle –studio.'
        ),
        'website': 'https://jaberramezan.com',
        'order': 1,
    },
]


PRODUCTIONS = [
    {
        'title': 'The Chairs',
        'slug': 'the-chairs',
        'status': 'upcoming',
        'date': datetime.date(2026, 10, 24),
        'venue': 'MC93 – Maison de la Culture de Seine-Saint-Denis, Paris',
        'duration': '',
        'ticket_url': 'https://www.festival-automne.com/fr/edition-2026/jaber-ramezan-the-chairs',
        'description': (
            'Six performers move across an unstable landscape of chairs without ever touching the ground. '
            'Through balance, risk, and collective attention, The Chairs explores interdependence, care, '
            'and resilience through movement.\n\n'
            'World Premiere at Festival d\'Automne \xe0 Paris 2026, October 24–25.'
        ),
        'concept': (
            '"A performance for six performers moving entirely across a shifting landscape of chairs '
            'without touching the ground. Through silence, precision, and collective coordination, '
            'the work investigates balance, endurance, and interdependence. The chairs function as '
            'choreographic partners, generating new relationships between bodies, objects, and space." '
            '— Jaber Ramezan'
        ),
        'cast': [
            ('Jaber Ramezan', 'Concept, Creation & Choreography'),
        ],
        'videos': [],
    },
    {
        'title': 'Boundaries of Bodies',
        'slug': 'boundaries-of-bodies',
        'status': 'past',
        'date': datetime.date(2025, 3, 1),
        'venue': 'Th\xe9\xe2tre de la Ville – Les Abbesses, Paris',
        'duration': '',
        'ticket_url': '',
        'description': (
            'Boundaries of Bodies is a contemporary performance exploring the invisible forces that '
            'shape, limit, and transform human bodies. Through movement, theatrical composition, and '
            'collective physicality, six performers navigate questions of resistance, conformity, and '
            'personal agency within social and political structures.\n\n'
            'Selected for the 2024 edition of Danse \xc9largie, the international choreography competition '
            'presented by Th\xe9\xe2tre de la Ville–Paris, the work was presented in 2025 as part of Focus '
            'Jeunes Cr\xe9ateurs – G\xe9n\xe9rations Danse \xc9largie at Th\xe9\xe2tre de la Ville – Les Abbesses.'
        ),
        'concept': (
            '"Boundaries of Bodies investigates the invisible forces that shape, limit, and transform '
            'human bodies — questions of resistance, conformity, and personal agency within social '
            'and political structures." — Jaber Ramezan'
        ),
        'cast': [
            ('Jaber Ramezan', 'Concept, Direction & Choreography'),
            ('Parastoo Amanzadeh', 'Performer'),
            ('Mohsen Karimi', 'Performer'),
            ('Dorsa Panjeband', 'Performer'),
            ('Hamed Rajaei', 'Performer'),
            ('Hasti Taraghi', 'Performer'),
            ('Sourena Zahedi', 'Performer'),
            ('Saba Kasmaie', 'Lighting Design'),
            ('Negar Nemati', 'Costume Design'),
            ('Behrang Najafi', 'Sound Design'),
        ],
        'videos': [],
    },
    {
        'title': 'Edge-Raw',
        'slug': 'edge-raw',
        'status': 'past',
        'date': None,
        'venue': 'Toronto, Canada',
        'duration': '',
        'ticket_url': '',
        'description': (
            'Edge-Raw is a Toronto-based performance laboratory exploring improvisation, movement '
            'research, and contemporary performance practices. Directed by Jaber Ramezan, the project '
            'brings together artists and participants in a shared space for experimentation, embodied '
            'inquiry, and the development of new performative languages.\n\n'
            'Through workshops, laboratories, and public presentations, Edge-Raw investigates the '
            'relationship between body, space, presence, and collective creation, bringing together '
            'newcomer, emerging, and interdisciplinary artists across Toronto\'s diverse artistic community.'
        ),
        'concept': '',
        'cast': [
            ('Jaber Ramezan', 'Founder & Artistic Director'),
        ],
        'videos': [],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with real Hole Studio data'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Delete existing data and reseed')

    def handle(self, *args, **kwargs):
        if kwargs['flush']:
            Production.objects.all().delete()
            Founder.objects.all().delete()
            self.stdout.write('Flushed existing data.')

        if Production.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Run with --flush to reset.'))
            return

        for data in FOUNDERS:
            Founder.objects.create(**data)
            self.stdout.write(f'Created founder: {data["name"]}')

        for data in PRODUCTIONS:
            cast = data.pop('cast')
            videos = data.pop('videos')
            prod = Production.objects.create(**data)
            self.stdout.write(f'Created: {prod.title}')
            for i, (name, role) in enumerate(cast):
                CastMember.objects.create(production=prod, name=name, role=role, order=i)
            for i, (title, url) in enumerate(videos):
                from core.models import ProductionVideo
                ProductionVideo.objects.create(production=prod, title=title, embed_url=url, order=i)

        self.stdout.write(self.style.SUCCESS('\nDone. Productions and founders seeded.'))
