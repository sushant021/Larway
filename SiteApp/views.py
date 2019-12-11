from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import QuoteRequest, DriverResume, Employee, Customer, FuelData, FuelSurcharge, Department, Invoice , ScheduleData, Schedule
from .forms import DriverResumeForm, QuoteRequestForm, EmployeeForm, InvoiceForm, CustomerForm, FuelSurchargeForm, FuelDataForm , ScheduleForm,DepartmentForm
from django.contrib.auth import logout
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.decorators import login_required
import openpyxl

import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.model_selection import train_test_split

import urllib3
import re

import csv

# front end views
# -------------------------------


def index(request):
    return render(request, 'SiteApp/index.html')


def ViewServices(request):
    return render(request, 'SiteApp/services.html')


def ViewAbout(request):
    return render(request, 'SiteApp/about.html')


def viewContact(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = QuoteRequestForm()
        return render(request, 'SiteApp/contact_us.html', {'form': form})


def DriveWithUs(request):
    if request.method == "POST":
        form = DriverResumeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = DriverResumeForm()
        return render(request, 'SiteApp/drive_with_us.html', {'form': form})


def RequestQuote(request):
    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = QuoteRequestForm()
        return render(request, 'SiteApp/quote_request.html', {'form': form})


# log user out
def UserLogout(request):
    logout(request)
    return redirect('/')

# Backend views
# -------------------------------------------------
@login_required
def UserDashBoard(request):
    return render(request, 'SiteApp/dashboard.html')


@login_required
def ViewQuoteRequests(request):
    quote_requests = QuoteRequest.objects.all()
    return render(request, 'SiteApp/list_quote_requests.html', {'quote_requests': quote_requests})


@login_required
def ViewQuote(request, id):
    quote = QuoteRequest.objects.get(id=id)
    return render(request, 'SiteApp/view_quote.html', {'quote': quote})


@login_required
def ViewDriverResumes(request):
    resumes = DriverResume.objects.all()
    return render(request, 'SiteApp/list_driver_resumes.html', {'resumes': resumes})


@login_required
def ViewResume(request, id):
    resume = DriverResume.objects.get(id=id)
    return render(request, 'SiteApp/view_resume.html', {'resume': resume})


@login_required
def FuelSurcharge(request):
    # scrape the data off the EIA website
    data = scrape_data()
    # all region prices, the weekly U.S average and last updated date
    price_dict = data[0]
    us_price = data[1]
    last_date = data[2]

    # get_surcharge_rates takes current fuel price and a column number(2 for TL and 3 for LTL) as parameters
    
    schedules = Schedule.objects.all()
    schedule_dict = {}
    for schedule in schedules:
        tl_surcharge = get_surcharge_rate(schedule,us_price,2)
        ltl_surcharge = get_surcharge_rate(schedule,us_price, 3)
        schedule_dict[schedule] = [tl_surcharge,ltl_surcharge]
    

    # tl_surcharge = get_surcharge_rate(us_price, 2)
    # ltl_surcharge = get_surcharge_rate(us_price, 3)

    # output surcharge rates for the form
    form_result_dict = {}

    # handling the user input form
    if request.method == "POST":
        form = FuelSurchargeForm(request.POST)
        if form.is_valid():
            input_price = form.cleaned_data['input_diesel_price']
            # schedule = form.cleaned_data['schedule']
            form_result_dict = {}
            for schedule in schedules:
                 form_tl_surcharge = get_surcharge_rate(schedule, input_price, 2)
                 form_ltl_surcharge = get_surcharge_rate(schedule, input_price, 3)
                 form_result_dict[schedule] = [form_tl_surcharge, form_ltl_surcharge]
           
        else:
            return HttpResponse("Invalid Form Request.")

    else:
        form = FuelSurchargeForm()

    context_dictionary = {'price_dict': price_dict,
                          'last_date': last_date,
                          'us_price': us_price,
                        #   'tl_surcharge': tl_surcharge,
                        #   'ltl_surcharge': ltl_surcharge,
                            'schedule_dict':schedule_dict,
                          'form_result_dict':form_result_dict,
                          'form_result_dict_len':len(form_result_dict),
                          'form': form}

    return render(request, 'SiteApp/fuel_surcharge.html', context_dictionary)


@login_required
def ListDepartments(request):
    departments = Department.objects.all()
    return render(request, 'SiteApp/list_departments.html', {'departments': departments})

@login_required
def AddDepartment(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_departments')
        else:
            error = "Invalid form submission"
            return render(request,'SiteApp/add_department.html',{'form':form,'error':error})
    else:
        form = DepartmentForm()
        return render(request, 'SiteApp/add_department.html', {'form': form})


@login_required
def ViewDepartment(request, id):
    department = Department.objects.get(id=id)
    employees = Employee.objects.filter(department= department)
    num_employees = len(employees)
    return render(request, 'SiteApp/view_department.html', {'department': department,'employees':employees,'num_employees':num_employees})


@login_required
def EditDepartment(request, id):
    template = 'SiteApp/edit_department.html'
    department = Department.objects.get(id=id)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('list_departments')
    context = {"form": form,'department':department}
    return render(request, template, context)

@login_required
def DeleteDepartment(request, id):
    department = Department.objects.get(id=id)
    department.delete()
    return redirect('list_departments')


@login_required
def ListInvoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'SiteApp/list_invoices.html', {'invoices': invoices})


@login_required
def AddInvoice(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_invoices')
        else:
            error = "Invalid form submission"
            return render(request, 'SiteApp/add_invoice.html', {'form': form, 'error': error})
    else:
        form = InvoiceForm()
        return render(request, 'SiteApp/add_invoice.html', {'form': form})



@login_required
def ViewInvoice(request, id):
    invoice = Invoice.objects.get(id = id)
    return render(request, 'SiteApp/view_invoice.html', {'invoice': invoice})


@login_required
def DeleteInvoice(request, id):
    invoice = Invoice.objects.get(id=id)
    invoice.delete()
    return redirect('list_invoices')


@login_required
def EditInvoice(request, id):
    template = 'SiteApp/edit_invoice.html'
    invoice = Invoice.objects.get(id=id)
    form = InvoiceForm(request.POST or None, instance=invoice)
    if form.is_valid():
        form.save()
        return redirect('list_invoices')
    context = {"form": form, 'invoice': invoice}
    return render(request, template, context)

@login_required
def ListEmployees(request):
    employees = Employee.objects.all()
    return render(request, 'SiteApp/list_employees.html', {'employees': employees})

@login_required
def ViewEmployee(request,id):
    employee = Employee.objects.get(employee_id=id)
    return render(request,'SiteApp/view_employee.html',{'employee':employee})

@login_required
def AddEmployee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_employees')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = EmployeeForm()
        return render(request, 'SiteApp/add_employee.html', {'form': form})


@login_required
def EditEmployee(request, id):
    template = 'SiteApp/edit_employee.html'
    employee = Employee.objects.get(employee_id=id)
    form = EmployeeForm(request.POST or None, instance=employee)
    if form.is_valid():
        form.save()
        return redirect('list_employees')
    context = {"form": form, 'employee': employee}
    return render(request, template, context)


@login_required
def DeleteEmployee(request, id):
    pass


@login_required
def ListCustomers(request):
    customers = Customer.objects.all()
    return render(request, 'SiteApp/list_customers.html', {'customers': customers})

@login_required
def ViewCustomer(request,id):
    customer = Customer.objects.get(id=id)
    return render(request,'SiteApp/view_customer.html',{'customer':customer})


@login_required
def AddCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_customer')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = CustomerForm()
        return render(request, 'SiteApp/add_customer.html', {'form': form})


@login_required
def EditCustomer(request, id):
    template = 'SiteApp/edit_customer.html'
    customer = Customer.objects.get(id=id)
    form = CustomerForm(request.POST or None, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('list_customers')
    context = {"form": form, 'customer': customer}
    return render(request, template, context)


@login_required
def DeleteCustomer(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    return redirect('list_customers')


@login_required
def FuelData(request):
    if request.method == "POST":
        form = FuelDataForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # calculate values
            context_dict = get_fuel_values(cd)
            flag = True
            context_dict.update({'flag': flag, 'form': form})

        else:
            return HttpResponse("Invalid form submission.")
    else:
        form = FuelDataForm()
        context_dict = {'form': form}

    return render(request, 'SiteApp/fuel_data.html', context_dict)

@login_required
def ListSchedules(request):
    schedules = Schedule.objects.all()
    return render(request,'SiteApp/list_schedules.html',{'schedules':schedules})

@login_required
def ViewSchedule(request,id):
    schedule = Schedule.objects.get(id = id)
    schedule_data = ScheduleData.objects.filter(schedule = schedule)
    return render(request, 'SiteApp/view_schedule.html',{'schedule':schedule, 'schedule_data':schedule_data})

@login_required
def DeleteSchedule(request,id):
    schedule = Schedule.objects.get(id = id)
    schedule.delete()
    return redirect('list_schedules') 

@login_required
def EditSchedule(request,id):
    template = 'SiteApp/edit_schedule.html'
    schedule = Schedule.objects.get(id=id)
    form = ScheduleForm(request.POST or None, instance=schedule)
    if form.is_valid():
        form.save()
        return redirect('list_schedules')
    context = {"form": form, 'schedule': schedule}
    return render(request, template, context)

@login_required
def AddSchedule(request):
    error = ""
    if request.method == "POST":
        form = ScheduleForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data["name"]
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                error = 'File is not CSV type'
                return render(request,'SiteApp/add_schedule.html',{'form':form,'error':error})
            
            #check if schedule name already exists
            schedules = Schedule.objects.all()
            names = []
            for item in schedules:
                names.append(item.name)

            data_saved = False
            if name in names:
                error = "A schedule with that name already exists"
            else:
                data_saved = StoreScheduleData(name,csv_file)
            
            if data_saved:
                return redirect('list_schedules')

            
        else:
            error = "Invalid form submission. Schedule not saved."
    else:
        form = ScheduleForm()
    
    return render(request, 'SiteApp/add_schedule.html', {'form':form,'error':error})

# Extra helper functions
# -----------------------------------------------------


# takes current fuel price in us gallons and a column number to return TL and LTL surcharge rates
# based on L2011 schedule of Larway
# column number is either 2 or 3 , 2 is for TL and 3 is for LTL


def get_surcharge_rate(schedule, fuel_price, col_num):
    try:
        schedule_data = ScheduleData.objects.filter(schedule=schedule).get(fuel_price = round(fuel_price,2))
        
        tl_surcharge = schedule_data.tl_surcharge_percent
        ltl_surcharge = schedule_data.ltl_surcharge_percent
        if col_num == 2:
            return round(tl_surcharge*100, 3)
        elif col_num == 3:
            return round(ltl_surcharge*100,3)
        else:
            return "Wrong column number"

    #create a data frame from the list 
    # df = pd.DataFrame(my_list, columns=['Fuel Price', 'TL Surcharge','LTL Surcharge'])
        # p = staticfiles_storage.path('data/surcharge_table.csv')
        # df = pd.read_csv(p)
    except:
          return "No Data."

    # get the data
    # if col_num == 2:
    #     x = df.iloc[80:, 1].values
    #     y = df.iloc[80:, col_num].values
    # elif col_num == 3:
    #     x = df.iloc[85:, 1].values
    #     y = df.iloc[85:, col_num].values
    # else:
    #     return False

    # # reshape the data
    # x = np.array(x).reshape(-1, 1)
    # y = np.array(y).reshape(-1, 1)

    # # split training data and test data
    # x_train, x_test, y_train, y_test = train_test_split(
    #     x, y, test_size=0.2, random_state=4)

    # # train the model
    # model_tl = LinearRegression().fit(x_train, y_train)
    # y_pred = model_tl.predict(np.array(fuel_price).reshape(1, -1))

    # # multiply by 100 and limit floating points to 3 decimal places
    # result = y_pred[0][0] * 100
    # result = round(result, 3)

    # # return the result
    # return result


def scrape_data():
    http = urllib3.PoolManager()
    r = http.request(
        'GET', 'https://www.eia.gov/petroleum/gasdiesel/includes/gas_diesel_rss.xml')
    content = r.data.decode('utf-8')

    result = content.find('On-Highway Diesel Fuel Retail Price')

    floats = re.findall(r'[+-]?\d+\.?\d*\.\d+', content[result:])

    regions = ['U.S.', 'East Coast', 'New England', 'Central Atlantic', 'Lower Atlantic', 'Midwest',
               'Gulf Coast', 'Rocky Mountain', 'West Coast', 'West Coast less California', 'California']
    price_dict = {}
    for i, region in enumerate(regions):
        price_dict[region] = floats[i]

    date_result = content.find('Data For')
    last_date = content[date_result+9:date_result+16]

    # floats[0] is the average U.S. price, last_date is the last update date.
    return [price_dict, float(floats[0]), last_date]


# inputs cleaned data from a form of caluclator and returns all the values in a dictionary
def get_fuel_values(cd):
    fsc_percent = cd['surcharge_percentage']
    fsc_dollar = cd['surcharge_per_mile']
    miles = cd['miles']
    rpm = cd['rate_per_mile']
    line_haul = cd['linehaul_amount']
    fsc_amt = cd['surcharge_amount']
    total = cd['total_amount']

    # if fsc_percent == 0:
    #     fsc_percent = 0.0

    # if fsc_dollar == 0:
    #     fsc_dollar = 0.0

    # if miles == 0:
    #     miles = 0.0

    # if rpm == 0:
    #     rpm = 0.0

    # if line_haul == 0:
    #     line_haul = 0.0

    # if fsc_amt == 0:
    #     fsc_amt = 0.0

    # if total == 0:
    #     total = 0.0

    if line_haul == 0:
        if rpm != 0 and miles != 0:
            line_haul = rpm * miles
        if total != 0 and fsc_amt != 0:
            line_haul = total - fsc_amt

    if fsc_percent != 0 and fsc_dollar != 0:
        fsc_amt = miles * fsc_dollar
    elif fsc_dollar != 0:
        fsc_amt = miles * fsc_dollar
    elif fsc_percent != 0:
        fsc_amt = line_haul * (fsc_percent/100)

    if total == 0:
        if fsc_amt != 0 and line_haul != 0:
            total = fsc_amt + line_haul

    if fsc_percent == 0:
        if fsc_amt != 0 and line_haul != 0:
            fsc_percent = (fsc_amt/line_haul)

    if fsc_dollar == 0:
        if fsc_amt != 0 and miles != 0:
            fsc_dollar = fsc_amt / miles

    if fsc_amt != 0 and total != 0:
        if fsc_amt != 0 and total != 0:
            fsc_percent = (fsc_amt / (total-fsc_amt)) * 100

    if line_haul == 0:
        if total != 0 and fsc_amt != 0:
            line_haul = total - fsc_amt

    if rpm == 0:
        if line_haul != 0 and miles != 0:
            rpm = line_haul / miles

    if miles == 0:
        if line_haul != 0 and rpm != 0:
            miles = line_haul / rpm

    if total != 0 and fsc_percent !=0:
        fsc_amt = (total * (fsc_percent /100))/ (1+(fsc_percent/100))
        line_haul = total - fsc_amt

    context_dict = {'fsc_amt': round(fsc_amt, 3),
                    'line_haul': round(line_haul, 3),
                    'fsc_percent': round(fsc_percent, 3),
                    'fsc_dollar': round(fsc_dollar, 3),
                    'total': round(total, 3),
                    'miles': round(miles, 3),
                    'rpm': round(rpm, 3),
                    }

    return context_dict


def StoreScheduleData(name,csv_file):
    new_schedule = Schedule.objects.create(name=name)
    new_schedule.save()
    schedule = Schedule.objects.get(name=name)

    data = csv_file.read().decode('utf-8')
    lines = data.split("\n")
    lines = lines[:-1]

    for line in lines[1:]:
        fields = line.split(",")
        schedule_data = ScheduleData(
            schedule=schedule, fuel_price=fields[1], tl_surcharge_percent=fields[2], ltl_surcharge_percent=fields[3])
        schedule_data.save()
    
    return True
