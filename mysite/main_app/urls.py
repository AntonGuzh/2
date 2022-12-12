from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login_page'),
    path('register/', views.MyRegisterView.as_view(), name='register_page'),
    path('logout/', views.MyLogoutView.as_view(), name='logout_page'),
    path('redactor/', views.RedactorView.as_view(), name='redactor_page'),
    path('', views.MyListView, name='list_page'),
    path('download/<int:id>', views.DownloadView, name='download_page'),
    path('delete/<int:pk>', views.DeleteCvView.as_view(), name='delete_page'),
    path('redactor/<int:pk>', views.UpdateCvView.as_view(), name='update_page'),
]