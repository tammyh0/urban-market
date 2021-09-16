from typing import List
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import RemoteUserBackend
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Saved, Bid


def index(request):
    # Get username
    username = request.user.username

    # Populate with all listings
    listings = Listing.objects.all()

    return render(request, "urbanmarket/index.html", {
        "username": username,
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "urbanmarket/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "urbanmarket/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "urbanmarket/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "urbanmarket/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "urbanmarket/register.html")


def category(request):
    # Get username
    username = request.user.username

    if request.method == "POST":
        category = request.POST["category"]

        # Get items in chosen category
        listings = []
        try:
            listings = Listing.objects.filter(category=category)
        except Listing.DoesNotExist:
            listings = None

        return render(request, "urbanmarket/category.html",  {
            "username": username,
            "category": category,
            "category_items": listings
        })


def listing(request, id):
    # Get username
    username = request.user.username

    # Get listing
    listing = Listing.objects.get(id=id)

    # Get listing's comments, if any
    comments = []
    try:
        comments = Comment.objects.filter(item=listing)
    except Comment.DoesNotExist:
        comments = None

    # Get current state of item save feature
    saved = []
    try:
        saved = Saved.objects.filter(username=User.objects.get(username=username), item=listing)
    except Saved.DoesNotExist:
        saved = None

    # Get current number of bids
    bidsCount = []
    try:
        bids = Bid.objects.filter(item=listing) 
        bidsCount = len(bids)
    except Bid.DoesNotExist:
        bidsCount = 0

    # Check to see if current bid price is user's bid
    highestBid = []
    minBid = listing.price
    try:
        bids = Bid.objects.filter(item=listing)
        highestBid = bids.order_by('bidPrice').first()

        if bidsCount > 0:
            minBid = float(minBid) + 0.01
    except Bid.DoesNotExist:
        highestBid = None

    return render(request, "urbanmarket/item.html", {
        "username": username,
        "listing": listing,
        "minBid": minBid,
        "comments": comments,
        "saved": saved,
        "bids": bidsCount,
        "highestBid": highestBid
    })


@login_required
def create(request):
    # Get username
    username = request.user.username

    if request.method == "POST":
        # Get user input
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        imageURL = request.POST["image"]
        size = request.POST["size"]
        category = request.POST["category"]

        # Attempt to create new listing
        try:
            listing = Listing(seller=User.objects.get(username=username), title=title, description=description,
                imgURL=imageURL, price=price, size=size, category=category, bidStatus="Open")
            listing.save()
        except IntegrityError:
            return render(request, "urbanmarket/index.html", {
                "message": "There was an error creating your listing. Try again."
            })
        return HttpResponseRedirect(reverse("index"))


@login_required
def comment(request):
    if request.method == "POST":

        # Get username
        username = request.user.username

        # Get user input
        id = request.POST["id"]
        listing = Listing.objects.get(id=id)
        comment = request.POST["comment"]

        # Attempt to create new comment
        try:
            new_comment = Comment(item=listing, username=User.objects.get(username=username), comment=comment)
            new_comment.save()
        except IntegrityError:
            return render(request, "urbanmarket/index.html", {
                "message": "There was an error creating your comment. Try again."
            })
        return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))

@login_required
def bid(request):
    if request.method == "POST":
        username = request.user.username

        bid = float(request.POST["bid"])
        id = request.POST["id"]

        listing = Listing.objects.get(id=id)

        # Place bid
        new_bid = Bid(username = User.objects.get(username=username), item = listing, bidPrice = bid)
        new_bid.save()

        # if bid price is higher than current price, update current price
        listing = Listing.objects.get(id=id)
        if bid > listing.price:
            listing.price = bid
            listing.save()

        return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
    

@login_required
def saved(request):
    username = request.user.username
    if request.method == "POST":
        # Get current state
        id = request.POST["id"]
        listing = Listing.objects.get(id=id)
        current = Saved.objects.filter(username=User.objects.get(username=username), item=listing)
        # If not already saved, then save, otherwise remove saved from database
        if (current):
            # Unsave
            saved = Saved.objects.filter(username=User.objects.get(username=username), item=listing).delete()
            # Redirect, indicating that heart icon is unsaved
            return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
        else:
            # Save
            saved = Saved(username=User.objects.get(username=username), item=listing)
            saved.save()
            # Redirect, indicating that heart icon is saved
            return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
    else:
        # Get user's saved items, if any
        saved = []
        try:
            saved = Saved.objects.filter(username=User.objects.get(username=username))
        except Comment.DoesNotExist:
            saved = None
        return render(request, "urbanmarket/saved.html", {
            "username": username,
            "saved_items": saved
        })

@login_required
def close(request):
    if request.method == "POST":
        id = request.POST["id"]
        listing = Listing.objects.get(id=id)
        listing.bidStatus = "Closed"
        listing.save()
        return HttpResponseRedirect(reverse("listing", kwargs={'id': id}))
