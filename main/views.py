import json
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from main.models import Calendar, Detail, User

# Create your views here.
from django.views import View

from main.controllers import emotionAnalyze, sentenceAnalyze
from main.models import Calendar, Detail, User


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

            return JsonResponse({'emotions': emotions}, status=200)

        except json.JSONDecodeError as e:
            return JsonResponse({'message': f'Json_ERROR:{e}'}, status=500)
        except KeyError:
            return JsonResponse({'message': 'Invalid Value'}, status=500)


class CalendarDetail(View):
    def get(self, request, id):
        try:
            # 데이터베이스 조회
            record = Calendar.objects.filter(calendar_id=id).values()[0]
            record_detail = Detail.objects.filter(detail=record['calendar_id']).values()[0]
            user = User.objects.filter(user_id=record['user_id']).values()[0]

            # 필요 데이터 조합
            detail = dict()
            detail['id'] = record['calendar_id']
            detail['month'] = record['date'].month
            detail['day'] = record['date'].day
            detail['user_name'] = user['name']
            detail['sentence'] = record_detail['sentence']
            detail['emotion'] = record['emotion']
            detail['analysis_result'] = dict()
            detail['analysis_result']['enjoyment'] = record_detail['enjoyment']
            detail['analysis_result']['sadness'] = record_detail['sadness']
            detail['analysis_result']['anger'] = record_detail['anger']
            detail['analysis_result']['surprise'] = record_detail['surprise']
            detail['analysis_result']['disgust'] = record_detail['disgust']
            detail['analysis_result']['fear'] = record_detail['fear']

            return JsonResponse({'record': detail}, status=200)

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
