from django.contrib import admin
from apps.courses.models import Course
from .models import Category, Subcategory, Language

# Register the Course model with the admin site using the default admin interface
admin.site.register(Course)

# Define an admin interface for the Subcategory model with customized list display and filtering options、
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

# Define an admin interface for the Subcategory model with customized list display and filtering options
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)

# Define an admin interface for the Language model to customize the list display
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)