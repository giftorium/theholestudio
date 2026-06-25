from django.contrib import admin
from django.utils.html import format_html
from .models import Production, CastMember, ProductionPhoto, ProductionVideo, ContactMessage, Founder, HomePage, HomePhoto, AboutPage


class CastMemberInline(admin.TabularInline):
    model = CastMember
    extra = 1
    fields = ['order', 'name', 'role']


class ProductionPhotoInline(admin.TabularInline):
    model = ProductionPhoto
    extra = 1
    fields = ['order', 'image', 'image_preview', 'caption']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:70px;object-fit:cover;">', obj.image.url)
        return '—'
    image_preview.short_description = 'Preview'


class ProductionVideoInline(admin.TabularInline):
    model = ProductionVideo
    extra = 1
    fields = ['order', 'title', 'embed_url']


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'date', 'venue', 'cover_preview']
    list_filter = ['status']
    search_fields = ['title', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CastMemberInline, ProductionVideoInline, ProductionPhotoInline]
    fieldsets = [
        (None, {'fields': ['title', 'slug', 'status']}),
        ('Details', {'fields': ['date', 'venue', 'duration', 'ticket_url']}),
        ('Content', {'fields': ['description', 'concept']}),
        ('Images', {'fields': ['cover_image', 'poster_image']}),
    ]

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="height:45px;object-fit:cover;">', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Cover'


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'order', 'photo_preview']
    list_editable = ['order']
    fields = ['order', 'name', 'role', 'bio', 'photo', 'photo_preview', 'website']
    readonly_fields = ['photo_preview']

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height:80px;width:80px;object-fit:cover;border-radius:4px;">',
                obj.photo.url
            )
        return '—'
    photo_preview.short_description = 'Preview'


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Branding', {'fields': ['logo']}),
        ('Hero', {'fields': ['hero_eyebrow', 'hero_tagline']}),
        ('Dark Band', {'fields': ['dark_band_heading', 'dark_band_body']}),
    ]

    def has_add_permission(self, request):
        return not HomePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomePhoto)
class HomePhotoAdmin(admin.ModelAdmin):
    list_display = ['photo_preview', 'caption', 'order']
    list_display_links = ['photo_preview']
    list_editable = ['caption', 'order']

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;object-fit:cover;">', obj.image.url)
        return '—'
    photo_preview.short_description = 'Preview'


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Header', {'fields': ['header_quote', 'header_intro']}),
        ('Stats', {'fields': [
            ('stat1_num', 'stat1_label'),
            ('stat2_num', 'stat2_label'),
            ('stat3_num', 'stat3_label'),
        ]}),
        ('Who We Are', {'fields': ['story_body']}),
        ('Land Acknowledgement', {'fields': ['land_acknowledgement']}),
        ('Our Approach — Value 1', {'fields': ['value1_label', 'value1_text']}),
        ('Our Approach — Value 2', {'fields': ['value2_label', 'value2_text']}),
        ('Our Approach — Value 3', {'fields': ['value3_label', 'value3_text']}),
        ('CTA', {'fields': ['cta_heading']}),
    ]

    def has_add_permission(self, request):
        return not AboutPage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['subject']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']

    def has_add_permission(self, request):
        return False
