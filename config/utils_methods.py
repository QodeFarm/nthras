#utils_methods file
from rest_framework.response import Response
from rest_framework import status
from django.db import models
import uuid,django_filters
from django.db.models import Q
from uuid import uuid4
import base64
import os
import json
from django.utils import timezone

# -------------- File Path Handler (for Vendor model only)----------------------
def custom_upload_to(instance, filename):
    file_extension = filename.split('.')[-1]
    unique_id = uuid4().hex[:7]  # Generate a unique ID (e.g., using UUID)
    new_filename = f"{unique_id}_{filename}"
    new_filename = new_filename.replace(' ', '_')
    return os.path.join('vendor', str(instance.name), new_filename)
# ---------------------------------------------------------

#functions for demonstration purposes
def encrypt(text):
    if text is None:
        return None
    # Encode the text using base64
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    encrypted_text = encoded_bytes.decode("utf-8")
    return encrypted_text

def decrypt(encrypted_text):
    if encrypted_text is None:
        return None
    # Decode the text using base64
    decoded_bytes = base64.b64decode(encrypted_text.encode("utf-8"))
    decrypted_text = decoded_bytes.decode("utf-8")
    return decrypted_text

class EncryptedTextField(models.TextField):
    """
    A custom field to store encrypted text.
    """
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        try:
            # Attempt to decrypt the value
            return decrypt(value)
        except Exception as e:
            # Handle decryption errors gracefully
            print("Error decrypting value:", e)
            return None
        # Implement decryption logic here
        return decrypt(value)

    def to_python(self, value):
        if isinstance(value, str):
            # Implement decryption logic here
            return decrypt(value)
        return value
 
    def get_prep_value(self, value):
        # Implement encryption logic here
        return encrypt(value)


#If you want to decrypt then you can uncomment this and run... in output you will find the decrypted account number 
# # Encoded account number
encoded_account_number = ""

# Decode from base64
decoded_bytes = base64.b64decode(encoded_account_number)

# Convert bytes to string
original_account_number = decoded_bytes.decode("utf-8")


# -----------------------------Filters for primary key-------------------------------
def filter_uuid(queryset, name, value):
    try:
        uuid.UUID(value)
    except ValueError:
        return queryset.none()
    return queryset.filter(Q(**{name: value}))


# -----------------------------Customised Filters-------------------------------
def count_sub_dicts(main_dict):
    count = 0
    for value in main_dict.values():
        if isinstance(value, dict):
            count += 1
    return count

def sale_by_customer():
    from apps.sales.models import SaleInvoiceOrders, SaleOrder, SaleOrderItems
    sale_orders = SaleOrder.objects.select_related('customer_id').all()

    # Calculate summary of sales for each customer

    sales_summary = {}
    for sale_order in sale_orders:
        customer_info = str(sale_order.customer_id)  # Accessing the customer_id field directly, convert to str otherwise error will come
        customer_name = customer_info.split('_')[0]
        customer_id = customer_info.split('_')[1]

        if customer_id not in sales_summary:
            customer_data = {
                'customer_id': customer_id,
                'name': customer_name,
            }
            sales_summary[customer_id] = {
                'customer_name': customer_name,
                'customer_id': customer_id,
                'total_sales_amount': 0,
                'num_of_sale_orders': 0,
                'avg_order_value': 0
            }

        # Calculae "total_sales_amount" | In each iteration, each value in 'amount' field in 'SaleOrderItems' is Summed up.
        sale_order_info = SaleOrderItems.objects.filter(sale_order_id=sale_order.sale_order_id)
        amount = 0
        for val in sale_order_info:
            amount = val.amount + amount

        if amount is not None:
            sales_summary[customer_id]['total_sales_amount'] += amount

        # Calculate "num_of_sale_orders"
        #Total iterations in this loop is equal to No of SaleOrders for one customer.
        sales_summary[customer_id]['num_of_sale_orders'] += 1

    # Calculate "avg_order_value"
    for summary in sales_summary.values():
        total_sales_amount = summary['total_sales_amount']
        num_orders = summary['num_of_sale_orders']
        if num_orders != 0:
            summary['avg_order_value'] = total_sales_amount / num_orders

    response_data = {
            'count': count_sub_dicts(sales_summary),
            'msg': None,
            'data': sales_summary.values()
        }
    return Response(response_data)

#=========
def sale_by_product(desc_param=None,p_id=None):
    from apps.sales.models import SaleOrderItems
    from apps.products.models import Products
    order_items = SaleOrderItems.objects.select_related('product_id').all()

    # Calculate summary of sales for each product
    sales_summary = {}
    for order_item in order_items:
        product_info = str(order_item.product_id)  # Accessing the customer_id field directly, convert to str otherwise error will come
        product_id = product_info.split('_')[0]
        product_name = product_info.split('_')[1] 

        if product_id not in sales_summary:
            sales_summary[product_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'total_quantity_sold': 0,
                'total_revenue': 0,
                'avg_selling_price': 0
            }

        # Fetch related product information
        product = Products.objects.get(product_id=product_id)

        # Update sales summary
        sales_summary[product_id]['total_quantity_sold'] += order_item.quantity
        sales_summary[product_id]['total_revenue'] += order_item.quantity * product.sales_rate

    # Calculate average selling price
    for product_id, summary in sales_summary.items():
        total_quantity_sold = summary['total_quantity_sold']
        if total_quantity_sold != 0:
            summary['avg_selling_price'] = summary['total_revenue'] / total_quantity_sold

    # http://127.0.0.1:8000/api/v1/sales/sale_order/?sales_by_product=true&p_id=<place ur product ID>
    if p_id: 
        rec = sales_summary[p_id]
        return Response(rec)
    
    # http://127.0.0.1:8000/api/v1/sales/sale_order/?sales_by_product=true&desc=true
    if desc_param == 'true':     
        # return Response(sales_summary.values())
        sorted_data = sorted(sales_summary.values(), key=lambda x: x['total_quantity_sold'], reverse=True)
        data = {}
        i = 1
        for item in sorted_data: #data is still in decimal format in sorted_data. To avoid the error, data is converted to float data type
                item['total_quantity_sold'] = float(item['total_quantity_sold'])
                item['total_revenue'] = float(item['total_revenue'])
                item['avg_selling_price'] = float(item['avg_selling_price'])
                data[i] = item
                i = i+1

        response_data = {
            'count': count_sub_dicts(data),
            'msg': None,
            'data': data.values()
        }
        return Response(response_data)
    
    # http://127.0.0.1:8000/api/v1/sales/sale_order/?sales_by_product=true
    else:
        response_data = {
            'count': count_sub_dicts(sales_summary),
            'msg': None,
            'data': sales_summary.values()
        }
        return Response(response_data)

#==========
def sale_return_report(): # take i/p 
    from apps.sales.models import SaleReturnOrders, SaleOrder
    from apps.sales.serializers import ModSaleOrderSerializer
    from apps.masters.models import OrderStatuses
 
    sale_order_returns = SaleReturnOrders.objects.all()

    # Calculate summary of sales for each product
    sales_summary = {}
    for sale_order_return in sale_order_returns:
        sale_return_id_info = str(sale_order_return.sale_return_id)  #get order ID 

        if sale_return_id_info not in sales_summary:
            sales_summary[sale_return_id_info] = {
                'sale_order_return_id': str(sale_order_return),
                'sale_id': sale_return_id_info,
                'original_sale_order_info': None, #invoice_no
                'ref_no':sale_order_return.ref_no,
                'ref_date':sale_order_return.ref_date,
                'due_date':sale_order_return.due_date,
                'item_value':sale_order_return.item_value,
                'total_amount':sale_order_return.total_amount,
                'vehicle_name':sale_order_return.vehicle_name,
                'total_boxes':sale_order_return.total_boxes,
                'Status': str(sale_order_return.order_status_id), #not Json Serializable so converted to str
                'reason_for_return': sale_order_return.return_reason,
                # 'amount_refunded': None,
            }

    response_data = {
            'count': count_sub_dicts(sales_summary),
            'msg': None,
            'data': sales_summary.values()
        }
    return Response(response_data)

#===========
def sale_order_status():
        from apps.sales.models import SaleOrder, SaleInvoiceOrders,PaymentTransactions,SaleOrderItems,OrderShipments
        from apps.products.models import Products
        sale_orders = SaleOrder.objects.all()

        sales_summary = {}
        for sale_order in sale_orders:
            customer_info = str(sale_order.customer_id)  # Accessing the customer_id field directly, convert to str otherwise error will come
            customer_name = customer_info.split('_')[0]
            customer_id = customer_info.split('_')[1]
            sale_order_id = str(sale_order.sale_order_id)

            if sale_order_id not in sales_summary:
                sales_summary[sale_order_id] = {
                    'sale_order_id': sale_order_id,
                    # 'customer_id':customer_id,
                    'customer_name':customer_name,
                    'order_date':sale_order.order_date,
                    'delivery_date':sale_order.delivery_date,
                    'order_no':sale_order.order_no,
                    'advance_amount':sale_order.advance_amount,
                    'order_status':str(sale_order.order_status_id),
                }
            sale_order_items = SaleOrderItems.objects.filter(sale_order_id=sale_order_id)
            for val in sale_order_items:
                sales_summary[sale_order_id]['product_id'] = str(val.product_id)
                sales_summary[sale_order_id]['quantity'] = str(val.quantity)
                sales_summary[sale_order_id]['unit_price'] = str(val.unit_price)
                sales_summary[sale_order_id]['rate'] = str(val.rate)
                sales_summary[sale_order_id]['amount'] = str(val.amount)

                product_id = str(val.product_id).split('_')[0]

                products = Products.objects.filter(product_id=product_id)
                for val in products:
                    sales_summary[sale_order_id]['product_name'] = str(val.name)


        response_data = {
            'count': count_sub_dicts(sales_summary),
            'msg': None,
            'data': sales_summary.values()
        }
        return Response(response_data)
# ------------------------------------------------------------------------------

def list_all_objects(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    serializer = self.get_serializer(queryset, many=True)


    sales_by_customer = request.query_params.get('sales_by_customer', 'false').lower() == 'true'
    if sales_by_customer:
        return sale_by_customer()
    
    sales_by_product = request.query_params.get('sales_by_product', 'false').lower() == 'true'
    p_id = request.query_params.get('p_id', None)
    desc_param = request.query_params.get('desc')
    
    if sales_by_product:
        return sale_by_product(desc_param,p_id)
    
    sales_return_report = request.query_params.get('sales_return_report', 'false').lower() == 'true'
    if sales_return_report:
        return sale_return_report()
    
    sales_order_status = request.query_params.get('sales_order_status', 'false').lower() == 'true'
    if sales_order_status:
        return sale_order_status()
    
    
    else:

        message = "NO RECORDS INSERTED" if not serializer.data else None
        response_data = {
            'count': queryset.count(),
            'msg': message,
            'data': serializer.data
        }
        return Response(response_data)

def create_instance(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': True,
            'message': 'Record created successfully',
            'data': serializer.data
        })
    else:
        return Response({
            'status': False,
            'message': 'Form validation failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

def update_instance(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response({
        'status': True,
        'message': 'Update successful',
        'data': serializer.data,
    })

def perform_update(self, serializer):
    serializer.save()  # Add any custom logic for updating if needed


#==================================================
#Patterns
SEQUENCE_FILE_PATH = 'order_sequences.json'

def load_sequences():
    if not os.path.exists(SEQUENCE_FILE_PATH):
        return {}
    with open(SEQUENCE_FILE_PATH, 'r') as file:
        return json.load(file)

def save_sequences(sequences):
    with open(SEQUENCE_FILE_PATH, 'w') as file:
        json.dump(sequences, file)

def generate_order_number(order_type_prefix):
    current_date = timezone.now()
    date_str = current_date.strftime('%y%m')
    
    sequences = load_sequences()
    
    key = f"{order_type_prefix}-{date_str}"
    
    sequence_number = sequences.get(key, 0)
    sequence_number += 1
    sequences[key] = sequence_number
    save_sequences(sequences)
    
    sequence_number_str = f"{sequence_number:05d}"
    
    order_number = f"{order_type_prefix}-{date_str}-{sequence_number_str}"
    return order_number

class OrderNumberMixin(models.Model):
    order_no_prefix = ''
    order_no_field = 'order_no'

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not getattr(self, self.order_no_field):
            setattr(self, self.order_no_field, generate_order_number(self.order_no_prefix))
        super().save(*args, **kwargs)
