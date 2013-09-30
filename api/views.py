from api.scraper import Scraper


def get_course_view(request):
    '''
    Get course data for the given course and section and return it as an HTTP response
    containing a JSON string
    '''
    course = request.GET.get('course')
    section = request.GET.get('section')
    s = Scraper()
    response_data = s.get_course(course, section, request.user.id)
    return response_data