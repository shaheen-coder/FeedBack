from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from core.models import Staff,Student,ClassStaff,Subject,FeedBack
from django.http import JsonResponse
from django.db.models import Q
# Create your views here
class Profile(View):
    def get(self,request,id):
        staff = Staff.objects.get(id=id)
        return render(self.request,'analysis.html',{'profile':staff})
class StaffStatsView(View):
    def get(self, request, sid,subject_code):
        staff = get_object_or_404(Staff, id=sid)
        subject = get_object_or_404(Subject, subject_code=subject_code)
        
        # Get all feedback related to this staff
        feedbacks = FeedBack.objects.filter(staff=staff,subject=subject)
        
        # Initialize totals
        total_feedbacks = feedbacks.count()
        if total_feedbacks == 0:
            return JsonResponse({
                "error": "No feedback found for this staff member."
            }, status=404)

        # Initialize category sums
        sum_cat1 = sum_cat2 = sum_cat3 = sum_cat4 = sum_cat5 = 0

        # Calculate sum for each category
        for feedback in feedbacks:
            sum_cat1 += feedback.cat1
            sum_cat2 += feedback.cat2
            sum_cat3 += feedback.cat3
            sum_cat4 += feedback.cat4
            sum_cat5 += feedback.cat5

        # Calculate averages for each category
        avg_cat1 = int(sum_cat1 / total_feedbacks)
        avg_cat2 = int(sum_cat2 / total_feedbacks)
        avg_cat3 = int(sum_cat3 / total_feedbacks)
        avg_cat4 = int(sum_cat4 / total_feedbacks)
        avg_cat5 = int(sum_cat5 / total_feedbacks)

        # Since max points for each category is 5, calculate percentages
        percentage_cat1 = (avg_cat1 / 5) * 100
        percentage_cat2 = (avg_cat2 / 5) * 100
        percentage_cat3 = (avg_cat3 / 5) * 100
        percentage_cat4 = (avg_cat4 / 5) * 100
        percentage_cat5 = (avg_cat5 / 5) * 100

        # Create response data
        data = {
            'staff': staff.name,
            'total_feedbacks': total_feedbacks,
            'average': {
                'cat1': avg_cat1,
                'cat2': avg_cat2,
                'cat3': avg_cat3,
                'cat4': avg_cat4,
                'cat5': avg_cat5
            },
            'percentage': {
                'cat1': percentage_cat1,
                'cat2': percentage_cat2,
                'cat3': percentage_cat3,
                'cat4': percentage_cat4,
                'cat5': percentage_cat5
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
            dept,year,section = self.pass_valid(password)
            print(f'name : {name} reg no : {regno}')
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
        if len(class_staff) == catid: return redirect('login')
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
        cat4 = score(request.POST.get('cat_3'))
        cat5 = score(request.POST.get('cat_4'))
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
            }
        )

        catid += 1
        return redirect('feed',sid=sid,catid=catid)


class Search(View):
    def get(self, request):
        return render(self.request, 'search.html')
    def post(self, request):
        query = request.POST.get('query')
        dept = request.POST.get('dept')  
        gender = request.POST.get('gender')
        hclass = request.POST.get('hclass')  
        if not query:
            return render(self.request, 'search.html', {'error': 'Empty search'})
        staff = Staff.objects.filter(
            Q(fname__icontains=query) | Q(sname__icontains=query)
        )
        if dept:
            staff = staff.filter(dept=dept)
        if gender:
            staff = staff.filter(gender=gender)
        if hclass:
            staff = staff.filter(hclass=hclass)
        return render(self.request, 'search.html', {
            'staffs': staff,
            'result': len(staff)
        })
