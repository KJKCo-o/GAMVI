import json

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

from main.models import Calendar


def home(request):
    return render(request, 'main/home.html')

def voice(request):
    return render(request, 'main/voice_record.html')

def emotion(request):
    return render(request, 'main/emotion_record.html')

def dailyDetail(request):
    return render(request, 'main/daily_detail.html')

class CalendarList(View):
    def get(self, request):
        try:
            user_id, year, month = request.GET.get('user_id', None), \
                                   request.GET.get('year', None), request.GET.get('month', None)

            year_month = year + ("-0" if int(month) < 10 else "-") + month
            emotions = list(Calendar.objects.filter(user=user_id, date__startswith=year_month).values())
            for emotion in emotions:
                emotion['date'] = emotion['date'].day

            return JsonResponse({'emotions': emotions})

        except json.JSONDecodeError as e:
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status=500)
        except KeyError:
            return JsonResponse({'message': 'Invalid Value'}, status=500)
