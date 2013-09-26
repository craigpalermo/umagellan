from django.contrib import admin
# from umagellan.models import Course, Route, Spot
from models import Course, Spot, UserProfile

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'build_code', 'start_time', 'end_time', 'user')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'home')

# class RouteAdmin(admin.ModelAdmin):
#     pass

class SpotAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Course, CourseAdmin)
# admin.site.register(Route, RouteAdmin)
admin.site.register(Spot, SpotAdmin)