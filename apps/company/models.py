from django.db import models
from django.core.validators import RegexValidator
from passlib.hash import bcrypt  # type: ignore
import bcrypt,uuid,os # type: ignore
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from utils_methods import *
from utils_variables import *

def company_logos(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]
    # Construct the filename
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"company/{original_filename}_{unique_id}{file_extension}"

class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    print_name = models.CharField(max_length=255, null=False)
    short_name = models.CharField(max_length=100, null=True, default =None)
    code = models.CharField(max_length=100, null=True, default=None)
    num_branches = models.IntegerField(default=0)
    num_employees = models.IntegerField(null=True, default =None)
    logo = models.ImageField(null=True, upload_to=company_logos, default=None)
    address = models.CharField(max_length=255, default=None, null=True)
    city_id = models.ForeignKey('masters.City', on_delete=models.CASCADE, null=False, db_column = 'city_id')
    state_id = models.ForeignKey('masters.State', on_delete=models.CASCADE, null=False, db_column = 'state_id')
    country_id = models.ForeignKey('masters.Country', on_delete=models.CASCADE, null=True, db_column = 'country_id')
    pin_code = models.CharField(max_length=20, null=True, default=None)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=20, null=True, default=None)
    email = models.EmailField(max_length=255, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=None)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, default=None)
    print_address = models.TextField(null=True, default=None)
    website = models.URLField(max_length=255, default=None, null=True)
    facebook_url = models.URLField(max_length=255, default=None, null=True)
    skype_id = models.CharField(max_length=50, default=None, null=True)
    twitter_handle = models.CharField(max_length=50, default=None, null=True)
    linkedin_url = models.URLField(max_length=255, default=None, null=True)
    pan = models.CharField(max_length=50, default=None, null=True)
    tan = models.CharField(max_length=50, default=None, null=True)
    cin = models.CharField(max_length=50, default=None, null=True)
    gst_tin = models.CharField(max_length=50, default=None, null=True)
    establishment_code = models.CharField(max_length=50, default=None, null=True)
    esi_no = models.CharField(max_length=50, default=None, null=True)
    pf_no = models.CharField(max_length=50, default=None, null=True)
    authorized_person = models.CharField(max_length=255, default=None, null=True)
    iec_code = models.CharField(max_length=50, default=None, null=True)
    eway_username = models.CharField(max_length=100, default=None, null=True)
    eway_password = models.CharField(max_length=100, default=None, null=True)
    gstn_username = models.CharField(max_length=100, default=None, null=True)
    gstn_password = models.CharField(max_length=100, default=None, null=True)
    VAT_GST_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Pending', 'Pending'),
    )
    vat_gst_status = models.CharField(max_length=10, choices=VAT_GST_STATUS_CHOICES, default=None, null=True)
    GST_TYPE_CHOICES = (
        ('Goods', 'Goods'),
        ('Service', 'Service'),
        ('Both', 'Both')
    )
    gst_type = models.CharField(max_length=10, choices=GST_TYPE_CHOICES, default=None, null=True)
    einvoice_approved_only = models.BooleanField(default=False)
    marketplace_url = models.URLField(max_length=255, default=None, null=True)
    drug_license_no = models.CharField(max_length=50, default=None, null=True)
    other_license_1 = models.CharField(max_length=50, default=None, null=True)
    other_license_2 = models.CharField(max_length=50, default=None, null=True)
    turnover_less_than_5cr = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.company_id}.{self.name}"

    class Meta:
        db_table = companytable

    @receiver(pre_delete, sender='company.Companies')
    def delete_company_logo(sender, instance, **kwargs):
        if instance.logo and instance.logo.name:
            file_path = instance.logo.path
            if os.path.exists(file_path):
                os.remove(file_path)
                logo_dir = os.path.dirname(file_path)
                if not os.listdir(logo_dir):
                    os.rmdir(logo_dir)

    def save(self, *args, **kwargs):
        if self.pk:  # Check if instance already exists
            original = Companies.objects.get(pk=self.pk)
            # Ensure type consistency when comparing strings
            byte_prefix = "b'$2b$'"
            # Check if the incoming password is different and not already hashed
            if self.eway_password and (self.eway_password != original.eway_password) and not self.eway_password.startswith(byte_prefix):
                self.eway_password = bcrypt.hashpw(self.eway_password.encode(), bcrypt.gensalt()).decode()
            if self.gstn_password and (self.gstn_password != original.gstn_password) and not self.gstn_password.startswith(byte_prefix):
                self.gstn_password = bcrypt.hashpw(self.gstn_password.encode(), bcrypt.gensalt()).decode()
        else:
            # For new records, hash any passwords that aren't already hashes
            if self.eway_password and not self.eway_password.startswith("b'$2b$'"):
                self.eway_password = bcrypt.hashpw(self.eway_password.encode(), bcrypt.gensalt()).decode()
            if self.gstn_password and not self.gstn_password.startswith("b'$2b$'"):
                self.gstn_password = bcrypt.hashpw(self.gstn_password.encode(), bcrypt.gensalt()).decode()
        super().save(*args, **kwargs)

    def verify_eway_password(self, password):
        #Here I am Verifying the eway_password using bcrypt
        if self.eway_password:
            return bcrypt.checkpw(password.encode(), self.eway_password)
        return False

    def verify_gstn_password(self, password):
        #Here I am Verifying the gstn_password using bcrypt
        if self.gstn_password:
            return bcrypt.checkpw(password.encode(), self.gstn_password)
        return False

def branches_picture(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]

    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]

    # Construct the filename
    branch_name = instance.name.replace(' ', '_')
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"company/branch/{branch_name}/{original_filename}_{unique_id}{file_extension}"


class Branches(models.Model):
    branch_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Companies, on_delete=models.CASCADE, null=False, db_column = 'company_id')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, default=None, null=True)
    party = models.CharField(max_length=255, default=None, null=True)  
    gst_no = models.CharField(max_length=50, default=None, null=True)
    status_id = models.ForeignKey('masters.Statuses', on_delete=models.CASCADE, null=False, db_column = 'status_id')
    allowed_warehouse = models.CharField(max_length=255, default=None, null=True)
    e_way_username = models.CharField(max_length=255, default=None, null=True)
    e_way_password = models.CharField(max_length=255, default=None, null=True) 
    gstn_username = models.CharField(max_length=255, default=None, null=True)
    gstn_password = models.CharField(max_length=255, default=None, null=True) 
    other_license_1 = models.CharField(max_length=255, default=None, null=True)
    other_license_2 = models.CharField(max_length=255, default=None, null=True)
    picture = models.ImageField(max_length=255, default=None, null=True, upload_to=branches_picture) 
    address = models.CharField(max_length=255, default=None, null=True)
    city_id = models.ForeignKey('masters.City', on_delete=models.CASCADE, null=False, db_column = 'city_id')
    state_id = models.ForeignKey('masters.State', on_delete=models.CASCADE, null=False, db_column = 'state_id')
    country_id = models.ForeignKey('masters.Country', on_delete=models.CASCADE, null=True, db_column = 'country_id')
    pin_code = models.CharField(max_length=20, default=None, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=20, default=None, null=True)  # validators should be a list
    email = models.EmailField(max_length=255, default=None, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=None, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.branch_id}.{self.name}"
    
    class Meta:
        db_table = branchestable

    @receiver(pre_delete, sender='company.Branches')
    def delete_branches_picture(sender, instance, **kwargs):
        if instance.picture and instance.picture.name:
            file_path = instance.picture.path
            if os.path.exists(file_path):
                os.remove(file_path)
                picture_dir = os.path.dirname(file_path)
                if not os.listdir(picture_dir):
                    os.rmdir(picture_dir)

    def save(self, *args, **kwargs):
        if self.pk:  # Check if instance already exists
            original = Branches.objects.get(pk=self.pk)

            # Ensure type consistency when comparing strings
            byte_prefix = "b'$2b$'"

            # Check if the incoming password is different and not already hashed
            if self.e_way_password and (self.e_way_password != original.e_way_password) and not self.e_way_password.startswith(byte_prefix):
                self.e_way_password = bcrypt.hashpw(self.e_way_password.encode(), bcrypt.gensalt()).decode()
            if self.gstn_password and (self.gstn_password != original.gstn_password) and not self.gstn_password.startswith(byte_prefix):
                self.gstn_password = bcrypt.hashpw(self.gstn_password.encode(), bcrypt.gensalt()).decode()
        else:
            # For new records, hash any passwords that aren't already hashes
            if self.e_way_password and not self.e_way_password.startswith("b'$2b$'"):
                self.e_way_password = bcrypt.hashpw(self.e_way_password.encode(), bcrypt.gensalt()).decode()
            if self.gstn_password and not self.gstn_password.startswith("b'$2b$'"):
                self.gstn_password = bcrypt.hashpw(self.gstn_password.encode(), bcrypt.gensalt()).decode()

        super().save(*args, **kwargs)

    def verify_e_way_password(self, password):
        # Verify e_way_password using bcrypt
        if self.e_way_password:
            return bcrypt.checkpw(password.encode(), self.e_way_password)
        return False

    def verify_gstn_password(self, password):
        # Verify gstn_password using bcrypt
        if self.gstn_password:
            return bcrypt.checkpw(password.encode(), self.gstn_password)
        return False
    
class BranchBankDetails(models.Model):
    bank_detail_id = models.AutoField(primary_key=True)
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, null=False, db_column = 'branch_id')
    bank_name = models.CharField(max_length=255,default=None, null=True)
    account_number = EncryptedTextField(max_length=255, default=None, null=True)  # Using custom encrypted field
    branch_name = models.CharField(max_length=255, default=None, null=True)
    ifsc_code = models.CharField(max_length=100, default=None, null=True)
    swift_code = models.CharField(max_length=100, default=None, null=True)
    address = models.CharField(max_length=255, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name}"

    class Meta:
        db_table = branchbankdetails





