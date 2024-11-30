from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
DEPT = (
    ('CSE','be-cse'),
    ('IT','btech-it'),
    ('EEE','be-eee'),
    ('ICE','be-ice'),
    ('ECE','be-ece'),
    ('MECH','be-mech'),
    ('MCA','mca'),
    ('MBA','mba'),
)

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
    status = models.BooleanField(null=True,blank=True)
    def save(self,*args,**kwargs):
        self.section = str(self.section).upper()
        super().save(*args,**kwargs)
    def __str__(self):
        return f'{self.name[:5]} - {self.dept}'
class Staff(models.Model):
    GENDER = (
        (1,'male'),
        (0,'female')
    )
    name = models.CharField(max_length=50)
    dept = models.CharField(max_length=20,choices=DEPT)
    gender = models.BooleanField(choices=GENDER)
    profile_pic = models.ImageField(upload_to='media',null=True,blank=True)
    def __str__(self):
        return f'{self.name[:5]} - {self.dept}'

class Subject(models.Model):
    name = models.CharField(max_length=40)
    code = models.CharField(max_length=7)
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
    dept = models.CharField(max_length=10,choices=DEPT)
    def save(self,*args,**kwargs):
        self.section = str(self.section).upper()
        super().save(*args,**kwargs)
    def __str__(self):
        return f'{self.staff.name} - {self.subject.code}'
    
class FeedBack(models.Model):
    staffd = models.ForeignKey(ClassStaff,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    feed = models.JSONField()
