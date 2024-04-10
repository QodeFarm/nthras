from django.db import models

class User(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer Not to Say', 'Prefer Not to Say')
    ]
    user_id = models.AutoField(primary_key=True)
    #ledger_account_id = models.ForeignKey(LedgerAccounts, on_delete=models.CASCADE, default=None, db_column='ledger_account_id')
#    branch_id = models.PositiveIntegerField(null=True, db_index=True)
#    company_id = models.PositiveIntegerField(db_index=True)
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.CharField(max_length=60)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    mobile = models.CharField(max_length=20, unique=True)
    otp_required = models.BooleanField(default=False)
   # role_id = models.PositiveIntegerField()
   # status_id = models.PositiveIntegerField()
    profile_picture_url = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True, null=True)
    language = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Prefer Not to Say')

    class Meta:
        db_table = 'users'
    
    # class Meta:
    #     indexes = [
    #         models.Index(fields=['branch_id']),
    #         models.Index(fields=['company_id']),
    #         models.Index(fields=['role_id']),
    #         models.Index(fields=['status_id']),
    #     ]
    #     constraints = [
    #         models.ForeignKeyConstraint(['branch_id'], ['branches.branch_id'], on_delete=models.SET_NULL),
    #         models.ForeignKeyConstraint(['company_id'], ['companies.company_id'], on_delete=models.CASCADE),
    #         models.ForeignKeyConstraint(['role_id'], ['roles.role_id']),
    #         models.ForeignKeyConstraint(['status_id'], ['statuses.status_id']),
    #     ]
