from django.core.management.base import BaseCommand
from hubspot.models import HubspotAPIToken


class Command(BaseCommand):
    help = "Syncs the contacts from Hubspot"

    def handle(self, *args, **options):
        for token in HubspotAPIToken.objects.all():
            token.fetch_contacts()
