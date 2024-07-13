from django.http import JsonResponse
from django.utils import timezone
import logging
from .tasks import send_email_task

# Get the logger for the root Django logger configuration
time_logger = logging.getLogger("core")

def log_time():
    try:
        current_time = timezone.now()
        time_logger.info(f'Current time: {current_time}')
    except Exception as e:
        time_logger.error(f'Error logging time: {str(e)}')

def send_message(request):
    sendmail = request.GET.get('sendmail')
    talktome = 'talktome' in request.GET

    if sendmail and talktome:
        email = sendmail  
        send_email_task.delay(email)  
        log_time() 
        return JsonResponse({'status': 'Email queued and current time logged successfully'})

    elif sendmail:
        email = sendmail 
        send_email_task.delay(email) 
        log_time() 
        return JsonResponse({'status': 'Email queued successfully'})

    elif talktome:
        log_time()
        return JsonResponse({'status': 'Current time logged successfully'})

    else:
        return JsonResponse({'error': 'No valid parameters provided'}, status=400)
