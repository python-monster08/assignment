# from django.db import models
# from django.db.models import Avg, Count, Q
# from django.utils.timezone import now

# # Create your models here.
# class Vendor(models.Model):
#     name = models.CharField(max_length=255)
#     contact_details = models.TextField()
#     address = models.TextField()
#     vendor_code = models.CharField(max_length=100, unique=True)
#     on_time_delivery_rate = models.FloatField(default=0.0)
#     quality_rating_avg = models.FloatField(default=0.0)
#     average_response_time = models.FloatField(default=0.0)
#     fulfillment_rate = models.FloatField(default=0.0)

#     def update_on_time_delivery_rate(self):
#         completed_orders = self.purchase_orders.filter(status='completed')
#         on_time_deliveries = completed_orders.filter(delivery_date__lte=F('order_date')) # type: ignore
#         if completed_orders.exists():
#             self.on_time_delivery_rate = (on_time_deliveries.count() / completed_orders.count()) * 100
#         else:
#             self.on_time_delivery_rate = 0
#         self.save()

#     def update_quality_rating_avg(self):
#         ratings = self.purchase_orders.filter(status='completed').aggregate(average_rating=Avg('quality_rating'))
#         self.quality_rating_avg = ratings.get('average_rating', 0.0)
#         self.save()

#     def update_average_response_time(self):
#         response_times = self.purchase_orders.filter(acknowledgment_date__isnull=False)
#         total_time = sum([(po.acknowledgment_date - po.issue_date).total_seconds() for po in response_times])
#         if response_times.exists():
#             self.average_response_time = total_time / response_times.count()
#         else:
#             self.average_response_time = 0
#         self.save()

#     def update_fulfillment_rate(self):
#         total_orders = self.purchase_orders.count()
#         fulfilled_orders = self.purchase_orders.filter(status='completed').count()
#         if total_orders > 0:
#             self.fulfillment_rate = (fulfilled_orders / total_orders) * 100
#         else:
#             self.fulfillment_rate = 0
#         self.save()

# class PurchaseOrder(models.Model):
#     po_number = models.CharField(max_length=100, unique=True)
#     vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
#     order_date = models.DateTimeField()
#     delivery_date = models.DateTimeField()
#     items = models.JSONField()
#     quantity = models.IntegerField()
#     status = models.CharField(max_length=50)
#     quality_rating = models.FloatField(null=True, blank=True)
#     issue_date = models.DateTimeField(auto_now_add=True)
#     acknowledgment_date = models.DateTimeField(null=True, blank=True)

#     # Handling Performance Metrics
#     def save(self, *args, **kwargs):
#         is_new = self._state.adding
#         super().save(*args, **kwargs)
#         if not is_new:
#             if self.status == 'completed':
#                 self.vendor.update_on_time_delivery_rate()
#                 self.vendor.update_quality_rating_avg()
#             if self.acknowledgment_date:
#                 self.vendor.update_average_response_time()
#             self.vendor.update_fulfillment_rate()


# class HistoricalPerformance(models.Model):
#     vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performances')
#     date = models.DateTimeField()
#     on_time_delivery_rate = models.FloatField()
#     quality_rating_avg = models.FloatField()
#     average_response_time = models.FloatField()
#     fulfillment_rate = models.FloatField()



from django.db import models
from django.db.models import Avg, F
from django.utils.timezone import now, timedelta

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def update_on_time_delivery_rate(self):
        completed_orders = self.purchase_orders.filter(status='completed')
        if completed_orders.exists():
            on_time_deliveries = completed_orders.filter(delivery_date__lte=F('order_date') + timedelta(days=5))  # Assuming a 5-day delivery window
            self.on_time_delivery_rate = (on_time_deliveries.count() / completed_orders.count()) * 100
        else:
            self.on_time_delivery_rate = 0
        self.save()


    def update_quality_rating_avg(self):
        ratings = self.purchase_orders.filter(status='completed').aggregate(average_rating=Avg('quality_rating'))
        self.quality_rating_avg = ratings.get('average_rating', 0.0) or 0.0
        self.save()

    def update_average_response_time(self):
        response_times = self.purchase_orders.filter(acknowledgment_date__isnull=False)
        if response_times.exists():
            total_time = sum([(po.acknowledgment_date - po.issue_date).total_seconds() for po in response_times])
            self.average_response_time = total_time / response_times.count()
        else:
            self.average_response_time = 0
        self.save()


    def update_fulfillment_rate(self):
        total_orders = self.purchase_orders.count()
        fulfilled_orders = self.purchase_orders.filter(status='completed').count()
        if total_orders > 0:
            self.fulfillment_rate = (fulfilled_orders / total_orders) * 100
        else:
            self.fulfillment_rate = 0
        self.save()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if not is_new:
            if self.status == 'completed':
                self.vendor.update_on_time_delivery_rate()
                self.vendor.update_quality_rating_avg()
            if self.acknowledgment_date:
                self.vendor.update_average_response_time()
            self.vendor.update_fulfillment_rate()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performances')
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()
