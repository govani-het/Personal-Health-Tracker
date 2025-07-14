from django.db import models
from user.models import UserData


class UserNutritionData(models.Model):

    id = models.AutoField(primary_key=True,db_column='id')
    user_id = models.ForeignKey(UserData,db_column="user_id", on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=100, db_column='meal_type')
    meal_date = models.DateField(db_column='meal_date',auto_now=True)
    food_quantity = models.IntegerField(db_column='food_quantity')
    food_name = models.CharField(max_length=500, db_column='food_name')
    kcal = models.FloatField(db_column='kcal', null=True, blank=True)
    protein = models.FloatField(db_column='protein', null=True, blank=True)
    carbs = models.FloatField(db_column='carbs', null=True, blank=True)
    fats = models.FloatField(db_column='fats', null=True, blank=True)


    def __str__(self):
        return "{} {} {} {} {} {} {} {}".format(self.meal_type, self.meal_date, self.food_quantity,self.food_name,self.kcal,self.protein,self.carbs,self.fats)


    def __as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'meal_type': self.meal_type,
            'meal_date': self.meal_date,
            'food_quantity': self.food_quantity,
            'food_name': self.food_name,
            'kcal': self.kcal,
            'protein': self.protein,
            'carbs': self.carbs,
            'fats': self.fats,

            }

    class Meta:
        db_table = 'user_nutrition_data'