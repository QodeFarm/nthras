from rest_framework import serializers

class VoucherSerializer(serializers.Serializer):
    voucher_value = serializers.CharField(max_length=255)
