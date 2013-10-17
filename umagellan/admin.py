from django.contrib import admin
from umagellan.models import Course, UserProfile

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'build_code', 'start_time', 'end_time')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'home')
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Course, CourseAdmin)