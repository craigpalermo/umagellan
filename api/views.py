from api.scraper import Scraper


def get_courses_view(request):
    '''
    Get course data for the given course and section and return it as an HTTP response
    containing a JSON string
    '''
    course = request.GET.get('course')
    section = request.GET.get('section')
    s = Scraper()
    response_data = s.get_courses(course, section, request.user.id)
    return response_data