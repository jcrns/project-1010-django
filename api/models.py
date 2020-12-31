from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image

class Preference(models.Model):
    owner = models.CharField(max_length=100)
    criminal_justice = models.SmallIntegerField(default=0)
    economy_taxes = models.SmallIntegerField(default=0)
    abortion = models.SmallIntegerField(default=0)
    education = models.SmallIntegerField(default=0)
    minority_support = models.SmallIntegerField(default=0)
    immigration = models.SmallIntegerField(default=0)
    environment = models.SmallIntegerField(default=0)
    lbgtq_rights = models.SmallIntegerField(default=0)
    womens_rights = models.SmallIntegerField(default=0)
    health_care = models.SmallIntegerField(default=0)
    corporations = models.SmallIntegerField(default=0)
    national_security = models.SmallIntegerField(default=0)
    gun_control = models.SmallIntegerField(default=0)
    social_left_to_right = models.SmallIntegerField(null=True, blank=True)
    economics_left_to_right = models.SmallIntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.owner}"

    # Overriding save function to calculate political ideaology
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        print("self.social_left_to_rsdsdight")
        print(self.social_left_to_right)
        print(self.economics_left_to_right)
        # if self.social_left_to_right == None or self.economics_left_to_right == None:
        social_left_to_right_number = 0
        social_left_to_right_number += self.abortion
        social_left_to_right_number += self.minority_support
        social_left_to_right_number += self.lbgtq_rights
        social_left_to_right_number += self.womens_rights
        social_left_to_right_number += self.environment

        economic_left_to_right_number = 0
        economic_left_to_right_number += self.criminal_justice
        economic_left_to_right_number += self.economy_taxes
        economic_left_to_right_number += self.education
        economic_left_to_right_number += self.immigration
        economic_left_to_right_number += self.health_care
        economic_left_to_right_number += self.corporations
        economic_left_to_right_number += self.gun_control
        print("social_left_to_right_number")
        print(social_left_to_right_number)
        print("economic_left_to_right_number")
        
        score = (((social_left_to_right_number/5)/2) +  ((economic_left_to_right_number/7)/2))
        print(((social_left_to_right_number/5)/2))
        print(((economic_left_to_right_number/7)/2))
        print('score')
        print(score)
        print('Political Score', (((score/2)/2) + 0.5))
        
        self.social_left_to_right = social_left_to_right_number
        self.economics_left_to_right = economic_left_to_right_number 

        super(Preference, self).save(force_insert, force_update, *args, **kwargs)
        # img = Image.open(self.image.path) # Open image using self

        # if img.height > 300 or img.width > 300:
        #     new_img = (300, 300)
        #     img.thumbnail(new_img)
        #     img.save(self.image.path) 
            
# Function to calculate political ideas
def calculatePoliticalScore(social_score, economic_score):
    score = (((social_score/5)/2) +  ((economic_score/7)/2))
    print(score)
    score = (((score/2)/2) + 0.5)
    print('final_score')
    print(score)
    return score
    
class Politician(models.Model):
    # Politician Info
    name = models.CharField(max_length=100)
    age = models.SmallIntegerField()
    position = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    up_for_election = models.BooleanField(max_length=100)
    biography = models.CharField(max_length=1000)
    preference = models.OneToOneField(Preference, on_delete=models.CASCADE)
    image = models.ImageField(default='profile-blank.png', upload_to='profile_pics')

    # Political Stances
    criminal_justice = models.CharField(max_length=1000)
    economy_taxes = models.CharField(max_length=1000)
    abortion = models.CharField(max_length=1000)
    education = models.CharField(max_length=1000)
    minority_support = models.CharField(max_length=1000)
    immigration = models.CharField(max_length=1000)
    environment = models.CharField(max_length=1000)
    lbgtq_rights = models.CharField(max_length=1000)
    womens_rights = models.CharField(max_length=1000)
    health_care = models.CharField(max_length=1000)
    corporations = models.CharField(max_length=1000)
    national_security = models.CharField(max_length=1000)
    gun_control = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.name}"

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.OneToOneField(Preference, on_delete=models.CASCADE)

    # Personal data
    location = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    # Event Info
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default='profile-blank.png', upload_to='event_pics')
    organizer = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    address = models.CharField(max_length=1000, null=True, blank=True )
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

class Movement(models.Model):
    # Mission Info
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default='group-blank.png', upload_to='movement_pics')
    mission = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"