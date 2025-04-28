from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.property_list, name='api-property-list'),
    path('<int:pk>/', api_views.property_detail, name='api-property-detail'),
    

    path('search/', api_views.property_search, name='api-property-search'),
    path('my-properties/', api_views.my_properties, name='api-my-properties'),
]
