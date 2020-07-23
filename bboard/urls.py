from django.urls import path
from .views import BbIndexView, BbByRubricView, BbDetailView, BbAddView, BbEditView, BbDeleteView

urlpatterns = [
    path('add/', BbAddView.as_view(), name='add'),
    path('update/<int:pk>', BbEditView.as_view(), name='update'),
    path('delete/<int:pk>', BbDeleteView.as_view(), name='delete'),
    path('', BbIndexView.as_view(), name='index'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    #path('add/', BbCreateView.as_view(), name='add'),
]