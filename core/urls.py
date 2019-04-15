from django.urls import path
from rest_framework import routers

from core import views

# router = routers.DefaultRouter()
# router.register("api/tweet", views.BinViewSet, "bin")

# urlpatterns = router.urls

app_name = "core"
urlpatterns = [
    path("", views.index, name="index"),
    path("tweet", views.new_tweet, name="new_tweet"),
    path("follow/<str:user_name>",views.follow,name="follow")
]