
from django.forms import ModelForm
from core.models import ClassStaff
class ClassStaffForm(ModelForm):
    class Meta:
        model = ClassStaff
        fields = '__all__'

    class Media:
        js = ('js/subject_filter.js',)