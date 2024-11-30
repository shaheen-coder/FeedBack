from django.contrib import admin
from core.models import Student,Staff,Subject,FeedBack,ClassStaff
from core.models import  CustomUser 
from core.forms import ClassStaffForm
from import_export.admin import ImportExportModelAdmin

admin.site.register(CustomUser)

@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(dept=request.user.dept)
#admin.site.register(Staff)
@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    list_filter = ('dept','gender')
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(dept=request.user.dept)
admin.site.register(Subject)
admin.site.register(FeedBack)

@admin.register(ClassStaff)
class ClassStaffAdmin(ImportExportModelAdmin):
    search_fields = ['staff__name','subject__code']
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(staff__dept=request.user.dept)