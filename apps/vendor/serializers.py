from rest_framework import serializers
from .models import *

#Create Serializers
#HyperlinkedModelSerializer
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class VendorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorCategory
        fields = '__all__'

class VendorPaymentTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPaymentTerms
        fields = '__all__'


class VendorAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAgent
        fields = '__all__'

class VendorAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAttachment
        fields = '__all__'

class VendorAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorAddress
        fields = '__all__'