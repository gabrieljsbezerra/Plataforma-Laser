from django.urls import path
from .views import ClientCreateView, ClientDeleteView, ClientListView, ClientReactivateView, ClientUpdateView
app_name = "clients"
urlpatterns = [path("", ClientListView.as_view(), name="list"), path("novo/", ClientCreateView.as_view(), name="create"), path("<int:pk>/editar/", ClientUpdateView.as_view(), name="update"), path("<int:pk>/excluir/", ClientDeleteView.as_view(), name="delete"), path("<int:pk>/reativar/", ClientReactivateView.as_view(), name="reactivate")]
