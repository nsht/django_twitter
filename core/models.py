from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.


class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_text = models.TextField()
    tweet_status = models.IntegerField(default=1)
    tweet_type = models.IntegerField(default=1)
    like_count = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    retweet_count = models.IntegerField(default=0)
    is_retweeted = models.BooleanField(default=False)
    original_tweet_id = models.IntegerField(null=True, blank=True)
    media_id = models.IntegerField(null=True, blank=True)
    tweet_created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tweet_text


class FollowerRelations(models.Model):
    class Meta:
        unique_together = (("user_id", "follower_id"),)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    follower_id = models.IntegerField()
    follow_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} follows {}".format(self.follower_id, self.user_id)
