from accounts.views import get_ip
from django.http import HttpResponse
from mainApp.models import Logs

class LogsMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        response = self.get_response(request)
        user = request.user
        ip_address = get_ip(request)[0]
        url_path = request.get_full_path()
        status_code = HttpResponse.status_code
        try:
            Logs.objects.create(ip_address=ip_address,method_type=request.method,method=url_path,user=user,status_code=status_code).save()
        except ValueError:
            return response
        return response