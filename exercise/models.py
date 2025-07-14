from django.db import models
from user.models import UserData

class Exercise(models.Model):

    user_id = models.ForeignKey(UserData, on_delete=models.CASCADE)
    exercise_type = models.CharField(max_length=200)
    exercise_name = models.CharField(max_length=200 )
    intensity = models.CharField(max_length=200 )
    kcal = models.FloatField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return "{} {} {} {} {} {}".format(self.user_id, self.exercise_type, self.exercise_name, self.intensity,self.date,self.kcal)

    def __ad_dict(self):
        return {
            'user_id': self.user_id,
            'exercise_type': self.exercise_type,
            'exercise_name': self.exercise_name,
            'intensity': self.intensity,
            'kcal': self.kcal,
            'date': self.date
        }

    class Meta:
        db_table = 'exercise'

class Cardio(models.Model):

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE,default=None)
    duration = models.FloatField()
    distance = models.FloatField()

    def __str__(self):
        return "{} {}".format( self.distance, self.duration)

    def __as_dict(self):
        return {

            'exercise': self.exercise,
            'duration': self.duration,
            'distance': self.distance,

        }
    class Meta:
        db_table = 'cardio'

class WeightLifting(models.Model):

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE,default=None)
    weight = models.FloatField()
    exercise_set = models.IntegerField(default=0)
    exercise_reps = models.IntegerField(default=0)


    def __str__(self):
        return "{} {}".format( self.weight, self.exercise_set)

    def __as_dict(self):
        return {

            'exercise': self.exercise,
            'weight': self.weight,
            'exercise_set': self.exercise_set,
            'exercise_reps': self.exercise_reps,
        }

    class Meta:
        db_table = 'weightlifting'