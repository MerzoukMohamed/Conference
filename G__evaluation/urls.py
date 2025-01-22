from django.urls import path
from G__evaluation import views




urlpatterns = [
    path('Update/<str:pk>',views.Update,name='Update'),



    	]