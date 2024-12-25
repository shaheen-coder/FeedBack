from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
DEPT = (
    ('CSE','be-cse'),
    ('IT','btech-it'),
    ('EEE','be-eee'),
    ('ICE','be-ice'),
    ('ECE','be-ece'),
    ('MECH','be-mech'),
    ('CIVIL','be-civil'),
    ('MCA','mca'),
    ('MBA','mba'),
)
four_year = ['CSE','ICE','ECE','MECH','IT','CIVIL','EEE']
two_year = ['MCA','MBA']
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_princpl',True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    is_hod = models.BooleanField(default=False)  
    is_princpl = models.BooleanField(default=False)  
    dept = models.CharField(max_length=100,choices=DEPT,null=False, blank=False)
    objects = CustomUserManager()
    def __str__(self):
        return self.username

class Student(models.Model):
    name = models.CharField(max_length=50)
    regno = models.BigIntegerField(unique=True)
    dob = models.DateField()
    dept = models.CharField(max_length=10,choices=DEPT)
    section = models.CharField(max_length=1)
    semester = models.SmallIntegerField()
    status = models.BooleanField(default=True,null=True,blank=True)
    feed1_status = models.BooleanField(default=False,null=True,blank=True)
    feed2_status = models.BooleanField(default=False,null=True,blank=True)
    def save(self,*args,**kwargs):
        self.section = str(self.section).upper()
        if self.semester == 9 and self.dept in four_year: 
            self.status = False 
        if self.semester == 5 and self.dept in two_year: 
            self.status = False 
        super().save(*args,**kwargs)
    def __str__(self):
        return f'{self.name[:7]} - {self.dept}'
class Staff(models.Model):
    GENDER = (
        (1,'male'),
        (0,'female')
    )
    def profile_path(instance,filename):
        return f'profile/{instance.fname}/{filename}'
    name = models.CharField(max_length=50)
    dept = models.CharField(max_length=20,choices=DEPT)
    gender = models.BooleanField(choices=GENDER)
    profile_pic = models.ImageField(upload_to=profile_path,null=True,blank=True)
    def save(self, *args, **kwargs):
        if not self.profile_pic:
            self.profile_pic = 'male.png' if self.gender == 1 else 'female.png'
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.name[:5]} - {self.dept}'

class Subject(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(primary_key=True,max_length=7)
    dept = models.CharField(max_length=10,choices=DEPT)
    semester = models.SmallIntegerField()
    mcourse = models.BooleanField(default=False)
    ecourse = models.BooleanField(default=False)
    oecourse = models.BooleanField(default=False)
    def __str__(self):
        return self.code
class ClassStaff(models.Model):
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    section = models.CharField(max_length=1)
    semester = models.SmallIntegerField()
    dept = models.CharField(max_length=10,choices=DEPT)
    class Meta:
        verbose_name = "class handling"
    def save(self,*args,**kwargs):
        self.section = str(self.section).upper()
        super().save(*args,**kwargs)
    def __str__(self):
        return f'{self.staff.name} - {self.subject.code}'
    
class FeedBack(models.Model):
    staffd = models.ForeignKey(ClassStaff,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    feed1 = models.JSONField(null=True,blank=True)
    feed2 = models.JSONField(null=True,blank=True)
    msg = models.CharField(max_length=50,null=True,blank=True)


class TimeScheduler(models.Model):
    start_time = models.DateField()
    end_time = models.DateField()
    dept = models.CharField(max_length=10,choices=DEPT)
    