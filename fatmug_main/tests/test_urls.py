from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from fatmug_main.models import PurchaseOrder, Vendor


class UrlsTest(TestCase):

    def setUp(self):
        # Create a superuser
        self.user = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@example.com',
            password='testpassword'
        )

        # Create an authentication token for the superuser
        self.token = Token.objects.create(user=self.user)

        # Authenticate the test client with the created token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create a Vendor for testing
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='testvendor@example.com',
            address='Test Address',
            vendor_code='123'
        )

        # Create a PurchaseOrder for testing
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date='2023-01-01T12:00:00Z',
            delivery_date='2023-01-10T12:00:00Z',
            items={'item1': 'Test Item'},
            quantity=10,
            status='pending',
            issue_date='2023-01-01T12:00:00Z',
        )

    def test_vendor_list_create_url_resolves(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vendor_retrieve_update_delete_url_resolves(self):
        url = reverse(
            'vendor-retrieve-update-delete',
            args=[1])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_purchase_order_list_create_url_resolves(self):
        url = reverse('purchase-order-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_purchase_order_retrieve_update_delete_url_resolves(self):
        url = reverse(
            'purchase-order-retrieve-update-delete',
            args=[1])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vendor_performance_url_resolves(self):
        url = reverse(
            'vendor_performance',
            args=[1])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_acknowledge_purchase_order_url_resolves(self):
        url = reverse(
            'acknowledge-purchase-order',
            args=[1])  
        response = self.client.post(url, data={})
        self.assertEqual(response.status_code, 200)
