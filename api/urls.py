from rest_framework import routers
from . import views
from django.urls import path, include

app_name = 'api'

router = routers.DefaultRouter()
router.register('invoices', views.InvoiceView)
router.register('schedules', views.ScheduleView)
router.register('customers', views.CustomerView)
router.register('departments', views.DepartmentView)
router.register('employees', views.EmployeeView)


urlpatterns = [
    path('', include(router.urls))
]
