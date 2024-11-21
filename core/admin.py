from django.contrib import admin
from core.models import Student,Staff,Subject,FeedBack,ClassStaff
from core.forms import ClassStaffForm
# Register your models here.

#admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subject)
#admin.site.register(FeedBack)

class ClassStaffAdmin(admin.ModelAdmin):
    form = ClassStaffForm
    list_display = ('staff','section','subject','semester')
    fieldsets = (
        ('Class Information', {
            'fields': ('course_type','semester', 'section', 'staff','subject')
        }),
    )
admin.site.register(ClassStaff, ClassStaffAdmin)