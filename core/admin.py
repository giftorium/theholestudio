from django.contrib import admin
from .models import Production, CastMember, ProductionPhoto, ProductionVideo, ContactMessage


class CastMemberInline(admin.TabularInline):
    model = CastMember
    extra = 1


class ProductionPhotoInline(admin.TabularInline):
    model = ProductionPhoto
    extra = 1


class ProductionVideoInline(admin.TabularInline):
    model = ProductionVideo
    extra = 1


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'date', 'venue']
    list_filter = ['status']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CastMemberInline, ProductionVideoInline, ProductionPhotoInline]


@admin.register(CastMember)
class CastMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'production', 'order']
    list_editable = ['order']
    list_filter = ['production']


@admin.register(ProductionPhoto)
class ProductionPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'production', 'caption', 'order']
    list_editable = ['order', 'caption']
    list_filter = ['production']


@admin.register(ProductionVideo)
class ProductionVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'production', 'order']
    list_editable = ['order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at']
    list_filter = ['subject']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
