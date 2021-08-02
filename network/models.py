from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

class PostManager(models.Manager):
    def newPost(self, author, content):
        new = self.create(author=author, content=content)
        new.full_clean()
        new.save()
        return new

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=CASCADE, related_name='posts')
    content = models.TextField(max_length=127)
    date = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False, blank=True)
    editdate = models.DateField(auto_now=True, null=True, blank=True)

    objects = PostManager()

    def __str__(self):
        return f"{self.author} : {self.content} -- ({self.date})"

    def userLike(self, user, post):
        return Like.objects.exists(user=user, post=self)

    def clean(self):
        if self.content == "":
            raise ValidationError("post can't be empty!")



class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete= CASCADE, related_name='liked')
    date = models.DateTimeField(auto_now = True)
    
    class Meta:
        unique_together = ('post', 'user')

class FollowManager(models.Manager):
    def follow(self, user, other):
        newFollow = self.create(user=user, user_follow= other)
        newFollow.save()
        return newFollow
    
    def unfollow(self, user, other):
        toDelete = self.filter(user = user).filter(user_follow = other)
        toDelete.delete()


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name='following')
    user_follow = models.ForeignKey(User,on_delete=CASCADE, related_name='followers')

    objects= FollowManager()

    def __str__(self):
        return f"{self.user} - {self.user_follow}"
    
    class Meta:
        unique_together = ('user', 'user_follow')

