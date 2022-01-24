import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.models import Calendar, Detail, User

# Create your views here.
from django.views import View

from main.controllers import emotionAnalyze, sentenceAnalyze


def home(request):
    return render(request, 'main/home.html')


def voice(request):
    return render(request, 'main/voice_record.html')


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


class Analyze(View):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)

        try:
            valid_token = sentenceAnalyze.tokenizer(data["sentence"])
            lemma_list = sentenceAnalyze.lemmatizer(valid_token)
            df_emotion = emotionAnalyze.open_emotion_dictionary()
            emotion = emotionAnalyze.analyzeEmotion(df_emotion, valid_token, lemma_list)

            calendar_instance = Calendar.objects.create(
                user=User.objects.get(user_id=data["user_id"]),
                date=datetime.now(),
                emotion=data["emotion"]
            )

            calendar_instance.save()
            Detail.objects.create(
                detail=calendar_instance,
                sentence=data["sentence"],
                voice="voice_url",
                enjoyment=emotion["기쁨"],
                sadness=emotion["슬픔"],
                anger=emotion["분노"],
                surprise=emotion["놀람"],
                disgust=emotion["혐오"],
                fear=emotion["공포"],
            ).save()

            return JsonResponse({'message': '문장 분석 완료', 'data': {'sentence': data['sentence'], 'emotions': emotion}},
                                status=201)

        except json.JSONDecodeError as e:
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status=500)
        except KeyError:
            return JsonResponse({'message': 'Invalid Value'}, status=500)
