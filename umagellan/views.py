from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from models import Course
from bs4 import BeautifulSoup
from forms import UserForm
from django.views.generic.base import View
from dateutil import parser
from umagellan.models import UserProfile
from api.scraper import Scraper
import urllib2
import json


def home_page_view(request):
    courses = Course.objects.filter(user = request.user.id)
    routes = None
    days = [('Monday', 'M'), ('Tuesday', 'Tu'), ('Wednesday', 'W'), ('Thursday', 'Th'), ('Friday', 'F') ]
    
    # if user is logged in, try to get their home location
    if request.user.is_authenticated():
        home = request.user.profile.home
    else:
        home = ''
        
    try:
        user = User.objects.get(id=request.user.id)
    except:
        user = None

    return render_to_response('index.html', 
        {'courses': courses, 'routes': routes, 'user': user, 'days': days, 'home': home}, 
        context_instance = RequestContext(request))

def set_home(request):
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(user=request.user)
        except:
            profile = UserProfile()
            profile.user = request.user
            
        profile.home = request.POST.get('user_home')
        profile.save()

    return render(request, 'index.html', None, context_instance = RequestContext(request))
        


class create_user(View):
    '''    
    form to create/register new user
    '''
    form_class = UserForm
    template_name = 'user_create.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                user = User.objects.get(id = request.user.id)
            except:
                user = User()
                
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.email = cd['email']
            user.password = cd['password']
            user.save()
                
            return HttpResponseRedirect('home')

        return render(request, self.template_name, {'form': form}, context_instance = RequestContext(request))


def delete_course(request, course_id):
    '''
    delete a course object from the database
    '''
    try:
        course = Course.objects.get(id=course_id)
        course.delete()
    except:
        pass # course doesn't exist
    return HttpResponse("Course deleted successfully") # redirect back to home page


def delete_all_courses(request):
    '''
    delete all courses related to the current user
    '''
    try:
        courses = Course.objects.filter(user=request.user)
        courses.delete()
    except:
        pass # course doesn't exist
    
    return home_page_view(request)


def add_course(request):
    '''
    add new course object to the database
    '''
    course = request.GET.get('course')
    section = request.GET.get('section')
    response_data = {}
    course_info = {}
    response_data['error'] = False
    response_data['error_msg'] = ''

    # print course
    # print section

    if len(section) != 4:
        if len(section) == 3:
            section = "0" + section
        else:
            response_data['error'] = True
            response_data['error_msg'] = 'Section ID is invalid!'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")

    # Set URL for testudo course search, term, and other query data
    page_url = "https://ntst.umd.edu/soc/all-courses-search.html?course=" + course + "&section=" + section + "&term=201308&level=ALL"
    page = urllib2.urlopen(page_url).read()
    soup = BeautifulSoup(page)

    if soup.find("div", {"class" : "no-courses-message"}) != None:
        response_data['error'] = True
        response_data['error_msg'] = 'That course does not exist!'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    if len(course) <= 4:
        response_data['error'] = True
        response_data['error_msg'] = 'That course does not exist!'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    course_container = soup.find("div", {"class" : "courses-container"})
    first_block = course_container.find("div", {"class" : "course"}, {"id": course})

    if first_block == None:
        response_data['error'] = True
        response_data['error_msg'] = 'That course does not exist!'
        return HttpResponse(json.dumps(response_data), mimetype="application/json")

    class_block = first_block.find('div', {'class' : 'class-days-container'})
    classes = class_block.findAll('div', {'class' : 'row'})
    response_data['courses'] = []
    for i in range(0, len(classes)):
        c = Course()
        c.name = course.upper()
        c.section = section

        room = classes[i].find('span', {'class' : 'class-room'}).text
        
        if room != None:
            if room == 'ONLINE':
                response_data['error'] = True
                response_data['error_msg'] = 'You cannot add online classes!'
                return HttpResponse(json.dumps(response_data), mimetype="application/json")
            else:
                c.room_number = room
        
        c.build_code = classes[i].find('span', {'class' : 'building-code'}).text
        
        class_start = classes[i].find('span', {'class' : 'class-start-time'}).text
        c.start_time =  parser.parse(class_start)
        
        class_end = classes[i].find('span', {'class' : 'class-end-time'}).text
        c.end_time = parser.parse(class_end)
        
        c.section_days = classes[i].find('span', {'class' : 'section-days'}).text
        c.link = page_url


        if classes[i].find('span', {'class' : 'class-type'}) != None:
            c.tag = classes[i].find('span', {'class' : 'class-type'}).text
        try:
            c.user = User.objects.get(id = request.user.id)
        except ObjectDoesNotExist:
            response_data['error'] = True
            response_data['error_msg'] = 'You must be logged in to add courses.'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        if Course.objects.filter(name=c.name, start_time=c.start_time, section_days=c.section_days, user=c.user).exists() != True:
            course_info = {}
            course_info['name']         = c.name
            course_info['section']      = c.section
            course_info['build_code']   = c.build_code
            course_info['room_number']  = c.room_number
            course_info['start_time']   = c.start_time.strftime("%H:%M")
            course_info['end_time']     = c.end_time.strftime("%H:%M")
            course_info['section_days'] = []
            s = Scraper()
            s.split_days(course_info['section_days'], c.section_days)
            course_info['user']         = c.user.username
            course_info['link']         = c.link
            course_info['tag']          = '' if c.tag == None else c.tag
            c.save()
            course_info['id']           = c.id
            response_data['courses'].append(course_info)
            response_data['error'] = False
            response_data['error_msg'] = ''
        else:
            response_data['error'] = True
            response_data['error_msg'] = 'That course already exists!'
            errorResponse = HttpResponse(json.dumps(response_data), mimetype="application/json")

    if response_data['error']:
        if course_info == {}:
            return errorResponse

    response_data['error'] = False
    response_data['error_msg'] = ''
    return HttpResponse(json.dumps(response_data), mimetype="application/json")