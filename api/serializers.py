from SiteApp.models import Invoice, Schedule, Customer, Employee, Department
from rest_framework import serializers


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    employees = serializers.StringRelatedField(many=True)

    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class ScheduleSerializer(serializers.ModelSerializer):
    schedule_data = serializers.StringRelatedField(many=True)

    class Meta:
        model = Schedule
        fields = ['name', 'schedule_data']
