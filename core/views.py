#django
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.views import View
from django.views.generic import TemplateView
from core.models import Staff,Student,ClassStaff,Subject,FeedBack
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Avg,Count
from django.contrib.auth.views import LogoutView
# others
import json 
from weasyprint import HTML
from collections import defaultdict


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
    ('Tnformation Technology','IT'),
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

def score_count(id,is_class=False,section=None,semester=None):
    if is_class:
        feedbacks = FeedBack.objects.filter(student__semester=int(semester),student__section=section)
    else :
        feedbacks = FeedBack.objects.filter(staff__id=id)
    category_counts = {
        'cat1': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat2': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat3': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat4': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat5': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat6': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat7': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat8': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat9': {5: 0, 4: 0, 3: 0, 2: 0},
        'cat10': {5: 0, 4: 0, 3: 0, 2: 0},
    }
    for feedback in feedbacks:
        for cat in range(1, 11): 
            value = feedback.categories[f'cat_{cat}']
            if value in category_counts[f'cat{cat}']:
                category_counts[f'cat{cat}'][value] += 1
    return category_counts

class StaffData(View):
    def get(self,request,sid,subject_code):
        feedbacks = FeedBack.objects.filter(staff_id=sid,subject__subject_code=subject_code)

        avg_scores = defaultdict(float)
        percentage_scores = defaultdict(float)
        count_of_5 = defaultdict(int)
        count_of_3 = defaultdict(int)
        count_of_1 = defaultdict(int)


        overall_count_of_5 = 0
        overall_count_of_3 = 0
        overall_count_of_1 = 0

        feedback_count = feedbacks.count()
        if feedback_count == 0:
            return {}   
        for feedback in feedbacks:
            for category, score in feedback.categories.items():
                avg_scores[category] += score
                if score == 5:
                    count_of_5[category] += 1
                    overall_count_of_5 += 1
                elif score == 3:
                    count_of_3[category] += 1
                    overall_count_of_3 += 1
                elif score == 1:
                    count_of_1[category] += 1
                    overall_count_of_1 += 1

        analysis_result = {
            "avg": {},
            "terms" : terms,
            "percentage": {},
            "percentage_of_5": {},
            "percentage_of_3": {},
            "percentage_of_1": {},
            "overall_counts": {
                "5": overall_count_of_5,
                "3": overall_count_of_3,
                "1": overall_count_of_1
            },
            "overall_percentages": {
                "5": (overall_count_of_5 / (feedback_count * 10)) * 100,  
                "3": (overall_count_of_3 / (feedback_count * 10)) * 100,
                "1": (overall_count_of_1 / (feedback_count * 10)) * 100
            }
        }

        for category, total_score in avg_scores.items():
            analysis_result["avg"][category] = total_score / feedback_count
            analysis_result["percentage"][category] = (total_score / (feedback_count * 5)) * 100
            analysis_result["percentage_of_5"][category] = (count_of_5[category] / feedback_count) * 100
            analysis_result["percentage_of_3"][category] = (count_of_3[category] / feedback_count) * 100
            analysis_result["percentage_of_1"][category] = (count_of_1[category] / feedback_count) * 100

        return JsonResponse(analysis_result)
class ClassData(View):
    def get(self,request,semester,section):
        feedbacks = FeedBack.objects.filter(student__semester=semester,student__section=section)
        avg_scores = defaultdict(float)
        percentage_scores = defaultdict(float)
        count_of_5 = defaultdict(int)
        count_of_3 = defaultdict(int)
        count_of_1 = defaultdict(int)


        overall_count_of_5 = 0
        overall_count_of_3 = 0
        overall_count_of_1 = 0

        feedback_count = feedbacks.count()
        if feedback_count == 0:
            return {}   
        for feedback in feedbacks:
            for category, score in feedback.categories.items():
                avg_scores[category] += score
                if score == 5:
                    count_of_5[category] += 1
                    overall_count_of_5 += 1
                elif score == 3:
                    count_of_3[category] += 1
                    overall_count_of_3 += 1
                elif score == 1:
                    count_of_1[category] += 1
                    overall_count_of_1 += 1

        analysis_result = {
            "avg": {},
            "terms": terms,
            "percentage": {},
            "percentage_of_5": {},
            "percentage_of_3": {},
            "percentage_of_1": {},
            "overall_counts": {
                "5": overall_count_of_5,
                "3": overall_count_of_3,
                "1": overall_count_of_1
            },
            "overall_percentages": {
                "5": (overall_count_of_5 / (feedback_count * 10)) * 100,  
                "3": (overall_count_of_3 / (feedback_count * 10)) * 100,
                "1": (overall_count_of_1 / (feedback_count * 10)) * 100
            }
        }

        for category, total_score in avg_scores.items():
            analysis_result["avg"][category] = total_score / feedback_count
            analysis_result["percentage"][category] = (total_score / (feedback_count * 5)) * 100
            analysis_result["percentage_of_5"][category] = (count_of_5[category] / feedback_count) * 100
            analysis_result["percentage_of_3"][category] = (count_of_3[category] / feedback_count) * 100
            analysis_result["percentage_of_1"][category] = (count_of_1[category] / feedback_count) * 100

        return JsonResponse(analysis_result)

def get_subjects(request,year):
    subjects = Subject.objects.filter(semester=year)
    data = [{'id': subject.id, 'name': subject.name,'subject_code':subject.subject_code} for subject in subjects]
    return JsonResponse(data, safe=False)

# feeback and student views 

class StudentLogin(View):
    def __init__(self):
        self.DEPARTMENT = (
            ('Computer Science and Engineering','CSE'),
            ('Tnformation Technology','IT'),
            ('Instrumentation and Controls Engineering','IT'),
            ('Electrical and Electronics Engineering','EEE')
        )

    def pass_valid(self,password):
        dept,yr,sec = password.split('-')
        for department,key in self.DEPARTMENT:
            if dept in key: dept = department
        return (dept,yr,sec)
    def get(self,request):
        return render(self.request,'login.html')
    def post(self,request):
        try :
            name = request.POST.get('name')
            regno = request.POST.get('regno')
            password = request.POST.get('info')
            dept,year,section = self.pass_valid(password)
            student = Student.objects.create(name=name,regno=regno,section=section,dept=dept,semester=year)
            return redirect('feed',sid=student.id,catid=0)
        except Exception as error:
            return render(self.request,'login.html',{'error':error})

class Manitiory(View):
    template_name = 'subject.html'
    def get(self,request,sid,count):
        is_both = None
        student = Student.objects.get(id=sid)
        course = ClassStaff.objects.filter(semester=student.semester,subject__mcourse=True)

        #print(f'course len : {course.count()}')
        if course.count() >= 6 :
            half = len(course) // 2 
            half += 1 if half % 2 != 0 else 0
            course1 = course[0:half]
            course2 = course[half::]
            is_both = True
            return render(self.request,self.template_name,{'student':student,'semester':student.semester,'course1':course1,'course2':course2,'count':count,'both_side':is_both})
        return render(self.request,self.template_name,{'student':student,'courses':course,'count':count,'both_side':is_both})
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
    def get(self,request,sid,csid,count):
        student = Student.objects.get(id=sid)
        data = ClassStaff.objects.get(id=csid)
        return render(self.request,self.template_name,{'data':data,'sid':student,'count':count})
    def post(self,request,sid,csid,count):
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
        count += 1
        return redirect('msubject',sid=sid,count=count)

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
        class_staff = ClassStaff.objects.filter(subject__semester=student.semester,section=student.section,subject__mcourse=False)
        if len(class_staff) == catid: 
            if(student.semester > 3) : return redirect('msubject',sid=sid,count=0)
            else : return redirect('home')
        return render(self.request,'feed.html',{'data':class_staff[catid],'sid':sid,'catid':catid})
    def post(self,request,sid,catid):
        student = Student.objects.get(id=sid)
        staff = request.POST.get('staff_name')
        staff = Staff.objects.get(id=staff)
        subject = request.POST.get('subject_code')
        subject = Subject.objects.get(subject_code=subject)
        categories = self.convert_json(request) 
        feedback, created = FeedBack.objects.update_or_create(
            subject=subject,
            student=student,
            staff=staff,
            categories=categories
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
        #print(f'is_class : {is_class}')
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
        subject = Subject.objects.get(subject_code=subject)
        dept = self.get_department_code(staff.dept)
        return render(self.request,'analysis.html',{'is_class':False,'dept':dept,'profile':staff,'subject':subject})

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
            cat_data[key] = [(data / count),(self.score((data / count)))]
        return cat_data
    
    def get(self,request,staff_id,subject_code):
        staff = Staff.objects.get(id=staff_id)
        subject = Subject.objects.get(subject_code=subject_code)
        datas = self.get_data(staff_id,subject_code)
        datas = [(key,value) for key,value in zip(terms,datas.values())]

        return render(self.request,self.template_name,{'staff':staff,'subject':subject,'datas':datas})
    def post(self,request,staff_id,subject_code):
        staff = Staff.objects.get(id=staff_id)
        subject = Subject.objects.get(subject_code=subject_code)
        data = self.get_data(staff.id,subject.subject_code)
        html = render(self.request,self.template_name,{'datas':data,'staff':staff,'subject':subject})
        pdf = HTML(string=html.content).write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{staff.fname}_{subject.subject_code}.pdf"'
        response.write(pdf)
        return response



