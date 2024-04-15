from rest_framework import serializers
from .models import *
from apps.masters.serializers import *
from django.conf import settings
from django.core.files.storage import default_storage

#Create Serializers
        
class LedgerAccountsSerializers(serializers.ModelSerializer):
    ledger_group = ModLedgerGroupsSerializer(source='ledger_group_id', read_only=True)
    class Meta:
        model = LedgerAccounts
        fields = '__all__'

class ModLedgerAccountsSerializers(serializers.ModelSerializer):
    class Meta:
        model = LedgerAccounts
        fields = ['ledger_account_id', 'name', 'code']
        

class CustomerSerializer(serializers.ModelSerializer):
    ledger_account = ModLedgerAccountsSerializers(source='ledger_account_id', read_only=True)
    firm_status = ModFirmStatusesSerializers(source='firm_status_id', read_only=True)
    territory = ModTerritorySerializers(source='territory_id', read_only=True)
    customer_category = ModCustomerCategoriesSerializers(source='customer_category_id', read_only=True)
    gst_category = GstCategoriesSerializers(source='gst_category_id', read_only=True)
    payment_term = ModCustomerPaymentTermsSerializers(source='payment_term_id', read_only=True)
    price_category = PriceCategoriesSerializers(source='price_category_id', read_only=True)
    transporter = ModTransportersSerializers(source='transporter_id', read_only=True)
    class Meta:
        model = Customer
        fields = '__all__'  
        
    def create(self, validated_data):
            picture = validated_data.pop('picture', None)
            instance = super().create(validated_data)
            if picture:
                instance.picture = picture
                instance.save()
            return instance
   
    def update(self, instance, validated_data):
        picture = validated_data.pop('picture', None)
        if picture:
            # Delete the previous picture file and its directory if they exist
            if instance.picture:
                picture_path = instance.picture.path
                if os.path.exists(picture_path):
                    os.remove(picture_path)
                    picture_dir = os.path.dirname(picture_path)
                    if not os.listdir(picture_dir):
                        os.rmdir(picture_dir)
            instance.picture = picture
            instance.save()
        return super().update(instance, validated_data)      
        
class ModCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'name']

class CustomerAddressesSerializers(serializers.ModelSerializer):
    customer = ModCustomersSerializer(source='customer_id', read_only=True)
    class Meta:
        model = CustomerAddresses
        fields = '__all__'