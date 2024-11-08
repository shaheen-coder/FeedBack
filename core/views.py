#django
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.views import View
from django.views.generic import TemplateView
from core.models import Staff,Student,ClassStaff,Subject,FeedBack
from django.http import JsonResponse
from django.db.models import Q
# others
import json 
from weasyprint import HTML

# normal template rendering page views 
class Home(TemplateView):
    template_name = 'landing.html'
class Team(TemplateView):
    template_name = 'team.html'
class Error(TemplateView):
    template_name = '404.html'

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

class StaffStatsView(View):
    def get(self, request, sid, subject_code):
        staff = get_object_or_404(Staff, id=sid)
        subject = get_object_or_404(Subject, subject_code=subject_code)
        feedbacks = FeedBack.objects.filter(staff=staff, subject=subject)
        total_feedbacks = feedbacks.count()

        if total_feedbacks == 0:
            return JsonResponse({"error": "No feedback found for this staff member."}, status=404)

        avg_cat = {f'cat_{i}': 0 for i in range(1, 11)}
        
        for feedback in feedbacks:
            for key, value in feedback.categories.items():
                avg_cat[key] += value
        
        # Calculate averages and percentages for each category
        averages = {key: avg_cat[key] // total_feedbacks for key in avg_cat}
        percentages = {key: (avg_cat[key] / 10) * 100 for key in avg_cat}
        
        data = {
            'staff': staff.fname,
            'total_feedbacks': total_feedbacks,
            'average': averages,
            'percentage': percentages
        }

        return JsonResponse(data)

class ClassStatsView(View):
    def get(self, request,semester,section):    
        feedbacks = FeedBack.objects.filter(student__section=section,student__semester=semester)
        total_feedbacks = feedbacks.count()
        if total_feedbacks == 0:
            return JsonResponse({
                "error": "No feedback found for this staff member."
            }, status=404)

        avg_cat = {}
        for data in feedbacks: 
            for key,value in data.categories.items():
                try : avg_cat[key] += value
                except Exception as e : avg_cat[key] = value
        #print(f'data : {avg_cat}')
        avg_cat1 = int(avg_cat['cat_1'] / total_feedbacks)
        avg_cat2 = int(avg_cat['cat_2'] / total_feedbacks)
        avg_cat3 = int(avg_cat['cat_3'] / total_feedbacks)
        avg_cat4 = int(avg_cat['cat_4'] / total_feedbacks)
        avg_cat5 = int(avg_cat['cat_5'] / total_feedbacks)
        avg_cat6 = int(avg_cat['cat_6'] / total_feedbacks)
        avg_cat7 = int(avg_cat['cat_7'] / total_feedbacks)
        avg_cat8 = int(avg_cat['cat_8'] / total_feedbacks)
        avg_cat9 = int(avg_cat['cat_9'] / total_feedbacks)
        avg_cat10 = int(avg_cat['cat_10'] / total_feedbacks)

        percentage_cat1 = (avg_cat['cat_1'] / 10) * 100
        percentage_cat2 = (avg_cat['cat_2'] / 10) * 100
        percentage_cat3 = (avg_cat['cat_3'] / 10) * 100
        percentage_cat4 = (avg_cat['cat_4'] / 10) * 100
        percentage_cat5 = (avg_cat['cat_5'] / 10) * 100
        percentage_cat6 = (avg_cat['cat_6'] / 10) * 100
        percentage_cat7 = (avg_cat['cat_7'] / 10) * 100
        percentage_cat8 = (avg_cat['cat_8'] / 10) * 100
        percentage_cat9 = (avg_cat['cat_9'] / 10) * 100
        percentage_cat10 = (avg_cat['cat_10'] / 10) * 100
        data = {
            'total_feedbacks': total_feedbacks,
            'average': {
                'cat1': avg_cat1,
                'cat2': avg_cat2,
                'cat3': avg_cat3,
                'cat4': avg_cat4,
                'cat5': avg_cat5,
                'cat5': avg_cat6,
                'cat7': avg_cat7,
                'cat8': avg_cat8,
                'cat9': avg_cat9,
                'cat10': avg_cat10,
            },
            'percentage': {
                'cat1': percentage_cat1,
                'cat2': percentage_cat2,
                'cat3': percentage_cat3,
                'cat4': percentage_cat4,
                'cat5': percentage_cat5,
                'cat6': percentage_cat6,
                'cat7': percentage_cat7,
                'cat8': percentage_cat8,
                'cat9': percentage_cat9,
                'cat10': percentage_cat10,
            }
        }

        # Return the data as JSON or pass to a template
        return JsonResponse(data)

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
        student = Student.objects.get(id=sid)
        course = ClassStaff.objects.filter(semester=student.semester,subject__mcourse=True)
        return render(self.request,self.template_name,{'student':student,'courses':course,'count':count})
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
        #print(f'is_class : {is_class}')
        query = request.POST.get('name')
        sem1,sem2 = self.year_valid(int(request.POST.get('year')))
        section = self.handleclass_valid(request.POST.get('class'))
        subject_code = request.POST.get('subject_code')
        gender =  1 if request.POST.get('gender') == '1' else  0
        if is_class:
            staff = ClassStaff.objects.filter(Q(semester=sem1) | Q(semester=sem2))
        else :
            staff = ClassStaff.objects.filter(
                Q(staff__fname__icontains=query) | Q(staff__sname__icontains=query)
            )
            if sem1:
                staff = staff.filter(Q(semester=sem1) | Q(semester=sem2))
            if section:
                staff = staff.filter(section=section)
            if subject_code:
                staff_ids = ClassStaff.objects.filter(subject__subject_code=subject_code).values_list('staff_id', flat=True)
                staff = staff.filter(id__in=staff_ids)
            if gender:
                staff = staff.filter(staff__gender=gender)
        return render(self.request,self.template_name, {
            'staffs': staff,
            'is_class' : is_class
        })




#   admin views
class Profile(View):
    def get(self,request,id,subject):
        staff = Staff.objects.get(id=id)
        subject = Subject.objects.get(subject_code=subject)
        score = score_count(id)
        return render(self.request,'analysis.html',{'profile':staff,'subject':subject,'score_count':score})

class ClassProfile(View):
    template_name = 'analysis-karthi.html'
    def get(self,request,semester,section):
        score = score_count(id=None,is_class=True,section=section,semester=semester)
        return render(self.request,self.template_name,{'semester':semester,'section':section,'score_count':score})
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
        cat_data = {
            'cat_1' : 0,
            'cat_2' : 0,
            'cat_3' : 0,
            'cat_4' : 0,
            'cat_5' : 0,
            'cat_6' : 0,
            'cat_7' : 0,
            'cat_8' : 0,
            'cat_9' : 0,
            'cat_10' : 0,
        }
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
