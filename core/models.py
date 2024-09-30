from django.db import models 

DEPARTMENT = (
    ('Computer Science and Engineering','CSE'),
    ('Tnformation Technology','IT'),
    ('Instrumentation and Controls Engineering','IT'),
    ('Electrical and Electronics Engineering','EEE')
)

class Subject(models.Model):
    name = models.CharField(max_length=20)
    subject_code = models.CharField(max_length=6)
    def __str__(self):
        return f'{self.name} - {self.subject_code}'
class Student(models.Model):
    name = models.CharField(max_length=20)
    regno = models.BigIntegerField()
    dept = models.CharField(max_length=50,choices=DEPARTMENT)
    section = models.CharField(max_length=1)
    def __str__(self):
        return f'{self.name} - {self.dept}'
class Staff(models.Model):
    GENDER = (
        (1,'male'),
        (0,'female')
    )
    name = models.CharField(max_length=20)
    dept = models.CharField(max_length=50,choices=DEPARTMENT)
    gender = models.BooleanField(choices=GENDER)
    hclass = models.CharField(max_length=1)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} - {self.dept}'

class FeedBack(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    cat1 = models.SmallIntegerField()
    cat2 = models.SmallIntegerField()
    cat3 = models.SmallIntegerField()
    cat4 = models.SmallIntegerField()
    cat5 = models.SmallIntegerField()
    avg_cat = models.FloatField(editable=False)
    def __str__(self):
        return f'{self.student}-{self.staff}'
    def save(self, *args, **kwargs):
        self.avg_cat = (self.cat1 + self.cat2 + self.cat3 + self.cat4 + self.cat5) / 5
        super().save(*args, **kwargs)


class ClassStaff(models.Model):
    section = models.CharField(max_length=1)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.section} - {self.staff.name}'