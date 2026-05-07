from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(TopicInfo)
admin.site.register(QuizQuestion)
admin.site.register(QuizResult)