from django.urls import path
from django.contrib.auth.decorators import login_required
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
    path("signup/", views.signup_view, name="signup"),

    path('manual/', login_required(listing_manual_view), name='listing_manual'),
    path('render/', login_required(listing_render_view), name='listing_render'),

    path('cbv-base/', login_required(ListingBaseCBV.as_view()), name='listing_cbv_base'),
    path('cbv-generic/', login_required(ListingGenericCBV.as_view()), name='listing_cbv_generic'),

    path('listings/', login_required(ListingGenericCBV.as_view()), name='listing_list'),
    path('listings/<int:pk>/', login_required(ListingDetailView.as_view()), name='listing_detail'),

    path('students/', login_required(StudentListView.as_view()), name='student_list'),
    path('students/<int:pk>/', login_required(StudentDetailView.as_view()), name='student_detail'),

    path('categories/', login_required(CategoryListView.as_view()), name='category_list'),
    path('categories/<int:pk>/', login_required(CategoryDetailView.as_view()), name='category_detail'),

    path('category/<str:category_name>/listings/',
         login_required(listing_by_category_name),
         name='listing_by_category_name'),

    path('search/', login_required(listing_search_get), name='listing_search_get'),
    path('filter/', login_required(views.ListingFilterCBV.as_view()), name='listing_filter_cbv'),
    path('stats/', login_required(aggregation_stats), name='aggregation_stats'),

    path('api/listings/', login_required(views.listing_api_list), name='api_listings'),
    path('api/test/', login_required(views.api_mime_demo), name='api_mime_test'),

    path('api/listings-per-category/',
         login_required(views.listings_per_category_api),
         name='api_listings_per_category'),
    # 3.1 (2/26)
    path('api/public/listings-per-category/',
        views.listings_per_category_api,
        name='public_api_listings_per_category'),

    path('api/listings-avg-price-per-category/',
         login_required(views.listings_avg_price_per_category_api),
         name='api_listings_avg_price_per_category'),

    path('api/external-demo/',
         login_required(views.external_api_demo),
         name='api_external_demo'),

    path('export/students/csv/',
         login_required(views.export_students_csv),
         name='export_students_csv'),

    path('export/students/json/',
         login_required(views.export_students_json),
         name='export_students_json'),

    path('reports/',
         login_required(views.reports_view),
         name='reports'),

    path('charts/categories/',
         login_required(views.category_chart_view),
         name='category_chart'),

    path('charts/price-line/',
         login_required(views.price_line_chart_view),
         name='price_line_chart'),

    path('analytics/category-chart.png',
         login_required(charts.marketplace_distribution_chart),
         name='category_stats_chart'),
]
