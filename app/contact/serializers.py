from rest_framework import serializers
from core.models import Contact, Email, PhoneNumber, SocialMediaLink


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = ['id', 'email']


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneNumber
        fields = ['id', 'phone_number']


class SocialMediaLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = ['id', 'platform_name', 'link', 'tag']


class ContactSerializer(serializers.ModelSerializer):
    emails = EmailSerializer(many=True, required=False)
    phone_numbers = PhoneNumberSerializer(many=True, required=False)
    social_media_links = SocialMediaLinkSerializer(many=True, required=False)

    class Meta:
        model = Contact
        fields = ['id',
                  'first_name',
                  'last_name',
                  'emails',
                  'phone_numbers',
                  'social_media_links']
        read_only_fields = ['id']

    def create(self, validated_data):
        emails_data = validated_data.pop('emails', [])
        phone_numbers_data = validated_data.pop('phone_numbers', [])
        social_media_links_data = validated_data.pop('social_media_links', [])
        contact = Contact.objects.create(**validated_data)
        for email_data in emails_data:
            Email.objects.create(contact=contact, **email_data)
        for phone_number_data in phone_numbers_data:
            PhoneNumber.objects.create(
                contact=contact, **phone_number_data)
        for social_media_link_data in social_media_links_data:
            SocialMediaLink.objects.create(
                contact=contact, **social_media_link_data)
        return contact

    def update(self, instance, validated_data):
        emails_data = (
            validated_data.pop('emails', None))
        phone_numbers_data = (
            validated_data.pop('phone_numbers', None))
        social_media_links_data = (
            validated_data.pop('social_media_links', None))

        if phone_numbers_data is not None:
            phone_number_ids = [item['id'] for
                                item in phone_numbers_data if 'id' in item]
            for phone_number in (
                    instance.phone_numbers.all()):
                if (phone_number.id not in
                        phone_number_ids):
                    # Delete phone numbers not included in the request
                    phone_number.delete()
            for phone_number_data in phone_numbers_data:
                phone_number_id = (
                    phone_number_data.get('id', None))
                if phone_number_id:
                    phone_number_instance = (
                        PhoneNumber.objects.get(
                            id=phone_number_id, contact=instance))
                    phone_number_instance.phone_number = (
                        phone_number_data.get(
                            'phone_number',
                            phone_number_instance.phone_number))
                    phone_number_instance.save()
                else:
                    PhoneNumber.objects.create(
                        contact=instance, **phone_number_data)

        if social_media_links_data is not None:
            social_media_link_ids = \
                [item['id']
                 for item in social_media_links_data if 'id' in item]
            for social_media_link in instance.social_media_links.all():
                if social_media_link.id not in social_media_link_ids:
                    # Delete social media links not included in the request
                    social_media_link.delete()
            for social_media_link_data in social_media_links_data:
                social_media_link_id = (
                    social_media_link_data.get('id', None))
                if social_media_link_id:
                    social_media_link_instance = (
                        SocialMediaLink.objects.get(
                            id=social_media_link_id, contact=instance))
                    social_media_link_instance.platform_name = (
                        social_media_link_data.get(
                            'platform_name',
                            social_media_link_instance.platform_name))
                    social_media_link_instance.link = (
                        social_media_link_data.get(
                            'link', social_media_link_instance.link))
                    social_media_link_instance.tag = (
                        social_media_link_data.get(
                            'tag', social_media_link_instance.tag))
                    social_media_link_instance.save()
                else:
                    SocialMediaLink.objects.create(
                        contact=instance, **social_media_link_data)

        # Handling for phone_numbers and social_media_links similarly...

        if emails_data is not None:
            email_ids = [item['id'] for item in emails_data if 'id' in item]
            for email in instance.emails.all():
                if email.id not in email_ids:
                    # Delete emails not included in the request
                    email.delete()
            for email_data in emails_data:
                email_id = email_data.get('id', None)
                if email_id:
                    email_instance = Email.objects.get(
                        id=email_id, contact=instance)
                    email_instance.email = email_data.get(
                        'email', email_instance.email)
                    email_instance.save()
                else:
                    Email.objects.create(contact=instance, **email_data)

        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.save()

        # Similar logic for updating phone_numbers and social_media_links...

        return instance
