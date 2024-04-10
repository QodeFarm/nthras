from django.db import models

# Create your models here.
class Statuses(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.status_name}"
    
    class Meta:
        db_table = 'statuses'
