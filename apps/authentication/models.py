# from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
 
# #create User Manager (User created models)
# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None, password2=None):
       
#         if not username:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#           username=self.normalize_email(username),
#                     )
        
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
         

#     def create_superuser(self, username,  password=None):
#         user = self.create_user(
#             username,
#             password=password,                        
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
         

# # Custom user models
# class User(AbstractBaseUser):
#     user_id = models.AutoField(primary_key=True)
#     branch_id = models.IntegerField()
#     company_id = models.IntegerField(null=False)
#     username = models.EmailField(verbose_name="Username",max_length=255,unique=True)
#     first_name = models.CharField(max_length=255, null=False)
#     last_name = models.CharField(max_length=255, null=False)
#     email = models.EmailField(max_length=255, unique=True)
#     mobile_no = models.CharField(max_length=20)
#     otp_required = models.SmallIntegerField(null=True, default=False)
#     role_id = models.IntegerField(null=False)
#     status_id = models.SmallIntegerField(null=True, default=None)
#     profile_picture_url = models.URLField(max_length=255, null=True, blank=True)
#     bio = models.TextField() 
#     created_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)
#     GENDER_CHOICES = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#         ('Other', 'Other'),
#         ('Prefer Not to Say', 'Prefer Not to Say')
#     ]
#     gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Prefer Not to Say')
#     objects = UserManager()

#     class Meta:
#         db_table = 'users'

#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.username
# =========================================================================================
   
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, username ,password=None, password2=None):
        """Creates and saves a User with the given email, user_id, username, password, password2."""

        if not username:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None ):
        """
        Creates and saves a superuser with the given email, user_id, and username.
        """
        user = self.create_user(
            username,
            password=password,           
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    user_id = models.AutoField(primary_key=True)
    branch_id = models.IntegerField()
    company_id = models.IntegerField(null=False)
    username = models.EmailField(verbose_name="Username",max_length=255,unique=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    mobile= models.CharField(max_length=20)
    otp_required = models.SmallIntegerField(null=True, default=False)
    role_id = models.IntegerField(null=False)
    status_id = models.SmallIntegerField(null=True, default=None)
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
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Prefer Not to Say')
    # branch_id = models.ForeignKeyConstraint(['branch_id'], ['branches.branch_id'], on_delete=models.SET_NULL)
    # branch_id = models.ForeignKey(branches, on_delete=models.SET_NULL, default=None,db_column='branch_id')

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['branch_id']),
    #         models.Index(fields=['company_id']),
    #         models.Index(fields=['role_id']),
    #         models.Index(fields=['status_id']),
    #     ]
         
    #     constraints = [
    #         models.ForeignKeyConstraint(['company_id'], ['companies.company_id'], on_delete=models.CASCADE),
    #         models.ForeignKeyConstraint(['role_id'], ['roles.role_id']),
    #         models.ForeignKeyConstraint(['status_id'], ['statuses.status_id']),
    #     ]

    class Meta:
        db_table = 'users'

    objects = UserManager()

     

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

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