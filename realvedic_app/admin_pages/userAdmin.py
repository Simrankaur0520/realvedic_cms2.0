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

    for i in user:
        add=user_address.objects.filter(user_id=i['id']).values()[0]
        user_lis={
            'user_id': i['id'],
            'created':i['created_at'],
            'user':{
                'name':i['first_name']+" "+i['last_name'],
                'email':i['email']

            },
            'destination_state':add['state'],
            'pincode':add['pincode']
        }
        conetnt.append(user_lis)
    res['titles']=titles
    res['content']=conetnt
    return Response(res)