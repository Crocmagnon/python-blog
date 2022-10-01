from django.urls import path

from attachments import views

app_name = "attachments"

urlpatterns = [
    path("<int:pk>/original/", views.get_original, name="original"),
    path("<int:pk>/processed/", views.get_processed, name="processed"),
]
