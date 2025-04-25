from django.test import TestCase, Client
from django.urls import reverse
from contacts.models.contact import Contact


class ContactFlowTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_htmx_create_contact_returns_card_and_saves(self):
        resp = self.client.post(
            reverse("contacts:create"),
            {"name": "contact1", "email": "contact1@example.com"},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'id="contact-1"')
        self.assertTrue(Contact.objects.filter(email="contact1@example.com").exists())

    def test_htmx_delete_contact_removes_and_swaps(self):
        c = Contact.objects.create(name="contact2", email="contact2@example.com")
        resp = self.client.delete(
            reverse("contacts:delete", args=[c.pk]), HTTP_HX_REQUEST="true"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.strip(), b"")
        self.assertFalse(Contact.objects.filter(pk=c.pk).exists())
