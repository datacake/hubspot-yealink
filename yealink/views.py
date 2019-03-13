import xml.etree.cElementTree as ET

import phonenumbers
from django.http import HttpResponse
from hubspot.models import HubspotContact


def phonebook(request):
    root = ET.Element("HubspotIPPhoneDirectory")

    for contact in HubspotContact.objects.all():
        if not contact.phone_number:
            continue
        entry = ET.SubElement(root, "DirectoryEntry")
        ET.SubElement(entry, "Name").text = f"{contact.first_name} {contact.last_name} ({contact.company})"
        number = phonenumbers.parse(contact.phone_number, "DE")
        ET.SubElement(entry, "Telephone").text = phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.E164
        )
        ET.SubElement(entry, "Telephone").text = phonenumbers.format_number(
            number, phonenumbers.PhoneNumberFormat.NATIONAL
        ).replace(" ", "")

    return HttpResponse(ET.tostring(root), content_type="text/xml")
