from datetime import datetime

from django.test import TestCase
from django.utils import timezone

from ..models import HistoricalPerformance, PurchaseOrder, Vendor


class VendorModelTest(TestCase):

    def test_vendor_creation(self):
        vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='testvendor@example.com',
            address='Test Address',
            vendor_code='123'
        )
        self.assertEqual(vendor.name, 'Test Vendor')
        self.assertEqual(vendor.contact_details, 'testvendor@example.com')
        self.assertEqual(vendor.address, 'Test Address')
        self.assertEqual(vendor.vendor_code, '123')


class PurchaseOrderModelTest(TestCase):

    def setUp(self):
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='testvendor@example.com',
            address='Test Address',
            vendor_code='123'
        )

    def test_purchase_order_creation(self):
        order_date = timezone.make_aware(
            datetime.strptime('2023-01-01T12:00:00', '%Y-%m-%dT%H:%M:%S'), timezone.utc)
        delivery_date = timezone.make_aware(
            datetime.strptime('2023-01-10T12:00:00', '%Y-%m-%dT%H:%M:%S'), timezone.utc)
        issue_date = timezone.make_aware(
            datetime.strptime('2023-01-01T12:00:00', '%Y-%m-%dT%H:%M:%S'), timezone.utc)

        purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date=order_date,
            delivery_date=delivery_date,
            items={'item1': 'Test Item'},
            quantity=10,
            status='pending',
            issue_date=issue_date,
        )

        self.assertEqual(purchase_order.po_number, 'PO123')
        self.assertEqual(purchase_order.vendor, self.vendor)
        self.assertEqual(purchase_order.order_date, order_date)
        self.assertEqual(purchase_order.delivery_date, delivery_date)
        self.assertEqual(purchase_order.items, {'item1': 'Test Item'})
        self.assertEqual(purchase_order.quantity, 10)
        self.assertEqual(purchase_order.status, 'pending')
        self.assertEqual(purchase_order.issue_date, issue_date)


class HistoricalPerformanceModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            contact_details="test@example.com",
            address="Test Address",
            vendor_code="123"
        )

    def test_historical_performance_creation(self):
        historical_performance = HistoricalPerformance.objects.create(
            vendor=self.vendor,
            date=timezone.now(),
            on_time_delivery_rate=90.5,
            quality_rating_avg=4.2,
            average_response_time=30.8,
            fulfillment_rate=95.0
        )

        saved_performance = HistoricalPerformance.objects.get(
            pk=historical_performance.pk)

        self.assertEqual(saved_performance.vendor, self.vendor)
        self.assertEqual(saved_performance.on_time_delivery_rate, 90.5)
        self.assertEqual(saved_performance.quality_rating_avg, 4.2)
        self.assertEqual(saved_performance.average_response_time, 30.8)
        self.assertEqual(saved_performance.fulfillment_rate, 95.0)
