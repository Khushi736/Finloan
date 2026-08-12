from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import random

from django.db import models
import random


class Signup(models.Model):

    full_name = models.CharField(max_length=100)

    mobile = models.CharField(
        max_length=15,
        unique=True
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=128
    )

    otp = models.CharField(
        max_length=6,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.otp:
            self.otp = str(
                random.randint(100000, 999999)
            )

        super().save(*args, **kwargs)

    



class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    mobile = models.CharField(
        max_length=10,
        unique=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    occupation = models.CharField(
        max_length=100,
        blank=True
    )

    monthly_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )



class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)



class LoanCategory(models.Model):

    name = models.CharField(max_length=100)

    description = models.TextField()

    banner = models.ImageField(
        upload_to='loan_banners/',
        blank=True,
        null=True
    )

    icon = models.ImageField(
        upload_to='loan_icons/',
        blank=True,
        null=True
    )

    interest_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    min_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    max_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    min_tenure = models.IntegerField()

    max_tenure = models.IntegerField()

    eligibility = models.JSONField(default=dict)

    documents_required = models.JSONField(default=list)

    features = models.JSONField(default=list)

    processing_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    is_active = models.BooleanField(default=True)

class KYCRecord(models.Model):

    user = models.OneToOneField(Signup,on_delete=models.CASCADE)

    aadhaar = models.FileField(upload_to='aadhaar/')

    pan = models.FileField(upload_to='pan/')

    selfie = models.ImageField(upload_to='selfie/')

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending','Pending'),
            ('Approved','Approved'),
            ('Rejected', 'Rejected'),
            
        ],
        default='Pending'
    )


class LoanApplication(models.Model):

    user = models.ForeignKey(Signup,on_delete=models.CASCADE)

    loan_category = models.ForeignKey(
        LoanCategory,
        on_delete=models.CASCADE
    )

    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)

    tenure = models.IntegerField()

    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)

    existing_emi = models.DecimalField(max_digits=10, decimal_places=2)

    credit_score = models.IntegerField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending','Pending'),
            ('Approved','Approved'),
            ('Rejected', 'Rejected'),
        ],
        default='Pending'
    )

class LoanRecommendation(models.Model):

    user = models.ForeignKey(Signup,on_delete=models.CASCADE)

    category = models.ForeignKey(
        LoanCategory,
        on_delete=models.CASCADE
    )

    score = models.FloatField()

    reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

class EMISchedule(models.Model):

    loan = models.ForeignKey(
        LoanApplication,
        on_delete=models.CASCADE
    )

    emi_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        default='Pending'
    )

class Notification(models.Model):

    user = models.ForeignKey(Signup,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email