from django.db import models 
from core.settings import AUTH_USER_MODEL as User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

DEPARTMENT = (
    ('Computer Science and Engineering','CSE'),
    ('Tnformation Technology','IT'),
    ('Instrumentation and Controls Engineering','IT'),
    ('Electrical and Electronics Engineering','EEE')
)
#custom user (student)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        if password:
            try:
                department, section = password.split('-')
            except ValueError:
                raise ValueError("Password must contain a '-' to split into department and section Like 'CSE-B'")
            extra_fields['department'] = department
            extra_fields['section'] = section

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    register_no = models.BigIntegerField(primary_key=True)
    section = models.CharField(max_length=1)
    department = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Password will be required in the form

    def save(self, *args, **kwargs):
        # Ensure that department and section are set correctly
        if not self.department or not self.section and self.password:
            department, section = self.password.split('-')
            self.department = department
            self.section = section
        super().save(*args, **kwargs)

    def __str__(self):
        return self.register_no

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


class ClassStaff:
    section = models.CharField(max_length=1)
    staff = models.ForeignKey(Staff,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)