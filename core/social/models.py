import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
    
class MyUUIDModel(models.Model):
	id = models.UUIDField(
		primary_key = True,
		default = uuid.uuid4,
		editable = False)
	# other fields
User= get_user_model()


class UserProfile(models.Model):
    user=models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
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
        return self.user.email

class Post(models.Model): 
    post_id =models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author =models.ForeignKey(User,on_delete=models.CASCADE)
    body =models.CharField(max_length=240)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on= models.DateTimeField(auto_now=True)
    likes =models.ManyToManyField(User,blank=True,related_name='likes',)
    dislikes =models.ManyToManyField(User,blank=True,related_name='dislikes',)
    expiration= models.DateTimeField(null=True)
    shared_body = models.TextField(blank=True, null=True)
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='+')
    shared_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    comments =models.ManyToManyField('Comment',blank=True,related_name='comments',)



    class Meta:
        ordering=['-created_on','-shared_on']

    def create_tags(self):
        for word in self.body.split():
            if (word[0] == '#'):
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()

        if self.shared_body:
            for word in self.shared_body.split():
                if (word[0] == '#'):
                    tag = Tag.objects.filter(name=word[1:]).first()
                    if tag:
                        self.tags.add(tag.pk)
                    else:
                        tag = Tag(name=word[1:])
                        tag.save()
                        self.tags.add(tag.pk)
                    self.save()

    def __str__(self):
        return self.body[:20]

    def get_number_of_likes(self):
        number_of_likes = self.likes.count()
        return number_of_likes

    def get_number_of_dislikes(self):
        number_of_dislikes = self.dislikes.count()
        return number_of_dislikes

    def get_author_picture(self):
        author_picture = self.author.profile.picture
        print(author_picture)
        return author_picture

    def get_absolute_url(self):
        return reverse('social:post-detail',args=[self.post_id])


class Image(models.Model):
    image_id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE ,related_name='images',blank=True,null=True)

   


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    tags = models.ManyToManyField('Tag', blank=True)
    reply =models.ManyToManyField("ReplyComment",blank=True,related_name="replies")

    def create_tags(self):
        for word in self.comment.split():
            if (word[0] == '#'):
                tag = Tag.objects.get(name=word[1:])
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



    class Meta:
        ordering=['-created_on']

class ReplyComment(models.Model):
    reply = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='reply_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='reply_dislikes')
    parent = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    tags = models.ManyToManyField('Tag', blank=True)

    def create_tags(self):
        for word in self.comment.split():
            if (word[0] == '#'):
                tag = Tag.objects.get(name=word[1:])
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()

    @property
    def children(self):
        return ReplyComment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False



    class Meta:
        ordering=['-created_on']

class Notification(models.Model):
	# 1 = Like, 2 = Comment, 3 = Follow, #4 = DM
	notification_type = models.IntegerField()
	to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
	from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	user_has_seen = models.BooleanField(default=False)

class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	is_read = models.BooleanField(default=False)


class Tag(models.Model):
	name = models.CharField(max_length=255)


@receiver(post_save,sender=User)
def ProfileCreate(sender,instance,created,*args, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print('profile created')

