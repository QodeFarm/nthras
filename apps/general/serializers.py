from rest_framework import serializers
from .models import *
from apps.master.serializers import *

#Create Serializers
        
class LedgerAccountsSerializers(serializers.ModelSerializer):
    ledger_group = Mod_LedgerGroupsSerializer(source='ledger_group_id', read_only=True)
    class Meta:
        model = LedgerAccounts
        fields = '__all__'

class Mod_LedgerAccountsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LedgerAccounts
        fields = ['ledger_account_id', 'name', 'code']
        

class CustomersSerializer(serializers.ModelSerializer):
    ledger_account = Mod_LedgerAccountsSerializers(source='ledger_account_id', read_only=True)
    firm_status = Mod_FirmStatusesSerializers(source='firm_status_id', read_only=True)
    territory = Mod_TerritorySerializers(source='territory_id', read_only=True)
    customer_category = Mod_CustomerCategoriesSerializers(source='customer_category_id', read_only=True)
    gst_category = GstCategoriesSerializers(source='gst_category_id', read_only=True)
    payment_term = Mod_CustomerPaymentTermsSerializers(source='payment_term_id', read_only=True)
    price_category = PriceCategoriesSerializers(source='price_category_id', read_only=True)
    transporter = Mod_TransportersSerializers(source='transporter_id', read_only=True)
    class Meta:
        model = Customers
        fields = '__all__'        
        
class Mod_CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = ['customer_id', 'name']

class CustomerAddressesSerializers(serializers.ModelSerializer):
    customer = Mod_CustomersSerializer(source='customer_id', read_only=True)
    class Meta:
        model = CustomerAddresses
        fields = '__all__'