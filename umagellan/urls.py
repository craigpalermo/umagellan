from django.conf.urls import patterns, include, url
from umagellan.views import home_page_view, create_user

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Load index page
    url(r'^$', home_page_view, name='home'),
        
    # Course Actions
    url(r'^add_course/', 'umagellan.views.add_course'),
    url(r'^get_courses/', 'api.views.get_courses_view'),
    url(r'^delete_course/(?P<course_id>\d+)/', 'umagellan.views.delete_course'),
    url(r'^delete_all_courses/$', 'umagellan.views.delete_all_courses', name='delete_all_courses'),

    # Admin views
    url(r'^admin/', include(admin.site.urls)),

    # Authentication
    url(r'^login/$', 'django_cas.views.login', name = 'user_login_page'),
    url(r'^logout/$', 'django_cas.views.logout', name = 'user_logout_page'),
    
    # User Actions
    url(r'^user/create/$', create_user.as_view(), name = 'user_create_page'),
    url(r'^user/sethome/$', 'umagellan.views.set_home', name = 'set_user_home'),
)
