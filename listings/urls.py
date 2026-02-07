from django.urls import path
from .views import (
   listing_manual_view,
   listing_render_view,
   ListingBaseCBV,
   ListingGenericCBV,
)

urlpatterns = [
   path('manual/', listing_manual_view, name='listing_manual'),
   path('render/', listing_render_view, name='listing_render'),
   path('cbv-base/', ListingBaseCBV.as_view(), name='listing_cbv_base'),
   path('cbv-generic/', ListingGenericCBV.as_view(), name='listing_cbv_generic'),
]
