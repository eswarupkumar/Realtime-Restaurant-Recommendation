from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import csv
import math
# import datetime
from datetime import datetime, timedelta
from re import search
import pandas as pd

user_row = []
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
    return render(request, 'home.html')


def login(request):
    global user_row
    user_row = []
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']
        print("Hit")
        user_data = pd.read_csv('user_data.csv')
        for row in range(len(user_data)):
            if(user_data.loc[row, 'email'] == email):
                print(str(user_data.loc[row, 'password']))
                if(user_data.loc[row, 'password'] == password):
                    # print(row+2)
                    # user_row=row+2
                    user_row.append(user_data.loc[row, 'name'])
                    user_row.append(user_data.loc[row, 'email'])
                    user_row.append(row)
                    return redirect('/dashboard')
                else:
                    return render(request, 'login.html', {'message': 'Please check your password'})

        return render(request, 'login.html', {'Issue': True})

    return render(request, 'login.html')


def signup(request):
    if(request.method == "POST"):
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user_data = pd.read_csv('user_data.csv')

        for row in range(len(user_data)):
            if(user_data.loc[row, 'email'] == email):
                return render(request, 'signup.html', {'Issue': True})

        i = len(user_data)+1
        user_data.loc[i, 'name'] = name
        user_data.loc[i, 'email'] = email
        user_data.loc[i, 'password'] = str(password)
        # user_data.loc[i,'history']=[]

        user_data.to_csv("user_data.csv", index=False)
        return redirect('/login')

    return render(request, 'signup.html')


def dashboard(request):
    global user_row
    print('Dashboard')
    # global data,final
    final = []
    csv_fp = open('restaurant.csv', 'r')

    reader = csv.DictReader(csv_fp)
    headers = [col for col in reader.fieldnames if col != 'Unnamed: 0']
    for row in reader:
        data = []
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
    if request.method == 'POST':
        print("Searching !!!")
        find = request.POST['search']
        print(find)
        csv_fp = open('restaurant.csv', 'r')
        reader = csv.DictReader(csv_fp)
        final = []
        for row in reader:
            if(find in row['Restaurant_Name']):
                data = []
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

    final.sort(key=lambda x: x[4], reverse=True)
    print(user_row)
    return render(request, 'dashboard.html', {'data': final, 'headers': headers, 'name': user_row[0]})


def filter(request):
    if(request.method == 'POST'):

        order = request.POST.get("online_order", None)
        book_table = request.POST.get("book_table", None)
        rate = request.POST.get("Rate", None)
        type = request.POST.get("type", None)
        lprice = request.POST.get("price", None)
        print("Order : ", order)
        print("Book table : ", book_table)
        print("Rating : ", rate)
        print("Typing : ", type)
        print("Price : ", lprice)
        if(lprice != None):
            uprice = int(lprice)+200
        else:
            uprice = 1000
            lprice = 0
        if(order == None):
            order = ""
        if(book_table == None):
            book_table = ""
        if(rate == None):
            rate = '0.0'
        if(type == None):
            type = ''
        csv_fp = open('restaurant.csv', 'r')
        reader = csv.DictReader(csv_fp)
        headers = [col for col in reader.fieldnames if col != 'Unnamed: 0']
        final = []
        for row in reader:
            if(order in row['Online Order'] and book_table in row['Book_Table'] and float(rate) <= float(row['Rate']) and type in row['Restaurant_Type'] and int(lprice) <= int(row['Approx_cost(for two people)']) < int(uprice)):
                data = []
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

    final.sort(key=lambda x: x[4], reverse=True)
    return render(request, 'dashboard.html', {'data': final, 'headers': headers})


def calculate_rating(line):
    csv = pd.read_csv('ratings.csv', sep=',')
    row = csv.loc[line]
    print(row)
    curr_rating = (float(row[2])*5+float(row[3])*4+float(row[4])
                   * 3+float(row[5])*2+float(row[6])*1)/float(row[1])
    print(round(curr_rating, 2))
    return round(curr_rating, 2)
    csv.loc[line, 'Rating'] = curr_rating
    csv.to_csv("ratings.csv", index=False)


def res_suggestion(line):
    # csv_res = open('restaurant.csv', 'r')
    csv_pd = pd.read_csv('restaurant.csv')
    # reader = csv.DictReader(csv_res)
    cuisines = (csv_pd.loc[line]['Cuisines']).split(',')
    # print(cuisines)
    dic = []
    for cuisine in cuisines:
        # for row in reader:
        #     if(cuisine in row['Cuisines']):
        #         temp.append(row['Restaurant_Name'])
        # final.append(temp)
        for i in range(len(csv_pd)):
            temp = []
            if(cuisine in csv_pd.loc[i, 'Cuisines'] and csv_pd.loc[i, 'Restaurant_Name'] not in dic and csv_pd.loc[i, 'Restaurant_Name'] != csv_pd.loc[line, 'Restaurant_Name']):
                temp.append(csv_pd.loc[i, 'Restaurant_Name'])
                temp.append(csv_pd.loc[i, 'Cuisines'])
                temp.append(csv_pd.loc[i, 'Rate'])
                temp.append(csv_pd.loc[i, 'Famou_ Dishes'])
                temp.append(csv_pd.loc[i, 'Approx_cost(for two people)'])
                temp.append(csv_pd.loc[i, 'Address'])
                dic.append(temp)

    # print(dic)
    # print(final)
    dic.sort(key=lambda x: x[2], reverse=True)
    return dic


def review(request):
    global user_row
    final = []
    rating_file = open('ratings.csv', 'r')

    reader = csv.DictReader(rating_file)
    for row in reader:
        final.append(row['Restaurant_Name'])
    rating_file.close()

    file = pd.read_csv('ratings.csv', sep=',')

    user_data = pd.read_csv('user_data.csv')

    if(request.method == "POST"):
        
        res=request.POST.get('restaurant')
        rate=request.POST.get('rating')
        print("Restaurant Selected is : ",res)
        print("Rating : ",rate)

        rating_file = open('ratings.csv', 'r')

        reader = csv.DictReader(rating_file)
        now = datetime.now()
        info=[]
        info.append(res)
        info.append(rate)
        info.append(now.strftime("%Y-%m-%d %H:%M:%S"))
        print(info)
        x=(user_data.loc[user_row[2],'history'])
        if(str(x) == 'nan'):
            user_data.loc[user_row[2],'history']=info
            user_data.to_csv('user_data.csv',index=False)
        else:
            # print(user_data.loc[user_row[2],'history'].split(',')[2][2:-2])
            time=user_data.loc[user_row[2],'history'].split(',')[2][2:-2]
            # restaurant=user_data.loc[user_row[2],'history'].split(',')[0][2:-1]
            converted_dt=datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            if(converted_dt + timedelta(hours=3)<=datetime.now()):
                print("You can submit a review.")
                print(','.join([str(x),str(info)]))
                user_data.loc[user_row[2],'history']=','.join([str(info),str(x)])
                user_data.to_csv('user_data.csv',index=False)

            else:
                print("You can submit only after 3hrs from previous.")
                return render(request,'review.html',{'data':final,'msg':'You can submit only after 3hrs from previous.'})

        
        for row in reader:
            if(res==row['Restaurant_Name']):
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

        data=res_suggestion(line-2)
        # data['data']=final
        
        return render(request,'review.html',{'data':final,'sugg':data})



    return render(request,'review.html',{'data':final})
