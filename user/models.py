from django.db import models

class UserData(models.Model):
    user_id = models.AutoField(db_column='user_id',primary_key=True,null=False)
    email = models.EmailField(db_column='email',unique=True,null=False)
    password = models.CharField(max_length=150,db_column='password',null=False)
    active = models.BooleanField(default=True)


    def __str__(self):
        return '{} {}'.format(self.email,self.password)

    def __as_dict__(self):
        return{
            'user_id': self.user_id,
            'email': self.email,
            'password': self.password,
            'active': self.active
        }

    class Meta:
        db_table = 'user_data'


class ProfileSetUp(models.Model):
    id = models.AutoField(db_column='id',primary_key=True,null=False)
    user_id = models.ForeignKey(UserData,db_column='user_id',null=False,on_delete=models.CASCADE)
    username = models.CharField(max_length=150,db_column='username',null=False,default='guest')
    height = models.IntegerField(db_column='height',null=False)
    weight = models.IntegerField(db_column='weight',null=False)
    goal = models.IntegerField(db_column='goal',null=False)
    dob = models.DateField(db_column='dob',null=False)
    gender = models.CharField(db_column='gender',max_length=100,null=False)
    activity_level = models.CharField(db_column='activity_level',max_length=200,null=False)

    def __str__(self):
        return '{} {} {} {} {} {} {}'.format(self.username,self.height,self.weight,self.goal,self.dob,self.gender,self.activity_level)

    def __as_dict__(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.username,
            'height': self.height,
            'weight': self.weight,
            'goal': self.goal,
            'dob': self.dob,
            'gender': self.gender,
            'activity_level': self.activity_level
        }

    class Meta:
        db_table = 'user_profile'