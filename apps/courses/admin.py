from django.contrib import admin
from apps.courses.models import Course
from .models import Category, Subcategory, Language


admin.site.register(Course)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'description')
    list_filter = ('category',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)