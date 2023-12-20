from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class UrlsTest(TestCase):

    def setUp(self):
        # Check if the user already exists
        username = 'testadmin'
        email = 'testadmin@example.com'
        password = 'testpassword'

        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={'password': password}
        )

        # If the user was created, generate an authentication token
        if created:
            self.token = Token.objects.create(user=user)
        else:
            # If the user already existed, retrieve their existing token
            self.token = Token.objects.get(user=user)

        # Authenticate the test client with the token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_vendor_list_create_url_resolves(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vendor_retrieve_update_delete_url_resolves(self):
        url = reverse('vendor-retrieve-update-delete', args=[1])  # Assuming vendor ID is 1
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_purchase_order_list_create_url_resolves(self):
        url = reverse('purchase-order-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_purchase_order_retrieve_update_delete_url_resolves(self):
        url = reverse('purchase-order-retrieve-update-delete', args=[1])  # Assuming PO ID is 1
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vendor_performance_url_resolves(self):
        url = reverse('vendor_performance', args=[1])  # Assuming vendor ID is 1
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_acknowledge_purchase_order_url_resolves(self):
        url = reverse('acknowledge-purchase-order', args=[1])  # Assuming PO ID is 1
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
