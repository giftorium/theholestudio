from pathlib import Path
from io import BytesIO
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from PIL import Image
from core.models import Photo, Event

MAX_SIZE = 1920
QUALITY = 85
SUPPORTED = {'.jpg', '.jpeg', '.png', '.webp'}


class Command(BaseCommand):
    help = 'Upload real event photos from a local folder, replacing all existing ones'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str, help='Path to folder containing photos')

    def handle(self, *args, **options):
        folder = Path(options['folder'])

        if not folder.exists() or not folder.is_dir():
            raise CommandError(f'Folder not found: {folder}')

        event = Event.objects.first()
        if not event:
            raise CommandError('No event in DB. Run "python manage.py seed" first.')

        files = sorted([f for f in folder.iterdir() if f.suffix.lower() in SUPPORTED])
        if not files:
            raise CommandError(f'No supported images found in {folder}')

        # Delete existing photos
        existing = Photo.objects.filter(event=event).count()
        self.stdout.write(f'Deleting {existing} existing photos...')
        Photo.objects.filter(event=event).delete()

        # Upload new ones
        self.stdout.write(f'Found {len(files)} images. Resizing and uploading to Cloudinary...\n')
        success = 0

        for i, filepath in enumerate(files):
            try:
                img = Image.open(filepath)

                # Convert to RGB (handles PNG transparency, palette mode, etc.)
                if img.mode not in ('RGB',):
                    img = img.convert('RGB')

                # Resize — keeps aspect ratio, won't upscale
                img.thumbnail((MAX_SIZE, MAX_SIZE), Image.LANCZOS)

                # Compress into buffer
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=QUALITY, optimize=True)
                buffer.seek(0)

                original_kb = filepath.stat().st_size // 1024
                compressed_kb = buffer.getbuffer().nbytes // 1024

                photo = Photo(event=event, order=i)
                photo.image.save(f'feedback_{i + 1}.jpg', ContentFile(buffer.read()), save=True)

                self.stdout.write(
                    f'  ✓ [{i + 1}/{len(files)}] {filepath.name} '
                    f'({original_kb}KB → {compressed_kb}KB)'
                )
                success += 1

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ✗ [{i + 1}/{len(files)}] {filepath.name} failed: {e}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone. {success}/{len(files)} photos uploaded to Cloudinary.'))
