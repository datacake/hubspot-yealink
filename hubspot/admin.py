from django.contrib import admin
from .models import HubspotAPIToken, HubspotContact


@admin.register(HubspotAPIToken)
class HubspotAPITokenAdmin(admin.ModelAdmin):
    pass


@admin.register(HubspotContact)
class HubspotContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company", "phone_number")
