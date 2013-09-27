from django.conf.urls import patterns, include, url
from views import HomePage, UserCreate

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Load index page
    url(r'^$', HomePage, name='home'),
        
    # Course Actions
    url(r'^add_course', 'umagellan.views.add_course'),
    url(r'^get_course', 'umagellan.views.get_course'),
    url(r'^delete_course/(?P<course_id>\d+)/', 'umagellan.views.delete_course'),
    url(r'^delete_all_courses/$', 'umagellan.views.delete_all_courses', name='delete_all_courses'),

    # Admin views
    url(r'^admin/', include(admin.site.urls)),

    # Authentication
    url(r'^login/$', 'django_cas.views.login', name = 'user_login_page'),
    url(r'^logout/$', 'django_cas.views.logout', name = 'user_logout_page'),
    
    # User Actions
    url(r'^user/create/$', UserCreate.as_view(), name = 'user_create_page'),
    url(r'^user/sethome/$', 'umagellan.views.SetHome', name = 'set_user_home'),
)
