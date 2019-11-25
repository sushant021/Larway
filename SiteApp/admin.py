from django.contrib import admin
from . models import Department, Employee, Customer


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', ]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', ]


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'key_person_name',
                    'key_person_contact', 'email', ]
