from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .tasks import send_email_task
import os

def home_view(request):
    return HttpResponse("HNG Internship")

def log_time(talktome_message=None):
    log_file_path = '/var/log/messaging_system.log'
    try:
        current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file_path, 'a') as log_file:
            log_entry = f'{current_time}: Logged time'
            if talktome_message:
                log_entry += f' - {talktome_message}'
            log_file.write(f'{log_entry}\n')
    except Exception as e:
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Error logging time: {str(e)}\n')

def send_message(request):
    sendmail = request.GET.get('sendmail')
    talktome = 'talktome' in request.GET

    if sendmail and talktome:
        email = sendmail  
        send_email_task.delay(email)  
        log_time('talktome')  # log 'talktome' message
        return JsonResponse({'status': 'Email queued and current time logged successfully'})

    elif sendmail:
        email = sendmail 
        send_email_task.delay(email) 
        log_time()  # log default message
        return JsonResponse({'status': 'Email queued successfully'})

    elif talktome:
        log_time('talktome')  # log 'talktome' message
        return JsonResponse({'status': 'Current time logged successfully'})

    else:
        return JsonResponse({'error': 'No valid parameters provided'}, status=400)

def view_log_file(request):
    log_file_path = '/var/log/messaging_system.log'

    if not os.path.exists(log_file_path):
        return JsonResponse({'error': 'Log file does not exist'}, status=404)

    with open(log_file_path, 'r') as log_file:
        log_content = log_file.read()

    return HttpResponse(log_content, content_type='text/plain')
