from django.db.models.base import Model
# from auctions.views import category
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # username = models.CharField() # unique
    # email = models.CharField() # unique
    # password = models.CharField() # use the hash code

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    # seller = models.CharField(max_length=64) # use username
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    imgURL = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    size = models.CharField(max_length=10)
    category = models.CharField(max_length=64)
    bidStatus = models.CharField(max_length=10, default="Open")


class Bid(models.Model):
    # username = models.CharField(max_length=64) # of bidder
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    # item = models.IntegerField() # might wanna use that item's id instead
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_item")
    bidPrice = models.DecimalField(max_digits=6, decimal_places=2)

class Saved(models.Model):
    # username = models.CharField(max_length=64)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saver")
    #item = models.IntegerField() # might wanna use that item's id instead
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="saved_item")

class Comment(models.Model):
    #item = models.IntegerField() # might wanna use that item's id instead
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="commented_item")
    # username = models.CharField(max_length=64)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    date = models.DateField(auto_now_add=True)
    comment = models.CharField(max_length=256)

