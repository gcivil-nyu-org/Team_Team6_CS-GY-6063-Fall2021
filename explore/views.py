from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from dayplanner.services import yelp_client
from resources.days.models import Day, FavoriteDay, DayVenue
from resources.categories.models import Category
from resources.venues.models import FavoriteVenue


ERROR_FAV_NoLOGIN = "To Save your Favourite day, Please Log in First"


def explore(requets):
    context = {}
    if "Error_Message" in requets.session:
        context["error"] = requets.session["Error_Message"]
        del requets.session["Error_Message"]
    elif "success_Message" in requets.session:
        context["message"] = requets.session["success_Message"]
        del requets.session["success_Message"]
    try:
        days = Day.objects.all().filter(is_active=True)
        List = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                if not requets.user.is_anonymous:
                    if day.favoriteday_set.filter(user=requets.user).count() == 1:
                        List.append({"day": day, "is_fav": True})
                    else:
                        List.append({"day": day, "is_fav": False})
                else:
                    List.append({"day": day, "is_fav": False})

        context["days"] = List
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(requets, "explore/explore.html", context)


def explore_cats(requests, cat):
    context = {}
    try:
        cat_object = Category.objects.get(cat=cat)
        days = []
        for day in Day.objects.all():
            for cats in day.daycategory_set.all():
                if cats.cat == cat_object:
                    days.append(day)
        List = []
        for day in days:
            if day.dayvenue_set.count() >= 1:
                if not requests.user.is_anonymous:
                    if day.favoriteday_set.filter(user=requests.user).count() == 1:
                        List.append({"day": day, "is_fav": True})
                    else:
                        List.append({"day": day, "is_fav": False})
                else:
                    List.append({"day": day, "is_fav": False})

        context["days"] = List
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse("Error Code: %s" % e)

    return render(requests, "explore/explore.html", context)


def day_summary(requests, day_id):
    day = get_object_or_404(Day, pk=day_id)
    context = {}
    context["active_categories"] = day.daycategory_set.all()
    DayVenues = day.dayvenue_set.all()
    fetch_list = []
    dayvenue_list = []

    if "Error_Message" in requests.session:
        context["error"] = requests.session["Error_Message"]
        del requests.session["Error_Message"]
    elif "success_Message" in requests.session:
        context["message"] = requests.session["success_Message"]
        del requests.session["success_Message"]

    for dv in DayVenues:
        fetch_list.append(dv.venue.yelp_id)
    context["dayvenue_list"] = dayvenue_list
    responses = yelp_client.fetch_many(fetch_list)
    coordinates = []
    # [{"latitude":<lat_val>,"longitude":<long_val>,"name":<name>}]
    for resp in responses:
        data = resp["coordinates"]
        data["name"] = resp["name"]
        coordinates.append(data)
    context["coordinates"] = coordinates

    return render(requests, "explore/day_summary.html", context)


def fork(request, day_id):
    day = get_object_or_404(Day, pk=day_id)

    new_day = day.fork(request.user)
    return HttpResponseRedirect("/creation/%i/edit" % new_day.id)


def search_handeler(request):
    context = {}
    search_key = request.POST["search_input"]
    if search_key == "":
        return explore(request)
    try:
        context["days"] = Day.objects.all().filter(
            name__contains=search_key, is_active=True
        )
        context["cats"] = Category.objects.all()
    except Exception as e:
        return HttpResponse(e)
    return render(request, "explore/explore.html", context=context)


def favorite_day(request, day_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        # Create a Error Message
        request.session["Error_Message"] = ERROR_FAV_NoLOGIN
        return HttpResponseRedirect(last_url)

    # Create a FavoriteDay relation
    day = Day.objects.get(pk=day_id)
    FavoriteDay.objects.create(user=request.user, day=day)
    # Create a success Message
    msg = "Added %s to Favorite List" % day.name
    request.session["success_Message"] = msg
    return HttpResponseRedirect(last_url)


def unfavorite_day(request, day_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        request.session["error"] = ERROR_FAV_NoLOGIN
        return HttpResponseRedirect(last_url)

    # Create a FavoriteDay relation
    day = Day.objects.get(pk=day_id)
    day.favoriteday_set.filter(user=request.user).delete()
    # Create a success Message
    msg = "Removed %s from Favorite List" % day.name
    request.session["success_Message"] = msg

    return HttpResponseRedirect(last_url)


def favorite_venue(request, dayvenue_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        # Create a Error Message
        request.session["Error_Message"] = ERROR_FAV_NoLOGIN
        return HttpResponseRedirect(last_url)

    # Create a FavoriteDay relation
    dayvenue = DayVenue.objects.get(pk=dayvenue_id)
    venue = dayvenue.venue
    FavoriteVenue.objects.create(user=request.user, venue=venue)

    # create a success message
    msg = "Added venue from Favorite List"
    request.session["success_Message"] = msg
    return HttpResponseRedirect(last_url)


def unfavorite_venue(request, dayvenue_id):
    last_url = request.GET.get("last")
    if request.user.is_anonymous:
        # Create a Error Message
        request.session["Error_Message"] = ERROR_FAV_NoLOGIN
        return HttpResponseRedirect(last_url)
    # Remove a FavoriteDay relation
    dayvenue = DayVenue.objects.get(pk=dayvenue_id)
    venue = dayvenue.venue
    FavoriteVenue.objects.get(user=request.user, venue=venue).delete()
    # Create a success message
    msg = "Removed venue from Favorite List"
    request.session["success_Message"] = msg
    return HttpResponseRedirect(last_url)
