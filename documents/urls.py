from django.urls import path
from .views import DocumentListCreateView, DocumentDetailView

urlpatterns = [
    # Список документов и загрузка нового
    path('', DocumentListCreateView.as_view(), name='document-list-create'),

    # Просмотр, обновление и удаление конкретного документа
    path('<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
]
