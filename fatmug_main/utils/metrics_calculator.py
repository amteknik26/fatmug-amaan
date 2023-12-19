# metrics_calculator.py
from logging import Logger
from django.utils import timezone

def calculate_on_time_delivery_rate(vendor,order_instance):
    try:
        total_completed_orders = vendor.purchaseorder_set.filter(
            status='completed',
        ).count()
        
        if vendor.on_time_delivery_rate == None:
            return round((1/total_completed_orders)*100)
        
        on_time_deliveries = round((vendor.on_time_delivery_rate/100) * total_completed_orders)

        if order_instance.delivery_date.date() <= timezone.now().date():
            on_time_delivery_rate = round(((on_time_deliveries + 1) / total_completed_orders)*100)
            return on_time_delivery_rate
        else:
            if on_time_deliveries == 0:
                return 0
            on_time_delivery_rate = round((on_time_deliveries / total_completed_orders)*100)
            return on_time_delivery_rate
    except Exception as e:
        Logger.info(f"An exception occured when calculating on time delivery rate : {e}")

def calculate_quality_rating_average(vendor,order_quality_rating):
    try:
        completed_pos = vendor.purchaseorder_set.filter(status='completed').exclude(quality_rating=None).count()
        current_quality_rating_avg = vendor.quality_rating_avg

        if current_quality_rating_avg == None:
            return order_quality_rating

        new_quality_rating_avg = ((current_quality_rating_avg * (completed_pos - 1)) + order_quality_rating)/completed_pos
        return round(new_quality_rating_avg)
    except Exception as e:
        Logger.info(f"An exception occured when calculating quality rating average : {e}")

def calculate_average_response_time(vendor,order_instance):
    try:
        current_average_response_time = vendor.average_response_time
        order_issue_date = order_instance.issue_date
        order_acknowledgement_date = order_instance.acknowledgment_date
        response_time_of_current_order = round((order_acknowledgement_date - order_issue_date).total_seconds()/ 60)

        if current_average_response_time == None:
            new_average_response_time = response_time_of_current_order
            return new_average_response_time
        
        total_acknowledged_pos = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False).count()
        new_average_response_time = ((current_average_response_time * (total_acknowledged_pos - 1)) + response_time_of_current_order)/total_acknowledged_pos
        return round(new_average_response_time)
    except Exception as e:
        Logger.info(f"An exception occured when calculating average response time : {e}")

def calculate_fulfillment_rate(vendor):
    try:
        current_fulfillment_rate = vendor.fulfillment_rate
        total_pos = vendor.purchaseorder_set.count()
        
        if current_fulfillment_rate == None:
            new_fulfillment_rate = round((1/total_pos)*100)
            return new_fulfillment_rate
        
        fulfilled_pos = round((current_fulfillment_rate/100) * total_pos) + 1 
        new_fulfillment_rate = round((fulfilled_pos / total_pos)*100)
        return new_fulfillment_rate
    except Exception as e:
        Logger.info(f"An exception occured when calculating fulfillment rate : {e}")
    
