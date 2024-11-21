
from django.forms import ModelForm
from core.models import ClassStaff
from django import forms
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