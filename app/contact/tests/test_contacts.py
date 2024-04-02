from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Contact, Email, PhoneNumber, SocialMediaLink

CONTACT_URL = reverse('contact:contact-list')


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email=email, password=password)


class PublicContactAPITests(APITestCase):
    """Test unauthenticated contact API access"""

    def test_auth_required(self):
        res = self.client.get(CONTACT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContactAPITests(APITestCase):
    """Test authenticated contact API access"""

    def setUp(self):
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_contacts(self):
        Contact.objects.create(
            user=self.user, first_name='John', last_name='Doe')
        Contact.objects.create(
            user=self.user, first_name='Jane', last_name='Doe')

        res = self.client.get(CONTACT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['first_name'], 'John')
        self.assertEqual(res.data[1]['first_name'], 'Jane')


class ContactAPITests(APITestCase):
    def setUp(self):
        self.user = create_user(
            email='test@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.contact_url = reverse('contact:contact-list')

    def test_create_contact_with_details(self):
        """Test creating a contact with emails,
        phone numbers, and social media links."""
        payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'emails': [{'email': 'john@example.com'}],
            'phone_numbers': [{'phone_number': '1234567890'}],
            'social_media_links': [
                {'platform_name': 'Twitter',
                 'link': 'https://twitter.com/johndoe', 'tag': 'personal'}]
        }
        response = self.client.post(self.contact_url, payload, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Email.objects.count(), 1)
        self.assertEqual(PhoneNumber.objects.count(), 1)
        self.assertEqual(SocialMediaLink.objects.count(), 1)

    def test_update_contact(self):
        """Test updating a contact's details."""
        contact = Contact.objects.create(
            user=self.user, first_name='Jane', last_name='Doe')
        email = Email.objects.create(
            contact=contact, email='jane@example.com')
        phone_number = PhoneNumber.objects.create(
            contact=contact, phone_number='0987654321')
        social_media_link = SocialMediaLink.objects.create(
            contact=contact, platform_name='Facebook',
            link='https://facebook.com/janedoe', tag='professional')

        url = reverse('contact:contact-detail', args=[contact.id])
        payload = {
            'first_name': 'Jane Updated',
            'last_name': 'Doe Updated',
            'emails':
                [{'id': email.id,
                  'email': 'janeupdated@example.com'}],
            'phone_numbers':
                [{'id': phone_number.id, 'phone_number': '1122334455'}],
            'social_media_links': [
                {'id': social_media_link.id,
                 'platform_name': 'LinkedIn',
                 'link': 'https://linkedin.com/in/janedoe',
                 'tag': 'professional'}]
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        contact.refresh_from_db()
        self.assertEqual(
            contact.first_name, 'Jane Updated')
        updated_emails = Email.objects.filter(contact=contact)
        updated_phone_numbers = (
            PhoneNumber.objects.filter(contact=contact))
        updated_social_media_links = (
            SocialMediaLink.objects.filter(contact=contact))

        self.assertTrue(updated_emails.exists())
        self.assertEqual(
            updated_emails.first().email,
            'janeupdated@example.com')
        self.assertTrue(updated_phone_numbers.exists())
        self.assertEqual(
            updated_phone_numbers.first().phone_number,
            '1122334455')
        self.assertTrue(updated_social_media_links.exists())
        self.assertEqual(
            updated_social_media_links.first().link,
            'https://linkedin.com/in/janedoe')

    def test_delete_contact(self):
        """Test deleting a contact."""
        contact = Contact.objects.create(
            user=self.user, first_name='John', last_name='Doe')
        url = reverse('contact:contact-detail', args=[contact.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)
