"""
Downloads dance / contemporary theatre demo photos from Pexels CDN.
Saves to core/static/core/img/demo/.
"""
import os
import requests
from django.core.management.base import BaseCommand
from django.conf import settings

# (filename, pexels_photo_id, width, height)
# All IDs are real Pexels photos in the dance/performance/theatre space.
PHOTOS = [
    # ── Production covers (portrait 3:4) ──────────────────────────────────
    ('cover_threshold.jpg',    5912320, 800, 1067),   # dancer on dark stage
    ('cover_body_archive.jpg', 1701194, 800, 1067),   # contemporary dancer
    ('cover_unground.jpg',     3355365, 800, 1067),   # dramatic stage light

    # ── Homepage photo strip (mix of portrait / landscape) ─────────────────
    ('strip_1.jpg', 1701195, 600, 800),   # dancer in studio
    ('strip_2.jpg', 6191462, 600, 960),   # performance on stage
    ('strip_3.jpg', 3822583, 600, 800),   # theatrical movement
    ('strip_4.jpg', 3799805, 600, 960),   # two performers

    # ── Production gallery photos ──────────────────────────────────────────
    ('gallery_1.jpg',  1701197, 900, 600),  # wide stage shot
    ('gallery_2.jpg',  2188012, 900, 600),  # movement study
    ('gallery_3.jpg',  4492129, 900, 600),  # contemporary dance
    ('gallery_4.jpg',  7991424, 900, 600),  # physical theatre
    ('gallery_5.jpg',  5912385, 900, 600),  # performer close
    ('gallery_6.jpg',  3990867, 900, 600),  # stage silhouette

    # ── About / founder portraits (portrait) ──────────────────────────────
    ('founder_jaber.jpg',  2531734, 600, 800),  # male dancer/artist
    ('founder_negar.jpg',  3361739, 600, 800),  # female dancer/artist
]

BASE = 'https://images.pexels.com/photos/{id}/pexels-photo-{id}.jpeg?auto=compress&cs=tinysrgb&w={w}&h={h}&fit=crop'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Referer': 'https://www.pexels.com/',
}


class Command(BaseCommand):
    help = 'Download demo dance/theatre photos for The Hole Studio'

    def handle(self, *args, **kwargs):
        out_dir = os.path.join(settings.BASE_DIR, 'core', 'static', 'core', 'img', 'demo')
        os.makedirs(out_dir, exist_ok=True)

        ok, fail = 0, []

        for filename, photo_id, w, h in PHOTOS:
            dest = os.path.join(out_dir, filename)
            url = BASE.format(id=photo_id, w=w, h=h)
            try:
                r = requests.get(url, headers=HEADERS, timeout=20)
                r.raise_for_status()
                if len(r.content) < 5000:
                    raise ValueError('Response too small — likely not a real image')
                with open(dest, 'wb') as f:
                    f.write(r.content)
                self.stdout.write(f'  OK  {filename}  ({len(r.content)//1024}kb)')
                ok += 1
            except Exception as e:
                self.stdout.write(f'  --  {filename}  FAILED: {e}')
                fail.append(filename)

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'{ok}/{len(PHOTOS)} downloaded'))
        if fail:
            self.stdout.write(self.style.WARNING('Failed: ' + ', '.join(fail)))
