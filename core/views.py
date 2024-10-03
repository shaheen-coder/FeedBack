from django.shortcuts import render,redirect
from django.views import View
from core.models import Staff,Student,ClassStaff,Subject,FeedBack
# Create your views here.

class Profile(View):
    def get(self,request,id):
        staff = Staff.objects.get(id=id)
        return render(self.request,'analysis.html',{'profile':staff})
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
        return render(self.request,'login1.html')
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
            return render(self.request,'login1.html',{'error':error})
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
    def get(self,request):
        return render(self.request,'search.html')
    def post(self,request):
        query = request.POST.get('query')
        staff = Staff.objects.filter(name__icontains=query)
        return render(self.request,'search.html',{'staffs':staff,'result':len(staff)})