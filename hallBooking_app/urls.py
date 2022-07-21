from django import urls
from django.urls import path

from hallBooking_app.views import AvailabilityView, HallBookingView, HallBookingorUpdating, HallDetail, HallList

urlpatterns = [
    # path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', HallList.as_view(), name='hall'),
    path('<int:pk>/', HallDetail.as_view(), name='hall'),

    path('booking/', HallBookingView.as_view(), name='booking'),
    path('booking/<int:pk>/', HallBookingorUpdating.as_view(), name='booking'),
    path('availability/', AvailabilityView.as_view(), name='available'),
]
