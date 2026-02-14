from django.urls import path
from . import views, charts
from .views import (
    listing_manual_view,
    listing_render_view,
    ListingBaseCBV,
    ListingGenericCBV,
    home_view,
    ListingDetailView,
    StudentDetailView,
    CategoryDetailView,
    StudentListView,
    CategoryListView,
    listing_search_get,
    ListingFilterCBV,
    listing_by_category_name,
    aggregation_stats,
)

urlpatterns = [
    path('', home_view, name='home'),
    # Week 2 team work
    path('manual/', listing_manual_view, name='listing_manual'),
    path('render/', listing_render_view, name='listing_render'),
    path('cbv-base/', ListingBaseCBV.as_view(), name='listing_cbv_base'),
    path('cbv-generic/', ListingGenericCBV.as_view(), name='listing_cbv_generic'),
    # Week 3 work starts here - Swarnika - detail views
    path('listings/', ListingGenericCBV.as_view(), name='listing_list'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('listings/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('search/', listing_search_get, name='listing_search_get'),
    path('filter/', views.ListingFilterCBV.as_view(), name='listing_filter_cbv'),
    path('category/<str:category_name>/listings/', listing_by_category_name, name='listing_by_category_name'),
    path('stats/', aggregation_stats, name='aggregation_stats'),
    path('api/listings/', views.listing_api_list, name='api_listings'),
    path('api/test/', views.api_mime_demo, name='api_mime_test'),
    # Week 3 - urvi added path below to create sample chart
    path('analytics/category-chart.png', charts.marketplace_distribution_chart, name='category_stats_chart'),
]
