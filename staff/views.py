from django.shortcuts import render
from django.views.generic import View,TemplateView
from core.models import Student,Staff,TimeScheduler
# Create your views here.

class StudentCheck(View):
    template_name = 'staff/analysis/student.html'
    def get(self,request):
        return render(self.request,self.template_name,{'students':None})
    def post(self,request):
        if request.POST.get('sem') == '':
            return render(self.request,self.template_name,{'error':'please select the year !! '})
        sem = request.POST.get('sem')
        section = request.POST.get('class')
        students = Student.objects.filter(semester=sem)
        if section:
            students = students.filter(section=section)
        return render(self.request,self.template_name,{'students':students})

class Search(View):
    template_name = 'staff/analysis/search.html'
    template_name2 = 'staff/analysis/ssearch.html'
    template_name3 = 'staff/analysis/dept.html'
    template_name4 = 'staff/analysis_dept.html'
    def get(self,request,mode,ana):
        if mode == 'stu': return render(self.request,self.template_name2,{'mode':"stu",'is_analysis':ana})
        if mode == 'stucomt': return render(self.request,self.template_name2,{'mode':"stucomt",'is_analysis':ana})
        if ana and mode == 'dept' : return render(self.request,self.template_name4,{'mode':'dept'})
        if mode == 'dept' : return render(self.request,self.template_name3,{'mode':mode,'is_analysis':ana})
        return render(self.request,self.template_name,{'mode':mode,'is_analysis':ana})
class ClassSearch(View):
    template_name = 'staff/analysis/csearch.html'
    def get(self,request,mode,ana):
        return render(self.request,self.template_name,{'mode':mode,'is_analysis':ana})
class StaffDash(View):
    template_name = 'staff/home.html'
    template_403 = '403.html'
    def get(self,request):
        if request.user.is_princpl: return render(self.request,self.template_403,{'content':'check prinicipal page'})
        return render(self.request,self.template_name)

class AnalysisMode(TemplateView):
    template_name = 'staff/analysis/searchmode.html'
class ReportMode(TemplateView):
    template_name = 'staff/report/reportmode.html'
class PReport(View):
    template_name = 'staff/report.html'
    def get(self,request,mode,key,dept):
        if mode == 'class':
            return render(self.request,self.class_template_name,{'mode':mode,'dept':dept,'section':key})
        elif mode == 'staffsub':
            staffd = ClassStaff.objects.get(id=int(key))
            file_name = f'{staffd.staff.name}-{staffd.section}-report'
            return render(self.request,self.template_name,{'file_name':file_name,'mode':mode,'staffd':staffd,'key':key,'dept':dept})
        elif mode == 'stu':
            student = Student.objects.get(id=int(key))
            file_name = f'{student.name}-{student.section}-report'
            return render(self.request,self.template_name,{'file_name':file_name,'mode':mode,'student':student,'dept':student.dept})
        staff = Staff.objects.get(id=key)
        file_name = f'{staff.name}-report'
        return render(self.request,self.template_name,{'file_name':file_name,'staff':staff,'mode':mode,'id':staff.id,'dept':dept})


class ClassReport(View):
    template_name = 'staff/report.html'
    def get(self,request,mode,sec,sem,dept):
        return render(self.request,self.template_name,{'mode':mode,'dept':dept,'section':sec,'sem':sem})
class DeptReport(View):
    template_name = 'staff/dept_report.html'
    def get(self,request,dept):
        file_name = f'{dept}-report'
        if dept == 'CLG':
            return render(self.request,self.template_name,{'file_name':file_name,'mode':'CLG','api':'ins'})
        return render(self.request,self.template_name,{'file_name':file_name,'mode':'dept','key':dept,'dept':dept})


class StaffCheck(View):
    template_name = 'staff/staffcheck.html'
    def get(self,request):
        return render(self.request,self.template_name)
    def post(self,request):
        dept = request.POST.get('dept',None)
        name = request.POST.get('name',None)
        gender = request.POST.get('gender',None)
        if not dept : return render(self.request,self.template_name,{'error':'department field missing'})
        staffs = Staff.objects.filter(dept=dept)
        if name: staffs = staffs.filter(name__icontains=name)
        if gender: staffs = staffs.filter(gender=int(gender))
        return render(self.request,self.template_name,{'staffs':staffs})

class FeedScheduler(View):
    template_name = 'staff/feedtime.html'
    def get(self,request):
        return render(self.request,self.template_name)
    def post(self,request):
        try :
            start_time = request.POST.get('start_time',None)
            end_time = request.POST.get('end_time',None)
            dept = request.POST.get('dept',None)
            print(f'st time : {start_time} and end time : {end_time}')
            TimeScheduler.objects.create(start_time=start_time,end_time=end_time,dept=dept)
        except Exception as ex :
            return render(self.request,self.template_name,{'error':ex})
        return render(self.request,self.template_name,{'error':'time has been schedule !!'})