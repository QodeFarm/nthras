from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, company_id=None, role_id=None, mobile=None, status_id=None,  password=None, is_active=True):
        """
        Creates and saves a User with the given branch_id, company_id, username, first_name, last_name, email, mobile,  password.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            
            username = username,
            first_name = first_name,
            last_name = last_name,
            company_id = company_id,
            role_id = role_id,
            mobile = mobile,
            status_id =status_id,
            is_active=is_active,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name,mobile,company_id = None , status_id = None,is_admin = True, password=None):
        """
        Creates super user and saves a User with the given branch_id, company_id, username, first_name, last_name, email, mobile and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            
            username = username,
            first_name = first_name,
            last_name = last_name,
            
            company_id = company_id,
            mobile = mobile,
            is_admin = is_admin,
            status_id =status_id
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
 

# Custom User Model.
class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
   # branch_id = models.IntegerField()
    company_id = models.IntegerField(null=False) 
    username = models.CharField(verbose_name="Username",max_length=255,unique=True) 
    is_admin = models.BooleanField(default=False)   
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255,unique=True)
    mobile= models.CharField(max_length=20, unique=True, null=False)
    otp_required = models.SmallIntegerField(null=True, default=False)
    role_id = models.IntegerField(null=False)
    status_id = models.SmallIntegerField(null=True, default=None)
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)
    bio = models.TextField()
    timezone = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #last_login = models.DateTimeField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer Not to Say', 'Prefer Not to Say')
    ]
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Prefer Not to Say')
    
    # branch_id = models.ForeignKeyConstraint(['branch_id'], ['branches.branch_id'], on_delete=models.SET_NULL)
    # branch_id = models.ForeignKey(branches, on_delete=models.SET_NULL, default=None,db_column='branch_id')
    
    class Meta:
        db_table = 'users'
        
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS=['first_name','last_name', 'email', 'mobile']



    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name 

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