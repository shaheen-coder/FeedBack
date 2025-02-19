from django.contrib import admin
from core.models import Student,Staff,Subject,FeedBack,ClassStaff,TimeScheduler
from core.models import  CustomUser 
from django.contrib.auth.admin import UserAdmin
from core.forms import ClassStaffForm
from import_export.admin import ImportExportModelAdmin
from core.resources import SubjectResource

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass 
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(dept=request.user.dept,status=True)
@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    list_filter = ('dept','gender')
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(dept=request.user.dept)
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource 
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else : return qs.filter(dept=request.user.dept)

admin.site.register(FeedBack)

@admin.register(ClassStaff)
class ClassStaffAdmin(ImportExportModelAdmin):
    search_fields = ['staff__name','subject__code','dept']
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(staff__dept=request.user.dept)

admin.site.register(TimeScheduler)