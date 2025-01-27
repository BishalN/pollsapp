from django.contrib import admin
from django.urls import path
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.poll_list, name='home'),

    path('polls/', views.poll_list, name='poll_list'),

    path('polls/create/', views.poll_create, name='poll_create'),
    
    path('polls/<int:pk>/', views.poll_detail, name='poll_detail'),
    path('polls/<int:pk>/edit/', views.poll_edit, name='poll_edit'),
    path('polls/<int:pk>/delete/', views.poll_delete, name='poll_delete'),
    path('polls/<int:pk>/vote/', views.poll_vote, name='poll_vote'),
    path('polls/<int:pk>/results/', views.poll_results, name='poll_results'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]