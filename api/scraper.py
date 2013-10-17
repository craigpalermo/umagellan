from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from umagellan.models import Course
import json

class Scraper:
    '''
    Contains methods that allow pulling course data from Testudo
    '''

    def get_courses(self, course, section, user_id):
        '''
        Gets the location, start time, and end time for the given course and section;
        returns a JSON string with all of the data for the course
        '''
        response_data = {}
        user = User.objects.get(id=user_id)
    
        if course == None and section == None:
            try:
                resp = user.profile.courses.all()
                
                response_data['courses'] = []
                self.fill_table(response_data, resp)
                response_data['error'] = False
                response_data['error_msg'] = ''
                return HttpResponse(json.dumps(response_data), mimetype="application/json")
            except ObjectDoesNotExist:
                response_data['error'] = True
                response_data['error_msg'] = 'You must be logged in to add courses.'
                return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
        if course == None and section != None:
            response_data['error'] = True
            response_data['error_msg'] = 'You must enter a course!'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
        elif course != None and section == None:
            response_data['error'] = True
            response_data['error_msg'] = 'You must enter a section!'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
        if section != None and len(section) != 4:
            if len(section) == 3:
                section = "0" + section
            else:
                response_data['error'] = True
                response_data['error_msg'] = 'That section ID is invalid!'
                return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
        try:
            resp = user.profile.courses.all().filter(name=course, section=section)
        except ObjectDoesNotExist:
            response_data['error'] = True
            response_data['error_msg'] = 'That username does not exist!'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
        if len(resp) == 0:
            response_data['error'] = True
            response_data['error_msg'] = 'That class or section was not found!'
            return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
        response_data['courses'] = []
        response_data = self.fill_table(response_data, resp)
        
        return HttpResponse(json.dumps(response_data), mimetype="application/json")
    
    
    def fill_table(self, table, resp):
        '''
        Add a dictionary containing resp's course info to table so that table can be returned to a view
        as a JSON string 
        '''
        for r in resp:
            course_info = {}
            course_info['name']         = r.name
            course_info['section']      = r.section
            course_info['build_code']   = r.build_code
            course_info['room_number']  = r.room_number
            course_info['start_time']   = r.start_time.strftime("%H:%M")
            course_info['end_time']     = r.end_time.strftime("%H:%M")
            course_info['section_days'] = []
            
            self.split_days(course_info['section_days'], r.section_days)
            
            course_info['link']         = r.link
            course_info['tag']          = r.tag
            course_info['id']           = r.id
            table['courses'].append(course_info)
            
        return table
            
    def split_days(self, table, section_days):
        for i in range(0, len(section_days)):
            if i+1 < len(section_days) and section_days[i+1].islower():
                table.append(section_days[i] + section_days[i+1])
                i += 2
            elif not section_days[i].islower():
                table.append(section_days[i])
