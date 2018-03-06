from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

from django.utils import timezone
import pytz
from datetime import datetime


passwordRegex = re.compile(r'^(?=.{8,16}$)(?=.*[A-Z])(?=.*[0-9]).*$')
emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
nameRegex = re.compile(r'^(?=.{2,})([a-zA-z]*)$')
bdayRegex = re.compile(r'^[0-3]?[0-9].[0-3]?[0-9].(?:[0-9]{2})?[0-9]{2}$')
apptRegex = re.compile(r'^[0-3]?[0-9].[0-3]?[0-9].(?:[0-9]{2})?[0-9]{2}$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        posteddata = postData['birthdate']
        print "1st time it prints ", postData['birthdate']
        originaldate = datetime.strptime(posteddata['%m/%d/%y'])
        print "Now printing original date ", originaldate
        bdate = datetime.datetime(originaldate, tzinfo=pytz.UTC)
        print "Printing bdate ", bdate
        
        if len(postData['name']) <  2:
            errors['name'] = "Your name must be 2 letters or more!"
            
        if not nameRegex.match(postData['name']):
            errors['name'] = "Your name can only contain letters!"

        # if not bdayRegex.match(bdate):
        #     errors['birthdate'] = "Your birthday is not in the correct format!"

        # if not bdate < datetime.datetime.now():
        #     errors['birthdate'] = "Your birthdate cannot be today or in the future!"

        if not emailRegex.match(postData['email']):
            errors['email'] = "Your email is not a valid address!"

        if not passwordRegex.match(postData['pw']):
            errors['pw'] = "Your password must be between 8 and 16 characters in length and can only be comprised of letters and numbers!"

        if not postData['pw'] == postData['confpw']:
            errors['confpw'] = "Your passwords don't match!"
        return errors
        

    def log_validator(self, postData):
        user = self.filter(email=postData['email'])
        errors1 = {}
        password = postData['pw']
        if user:
            if not bcrypt.hashpw(postData['pw'].encode(), user[0].password.encode()) == user[0].password.encode():
                errors1['pw'] = "Your email/password combo doesn't match!!"
        else: 
            errors['email'] = "Your email does not exist in the database!"
        return errors1

    def add_validator(self, postData):
        errors3 = {}
        if not apptRegex.match(postData['taskdate']):
            errors3['taskdate'] = "Your task date is not in the correct format! Needs to be YYYY-MM-DD"
            return errors3

        
        
class User(models.Model):
    name = models.CharField(max_length = 255)
    birthdate = models.DateTimeField(blank=True, null=True)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()


class Task(models.Model):
    task_name = models.CharField(max_length = 255)
    status = models.CharField(max_length = 255, default="Pending")
    task_date = models.DateTimeField(blank=True, null=True)
    task_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    users = models.ForeignKey(User, related_name="tasks")
    