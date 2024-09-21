from django.shortcuts import render
from django.views import View
from core.models import Staff
# Create your views here.

class Profile(View):
    def get(self,request,id):
        staff = Staff.objects.get(id=id)
        return render(self.request,'analysis.html',{'profile':staff})
class StudentLogin(View):
    def get(self,request):
        return render(self.request,'login.html')
    def post(self,request):
        name = request.POST.get('name')
        regno = request.POST.get('regno')
        #section = request.POST.get('section')
        print(f'name : {name} reg no : {regno}')
        return render(self.request,'login.html')

class FeedBackView(View):
    def get(self,request):
        return render(self.request,'feed.html')
        