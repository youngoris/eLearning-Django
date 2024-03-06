from django import forms
from .models import Course, Material, TeacherFile
from django.forms.models import inlineformset_factory


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'language', 'start_date', 'end_date', 'cover', 'videos']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control date-input'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control date-input'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'file']

MaterialFormSet = inlineformset_factory(Course, Material, fields=('name', 'file',), extra=2, can_delete=True)


class TeacherFileForm(forms.ModelForm):
    class Meta:
        model = TeacherFile
        fields = ['file']