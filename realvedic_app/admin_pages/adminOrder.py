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
            'invoice_id':i['id'],
            'created':i['order_date'],
            'customer':{
                'name':user_dataa["first_name"]+' '+user_dataa["last_name"],
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

@api_view(['POST'])
def admin_order_edit_view(request,format=None):
    order_id=request.data['order_id']
    order_obj=PaymentOrder.objects.filter(id=order_id).values()[0]
    user=user_data.objects.filter(id=order_obj['user_id']).values()[0]
    user_ad=user_address.objects.filter(user_id=order_obj['user_id']).values()[0]
    prod=Product_data.objects.values()
    items=[]

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
      "status_name": "Cancelled",
      "status_color": "#FF0000"
    },
    {
      "status_name": "Returned",
      "status_color": "#e99f15"
    },
    {
      "status_name": "Placed",
      "status_color": "#e99f15"
    },
     {
      "status_name": "On the way",
      "status_color": "#638CE6"
    }
    ]
  #-----------------------------------------------
    item_list=eval(order_obj['order_product'])['items']
    print(item_list)
    for i in item_list:
      itemss={
        "id": i['product_id'],
        "image":i["image"],
        "title":i["name"] ,
        "unit_price":i["net_price"] ,
        "size":i["size"] ,
        "quantity":i["quantity"],
        "quantity_price":i["final_net_price"] ,
        "category":""
      }
      items.append(itemss)
    Payment_info={
      "sub_total":eval(order_obj['order_product'])['item_total'] ,
      "shipping": "50",
      "tax": eval(order_obj['order_product'])['tax'],
      "grand_total": eval(order_obj['order_product'])['order_total']
    }
    shipping_info= {
      "address_line_1":eval(order_obj['order_product'])['address_info']['address_line_1'],
      "address_line_2": eval(order_obj['order_product'])['address_info']['address_line_2'],
      'landmark':user_ad['landmark'],
      "city": eval(order_obj['order_product'])['address_info']['city'],
      "state":eval(order_obj['order_product'])['address_info']['state'],
      "country":eval(order_obj['order_product'])['address_info']['country']
    }
    billing_info= {
      "address_line_1":eval(order_obj['order_product'])['address_info']['address_line_1'],
      "address_line_2": eval(order_obj['order_product'])['address_info']['address_line_2'],
      'landmark':user_ad['landmark'],
      "city": eval(order_obj['order_product'])['address_info']['city'],
      "state":eval(order_obj['order_product'])['address_info']['state'],
      "country":eval(order_obj['order_product'])['address_info']['country']
    }
    contact_info= {
      "first_name": user['first_name'],
      "last_name":user['last_name'],
      "email": user['email'],
      "phone_number":  user['phone_code']+user['phone_no']
    }
    

    res['order_id']=order_id
    res['status']=order_obj['order_status']
    res['order_date']=str(order_obj['order_date'])[:10]
    res['order_time']=str(order_obj['order_date'])[11 :19]
    res['items']=items
    res['payment_info']=Payment_info
    res['shipping_info']=shipping_info
    res['billing_info']=billing_info
    res['contact_info']=contact_info
    res['status_list']=status_list
    datee=(order_obj['order_date'])
   
    return Response(res)

    
@api_view(['POST'])
def admin_order_edit(request,format=None):
  status=request.data['status']
  order_id=request.data['order_id']
  try:
    order_obj=PaymentOrder.objects.filter(order_payment_id=order_id).update(order_status=status)
    res={
      'status':True,
      'Message':"Status updated successfully"
    }
  except:
    res={
      'status':False,
      'Message':"Something went wrong"
    }
  return Response(res)

@api_view(['GET','PUT'])
def admin_order_create(request,format=None):
    if request.method=='GET':
      prod_dict_list=[]
      prod=Product_data.objects.values()
      for i in prod:
        prod_dict={
            "id":i['id'],
            "title":i['title'] ,
            "image":i['image'] ,
            "category":i['category'] ,
            "size":i['size'].split('|') ,
            "price":i['price'].split('|')

        }
        prod_dict_list.append(prod_dict)

     
      res={
      'product':prod,
      'order_product' :"", 
      'order_amount' :"", 
      'order_payment_id' :"", 
      'isPaid' :"", 
      'user_id':"",
      'order_status' :"" 
      }
     
      return Response(prod_dict_list)
    if request.method=='PUT':
      ord_obj=PaymentOrder.objects.values()
      data=request.data
      if data['order_product'] == "":
        res={
                    'status':False,
                    'message':'Field Required'
                }
        return Response(res)
      else:
        order_product=data['order_product']
        
      if data['order_amount'] == "":
        res={
                    'status':False,
                    'message':'Field Required'
                }
      else:
        order_amount=data['order_amount']

      if data['order_payment_id'] == "":
        res={
                    'status':False,
                    'message':'Field Required'
                }
      else:
        order_payment_id=data['order_payment_id']

      if data['isPaid'] == "":
        res={
                    'status':False,
                    'message':'Field Required'
                }
      else:
        isPaid=data['isPaid']

      if data['user_id'] == "":
        res={
                    'status':False,
                    'message':'Field Required'
                }
      else:
        user_id=data['user_id']

      if data['order_status'] == "":
        res={
                    'status':False,
                    'message':'Field Required'
                }
        return Response(res)
      else:
        order_status=data['order_status']
      
      new_obj=PaymentOrder(
        order_product = order_product, 
        order_amount = order_amount, 
        order_payment_id = order_payment_id, 
        isPaid = isPaid, 
   
        user_id = user_id,
        order_status = order_status

      )
      new_obj.save()

      res={
        'status':True,
        'message':'Order created successfully'
      }


      return Response(ord_obj)
    
@api_view(['POST'])
def adminOrderDelete(request,format=None):
   admin_token=request.data['token']
   order_id=request.data['id']
   try:
    obj=PaymentOrder.objects.get(id=order_id)
    obj.delete()
    prod_obj=PaymentOrder.objects.values()

    res={
           'status':True,
           "Message":"Product deleted successfully !",
           'prod':prod_obj
       }
   except:
       res={
           'status':False,
           "Message":"Something went wrong !",
           'prod':prod_obj
       }
   return Response(res)

'''@api_view(['POST'])
def admincheckout(request):
    
    #token = data['token']
    res = {}
    data=request.data
    product_id=data['id']
    title=data['title']  
    size=data['size']
    unit_price=data['price']  
    quantity=data['quantity']
    tax=data['tax ']
    discount=['discount']
    prod_obj=Product_data.objects.values()
    net_price=int(unit_price)-int(discount)
    original_price=net_price-tax
    prod_details={
      'product_id':product_id,
      'title':title,
      'size':size,
      'unit_price':unit_price,
      'quantity':quantity,
      'tax':tax,
      'discount':discount,
      'net_price':net_price,
      'original_price':original_price




    }'''
    
'''cartItems = user_cart.objects.filter(user_id = data['user_id']).values()
    def getProductName(x):
        return Product_data.objects.filter(id=x).values_list('title',flat=True)[0]
    def getProductImage(x):
        return Product_data.objects.filter(id = x).values_list('image',flat=True)[0].split(',')[0]
    def getProductPrice(row):
        prod_obj = Product_data.objects.filter(id = row['product_id']).values('size','price').last()
        size = prod_obj['size'].split('|')        
        price = prod_obj['price'].split('|')        
        for i in range(len(size)):
            if size[i] == row['size']:
                return eval(price[i])
    def getDiscountPrice(row):
        prod_obj = Product_data.objects.filter(id = row['product_id']).values('discount','price').last()
        discount = prod_obj['discount']
        return eval(str(row['unit_price'])) - ((eval(str(row['unit_price'])) * 100) // (100 + eval(discount)))
    def calculateNetPrice(row):
        return eval(str(row['unit_price'])) - eval(str(row['discount_price']))
    def calculateTaxPrice(row):
        prod_obj = Product_data.objects.filter(id = row['product_id']).values().last()
        tax = prod_obj['tax']
        return eval(str(row['unit_price'])) - ((eval(str(row['unit_price'])) * 100) // (100 + eval(tax)))
    def calculatePrice(row):
        return eval(str(row['net_price'])) - eval(str(row['tax_price']))
    def calculateFinalPrice(row):
        return eval(str(row['price'])) * eval(str(row['quantity']))
    def calculateFinalTax(row):
        return eval(str(row['tax_price'])) * eval(str(row['quantity']))
    def calculateFinalNetPrice(row):
        return eval(str(row['net_price'])) * eval(str(row['quantity']))
    if len(cartItems) > 0:
        cartItems = pd.DataFrame(cartItems)

        cartItems['id'] = cartItems['id']
        cartItems['name'] = cartItems['product_id'].apply(getProductName)

        cartItems['unit_price'] = cartItems.apply(getProductPrice,axis=1)
        cartItems['discount_price'] = cartItems.apply(getDiscountPrice,axis=1)
        cartItems['net_price'] = cartItems.apply(calculateNetPrice,axis=1)
        cartItems['tax_price'] = cartItems.apply(calculateTaxPrice,axis=1)
        cartItems['price'] = cartItems.apply(calculatePrice,axis=1)

        cartItems['final_net_price'] = cartItems.apply(calculateFinalNetPrice,axis=1)
        cartItems['final_price'] = cartItems.apply(calculateFinalPrice,axis=1)
        cartItems['final_tax'] = cartItems.apply(calculateFinalTax,axis=1)

        cartItems['quantity'] = cartItems['quantity']
        cartItems['size'] = cartItems['size']
        cartItems['image'] = cartItems['product_id'].apply(getProductImage)
        cartItems = cartItems[['product_id','name','unit_price','discount_price','net_price','tax_price','price','final_net_price','final_price','final_tax','quantity','image','size']].to_dict(orient='records')
        res['items'] = cartItems
    else:
        res['items'] = []
    cartItems = pd.DataFrame(cartItems)
    res['item_total'] = sum(list(cartItems['final_price'])) 
    res['delivery_charges'] = 0
    res['tax'] = sum(list(cartItems['final_tax']))
    res['order_total'] = res['item_total'] + res['delivery_charges'] + res['tax']'''
    