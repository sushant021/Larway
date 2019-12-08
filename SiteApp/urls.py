from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),


    # front end urls
    path('services/', views.ViewServices, name='view_services'),
    path('about/', views.ViewAbout, name='view_about'),
    path('contact-us/', views.viewContact, name='view_contact'),
    path('drive-with-us/', views.DriveWithUs, name='drive_with_us'),
    path('request-quote/', views.RequestQuote, name='request_quote'),
    path('fuel-surcharge/', views.FuelSurcharge, name="fuel_surcharge"),

    # backend urls
    path('dashboard/', views.UserDashBoard, name='dashboard'),
    path('view-quote-list/', views.ViewQuoteRequests, name='view_quote_requests'),
    path('view-resumes/', views.ViewDriverResumes, name='view_resumes'),
    path('view-quote/<int:id>/', views.ViewQuote, name='view_quote'),
    path('view-resume/<int:id>/', views.ViewResume, name='view_resume'),
    path('calculator/', views.FuelData, name='fuel_data'),

    # authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.UserLogout, name='logout'),

    # employee CRUD
    path('employee/add/', views.AddEmployee, name='add_employee'),
    path('employees/', views.ListEmployees, name='list_employees'),
    path('employee/delete', views.DeleteEmployee, name='delete_employees'),
    path('employee/edit', views.EditEmployee, name='edit_employees'),

    # customer CRUD
    path('customer/add/', views.AddCustomer, name='add_customer'),
    path('customers/', views.ListCustomers, name='list_customers'),
    path('customer/delete', views.DeleteCustomer, name='delete_customers'),
    path('customer/edit', views.EditCustomer, name='edit_customers'),


]
