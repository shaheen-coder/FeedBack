from django.db import models 

DEPARTMENT = (
    ('Computer Science and Engineering','CSE'),
    ('Tnformation Technology','IT'),
    ('Instrumentation and Controls Engineering','IT'),
    ('Electrical and Electronics Engineering','EEE')
)
def profile_path(instance,filename):
    return f'profile/{instance.fname}/{filename}'

class Subject(models.Model):
    name = models.CharField(max_length=50)
    subject_code = models.CharField(max_length=6)
    semester = models.SmallIntegerField()
    mcourse = models.BooleanField(default=False,help_text='manitaory course')
    ecourse = models.BooleanField(default=False,help_text='elective course')
    oecourse = models.BooleanField(default=False,help_text='open elective course')
    def __str__(self):
        return f'{self.name} - {self.subject_code}'
class Student(models.Model):
    name = models.CharField(max_length=20)
    regno = models.BigIntegerField(unique=True)
    dept = models.CharField(max_length=50,choices=DEPARTMENT)
    section = models.CharField(max_length=1)
    semester = models.SmallIntegerField()
    def __str__(self):
        return f'{self.name} - {self.section}'
class Staff(models.Model):
    GENDER = (
        (1,'male'),
        (0,'female')
    )
    fname = models.CharField(max_length=20)
    sname = models.CharField(max_length=20,null=True)
    intial = models.CharField(max_length=1)
    proflie_pic = models.ImageField(upload_to=profile_path,null=True,blank=True)
    dept = models.CharField(max_length=50,choices=DEPARTMENT)
    gender = models.BooleanField(choices=GENDER)
    def save(self, *args, **kwargs):
        if not self.proflie_pic:
            self.proflie_pic = 'male.png' if self.gender == 1 else 'female.png'
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.fname} {self.sname}'

class FeedBack(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    categories = models.JSONField() 
    def __str__(self):
        return f'{self.student}-{self.staff}'

class ClassStaff(models.Model):
    semester = models.SmallIntegerField()
    section = models.CharField(max_length=1)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.section} - {self.staff.fname}'
    class Meta:
        verbose_name = "handling class"