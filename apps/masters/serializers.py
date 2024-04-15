from rest_framework import serializers
from .models import *

class ModCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_id','country_name']

class ModStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['state_id','state_name']

class ModCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_id','city_name']
        
class ModStatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses
        fields = ['status_id','status_name']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class StateSerializer(serializers.ModelSerializer):
    country = ModCountrySerializer(source='country_id', read_only = True)
    class Meta:
        model = State
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    state = ModStateSerializer(source='state_id', read_only = True)
    class Meta:
        model = City
        fields = '__all__'
        
class StatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses 
        fields = '__all__'


class ProductTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypes
        fields = '__all__'

class ProductUniqueQuantityCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUniqueQuantityCodes
        fields = '__all__'

class UnitOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitOptions
        fields = '__all__'

class ProductDrugTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDrugTypes
        fields = '__all__'

class ProductItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItemType
        fields = '__all__'


class ModBrandSalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandSalesman
        fields = ['brand_salesman_id','code','name','commission_rate','rate_on']

class BrandSalesmanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandSalesman
        fields = '__all__'



class ModProductBrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBrands
        fields = ['brand_id','brand_name','code']
        
class ProductBrandsSerializer(serializers.ModelSerializer):
    brand_salesman = ModBrandSalesmanSerializer(source='brand_salesman_id',read_only=True)
    class Meta:
        model = ProductBrands
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