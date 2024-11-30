
from django.forms import ModelForm
from core.models import ClassStaff
from django import forms
from captcha.fields import CaptchaField
from core.models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'dept', 'is_hod', 'is_princpl', 'is_staff', 'is_superuser')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'dept', 'is_hod', 'is_princpl', 'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_hod', 'is_princpl', 'dept')




class ClassStaffForm(ModelForm):
    COURSE_TYPE_CHOICES = [
        ('0',''),
        ('1', 'Mandatory'),
        ('2', 'Open Elective'),
        ('3', 'Elective'),
    ]
    
    course_type = forms.ChoiceField(
        choices=COURSE_TYPE_CHOICES,
        required=False, 
        label="Course Type"
    )
    class Meta:
        model = ClassStaff
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Reorder the fields so course_type is first
        self.fields = {'course_type': self.fields['course_type'], **self.fields}

    class Media:
        js = ('js/subject_filter.js',)


class StudentLoginForm(forms.Form):
    
    captcha = CaptchaField()
