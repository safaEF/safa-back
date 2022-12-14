from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import productapi, FileUploadView, getallproduct

urlpatterns = [
    path('product/create', productapi.as_view()),
    path('product', getallproduct.as_view()),
    path('product/<int:pk>', productapi.as_view()),
    path('upload', FileUploadView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
