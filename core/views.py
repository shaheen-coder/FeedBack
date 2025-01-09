#django
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail
from datetime import date
# view 
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import UserPassesTestMixin
#models 
from core.models import Staff,Student,ClassStaff,Subject,FeedBack,TimeScheduler
from core.models import CustomUser as User 
from django.db.models import Q
from django.db.models import Avg,Count
from django.db import IntegrityError
#forms 
# others
from datetime import datetime
import json 
from collections import defaultdict
import pandas as pd

# gobale  
terms = [
    "Aids Utilization",
    "Clarity",
    "Confidence",
    "Pacing",
    "Discipline",
    "Engagement",
    "Accessibility",
    "Punctuality",
    "Guidance",
    "Feedback"
]
DEPARTMENT = (
    ('Computer Science and Engineering','CSE'),
    ('Information Technology','IT'),
    ('Instrumentation and Controls Engineering','IT'),
    ('Electrical and Electronics Engineering','EEE')
)

# normal template rendering page views 
class Home(TemplateView):
    template_name = 'landing.html'
class Team(TemplateView):
    template_name = 'team.html'
class Error(TemplateView):
    template_name = '404.html'
class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']
# api views 

# feeback and student views 

class StudentLogin(View):
    template_name = 'login22.html'
    def get(self,request):
        return render(self.request,self.template_name)
    def post(self,request):
        regno = int(request.POST.get('regno'))
        dob = request.POST.get('dob')
        dob = datetime.strptime(dob,'%Y-%m-%d').date()
        try:
            student = Student.objects.get(regno=regno,dob=dob)
            time_scheduler = TimeScheduler.objects.filter(dept=student.dept).first()
            if not time_scheduler:
                return render(self.request,self.template_name,{"error": "No FeedBack found for the department."})

            current_time = date.today()
            if not (time_scheduler.start_time <= current_time <= time_scheduler.end_time):
                return render(self.request,self.template_name,{"error": "Feedback time is ended !!."})
            if (time_scheduler.feed == 1 and student.feed1_status) or (time_scheduler.feed == 2 and student.feed2_status):
                return render(self.request,self.template_name,{'error':"you have already sumited feedback"})
            # Check if the student's status is active
            if not student.status:
                return render(self.request,self.template_name,{"error": "Student ID isn't updated."})

            # Check feed1_status and feed2_status
            if student.feed1_status and student.feed2_status:
                return render(self.request,self.template_name,{"error": "Student has already filled feedback forms."})

            # Determine which feedback is available
            available_feedback = 0
            if not student.feed1_status:
                available_feedback = 1 
            elif not student.feed2_status:
                available_feedback = 2 
            return redirect('feed',sid=student.id,fid=available_feedback)
        except Student.DoesNotExist:
            print('error student doesnt exists')
            return render(self.request,self.template_name,{'error' : 'Student doesnt exists'})
class Course(View):
    template_name = 'coruse.html'
    def get(self,request,sid,fid):
        return render(self.request,self.template_name,{'sid':sid,'fid':fid})

class Manitiory(View):
    template_name = 'subject.html'
    def get(self,request,sid,cid,fid):
        return render(self.request,self.template_name,{'cid':cid,'sid':sid,'fid':fid})
class ManitioryForm(View):
    template_name = 'feed_sample.html'
    def get(self,request,sid,cid,fid,subid):
        return render(self.request,self.template_name,{'id':sid,'cid':cid,'fid':fid,'subid':subid,'is_manitiory':1})


class FeedBackView(View):
    def get(self,request,sid,fid):
        manitiory = 0
        student = Student.objects.get(id=sid)
        if student.semester > 4: manitiory = 1
        return render(self.request,'feed_sample.html',{'id':sid,'fid':fid,'cid':0,'subid':'null','is_manitiory':manitiory})
    

#   admin view

class Profile(View):
    
    def get_department_code(self,department_name):
        for dept in DEPARTMENT:
            if dept[0] == department_name:
                return dept[1]
        return None 
    def get(self,request,id,subject):
        staff = Staff.objects.get(id=id)
        subject = Subject.objects.get(code=subject)
        staffd = ClassStaff.objects.get(staff=staff,subject=subject)
        #dept = self.get_department_code(staff.dept)
        return render(self.request,'analysis.html',{'mode':'staffsub','profile':staff,'subject':subject,'staffd':staffd})
class StaffProfile(View):
    template_name = 'analysis.html'
    def get(self,request,id,dept):
        staff = Staff.objects.get(id=id)
        return render(self.request,self.template_name,{'mode':'staff','staff':staff})
class DeptProfile(View):
    template_name = 'analysis.html'
    def get(self,request,dept):
        return render(self.request,self.template_name,{'mode':'dept','dept':dept})
class ClassProfile(View):
    template_name = 'analysis.html'
    def get(self,request,semester,section,dept):
        return render(self.request,self.template_name,{'mode':'class','semester':semester,'section':section,'dept':dept})
'''.
principal views 
'''
# report search view 
class IsPrincipal(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_princpl
    def handle_no_permission(self):
        return render(self.request,'403.html',)
        return render(self.request,'403.html', status=403)
class Search(IsPrincipal,View):
    template_name = 'prinicipal/analysis/search.html'
    template_name2 = 'prinicipal/analysis/ssearch.html'
    template_name3 = 'prinicipal/analysis/dept.html'
    template_name4 = 'prinicipal/analysis/analysis_dept.html'
    def get(self,request,mode,ana):
        if mode == 'stu' : return render(self.request,self.template_name2,{'mode':mode,'is_analysis':ana})
        if mode == 'stucomt' : return render(self.request,self.template_name2,{'mode':mode,'is_analysis':ana})
        if ana and mode == 'dept' : return render(self.request,self.template_name4,{'mode':'dept'})
        if mode == 'dept' : return render(self.request,self.template_name3,{'mode':mode,'is_analysis':ana})
        return render(self.request,self.template_name,{'mode':mode,'is_analysis':ana})
class ClassSearch(View):
    template_name = 'prinicipal/analysis/csearch.html'
    def get(self,request,mode,ana):
        return render(self.request,self.template_name,{'mode':mode,'is_analysis':ana})
class PrinicpalDash(IsPrincipal,View):
    template_name = 'prinicipal/home.html'
    def get(self,request):
        return render(self.request,self.template_name)

class AddHodUser(View):
    template_name = 'prinicipal/add_hod.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        file = request.FILES['file']
        xl = pd.read_excel(file)
        try :
            for index, row in xl.iterrows():
                username = row['username']
                email = row['email']
                password = row['password']
                dept = row['department']
                if not User.objects.filter(email=email).exists():
                    user = User(username=username, email=email,dept=dept,is_staff=True,is_superuser=True,is_hod=True)
                    user.set_password(password) 
                    user.save()
                else : return render(request,self.template_name,{'error':f'the email {email} already exists !!'})
        except Exception as error:
            return render(request,self.template_name,{'error':f'field {error} not found'})
        return render(request,self.template_name,{'success':'user added !!'})      

class AnalysisMode(TemplateView):
    template_name = 'prinicipal/analysis/searchmode.html'
class ReportMode(TemplateView):
    template_name = 'prinicipal/report/reportmode.html'
class PReport(View):
    template_name = 'prinicipal/report.html'
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
    template_name = 'prinicipal/report.html'
    def get(self,request,mode,sec,sem,dept):
        return render(self.request,self.template_name,{'mode':mode,'dept':dept,'section':sec,'sem':sem})
class DeptReport(View):
    template_name = 'prinicipal/dept_report.html'
    def get(self,request,dept):
        file_name = f'{dept}-report'
        if dept == 'CLG':
            return render(self.request,self.template_name,{'file_name':file_name,'mode':'CLG','api':'ins'})

        return render(self.request,self.template_name,{'file_name':file_name,'mode':'dept','key':dept,'dept':dept})


class StudentPromote(View):
    template_name = 'prinicipal/promoson.html'
    def get(self,request):
        return render(self.request,self.template_name)
    def post(self, request):
        try:
            dept = request.POST.get('CSE', None)
            if dept is not None:  # Ensure dept is provided
                dept = int(dept)  # Convert to integer
                print(f'sem: {dept}')
                # Update only if valid dept is provided
                Student.objects.filter(dept='CSE', semester=dept).update(semester=dept + 1,status=False)
                
                return render(self.request, self.template_name, {'error': 'Students year is updated!'})
            else:
                return render(self.request, self.template_name, {'error': 'Invalid semester value provided!'})
        except Exception as ex:
            return render(self.request, self.template_name, {'error': f'Error: {ex}'})
class CommentSearch(View):
    template_name = 'prinicipal/comment.html'
    def get(self,request):
        return render(self.request,self.template_name,{'mode':'stu','is_analysis':0})
class CommentView(View):
    template_name = 'comment.html'
    def get(self,request,sid):
        student = Student.objects.get(id=sid)
        return render(self.request,self.template_name,{'student':student,'sid':sid})