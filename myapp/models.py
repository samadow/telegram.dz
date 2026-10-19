from django.db import models
from django.contrib.auth.models import AbstractUser
class Acounts(AbstractUser):
    phone_number = models.CharField(max_length=50,unique=True)
    
    
    
class Profile(models.Model):
    user_id = models.ForeignKey(Acounts, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    last_name = models.CharField( max_length=50)
    bio = models.TextField()
    username = models.CharField(max_length=50,unique=True)
    
    
class Avatar(models.Model):
    profile = models.CharField(max_length=50)
    image = models.FileField( max_length=100)
    
    
class Group_number(models.Model):
    user = models.ForeignKey(Acounts, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    joing_data = models.DateField(auto_now_add=True)
    
class Chanal(models.Model):
    owner = models.ForeignKey(Acounts, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    cr_at = models.DateField( auto_now=False, auto_now_add=False)
    link = models.CharField(max_length=50)
    

class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    chanal_id = models.ForeignKey(Chanal, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    cr_at = models.DateTimeField(auto_now_add=True)
    
    
class Flowing(models.Model):
    user_id = models.ForeignKey(Acounts, on_delete=models.CASCADE)
    chanal_id = models.ForeignKey(Chanal, on_delete=models.CASCADE)
    
    

class Chat(models.Model):
    user_1 = models.ForeignKey(Acounts,on_delete=models.CASCADE,related_name='chats_as_user_1')
    user_2 = models.ForeignKey(Acounts,on_delete=models.CASCADE,related_name='chats_as_user_2')
    cr_at = models.DateField(auto_now_add=True)
    
class Message(models.Model):
    sender = models.ForeignKey(Acounts, on_delete=models.CASCADE)
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    cr_at = models.TimeField(auto_now_add=True)
    
class Group(models.Model):
    owner = models.ForeignKey(Acounts, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    
class Group_message(models.Model):
    user = models.ForeignKey(Acounts, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    cr_at = models.DateField(auto_now=False, auto_now_add=False)
    
    
