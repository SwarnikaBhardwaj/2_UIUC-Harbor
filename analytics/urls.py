from django.urls import path

from .views import dashboard_data_api, dashboard_view

urlpatterns = [
    path("dashboard/", dashboard_view, name="analytics_dashboard"),
    path("api/dashboard-data/", dashboard_data_api, name="dashboard_data_api"),
]

