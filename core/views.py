from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from core.models import Staff,Student,ClassStaff,Subject,FeedBack
from django.http import JsonResponse
from django.db.models import Q

# Create your views here

class Home(TemplateView):
    template_name = 'landing.html'
class Team(TemplateView):
    template_name = 'team.html'
class Error(TemplateView):
    template_name = '404.html'
def score_count(id):
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
            value = getattr(feedback, f'cat{cat}')
            if value in category_counts[f'cat{cat}']:
                category_counts[f'cat{cat}'][value] += 1
    return category_counts
class Profile(View):
    def get(self,request,id):
        staff = Staff.objects.get(id=id)
        score = score_count(id)
        return render(self.request,'analysis.html',{'profile':staff,'score_count':score})
class StaffStatsView(View):
    def get(self, request, sid,subject_code):
        staff = get_object_or_404(Staff, id=sid)
        subject = get_object_or_404(Subject, subject_code=subject_code)
        
        feedbacks = FeedBack.objects.filter(staff=staff,subject=subject)
        
        total_feedbacks = feedbacks.count()
        if total_feedbacks == 0:
            return JsonResponse({
                "error": "No feedback found for this staff member."
            }, status=404)

        sum_cat1 = sum_cat2 = sum_cat3 = sum_cat4 = sum_cat5 =  sum_cat6 = 0
        sum_cat7 = sum_cat8 = sum_cat9 = sum_cat10 = 0

        for feedback in feedbacks:
            sum_cat1 += feedback.cat1
            sum_cat2 += feedback.cat2
            sum_cat3 += feedback.cat3
            sum_cat4 += feedback.cat4
            sum_cat5 += feedback.cat5
            sum_cat6 += feedback.cat6
            sum_cat7 += feedback.cat7
            sum_cat8 += feedback.cat8
            sum_cat9 += feedback.cat9
            sum_cat10 += feedback.cat10

        avg_cat1 = int(sum_cat1 / total_feedbacks)
        avg_cat2 = int(sum_cat2 / total_feedbacks)
        avg_cat3 = int(sum_cat3 / total_feedbacks)
        avg_cat4 = int(sum_cat4 / total_feedbacks)
        avg_cat5 = int(sum_cat5 / total_feedbacks)
        avg_cat6 = int(sum_cat6 / total_feedbacks)
        avg_cat7 = int(sum_cat7 / total_feedbacks)
        avg_cat8 = int(sum_cat8 / total_feedbacks)
        avg_cat9 = int(sum_cat9 / total_feedbacks)
        avg_cat10 = int(sum_cat10 / total_feedbacks)

        percentage_cat1 = (avg_cat1 / 10) * 100
        percentage_cat2 = (avg_cat2 / 10) * 100
        percentage_cat3 = (avg_cat3 / 10) * 100
        percentage_cat4 = (avg_cat4 / 10) * 100
        percentage_cat5 = (avg_cat5 / 10) * 100
        percentage_cat6 = (avg_cat6 / 10) * 100
        percentage_cat7 = (avg_cat7 / 10) * 100
        percentage_cat8 = (avg_cat8 / 10) * 100
        percentage_cat9 = (avg_cat9 / 10) * 100
        percentage_cat10 = (avg_cat10 / 10) * 100
        data = {
            'staff': staff.fname,
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
            dept,section,year = self.pass_valid(password)
            student = Student.objects.create(name=name,regno=regno,section=section,dept=dept,year=year)
            return redirect('feed',sid=student.id,catid=0)
        except Exception as error:
            return render(self.request,'login.html',{'error':error})
def score(data:str) -> int :
    if data == 'excellent': return 5
    elif data == 'good': return 4
    elif data == 'average': return 2
    elif data == 'poor': return 1
    else : return -1 
class FeedBackView(View):
    def get(self,request,sid,catid):
        #if catid == 0 :
        student = Student.objects.get(id=sid)
        class_staff = ClassStaff.objects.filter(section=student.section)
        if len(class_staff) == catid: return redirect('home')
        return render(self.request,'feed.html',{'data':class_staff[catid],'sid':sid,'catid':catid})
    def post(self,request,sid,catid):
        student = Student.objects.get(id=sid)
        staff = request.POST.get('staff_name')
        staff = Staff.objects.get(id=staff)
        subject = request.POST.get('subject_code')
        subject = Subject.objects.get(subject_code=subject)
        cat1 = score(request.POST.get('cat_1'))
        cat2 = score(request.POST.get('cat_2'))
        cat3 = score(request.POST.get('cat_3'))
        cat4 = score(request.POST.get('cat_4'))
        cat5 = score(request.POST.get('cat_5'))
        cat6 = score(request.POST.get('cat_6'))
        cat7 = score(request.POST.get('cat_7'))
        cat8 = score(request.POST.get('cat_8'))
        cat9 = score(request.POST.get('cat_9'))
        cat10 = score(request.POST.get('cat_10'))
        feedback, created = FeedBack.objects.update_or_create(
            subject=subject,
            student=student,
            staff=staff,
            defaults={
                'cat1': cat1,
                'cat2': cat2,
                'cat3': cat3,
                'cat4': cat4,
                'cat5': cat5,
                'cat6' : cat6,
                'cat7' : cat7,
                'cat8' : cat8,
                'cat9' : cat9,
                'cat10' : cat10,
            }
        )

        catid += 1
        return redirect('feed',sid=sid,catid=catid)


class Search(View):
    def dept_vaild(self,dept):
        depts = {
            'CSE' : 'Computer Science and Engineering',
            'IT' : 'Information Technology'
        }
        return depts[dept] if dept in depts else None
    def handleclass_valid(self,hclass):
        return hclass if hclass != '' else None
    def get(self, request):
        return render(self.request, 'search.html')
    def post(self, request):
        query = request.POST.get('query')
        dept = self.dept_vaild(request.POST.get('department'))  
        year = request.POST.get('year')
        hclass = self.handleclass_valid(request.POST.get('hclass')) 
        staff = Staff.objects.filter(
            Q(fname__icontains=query) | Q(sname__icontains=query)
        )
        if dept:
            staff = staff.filter(dept=dept)
        if year:
            staff = staff.filter(year=year)
        if hclass:
            staff = staff.filter(hclass=hclass)
        return render(self.request, 'search.html', {
            'staffs': staff,
            'result': len(staff)
        })
