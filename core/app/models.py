import uuid
from django.db import models

    
class MyUUIDModel(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	# other fields

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User= get_user_model()



class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    avater =models.ImageField(upload_to='core/media/profilepix',null=True)
    country =models.CharField(max_length=50,null=True,blank=True)
    club =models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.user.email

class Upvote(models.Model):
    post =models.ForeignKey("Posts",on_delete=models.CASCADE)
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.post}:{self.user.first_name}"

class Downvote(models.Model):
    post =models.ForeignKey("Posts",on_delete=models.CASCADE)
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp =models.DateTimeField(auto_now_add=True)
   
    def __str__(self) -> str:
        return f"{self.post}:{self.user.first_name}"

class Posts(models.Model): 
    post_id =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    content =models.CharField(max_length=240)
    screenshot =models.ImageField(upload_to='core/media/screenshots',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    upvotes =models.ManyToManyField(User,blank=True,related_name='user_upvote',through=Upvote)
    downvotes =models.ManyToManyField(User,blank=True,related_name='user_downvote',through=Downvote)
    expiration= models.DateTimeField()

    def __str__(self):
        return self.content[:20]



@receiver(post_save,sender=User)
def ProfileCreate(sender,instance,created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('profile created')

