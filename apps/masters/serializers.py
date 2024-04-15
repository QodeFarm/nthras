from rest_framework import serializers
from .models import *

#Create serializers

class LedgerGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerGroups
        fields = '__all__'

class ModLedgerGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerGroups
        fields = ['ledger_group_id', 'name', 'code']

class FirmStatusesSerializers(serializers.ModelSerializer):
    class Meta:
        model = FirmStatuses
        fields = '__all__'
        
class ModFirmStatusesSerializers(serializers.ModelSerializer):
    class Meta:
        model = FirmStatuses
        fields = ['firm_status_id', 'name']

class TerritorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = '__all__'

class ModTerritorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Territory
        fields = ['territory_id', 'name', 'code']
        
class CustomerCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerCategories
        fields = '__all__'

class ModCustomerCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerCategories
        fields = ['customer_category_id', 'name', 'code']


class GstCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = GstCategories
        fields = '__all__'

class CustomerPaymentTermsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerPaymentTerms
        fields = '__all__'

class ModCustomerPaymentTermsSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomerPaymentTerms
        fields = ['payment_term_id', 'name', 'code']
        
class PriceCategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = PriceCategories
        fields = '__all__'
        
class TransportersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transporters
        fields = '__all__'

class ModTransportersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transporters
        fields = ['transporter_id', 'name', 'code', 'gst_no', 'website_url']