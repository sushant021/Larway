from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import QuoteRequest, DriverResume, Employee, Customer
from .forms import DriverResumeForm, QuoteRequestForm, EmployeeForm, CustomerForm, FuelSurchargeForm
from django.contrib.auth import logout
from django.contrib.staticfiles.storage import staticfiles_storage

import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd
from sklearn.model_selection import train_test_split

import urllib3
import re


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


def UserLogout(request):
    logout(request)
    return redirect('/')


def UserDashBoard(request):
    return render(request, 'SiteApp/dashboard.html')


def ViewQuoteRequests(request):
    quote_requests = QuoteRequest.objects.all()
    return render(request, 'SiteApp/list_quote_requests.html', {'quote_requests': quote_requests})


def ViewDriverResumes(request):
    resumes = DriverResume.objects.all()
    return render(request, 'SiteApp/list_driver_resumes.html', {'resumes': resumes})


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


def ViewQuote(request, id):
    quote = QuoteRequest.objects.get(id=id)
    return render(request, 'SiteApp/view_quote.html', {'quote': quote})


def ViewResume(request, id):
    resume = DriverResume.objects.get(id=id)
    return render(request, 'SiteApp/view_resume.html', {'resume': resume})


def FuelSurcharge(request):
    # scrape the data off the EIA website
    data = scrape_data()
    # all region prices, the weekly U.S average and last updated date
    price_dict = data[0]
    us_price = data[1]
    last_date = data[2]

    # get_surcharge_rates takes current fuel price and a column number(2 for TL and 3 for LTL) as parameters
    tl_surcharge = get_surcharge_rate(us_price, 2)
    ltl_surcharge = get_surcharge_rate(us_price, 3)

    # output surcharge rates for the form
    form_tl_surcharge = 0
    form_ltl_surcharge = 0

    # handling the user input form
    if request.method == "POST":
        form = FuelSurchargeForm(request.POST)
        if form.is_valid():
            input_price = form.cleaned_data['input_diesel_price']
            form_tl_surcharge = get_surcharge_rate(input_price, 2)
            form_ltl_surcharge = get_surcharge_rate(input_price, 3)
        else:
            return HttpResponse("Invalid Form Request.")

    else:
        form = FuelSurchargeForm()

    context_dictionary = {'price_dict': price_dict,
                          'last_date': last_date,
                          'us_price': us_price,
                          'tl_surcharge': tl_surcharge,
                          'ltl_surcharge': ltl_surcharge,
                          'form_tl_surcharge': form_tl_surcharge,
                          'form_ltl_surcharge': form_ltl_surcharge,
                          'form': form}

    return render(request, 'SiteApp/fuel_surcharge.html', context_dictionary)


def ListEmployees(request):
    employees = Employee.objects.all()
    return render(request, 'SiteApp/list_employees.html', {'employees': employees})


def AddEmployee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = EmployeeForm()
        return render(request, 'SiteApp/add_employee.html', {'form': form})


def EditEmployee(request, id):
    pass


def DeleteEmployee(request, id):
    pass


def ListCustomers(request):
    customers = Customer.objects.all()
    return render(request, 'SiteApp/list_customers.html', {'customers': customers})


def AddCustomer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid Form')
    else:
        form = CustomerForm()
        return render(request, 'SiteApp/add_customer.html', {'form': form})


def EditCustomer(request, id):
    pass


def DeleteCustomer(request, id):
    pass


# takes current fuel price in us gallons and a column number to return TL and LTL surcharge rates
# based on L2011 schedule of Larway
# column number is either 2 or 3 , 2 is for TL and 3 is for LTL
def get_surcharge_rate(fuel_price, col_num):
    try:
        p = staticfiles_storage.path('data/surcharge_table.csv')
        df = pd.read_csv(p)
    except:
        return False

    # get the data
    if col_num == 2:
        x = df.iloc[80:, 1].values
        y = df.iloc[80:, col_num].values
    elif col_num == 3:
        x = df.iloc[85:, 1].values
        y = df.iloc[85:, col_num].values
    else:
        return False

    # reshape the data
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)

    # split training data and test data
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=4)

    # train the model
    model_tl = LinearRegression().fit(x_train, y_train)
    y_pred = model_tl.predict(np.array(fuel_price).reshape(1, -1))

    # multiply by 100 and limit floating points to 3 decimal places
    result = y_pred[0][0] * 100
    result = round(result, 3)

    # return the result
    return result


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
