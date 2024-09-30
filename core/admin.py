from django.contrib import admin
from core.models import Student,Staff,Subject,FeedBack,ClassStaff
# Register your models here.

admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
admin.site.register(FeedBack)
admin.site.register(ClassStaff)