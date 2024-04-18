from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import pre_delete
from apps.company.models import Companies
from apps.masters.models import Statuses
from apps.company.models import Branches
from django.dispatch import receiver
from utils_variables import *
from django.db import models
import uuid, os


class Roles(models.Model):
    role_name = models.CharField( max_length=255, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role_id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = rolestable

    def __str__(self):
        return f"{self.role_id}.{self.role_name}"


class Permissions(models.Model):
    permission_name = models.CharField( max_length=255, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    permission_id = models.AutoField(primary_key=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    
    class Meta:
        db_table = permissionstable

    def __str__(self):
        return f"{self.permission_id}.{self.permission_name}"
  

class Role_Permissions(models.Model):
    permission_id = models.ForeignKey(Permissions, on_delete=models.CASCADE, null=True, default=None, db_column = 'permission_id')
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, default=None, db_column = 'role_id')
    access_level = models.CharField( max_length=255, null=False)
    role_permission_id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = rolepermissionstable

    def __str__(self):
        return f"{self.role_permission_id}.{self.access_level}"


class Actions(models.Model):
    action_name = models.CharField( max_length=255, null=False, unique=True)
    action_id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = actionstable

    def __str__(self):
        return f"{self.action_id}.{self.action_name}"


class Modules(models.Model):
    module_name = models.CharField( max_length=255, null=False, unique=True)
    module_id = models.AutoField(primary_key=True)
    description = models.TextField()

    class Meta:
        db_table = modulestable

    def __str__(self):
        return f"{self.module_id}.{self.module_name}"


class Module_Sections(models.Model):
    module_id = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, default=None, db_column = 'module_id')
    section_name = models.CharField( max_length=255, null=False)
    section_id = models.AutoField(primary_key=True)


    class Meta:
        db_table = modulesections

    def __str__(self):
        return f"{self.section_id}.{self.section_name}"



class UserManager(BaseUserManager):
    '''Creating User'''
    def create_user(self, email, username, password = None, **extra_fields):
        if not email:
            raise ValueError("The Email Field Must be set")        
        email = self.normalize_email(email)
        user = self.model(
        email = email,
        username = username,
        **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username, email, password=password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

def profile_picture(instance, filename):
    '''Uploading Profile Picture'''
    # Get the file extension
    file_extension = os.path.splitext(filename)[-1]
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:6]
    # Construct the filename
    original_filename = os.path.splitext(filename)[0]  # Get the filename without extension
    return f"users/{original_filename}_{unique_id}{file_extension}"


class User(AbstractBaseUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer Not to Say', 'Prefer Not to Say')
    ]
    profile_picture_url = models.ImageField(max_length=255, default=None, null=True, upload_to=profile_picture) 
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Prefer Not to Say')
    username = models.CharField(verbose_name="Username",max_length=255,unique=True) 
    timezone = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    otp_required = models.SmallIntegerField(null=True, default=False)
    mobile= models.CharField(max_length=20, unique=True, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_login = models.DateTimeField(blank=True, null=True)
    last_name = models.CharField(max_length=255, null=False)
    date_of_birth = models.DateField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    user_id = models.AutoField(primary_key=True)
    bio = models.TextField() 
    
    company_id = models.ForeignKey(Companies, on_delete=models.CASCADE,db_column='company_id')
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, db_column='branch_id')
    status_id = models.ForeignKey(Statuses, on_delete=models.CASCADE,db_column='status_id')
    role_id = models.ForeignKey(Roles, on_delete=models.CASCADE, db_column='role_id')

    objects = UserManager()
    
    class Meta:
        db_table = userstable

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'mobile', 'profile_picture_url','bio', 'language', 'date_of_birth', 'gender', 'timezone','company_id','status_id','branch_id','role_id'] 

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name} "

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    @receiver(pre_delete, sender='users.User')
    def delete_user_picture(sender, instance, **kwargs):
        if instance.profile_picture_url and instance.profile_picture_url.name:
            file_path = instance.profile_picture_url.path
            if os.path.exists(file_path):
                os.remove(file_path)
                picture_dir = os.path.dirname(file_path)
                if not os.listdir(picture_dir):
                    os.rmdir(picture_dir)
