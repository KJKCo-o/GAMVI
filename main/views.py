from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def voice(request):
    return render(request, 'main/voice_record.html')
