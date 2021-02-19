from django.db import models

class Subscription(models.Model):
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=False, auto_now_add=False)
    ended_on = models.DateField(auto_now=False, auto_now_add=False)