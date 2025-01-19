"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from api.requests import backend_csrf, backend_login, backend_logout
from django.contrib import admin
from django.urls import path

# from api.views import test , adminview, instructorview, groupview
from api.requests import (
    backend_login,
    backend_logout,
    backend_csrf,
    crud_group,
    crud_instructor,
    crud_schedule,
    crud_institution,
    handle_input,
    calculate_for_schedule,
    get_calculate_progress_for_schedule,
    get_results_for_schedule,
    change_result_access_by_schedule,
    get_own_info,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", backend_login),
    path("logout/", backend_logout),
    path("csrf/", backend_csrf),
    path("group/", crud_group),
    path("instructor/", crud_instructor),
    path("schedule/", crud_schedule),
    path("institution/", crud_institution),
    path("input/", handle_input),
    path("calculate/", calculate_for_schedule),
    path("progress/", get_calculate_progress_for_schedule),
    path("results/", get_results_for_schedule),
    path("result_access/", change_result_access_by_schedule),
    path("info/", get_own_info),
    # path("test/<str:id>/", test),
]
