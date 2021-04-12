from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import csv
from re import search
import pandas as pd
# data=[]
# final=[]
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'login.html')

def signup(request):
    return render(request,'signup.html')

def dashboard(request):
    print('Dashboard')
    # global data,final
    final=[]
    csv_fp = open('restaurant.csv', 'r')

    reader = csv.DictReader(csv_fp)
    headers = [col for col in reader.fieldnames]
    for row in reader:
        data=[]
        data.append(row['Restaurant_Name'])
        data.append(row['Address'])
        data.append(row['Online Order'])
        data.append(row['Book_Table'])
        data.append(row['Rate'])
        data.append(row['Phone'])
        data.append(row['Restaurant_Type'])
        data.append(row['Famou_ Dishes'])
        data.append(row['Cuisines'])
        data.append(row['Approx_cost(for two people)'])
        data.append(row['Type'])
        final.append(data)
    if request.method=='POST':
        print("Searching !!!")
        find=request.POST['search']
        print(find)
        csv_fp = open('restaurant.csv', 'r')
        reader = csv.DictReader(csv_fp)
        final=[]
        for row in reader:
            if(find in row['Restaurant_Name']):
                data=[]
                data.append(row['Restaurant_Name'])
                data.append(row['Address'])
                data.append(row['Online Order'])
                data.append(row['Book_Table'])
                data.append(row['Rate'])
                data.append(row['Phone'])
                data.append(row['Restaurant_Type'])
                data.append(row['Famou_ Dishes'])
                data.append(row['Cuisines'])
                data.append(row['Approx_cost(for two people)'])
                data.append(row['Type'])
                final.append(data)
                # print(row['Number'])

    return render(request, 'dashboard.html', {'data':final, 'headers' : headers})

def filter(request):
    if(request.method=='POST'):
        
        order = request.POST.get("online_order", None)
        book_table = request.POST.get("book_table", None)
        rate = request.POST.get("Rate", None)
        type = request.POST.get("type", None)
        lprice = request.POST.get("price", None)
        print("Order : ",order)
        print("Book table : ",book_table)
        print("Rating : ",rate)
        print("Typing : ",type)
        print("Price : ",lprice)
        if(lprice!=None):
            uprice=int(lprice)+200
        else:
            uprice=1000
            lprice=0
        if(order==None):
            order=""
        if(book_table==None):
            book_table="" 
        if(rate==None):
            rate='0.0'   
        if(type==None):
            type=''         
        csv_fp = open('restaurant.csv', 'r')
        reader = csv.DictReader(csv_fp)
        headers = [col for col in reader.fieldnames]
        final=[]
        for row in reader:
            if(order in row['Online Order'] and book_table in row['Book_Table'] and float(rate) <= float(row['Rate']) and type in row['Restaurant_Type'] and int(lprice)<= int(row['Approx_cost(for two people)'])<int(uprice)):
                data=[]
                data.append(row['Restaurant_Name'])
                data.append(row['Address'])
                data.append(row['Online Order'])
                data.append(row['Book_Table'])
                data.append(row['Rate'])
                data.append(row['Phone'])
                data.append(row['Restaurant_Type'])
                data.append(row['Famou_ Dishes'])
                data.append(row['Cuisines'])
                data.append(row['Approx_cost(for two people)'])
                data.append(row['Type'])
                final.append(data)

    return render(request, 'dashboard.html', {'data':final, 'headers' : headers})

def review(request):
    final=[]
    csv_fp = open('restaurant.csv', 'r')

    reader = csv.DictReader(csv_fp)
    for row in reader:
        final.append(row['Restaurant_Name'])
    
    if(request.method=="POST"):
        res=request.POST.get('restaurant')
        rate=request.POST.get('rating')
    
        print(res,rate)
        file=pd.read_csv('ratings.csv',sep=',')

        a=file[file['Restaurant_Name'==res]]
        # a.to_csv('ratings.csv')
        print(a)



    return render(request,'review.html',{'data':final})