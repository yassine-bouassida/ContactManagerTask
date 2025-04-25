from django.urls import path
from contacts.views import contact_list, contact_create, contact_delete

app_name = "contacts"
urlpatterns = [
    path("", contact_list, name="list"),
    path("create/", contact_create, name="create"),
    path("<int:pk>/delete/", contact_delete, name="delete"),
]
