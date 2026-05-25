from django.contrib import admin
from .models import Event, Artist, Photo, Video, ContactMessage


class ArtistInline(admin.TabularInline):
    model = Artist
    extra = 1


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1


class VideoInline(admin.TabularInline):
    model = Video
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'location']
    inlines = [ArtistInline, VideoInline, PhotoInline]


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'event', 'order']
    list_editable = ['order']
    list_filter = ['event']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'caption', 'order']
    list_editable = ['order', 'caption']
    list_filter = ['event']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'order']
    list_editable = ['order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    readonly_fields = ['name', 'email', 'message', 'created_at']
