from django import forms
from .models import Course, Material, TeacherFile
from django.forms.models import inlineformset_factory

# Define a form for creating and editing Course instances, specifying fields to include in the form and customizing widgets for date inputs
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'category', 'language', 'start_date', 'end_date', 'cover', 'videos']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control date-input'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control date-input'}),
        }

# Define a form for creating and editing Material instances associated with a Course, including only the name and file fields
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'file']

# Create a formset for managing multiple Material instances related to a single Course instance, allowing dynamic addition and deletion of materials
MaterialFormSet = inlineformset_factory(Course, Material, fields=('name', 'file',), extra=2, can_delete=True)

# Define a form for uploading files by teachers, focusing on the file upload field
class TeacherFileForm(forms.ModelForm):
    class Meta:
        model = TeacherFile
        fields = ['file']
