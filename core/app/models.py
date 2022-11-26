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
    first_name =models.CharField(max_length=20, blank=True, null=True)
    last_name =models.CharField(max_length=20, blank=True, null=True)
    bio =models.TextField(max_length=500, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default.png', blank=True)
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    country =models.CharField(max_length=50,null=True,blank=True)
    favourite_club =models.CharField(max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.first_name



class Posts(models.Model): 
    post_id =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    content =models.CharField(max_length=240)
    image = models.ManyToManyField('Image', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    upvotes =models.ManyToManyField(User,blank=True,related_name='user_upvote',)
    downvotes =models.ManyToManyField(User,blank=True,related_name='user_downvote',)
    expiration= models.DateTimeField()

    def __str__(self):
        return self.content[:20]



class Image(models.Model):
	image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)


@receiver(post_save,sender=User)
def ProfileCreate(sender,instance,created,*args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print('profile created')

