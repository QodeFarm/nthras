import os
from uuid import uuid4
from requests import request
from rest_framework import status
from rest_framework.response import Response
import base64
from django.db import models

# -------------- File Path Handler (for Vendor model only)----------------------
def custom_upload_to(instance, filename):
    file_extension = filename.split('.')[-1]
    unique_id = uuid4().hex[:7]  # Generate a unique ID (e.g., using UUID)
    new_filename = f"{unique_id}_{filename}"
    new_filename = new_filename.replace(' ', '_')
    return os.path.join('vendor', str(instance.name), new_filename)


# -----------------------------Customised Filters-------------------------------
def count_sub_dicts(main_dict):
    count = 0
    for value in main_dict.values():
        if isinstance(value, dict):
            count += 1
    return count

def sale_by_customer():
    from apps.sales.models import Invoices, SaleOrder
    sale_orders = SaleOrder.objects.select_related('customer_id').all()

    # Calculate summary of sales for each customer

    sales_summary = {}
    for sale_order in sale_orders:
        customer_id = str(sale_order.customer_id)  # Accessing the customer_id field directly, convert to str otherwise error will come
        customer_id = customer_id[-1]


        if customer_id not in sales_summary:
            customer_data = {
                'customer_id': str(sale_order.customer_id)[-1], #convert to str otherwise error will come
                'name': str(sale_order.customer_id)[ : -2],  # Assuming customer_id is a field in SaleOrder model
            }
            sales_summary[customer_id] = {
                'customer': customer_data,
                'total_sales_amount': 0,
                'num_orders': 0,
                'avg_order_value': 0
            }
        # Fetch related invoices for the sale order
        invoices = Invoices.objects.filter(order_id=sale_order.order_id)
        total_amount = invoices.aggregate(total_amount=models.Sum('total_amount'))['total_amount']
        if total_amount is not None:
            sales_summary[customer_id]['total_sales_amount'] += total_amount
        sales_summary[customer_id]['num_orders'] += 1

    # Calculate average order value
    for summary in sales_summary.values():
        total_sales_amount = summary['total_sales_amount']
        num_orders = summary['num_orders']
        if num_orders != 0:
            summary['avg_order_value'] = total_sales_amount / num_orders
            avg = total_sales_amount / num_orders

    
    # return Response(sales_summary.values())
    response_data = {
            'count': count_sub_dicts(sales_summary),
            'msg': None,
            'data': sales_summary.values()
        }
    return Response(response_data)

#=========
def sale_by_product(desc_param=None,p_id=None):
    from apps.sales.models import OrderItems
    from apps.products.models import products
    order_items = OrderItems.objects.select_related('product_id').all()

    # Calculate summary of sales for each product
    sales_summary = {}
    for order_item in order_items:
        product_id = str(order_item.product_id)  #get item example : Apple
        product_id = product_id[0]    # get that itemm  ID
        if product_id not in sales_summary:
            sales_summary[product_id] = {
                'product_id': product_id,
                'name': order_item.product_id.name,  #item name Example Apple
                'total_quantity_sold': 0,
                'total_revenue': 0,
                'avg_selling_price': 0
            }

        # Fetch related product information
        product = products.objects.get(product_id=product_id)

        # Update sales summary
        sales_summary[product_id]['total_quantity_sold'] += order_item.quantity
        sales_summary[product_id]['total_revenue'] += order_item.quantity * product.sales_rate

    # Calculate average selling price
    for product_id, summary in sales_summary.items():
        total_quantity_sold = summary['total_quantity_sold']
        if total_quantity_sold != 0:
            summary['avg_selling_price'] = summary['total_revenue'] / total_quantity_sold

    #http://127.0.0.1:8000/api/v1/sales/sale_order/?sales_by_product=true&p_id=1
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
def sale_return_report():
    from apps.sales.models import SaleOrderReturns, SaleOrder
    from apps.sales.serializers import ModSaleOrderSerializer
    # Retrieve all returns with related return information
    sale_order_returns = SaleOrderReturns.objects.select_related('sale_id').all()

    # Calculate summary of sales for each product
    sales_summary = {}
    for sale_order_return in sale_order_returns:
        sale_id = str(sale_order_return.sale_id)  #get order ID 


        if sale_id not in sales_summary:
            sales_summary[sale_id] = {
                'sale_order_return_id': str(sale_order_return),  # from SaleOrderReturns
                'sale_id': sale_id,   # From SaleOrder
                'original_sale_order_info': sale_id,   # sale_id Details
                'reason_for_return': sale_order_return.return_reason,
                'amount_refunded': 0,
            }

        # sale_orders = SaleOrder.objects.all()
        sale_orders = SaleOrder.objects.filter(order_id=sale_id)

        serializer = ModSaleOrderSerializer(sale_orders, many=True)

        # Convert the serialized data to JSON format
        json_data = {'sale_id': serializer.data}

        sales_summary[sale_id]['original_sale_order_info'] = json_data

    response_data = {
            'count': count_sub_dicts(sales_summary),
            'msg': None,
            'data': sales_summary.values()
        }
    return Response(response_data)

#===========
def sale_order_status():
        from apps.sales.models import SaleOrder, Invoices,PaymentTransactions,OrderItems,Shipments
        from apps.masters.models import ShippingCompanies
        delivery_dates = SaleOrder.objects.values_list('delivery_date', flat=True)
        sale_orders = SaleOrder.objects.values_list('order_id', flat=True)

        sales_summary = {}
        
        for sale_order,delivery_date in zip(sale_orders,delivery_dates):
            order_id = str(sale_order)  #get order ID 

            invoices = Invoices.objects.filter(order_id=order_id)
            for invoices in invoices:
                invoice_id = invoices.invoice_id                     # get invoice_id 
                invoices = Invoices.objects.get(pk=invoice_id)
                amount = invoices.total_amount
                status = invoices.status

                payment = PaymentTransactions.objects.filter(invoice_id=invoice_id) if invoices else None
                for id in payment:
                    transaction_id = id.transaction_id
                    pay_status = id.payment_status

                order_items = OrderItems.objects.filter(order_id=order_id) 
                for id in order_items:
                    order_item_id = id.order_item_id
                    quantity = id.quantity
                    price = id.unit_price

                shipments = Shipments.objects.filter(order_id=order_id) 
                for id in shipments:
                    shipment_id = id.shipment_id
                    shipping_tracking_no = id.shipping_tracking_no
                    destination = id.destination
                    shipping_date = id.shipping_date
                
                companies = ShippingCompanies.objects.filter(shipping_company_id=shipment_id)
                for name in companies:
                    name = name.name

            if order_id not in sales_summary:
                sales_summary[order_id] = {
                            'order_id' : order_id,
                            'delivery_date' : delivery_date,
  
                            'invoice_id' : invoice_id,
                            'total_amount' : float(amount),
                            'status': status,

                            'transaction_id':transaction_id if payment else None,
                            'payment_status' :pay_status if payment else None,

                            'order_item_id': order_item_id if order_items else None,
                            'quantity' : float(quantity) if order_items else None,
                            'unit_price' : price if order_items else None,

                            'shipment_id':shipment_id if shipments else None,
                            'shipping_tracking_no' :shipping_tracking_no if shipments else None,
                            'destination' :destination if shipments else None,
                            'shipping_date' :shipping_date if shipments else None,
                            'shipping_company_name' :name if companies else None,
                            
                }
        response_data = {
            'count': count_sub_dicts(sales_summary),
            'msg': None,
            'data': sales_summary.values()
        }
        return Response(response_data)
# ------------------------------------------------------------------------------

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

#======================================================================

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