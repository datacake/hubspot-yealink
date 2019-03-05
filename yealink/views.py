import xml.etree.cElementTree as ET

import phonenumbers
from django.http import HttpResponse
from hubspot.models import HubspotContact


def phonebook(request):
    root = ET.Element("HubspotIPPhoneDirectory")

    for contact in HubspotContact.objects.all():
        entry = ET.SubElement(root, "DirectoryEntry")
        ET.SubElement(entry, "Name").text = f"{contact.first_name} {contact.last_name}"
        if contact.phone_number:
            number = phonenumbers.parse(contact.phone_number, "DE")
            ET.SubElement(entry, "Telephone").text = phonenumbers.format_number(
                number, phonenumbers.PhoneNumberFormat.E164
            )
            ET.SubElement(entry, "Telephone").text = phonenumbers.format_number(
                number, phonenumbers.PhoneNumberFormat.NATIONAL
            ).replace(" ", "")
        if contact.company:
            ET.SubElement(entry, "Company").text = contact.company

    return HttpResponse(ET.tostring(root), content_type="text/xml")
