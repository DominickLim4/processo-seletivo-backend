from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vagas.views import VagaViewSet
from django.conf import settings
from django.conf.urls.static import static

# Configuração do Router
# GET /vagas/ (Lista)
# POST /vagas/ (Criar)
# GET /vagas/{id}/ (Detalhe)
# PUT /vagas/{id}/ (Atualiza)
# DELETE /vagas/{id}/ (Remove)
router = DefaultRouter()
router.register(r'vagas', VagaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

# Se a url começar com midia procurar na pasta o arquivo (Apenas Desenvolvimento)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa
