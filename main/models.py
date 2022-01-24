from django.db import models


class Calendar(models.Model):
    calender_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    date = models.DateTimeField()
    emotion = models.CharField(max_length=12)

    class Meta:
        managed = False
        db_table = 'calendar'


class Detail(models.Model):
    detail = models.OneToOneField(Calendar, models.DO_NOTHING, primary_key=True)
    sentence = models.TextField()
    voice = models.TextField()
    enjoyment = models.FloatField()
    sadness = models.FloatField()
    anger = models.FloatField()
    surprise = models.FloatField()
    disgust = models.FloatField()
    fear = models.FloatField()

    class Meta:
        managed = False
        db_table = 'detail'


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=10)
    age = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=7, blank=True, null=True)
    contact = models.CharField(max_length=11, blank=True, null=True)
    password = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'user'
