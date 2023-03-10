import numpy as np
import pandas as pd
import time
from datetime import datetime as dt
import datetime
import re
from operator import itemgetter 
import os
import random


#-------------------------Django Modules---------------------------------------------
from django.http import Http404, HttpResponse, JsonResponse,FileResponse
from django.shortcuts import render
from django.db.models import Avg,Count,Case, When, IntegerField,Sum,FloatField,CharField
from django.db.models import F,Func,Q
from django.db.models import Value as V
from django.db.models.functions import Concat,Cast,Substr
from django.contrib.auth.hashers import make_password,check_password
from django.db.models import Min, Max
from django.db.models import Subquery
#----------------------------restAPI--------------------------------------------------
from rest_framework.decorators import parser_classes,api_view
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.response import Response
from operator import itemgetter
import datetime

#----------------------------models---------------------------------------------------
from realvedic_app.models import Product_data,categoryy,images_and_banners,blogs,user_cart,Order_data,user_data,user_address,PaymentOrder

@api_view(['GET'])
def admin_user_view(request,format=None):
    #static data
    titles= [
    "User ID",
    "Created",
    "Customer",
    "State",
    "Pincode",
    "Actions"
    ]
    conetnt=[]
    res={}
    user=user_data.objects.values()
    add=user_address.objects.values()
    
    for i in user:
        add=user_address.objects.filter(user_id=str(i['id'])).values()[0]
    
        


        user_lis={
                'user_id': i['id'],
                'created':i['created_at'],
                'user':{
                    'name':i['first_name']+" "+i['last_name'],
                    'email':i['email'],
                    'token':i['token'],

                },
                'destination_state':add['state'],
                'pincode':add['pincode']
            }
        conetnt.append(user_lis)
    res['titles']=titles
    res['content']=conetnt

    return Response(res)


@api_view(['POST'])
def admin_single_user_view(request,format=None):
    user_token=request.data['token']
    user=user_data.objects.get(token=user_token)
    res={}
    
   
    if  str(user.id) in PaymentOrder.objects.values_list('user_id',flat=True):
    
        order_obj=PaymentOrder.objects.filter(user_id=user.id).values()
        
          
    else: 
        order_obj="none"
   
        
    
    user_add=user_address.objects.get(user_id=user.id)
    user_details={
        'id':user.id,
        'gender': user.gender,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'dob': user.dob,
        'phone_code': user.phone_code,
        'phone_no': user.phone_no,
        'password': user.password,

    }
    address_details={
        'user_id' : user_add.user_id,
        'add_line_1' : user_add.add_line_1,
        'add_line_2' : user_add.add_line_2,
        'landmark' : user_add.landmark,
        'city' : user_add.city,
        'state' : user_add.state,
        'country' : user_add.country,
        'pincode' : user_add.pincode,
        'phone_no' : user_add.phone_no

    }
    res['user_details']=user_details
    res['address_details']=address_details
    res['order_info']=order_obj
    
    ord=PaymentOrder.objects.values()
    return Response(res)


    
@api_view(['GET','PUT'])
def admin_user_add(request,format=None):
    if request.method=='GET':
        res={
        'gender' : "",
        'first_name' : "", 
        'last_name' : "", 
        'email' : "", 
        'dob' : "", 
        'phone_code' : "", 
        'phone_no' : "", 
        'password' : "",
        'add_line_1' : "", 
        'add_line_2' : "", 
        'landmark' : "", 
        'city' : "", 
        'state' : "", 
        'country' : "", 
        'pincode' : ""
       
        }
        return Response(res)

    if request.method == 'PUT':
        data=request.data
        gender = data['gender']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        dob = data['dob']
        phone_code = data['phone_code']
        phone_no = data['phone_no']
        password = data['password']
        #address
        add_line_1 = data['add_line_1']
        add_line_2 = data['add_line_2']
        landmark = data['landmark']
        city = data['city']
        state = data['state']
        country = data['country']
        pincode = data['pincode']
        
        enc_pass = make_password(password)
        token = make_password(email+password)

        if email in user_data.objects.values_list('email',flat=True):
            return Response({'message':'Email already exist',
                            'status':False    
                            })
        if phone_no in user_data.objects.values_list('email',flat=True):
            return Response({'message':'Phone number already exist',
                            'status':False 
                            })
        data = user_data(
                            first_name = first_name,
                            last_name = last_name,
                            email = email,
                            gender = gender,
                            dob = dob,
                            phone_code = phone_code,
                            phone_no = phone_no,
                            password = enc_pass,
                            token = token,
                        )
        data.save()
        user=user_data.objects.get(phone_no=phone_no)

        data = user_address(
                            user_id = user.id,
                            add_line_1 = add_line_1,
                            add_line_2 = add_line_2,
                            landmark = landmark,
                            city = city,
                            state = state,
                            country = country,
                            pincode = pincode,
                            phone_no = phone_no,
                        )
        data.save()
        
        res = { 
                'message':'User created successfully',
                'status':True    
        }   




        return Response(res)
    
@api_view(['POST'])
def admin_user_edit(request,format=None):
        admin_token=data['admin_token']
        data=request.data
        token = data['token']
        
        gender = data['gender']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        dob = data['dob']
        phone_code = data['phone_code']
        phone_no = data['phone_no']
        add_line_1 = data['add_line_1']
        add_line_2 = data['add_line_2']
        landmark = data['landmark']
        city = data['city']
        state = data['state']
        country = data['country']
        pincode = data['pincode']
        phone_no = data['phone_no']
        try:
            user=user_data.objects.get(token=token)
        
       
            data = user_data.objects.filter(id=user.id).update(
                                first_name = first_name,
                                last_name = last_name,
                                email = email,
                                gender = gender,
                                dob = dob,
                                phone_code = phone_code,
                                phone_no = phone_no,
                            
                            )
           


            data = user_address.objects.filter(user_id=user.id).update(

                                add_line_1 = add_line_1,
                                add_line_2 = add_line_2,
                                landmark = landmark,
                                city = city,
                                state = state,
                                country = country,
                                pincode = pincode,
                                phone_no = phone_no,
                            )
           
            res={
                    'status':True,
                    'message':"Updated successfully"
                }
        except:
            res={
                'status':False,
                'message':"something went wrong"
            }
        return Response(res)


@api_view(['POST'])
def admin_user_delete(request,format=None):
 
    token = request.data['token']
    try:
        user=user_data.objects.get(id=token)
        user.delete()
        res={
            'status':True,
            'message':"Deleted successfully"

        }
    except:
        res={
                'status':False,
                'message':"something went wrong"
            }
        userr=user_data.objects.values()
    return Response(res)
