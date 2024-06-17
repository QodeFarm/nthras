from django.db.models import Q
from apps.sales.models import SaleOrder

# Collect all primary keys of instances
primary_keys = SaleOrder.objects.values_list('id', flat=True)
print("Primary Keys:", primary_keys)

# Create a Q object for the primary keys
query = Q(id__in=primary_keys)

# Delete all instances with the collected primary keys
SaleOrder.objects.filter(query).delete()
