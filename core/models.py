from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser

import string
import random

# Create your models here.

class CustomUser(AbstractUser):
    # Extending the User model

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, default=None, null=True)
    current_class = models.CharField(max_length=10, default=None, null=True)
    school_name = models.CharField(max_length=150, default=None, null=True)
    parent_phone_number = models.CharField(max_length=15, default=None, null=True)
    mother_name = models.CharField(max_length=50, default=None, null=True)
    father_name = models.CharField(max_length=50, default=None, null=True)
    parent_email = models.EmailField(default=None, null=True)
    home_address = models.CharField(max_length=500, default=None, null=True)
    registration_number = models.CharField(max_length=10, default=None, unique=True)
    best_score = models.IntegerField(default=0, null=True)
    average_score = models.IntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} with reg num {self.registration_number}'
    
    def generate_reg_number(self):
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        while True:
            random_part = ''.join(random.choices(chars, k=6))
            reg_number = f'{self.current_class}-{random_part}'
            if not self.__class__.objects.filter(registration_number=reg_number):
                return reg_number
    
    def save(self, *args, **kwargs):
        if not self.registration_number:
            for _ in range(10):
                self.registration_number = self.generate_reg_number()
                try:
                    super().save(*args, **kwargs)
                    return
                
                except IntegrityError:
                    self.registration_number = None

            raise ValueError('Could not generate unique registration number')
        else:
            super().save(*args, **kwargs)


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    icon = models.CharField(max_length=50)
    topic_count = models.IntegerField(default=None, null=True)

    def __str__(self):
        return f'{self.name} with {self.topic_count} topics'
    

