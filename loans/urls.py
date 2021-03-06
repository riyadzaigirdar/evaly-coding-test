from loans import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'loans'

router = DefaultRouter()

router.register("loan", views.LoanView, basename="loan")

urlpatterns = [
    path('', include(router.urls)),
    path('get-excel-for-loans', views.get_excel_for_loans)
]
