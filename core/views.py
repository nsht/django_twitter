import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TweetForm


from .models import Tweet, FollowerRelations

import pdb

# Create your views here.


@login_required(login_url="/accounts/login/")
def index(request):
    following = FollowerRelations.objects.filter(follower_id=request.user.id)
    if len(following) == 0:
        return HttpResponse(
            json.dumps({"error": "Follow Users to see their tweets"}),
            status=404,
            content_type="application/json",
        )

    following_ids = [f_user.user_id for f_user in following]
    tweets = Tweet.objects.filter(user_id__in=following_ids).order_by(
        "-tweet_created_timestamp"
    )
    tweet_list = []
    for tweet in tweets:
        tw = {}
        tw["tweet_text"] = tweet.tweet_text
        tw["tweet_author"] = tweet.user.username
        tw["created"] = str(tweet.tweet_created_timestamp)
        tw["like_count"] = tweet.like_count
        tw["reply_count"] = tweet.reply_count
        tw["retweet_count"] = tweet.reply_count
        if tweet.is_retweeted:
            tw["original_tweet_id"] = tweet.original_tweet_id
        if tweet.media_id:
            tw["media_id"] = tweet.media_id
        tweet_list.append(tw)
    payload = json.dumps(tweet_list)
    return HttpResponse(payload, status=200, content_type="application/json")


@login_required(login_url="/accounts/login/")
def new_tweet(request):
    if request.method == "POST":
        form = TweetForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("core:index")
    else:
        form = TweetForm()
        return render(request, "core/new_tweet.html", {"form": form})
        return HttpResponse(status=200)


@login_required(login_url="/accounts/login/")
def follow(request, user_name):
    follow_user = User.objects.filter(username=user_name).first()
    follow = FollowerRelations(user_id=follow_user, follower_id=request.user.id)
    follow.save()
    return redirect("core:index")
