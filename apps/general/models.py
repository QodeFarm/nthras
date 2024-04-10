from django.db import models
from django.core.validators import RegexValidator
from passlib.hash import bcrypt 
import bcrypt,uuid,base64

def company_logos(instance, filename):
    company_name = instance.name.replace(' ', '_')
    unique_id = uuid.uuid4().hex[:6] #Generates a unique identifier
    return f"company_logos/{company_name}_{unique_id}/{filename}"

class Companies(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    print_name = models.CharField(max_length=255, null=True, default=None)
    short_name = models.CharField(max_length=100, null=True, default =None)
    code = models.CharField(max_length=100, null=True, default=None)
    num_branches = models.IntegerField(default=0)
    logo = models.ImageField(null=True, upload_to=company_logos, default=None)
    address = models.TextField(null=True)
    country = models.CharField(max_length=100,null=True, default=None)
    state = models.CharField(max_length=255, null=True, default=None)
    city = models.CharField(max_length=255, null=True, default=None)
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
        db_table = 'companies'

    def save(self, *args, **kwargs):
        if self.eway_password:
            #Here I am Hashig the eway_password using bcrypt and save as bytes
            hashed_eway_password = bcrypt.hashpw(self.eway_password.encode(), bcrypt.gensalt())
            self.eway_password = hashed_eway_password
        if self.gstn_password:
            #Here I am Hashig the gstn_password using bcrypt and save as bytes
            hashed_gstn_password = bcrypt.hashpw(self.gstn_password.encode(), bcrypt.gensalt())
            self.gstn_password = hashed_gstn_password
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
    # Assuming 'instance' is an instance of our model
    branch_name = instance.name.replace(' ', '_')
    unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
    return f"branches_pictures/{branch_name}_{unique_id}/{filename}"

class Branches(models.Model):
    branch_id = models.AutoField(primary_key=True)
    company_id = models.ForeignKey(Companies, on_delete=models.CASCADE, null=True, default=None, db_column = 'company_id')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    party = models.CharField(max_length=255, default=None, null=True)  
    gst_no = models.CharField(max_length=50, unique=True,  null=True)
    status_id = models.ForeignKey('masters.Statuses', on_delete=models.CASCADE, null=True, default=None, db_column = 'status_id')
    allowed_warehouse = models.CharField(max_length=255, default=None, null=True)
    e_way_username = models.CharField(max_length=255, default=None, null=True)
    e_way_password = models.CharField(max_length=255, default=None, null=True) 
    gstn_username = models.CharField(max_length=255, default=None, null=True)
    gstn_password = models.CharField(max_length=255, default=None, null=True) 
    other_license_1 = models.CharField(max_length=255, default=None, null=True)
    other_license_2 = models.CharField(max_length=255, default=None, null=True)
    picture = models.ImageField(max_length=255, default=None, null=True, upload_to=branches_picture) 
    address = models.TextField(default=None, null=True)
    country = models.CharField(max_length=50, default=None, null=True)
    state = models.CharField(max_length=50, default=None, null=True)
    city = models.CharField(max_length=50, default=None, null=True)
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
        db_table = 'branches' 

    def save(self, *args, **kwargs):
        if self.e_way_password:
            # Hash the e_way_password using bcrypt and save as bytes
            hashed_eway_password = bcrypt.hashpw(self.e_way_password.encode(), bcrypt.gensalt())
            self.e_way_password = hashed_eway_password
        if self.gstn_password:
            # Hash the gstn_password using bcrypt and save as bytes
            hashed_gstn_password = bcrypt.hashpw(self.gstn_password.encode(), bcrypt.gensalt())
            self.gstn_password = hashed_gstn_password
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
    

# Dummy encryption and decryption functions for demonstration purposes
def encrypt(text):
    # Encode the text using base64
    encoded_bytes = base64.b64encode(text.encode("utf-8"))
    encrypted_text = encoded_bytes.decode("utf-8")
    return encrypted_text

def decrypt(encrypted_text):
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

class BranchBankDetails(models.Model):
    bank_detail_id = models.AutoField(primary_key=True)
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, null=True, default=None, db_column = 'branch_id')
    bank_name = models.CharField(max_length=255)
    account_number = EncryptedTextField(max_length=255)  # Using custom encrypted field
    branch_name = models.CharField(max_length=255, default=None, null=True)
    ifsc_code = models.CharField(max_length=100, default=None, null=True)
    swift_code = models.CharField(max_length=100, default=None, null=True)
    address = models.TextField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bank details for Branch ID: {self.bank_name}"

    class Meta:
        db_table = 'branch_bank_details' 

'''
#If you want to decrypt then you can uncomment this and run... in output you will find the decrypted account number 

import base64

# Encoded account number
encoded_account_number = "pass encoded account number here which will be available in your database"

# Decode from base64
decoded_bytes = base64.b64decode(encoded_account_number)

# Convert bytes to string
original_account_number = decoded_bytes.decode("utf-8")

print("Decrypted Account Number:", original_account_number)

'''
