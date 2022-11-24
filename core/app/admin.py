from django.contrib import admin
from .models import Posts,Profile,Upvote,Downvote


admin.site.register(Posts)
admin.site.register(Profile)
admin.site.register(Upvote)
admin.site.register(Downvote)
