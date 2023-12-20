from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from ..models import Vendor, PurchaseOrder

class ViewsTest(TestCase):
    def setUp(self):
        # Create a user and obtain a token for authentication
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Create a vendor for testing
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='testvendor@example.com',
            address='Test Address',
            vendor_code='123'
        )

        # Create a purchase order for testing
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

    def test_vendor_list_create_view(self):
        url = reverse('vendor-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_retrieve_update_delete_view(self):
        url = reverse('vendor-retrieve-update-delete', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_vendor_performance_view(self):
        url = reverse('vendor_performance', args=[self.vendor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purchase_order_list_create_view(self):
        url = reverse('purchase-order-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_purchase_order_retrieve_update_delete_view(self):
        url = reverse('purchase-order-retrieve-update-delete', args=[self.purchase_order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_acknowledge_purchase_order_view(self):
        url = reverse('acknowledge-purchase-order', args=[self.purchase_order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
