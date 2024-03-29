# Generated by Django 5.0.2 on 2024-03-03 07:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Category Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Language Name')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='courses/covers/', verbose_name='Course Cover')),
                ('videos', models.FileField(blank=True, null=True, upload_to='courses/videos/', verbose_name='Course Videos')),
                ('materials', models.FileField(blank=True, null=True, upload_to='courses/materials/', verbose_name='Course Materials')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='courses.category', verbose_name='Category')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authored_courses', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('language', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courses.language', verbose_name='Language')),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_enrolled', models.DateField(auto_now_add=True, verbose_name='Date Enrolled')),
                ('grade', models.CharField(blank=True, max_length=2, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed')], default='active', max_length=20, verbose_name='Status')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='courses.course', verbose_name='Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Feedback Text')),
                ('rating', models.IntegerField(verbose_name='Rating')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='courses.course', verbose_name='Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_feedbacks', to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Subcategory Name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='courses.category', verbose_name='Parent Category')),
            ],
        ),
    ]
