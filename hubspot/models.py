import uuid
import requests
import time

from django.db import models


class HubspotAPIToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.CharField(max_length=255)

    def fetch_contacts(self):
        has_more = True
        vid_offset = 0
        while has_more:
            response = requests.get(
                f"https://api.hubapi.com/contacts/v1/lists/all/contacts/all?hapikey={self.token}&count=100&property=phone&property=firstname&property=lastname&property=company&vidOffset={vid_offset}"
            ).json()
            vid_offset = response["vid-offset"]
            has_more = response["has-more"]

            for contact in response["contacts"]:
                HubspotContact.objects.update_or_create(
                    portal_id=contact["profile-token"],
                    defaults={
                        "first_name": contact["properties"].get("firstname", {}).get('value', ''),
                        "last_name": contact["properties"].get("lastname", {}).get('value', ''),
                        "company": contact["properties"].get("company", {}).get('value', ''),
                        "phone_number": contact["properties"].get("phone", {}).get('value', ''),
                    },
                )

            if has_more:
                time.sleep(1)


class HubspotContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portal_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.company}"

