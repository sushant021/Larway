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
    path('quotes/', views.ViewQuoteRequests, name='view_quote_requests'),
    path('resumes/', views.ViewDriverResumes, name='view_resumes'),
    path('quotes/<int:id>/', views.ViewQuote, name='view_quote'),
    path('resumes/<int:id>/', views.ViewResume, name='view_resume'),
    path('calculator/', views.FuelData, name='fuel_data'),


    # authentication
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.UserLogout, name='logout'),

    # department CRUD
    path('departments/', views.ListDepartments, name="list_departments"),
    path('departments/<int:id>/', views.ViewDepartment, name="view_department"),
    path('departments/add/', views.AddDepartment, name="add_department"),
    path('departments/edit/<int:id>/',
         views.EditDepartment, name="edit_department"),
    path('departments/delete/<int:id>/',
         views.DeleteDepartment, name="delete_department"),

    # employee CRUD
    path('employees/add/', views.AddEmployee, name='add_employee'),
    path('employees/', views.ListEmployees, name='list_employees'),
    path('employees/<int:id>/', views.ViewEmployee, name='view_employee'),
    path('employees/delete/<int:id>',
         views.DeleteEmployee, name='delete_employees'),
    path('employees/edit/<int:id>', views.EditEmployee, name='edit_employees'),

    # customer CRUD
    path('customers/add/', views.AddCustomer, name='add_customer'),
    path('customers/', views.ListCustomers, name='list_customers'),
    path('customers/<int:id>/', views.ViewCustomer, name='view_customer'),
    path('customers/delete/<int:id>',
         views.DeleteCustomer, name='delete_customers'),
    path('customers/edit/<int:id>', views.EditCustomer, name='edit_customers'),

    # invoice CRUD
    path('invoices/', views.ListInvoices, name="list_invoices"),
    path('invoices/<str:invoice_num>/',
         views.ViewInvoice, name="view_invoice"),
    path('invoices/add/', views.AddInvoice, name="add_invoice"),
    path('invoices/edit/<str:invoice_num>/',
         views.EditInvoice, name="edit_invoice"),
    path('invoices/delete/<str:invoice_num>/',
         views.DeleteInvoice, name="delete_invoice"),

    # schedules CRUD
    path('schedules/add/', views.AddSchedule, name="add_schedule"),
    path('schedule/<int:id>/', views.ViewSchedule, name="view_schedule"),
    path('schedules/', views.ListSchedules, name="list_schedules"),
    path('schedules/delete/<int:id>/',
         views.DeleteSchedule, name="delete_schedule"),
    path('schedule/edit/<int:id>/', views.EditSchedule, name="edit_schedule"),

]
