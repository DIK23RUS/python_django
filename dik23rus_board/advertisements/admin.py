from django.contrib import admin
from .models import Advertisement, AdvertisementStatus, AdvertisementType, AdvertisementHeading, Author


# Register your models here.

@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementStatus)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementType)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(AdvertisementHeading)
class AdvertisementAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AdvertisementAdmin(admin.ModelAdmin):
    pass
