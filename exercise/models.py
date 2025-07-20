
from django.db import models
from user.models import UserData


class Exercise(models.Model):

    class ExerciseType(models.TextChoices):
        CARDIO = 'Cardio', 'Cardio'
        WEIGHT_LIFTING = 'Weight Lifting', 'Weight Lifting'

    class IntensityLevel(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium'
        HIGH = 'High', 'High'


    user = models.ForeignKey(UserData, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=50, choices=ExerciseType.choices)
    exercise_name = models.CharField(max_length=200)
    intensity = models.CharField(max_length=50, choices=IntensityLevel.choices)


    kcal = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    log_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'exercise'
        ordering = ['-log_date']

    def __str__(self):
        return f"{self.exercise_name} for {self.user} on {self.log_date.strftime('%Y-%m-%d')}"

    def to_dict(self):
        return {
            'user': self.user.id,
            'exercise_type': self.exercise_type,
            'exercise_name': self.exercise_name,
            'intensity': self.intensity,
            'kcal': self.kcal,
            'log_date': self.log_date
        }


class Cardio(models.Model):

    exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE, primary_key=True, related_name='cardio_details')

    duration_minutes = models.PositiveIntegerField()
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'cardio'

    def __str__(self):
        return f"Cardio details for log #{self.exercise_id}"

    def to_dict(self):
        return {
            'duration_minutes': self.duration_minutes,
            'distance_km': self.distance_km,
        }


class WeightLifting(models.Model):

    exercise = models.OneToOneField(Exercise, on_delete=models.CASCADE, primary_key=True,
                                    related_name='weight_lifting_details')


    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()

    class Meta:
        db_table = 'weightlifting'

    def __str__(self):
        return f"Weight details for log #{self.exercise_id}"

    def to_dict(self):
        return {
            'weight_kg': self.weight_kg,
            'sets': self.sets,
            'reps': self.reps,
        }