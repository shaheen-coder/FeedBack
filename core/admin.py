from django.contrib import admin
from core.models import Student,Staff,Subject,FeedBack,ClassStaff,TimeScheduler
from core.models import  CustomUser 
from core.forms import ClassStaffForm
from import_export.admin import ImportExportModelAdmin
from core.resources import SubjectResource

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        if hasattr(request.user, 'is_princpl') and request.user.is_princpl:
            print(f'permission granted for CUser model !!')
            return False
        else:
            print(f'permission wasnt granted for CUser model !!')
            return True 
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(dept=request.user.dept)
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
    search_fields = ['staff__name','subject__code']
    def get_queryset(self,request):
        qs = super().get_queryset(request)
        if request.user.is_princpl : return qs 
        else: return qs.filter(staff__dept=request.user.dept)

admin.site.register(TimeScheduler)