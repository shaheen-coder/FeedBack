#django
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.views import View
from django.views.generic import TemplateView
from core.models import Staff,Student,ClassStaff,Subject,FeedBack
from core.models import CustomUser as User 
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Avg,Count
from django.contrib.auth.views import LogoutView
from django.db import IntegrityError
from core.forms import StudentLoginForm
# others
from datetime import datetime
import json 
from weasyprint import HTML
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
    template_name = 'captcha.html'
    def get(self,request):
        form = StudentLoginForm()
        return render(self.request,self.template_name,{'form':form})
    def post(self,request):
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            regno = int(request.POST.get('regno'))
            dob = request.POST.get('dob')
            dob = datetime.strptime(dob,'%Y-%m-%d').date()
            try:
                student = Student.objects.get(regno=regno,dob=dob)
                return redirect('feed',sid=student.id,catid=0)
            except Student.DoesNotExist:
                return render(self.request,self.template_name,{'error' : 'Student doesnt exists'})
        else: return render(self.request,self.template_name,{'form':form})
        
class Course(View):
    template_name = 'coruse.html'
    def get(self,request,sid):
        return render(self.request,self.template_name,{'sid':sid})

class Manitiory(View):
    template_name = 'subject.html'
    def get(self,request,sid,cid):
        is_both = None
        student = Student.objects.get(id=sid)
        manitiory,openelective,elective = False,False,False
        if cid == 1 : manitiory = True
        elif cid == 2 : openelective = True 
        elif cid == 3 : elective = True
        course = ClassStaff.objects.filter(semester=student.semester,subject__mcourse=manitiory,subject__ecourse=elective,subject__oecourse=openelective)
        if course.count() == 0: return render(self.request,self.template_name,{'error':'no courses are available','student':student,'cid':cid})
        if course.count() >= 6 :
            half = len(course) // 2 
            half += 1 if half % 2 != 0 else 0
            course1 = course[0:half]
            course2 = course[half::]
            is_both = True
            return render(self.request,self.template_name,{'cid':cid,'student':student,'semester':student.semester,'course1':course1,'course2':course2,'both_side':is_both})
        print(f'cid : {cid}')
        return render(self.request,self.template_name,{'student':student,'semester':student.semester,'courses':course,'cid':cid,'both_side':is_both})
class ManitioryForm(View):
    template_name = 'mfeed.html'
    def score(self,data) :
        if data == 'excellent': return 5
        elif data == 'good': return 3
        elif data == 'average': return 1
        else : None
    def convert_json(self,request):
        data = {}
        for i in range(0,11):
            cat = request.POST.get(f'cat_{i}')
            data[f'cat_{i}'] = self.score(cat)
        return data 
    def get(self,request,sid,csid,cid):
        student = Student.objects.get(id=sid)
        data = ClassStaff.objects.get(id=csid)
        return render(self.request,self.template_name,{'data':data,'sid':student,'cid':cid})
    def post(self,request,sid,csid,cid):
        student = Student.objects.get(id=sid)
        staff = int(request.POST.get('staff_name'))
        #print(f'satff id : {staff}')
        staff = Staff.objects.get(id=staff)
        subject_code = request.POST.get('subject_code')
        subject = Subject.objects.get(subject_code=subject_code)
        categories = self.convert_json(request) 
        feedback, created = FeedBack.objects.update_or_create(
            subject=subject,
            student=student,
            staff=staff,
            categories=categories
        )
        return redirect('msubject',sid=sid,cid=cid)

class FeedBackView(View):
    def score(self,data) :
        if data == 'excellent': return 5
        elif data == 'good': return 3
        elif data == 'average': return 1
        else : None
    def convert_json(self,request):
        data = {}
        for i in range(0,10):
            cat = request.POST.get(f'cat_{i}')
            data[f'cat_{i+1}'] = self.score(cat)
        return data 
    def get(self,request,sid,catid):
        student = Student.objects.get(id=sid)
        class_staff = ClassStaff.objects.filter(dept=student.dept,subject__semester=student.semester,section=student.section,subject__mcourse=False,subject__ecourse=False,subject__oecourse=False)
        if len(class_staff) == catid: 
            if(student.semester > 3) : return redirect('course',sid=sid)
            else : return redirect('home')
        return render(self.request,'feed_sample.html',{'data':class_staff[catid],'sid':sid,'catid':catid})
    def post(self,request,sid,catid):
        student = Student.objects.get(id=sid)
        staff = request.POST.get('staff_name')
        staff = Staff.objects.get(id=staff)
        subject = request.POST.get('subject_code')
        subject = Subject.objects.get(code=subject)
        categories = self.convert_json(request) 
        staffd = ClassStaff.objects.get(staff=staff,subject=subject)
        feedback, created = FeedBack.objects.update_or_create(
            staffd=staffd,
            student=student,
            feed=categories
        )

        catid += 1
        return redirect('feed',sid=sid,catid=catid)


class Search(View):
    template_name = 'admin/search.html'
    def dept_vaild(self,dept):
        depts = {
            'CSE' : 'Computer Science and Engineering',
            'IT' : 'Information Technology'
        }
        return depts[dept] if dept in depts else None
    def year_valid(self,yr):
        if yr == 1 : return (1,2)
        elif yr == 2 : return (3,4)
        elif yr == 3 : return (5,6)
        elif yr == 4 : return (7,8)
    def handleclass_valid(self,hclass):
        return hclass if hclass != '' else None
    def get(self, request):
        return render(self.request, self.template_name)
    def post(self, request):
        is_class = bool(request.POST.get('class_search'))
        is_loop = True
        query = request.POST.get('name')
        year = request.POST.get('year')
        if year != '':  
            sem1,sem2 = self.year_valid(int(request.POST.get('year')))
        section = request.POST.get('class')
        if section != '' : section = self.handleclass_valid(request.POST.get('class'))
        subject_code = request.POST.get('subject_code')
        print(f"resquest gender : {request.POST.get('gender')}")
        gender = request.POST.get('gender')
        if is_class:
            staff = ClassStaff.objects.filter(Q(semester=sem1) | Q(semester=sem2))
            if not section:
                staff1 = staff.filter(section='A').first()
                staff2 = staff.filter(section='B').first()
                if staff1 and staff2: staff = [staff1, staff2]
                elif staff1: 
                    staff = staff1
                    is_loop = False 
                else: 
                    staff = staff2
                    is_loop = False
            else :
                staff = staff.filter(section=section).first()
                is_loop = False
        else :
            staff = ClassStaff.objects.filter(
                Q(staff__fname__icontains=query) | Q(staff__sname__icontains=query)
            )
            if subject_code:
                staff = staff.filter(subject__subject_code=subject_code)
            if year != '':
                staff = staff.filter(Q(semester=sem1) | Q(semester=sem2))
            if section:
                staff = staff.filter(section=section).distinct()
            if gender:
                print(f'gender : {gender}')
                gender = 1 if gender == '1' else 0
                staff = staff.filter(staff__gender=gender)
        return render(self.request,self.template_name, {
            'staffs': staff,
            'is_class' : is_class,
            'is_loop':is_loop
        })




#   admin views
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
        return render(self.request,'analysis.html',{'is_class':False,'profile':staff,'subject':subject,'staffd':staffd})

class ClassProfile(View):
    template_name = 'analysis.html'
    def get(self,request,semester,section):
        return render(self.request,self.template_name,{'is_class':True,'semester':semester,'section':section})
class StudentCheck(View):
    template_name = 'admin/student.html'
    def valid_year(self,year):
        if year == '1' : return (1,2)
        elif year == '2' : return (3,4)
        elif year == '3' : return (5,6)
        elif year == '4' : return (7,8)
    def get(self,request):
        student = Student.objects.all()
        return render(self.request,self.template_name,{'students':student})
    def post(self,request):
        if request.POST.get('year') == '':
            return render(self.request,self.template_name,{'error':'please select the year !! '})
        sem1,sem2  = self.valid_year(request.POST.get('year'))
        section = request.POST.get('class')
        students = Student.objects.filter(Q(semester=sem1) | Q(semester=sem2))
        if section:
            students = students.filter(section=section)
        return render(self.request,self.template_name,{'students':students})
class ReportView(View):
    template_name = 'admin/report.html'
    def score(self,points):
        if points >= 4.0 : return 'excelent'
        elif points >= 3.0 : return 'good'
        else : return 'bad' 
    def get_data(self,staff_id,subject_code):
        cat_data = {f'cat_{i}':0 for i in range(1,11)}
        feeds = FeedBack.objects.filter(staff__id=staff_id,subject__subject_code=subject_code)
        count = feeds.count()
        for feed in feeds:
            for key,data in feed.categories.items():
                cat_data[key] += data
        for key,data in cat_data.items():
            cat_data[key] = [round((data / count),2),(self.score((data / count)))]
        return cat_data
    
    def get(self,request,staff_id,subject_code):
        staff = Staff.objects.get(id=staff_id)
        subject = Subject.objects.get(code=subject_code)
        #datas = self.get_data(staff_id,subject_code)
        #datas = [(key,value) for key,value in zip(terms,datas.values())]

        return render(self.request,self.template_name,{'staff':staff,'subject':subject})
    def post(self,request,staff_id,subject_code):
        staff = Staff.objects.get(id=staff_id)
        subject = Subject.objects.get(subject_code=subject_code)
        datas = self.get_data(staff.id,subject.subject_code)
        datas = [(key,value) for key,value in zip(terms,datas.values())]
        html = render(self.request,self.template_name,{'staff':staff,'subject':subject,'datas':datas})
        pdf = HTML(string=html.content).write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{staff.fname}_{subject.subject_code}.pdf"'
        response.write(pdf)
        return response





# admin view 
class AddHodUser(View):
    template_name = 'prinicipal/add_hod.html'
    def get(self,request):
        return render(request,self.template_name)
    def post(self,request):
        file = request.FILES['file']
        xl = pd.read_excel(file)
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
        return render(request,self.template_name,{'error':'user added !!'})      




# test 

class Feed(TemplateView):
    template_name = 'feed_sample.html'
