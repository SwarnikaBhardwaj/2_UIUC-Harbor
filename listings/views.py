# from django.shortcuts import render
#
# # Create your views here.
#
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.views import View
# from django.views.generic import ListView
# from .models import Listing
#
# def listing_manual_view(request):
#    listings = Listing.objects.filter(is_active=True)
#
#
#    html = "<h1>Collective Circle Listings</h1>"
#    for listing in listings:
#        html += f"""
#            <div>
#                <h3>{listing.title}</h3>
#                <p>Category: {listing.category.name}</p>
#                <p>Seller: {listing.seller.first_name}</p>
#            </div>
#            <hr>
#        """
#
#
#    return HttpResponse(html)
#
# def listing_render_view(request):
#    listings = Listing.objects.filter(is_active=True)
#    return render(
#        request,
#        "listings/listing_features.html",
#        {"listings": listings}
#    )
#
# class ListingBaseCBV(View):
# def get(self, request):
#        listings = Listing.objects.filter(is_active=True)
#        return render(
#            request,
#            "listings/listing_features.html",
#            {"listings": listings}
#        )
#
# class ListingGenericCBV(ListView):
#    model = Listing
#    template_name = "listings/listing_features.html"
#    context_object_name = "listings"
#
#     def get_queryset(self):
#         return Listing.objects.filter(is_active=True)
#

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import Listing

# --- Function Based Views ---

def listing_manual_view(request):
    listings = Listing.objects.filter(is_active=True)
    html = "<h1>Collective Circle Listings</h1>"
    for listing in listings:
        html += f"""
            <div>
                <h3>{listing.title}</h3>
                <p>Category: {listing.category.name}</p>
                <p>Seller: {listing.seller.first_name}</p>
            </div>
            <hr>
        """
    return HttpResponse(html)

def listing_render_view(request):
    listings = Listing.objects.filter(is_active=True)
    return render(
        request,
        "listings/listing_features.html",
        {"listings": listings}
    )

# --- Class Based Views (Project Section 2) ---

class ListingBaseCBV(View):
    def get(self, request): # Fixed Indentation
        listings = Listing.objects.filter(is_active=True)
        return render(
            request,
            "listings/listing_features.html",
            {"listings": listings})


class ListingGenericCBV(ListView):
    model = Listing
    template_name = "listings/listing_features.html"
    context_object_name = "listings"

    def get_queryset(self): # Fixed Indentation
        return Listing.objects.filter(is_active=True)


