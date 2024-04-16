from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from apps.company.models import Companies
from apps.masters.models import Statuses
from apps.company.models import Branches

class UserManager(BaseUserManager):
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


class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(verbose_name="Username",max_length=255,unique=True) 
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, unique=True)
    mobile= models.CharField(max_length=20, unique=True, null=False)
    otp_required = models.SmallIntegerField(null=True, default=False)
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)
    bio = models.TextField()
    timezone = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer Not to Say', 'Prefer Not to Say')
    ]

    is_active = models.BooleanField(default=True) 
    is_admin = models.BooleanField(default=False)


    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Prefer Not to Say')
    company_id = models.ForeignKey(Companies, on_delete=models.CASCADE, default=None,db_column='company_id')
    status_id = models.ForeignKey(Statuses, on_delete=models.CASCADE, default=None,db_column='status_id')
    role_id = models.IntegerField(null=False)
    branch_id = models.ForeignKey(Branches, on_delete=models.CASCADE, default=None,db_column='branch_id')


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'Last_name' ]

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
    
