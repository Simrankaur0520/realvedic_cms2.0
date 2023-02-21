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

#----------------------------models---------------------------------------------------
from realvedic_app.models import Product_data,categoryy,images_and_banners,blogs,user_cart,Order_data,user_data,user_address,PaymentOrder

@api_view(['GET'])
def admin_order_view(request,format=None):
    #---------------------------------------------------------
    content=[]
    res={}
    #------------------static data ------------------
    titles= [
    "Order ID",
    "Timestamp",
    "Customer",
    "Items",
    "State",
    "Grand Total",
    "Delivery Status",
    "Actions"
    ]
    delivery_status= [
    {
      "name": "Placed",
      "color": ""
    },
    {
      "name": "Processed",
      "color": ""
    },
    {
      "name": "On the way",
      "color": ""
    },
    {
      "name": "Dispatched",
      "color": ""
    },
    {
      "name": "Delivered",
      "color": "#00ac69"
    },
    {
      "name": "Cancelled",
      "color": ""
    },
    {
      "name": "Returned",
      "color": ""
    }
    ]
  #-------------------static data ends ----------------
    order_obj=PaymentOrder.objects.values()
   
    for i in order_obj:
        user_dataa=user_data.objects.filter(id=i['user_id']).values()[0]
        prod_name=eval(i['order_product'])['items']
        content_details={
            'invoice_id':i['order_payment_id'],
            'created':i['order_date'],
            'customer':{
                'name':user_dataa["first_name"]+user_dataa["last_name"],
                'email':user_dataa["email"] } 
                }

        
        content_details['items'] = list(map(itemgetter('name'),prod_name))
        content_details['destination_state']=eval(i['order_product'])['address_info']['state']
        content_details['grand_total']=i['order_amount']
        content_details['status']=i['order_status']
        content.append(content_details)

    #----------------------------------------------------
    res['titles']=titles
    res['content']=content
    res['status']=delivery_status

    return Response(res )

@api_view(['GET'])
def admin_order_edit_view(request,format=None):
    order_obj=PaymentOrder.objects.filter(user_id=8).values()
    res={}
    #--------------------------static data
    status_list= [
    {
      "status_name": "Delivered",
      "status_color": "#00ac69"
    },
    {
      "status_name": "Dispatched",
      "status_color": "#303030"
    },
    {
      "status_name": "Canceled",
      "status_color": "#FF0000"
    },
    {
      "status_name": "Returned",
      "status_color": "#e99f15"
    }
  ]

    res['order_id']=""
    res['order_date']=""
    res['order_time']=""
    return Response(order_obj)

    

