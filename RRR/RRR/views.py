from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import csv
from re import search
import pandas as pd

# file=pd.read_csv('ratings.csv')
# for i in range(len(file)):
#     file.loc[i,'1']=0
#     file.loc[i,'2']=0
#     file.loc[i,'3']=0
#     file.loc[i,'4']=0
#     file.loc[i,'5']=0
#     file.loc[i,'Total Vote']=0
#     file.loc[i,'Rating']=0.0

# file.to_csv('ratings.csv',index=False)

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
    headers = [col for col in reader.fieldnames if col!='Unnamed: 0']
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

    final.sort(key=lambda x:x[4],reverse=True)
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
        headers = [col for col in reader.fieldnames if col!='Unnamed: 0']
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

    final.sort(key=lambda x:x[4],reverse=True)
    return render(request, 'dashboard.html', {'data':final, 'headers' : headers})

def calculate_rating(line):
    csv=pd.read_csv('ratings.csv',sep=',')
    row=csv.loc[line]
    print(row)
    curr_rating=(float(row[2])*5+float(row[3])*4+float(row[4])*3+float(row[5])*2+float(row[6])*1)/float(row[1])
    print(round(curr_rating,2))
    return round(curr_rating,2)
    csv.loc[line,'Rating']=curr_rating
    csv.to_csv("ratings.csv", index=False)
    
def res_suggestion(line):
    csv_res = open('restaurant.csv', 'r')
    csv_pd=pd.read_csv('restaurant.csv')
    reader = csv.DictReader(csv_res)
    cuisines=(csv_pd.loc[line]['Cuisines']).split(',')
    print(cuisines)
    final=[]
    for cuisine in cuisines:
        temp=[]
        for row in reader:
            if(cuisine in row['Cuisines']):
                temp.append(row)
        final.append(temp)
    
    print(final)


def review(request):
    final=[]
    rating_file = open('ratings.csv', 'r')

    reader = csv.DictReader(rating_file)
    for row in reader:
        final.append(row['Restaurant_Name'])
    rating_file.close()
    
    file=pd.read_csv('ratings.csv',sep=',')


    if(request.method=="POST"):
        res=request.POST.get('restaurant')
        rate=request.POST.get('rating')
        print("Restaurant Selected is : ",res)
        print("Rating : ",rate)

        rating_file = open('ratings.csv', 'r')

        reader = csv.DictReader(rating_file)
        

        for row in reader:
            # print(row)
            if(res==row['Restaurant_Name']):
                # print(reader.line_num)
                line=reader.line_num
                value=float(row[rate])
                total=float(row['Total Vote'])
                
        print("Line no is : ",line)
        file.loc[line-2,rate]=value+1.0
        file.loc[line-2,'Total Vote']=total+1.0
        file.to_csv("ratings.csv", index=False)
        print("No of {} star rating is : {}".format(rate,file.loc[line-2,rate]))
        print("Total ratings : {}".format(file.loc[line-2,'Total Vote']))
        curr_rating=calculate_rating(line-2)
        file.loc[line-2,'Rating']=curr_rating
        file.to_csv("ratings.csv", index=False)
        
        restaurant_file = pd.read_csv('restaurant.csv',sep=',')
        restaurant_file.loc[line-2,'Rate']=curr_rating
        restaurant_file.to_csv("restaurant.csv", index=False)

        list=res_suggestion(line-2)


    return render(request,'review.html',{'data':final})