from django.db import models, IntegrityError
from django.contrib.auth.models import AbstractUser

import string
import random

# Create your models here.

class CustomUser(AbstractUser):
    # Extending the User model

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15, default=None, null=True, blank=True)
    current_class = models.CharField(max_length=10, default=None, null=True, blank=True)
    school_name = models.CharField(max_length=150, default=None, null=True, blank=True)
    parent_phone_number = models.CharField(max_length=15, default=None, null=True, blank=True)
    mother_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    father_name = models.CharField(max_length=50, default=None, null=True, blank=True)
    parent_email = models.EmailField(default=None, null=True, blank=True)
    home_address = models.CharField(max_length=500, default=None, null=True)
    registration_number = models.CharField(max_length=15, default=None, unique=True, null=True, blank=True)
    
    def __str__(self):
        if self.registration_number:
            return f'{self.first_name} {self.last_name} with reg num {self.registration_number}'
        
        return f'{self.first_name} {self.last_name}'
    
    def generate_reg_number(self):
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        while True:
            random_part = ''.join(random.choices(chars, k=6))

            if self.current_class:
                reg_number = f'{self.current_class}-{random_part}'
            else:
                reg_number = f'ADMIN-{random_part}'

            if not self.__class__.objects.filter(registration_number=reg_number).exists():
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
    topic_count = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} with {self.topic_count} topics'
    
    class Meta:
        ordering = ['name']
    

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    estimated_minutes = models.IntegerField(default=15)
    question_count = models.IntegerField(default=0, null=True)
    difficulty = models.CharField(max_length=20, choices=[('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')])
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f'{self.name} for {self.subject.name}'
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.subject.topic_count += 1
            self.subject.save(update_fields=['topic_count'])

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.subject.topic_count -= 1
        self.subject.save(update_fields=['topic_count'])
        super().delete(*args, **kwargs)


class TopicInfo(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, related_name='topic_info')
    short_note = models.TextField()
    learning_objectives = models.TextField()
    key_points = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.topic.name} information'


class QuizQuestion(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='quiz_questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=5, choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')])
    explanation = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic.name}'s question: {self.question_text}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.topic.question_count += 1
            self.topic.save(update_fields=['question_count'])

        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.topic.question_count -= 1
        self.topic.save(update_fields=['question_count'])
        super().delete(*args, **kwargs)


    

class QuizResult(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_results')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField(default=0, null=True, blank=True)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.first_name} {self.student.last_name} - {self.topic.name} result'
