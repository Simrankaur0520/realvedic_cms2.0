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
from realvedic_app.admin_pages.image_upload import image_upload
#----------------------------models---------------------------------------------------
from realvedic_app.models import Product_data,categoryy,images_and_banners,blogs,user_cart


#----------------------------extra---------------------------------------------------
import simplejson as json

  
@api_view(['GET'])
def adminProductView(request,format=None):
    status= [{
        "name": "In stock",
        "color": "#00ac69"
        },
        {
        "name": "Out of stock",
        "color": "#FF0000"
        }
  ]
    res={}
    prod_list=[]
    titles=["Product ID", "Product Name", "Category"," HSN", "Stock", "Status","Actions"]

    prod_obj=Product_data.objects.values()
    for i in prod_obj:
        prods={
            'product_id':i['id'],
            'product_name':i["title"],
            "category":i["category"],
            "hsn":i["HSN"],
            "stock": 25,
            "status": "In stock"
        }
        prod_list.append(prods)
    res['titles']=titles
    res['content']=prod_list
    res['status']=status


    

    
    return Response(res)


@api_view(['POST'])
def adminProductEditView(request,format=None):
    prod_id=request.data['token']
   
    sibling_prod_list=[]
    variant_data=[]
    res={}
    meta_fields_dict={}
    sibling_product={}
    mock_id=0
    #-------------------------------------------------------------
    prods_obj=Product_data.objects.values()
    prod=prods_obj.filter(id=prod_id).values()
    single_prod_obj=prod[0]
    #-----------------------------------------------------------
    for i in prods_obj:
        img=i['image'].split(',')
        prods={
            'id':i['id'],
            'title':i["title"],
            "image":img[0],
            "category":i["category"],
           
        }
        sibling_prod_list.append(prods)
    #-----------------------------------------------------------
    weights=single_prod_obj['size'].split('|')
    price=single_prod_obj['price'].split('|')
    sku=single_prod_obj['SKU'].split('|')
    #-----------------------------------------------------------
    sibling=single_prod_obj['sibling_product']
    siblingprod=prods_obj.filter(title=sibling).values()
    sibling_product['product_id']=siblingprod[0]['id']
    sibling_product['product_name']=siblingprod[0]['title']
    sibling_product['img']=siblingprod[0]['image'].split(',')[0]
    sibling_product['category']=siblingprod[0]['category']
    
    #-----------------------------------------------------------
    nutrition=single_prod_obj['nutrition'].split('|')
    nutritional_info=[
        {
        "id":0,
       "n_name": "Total Fat",
       "n_value": nutrition[0].split(' ')[0],
       "n_unit": "g"
     },
     {
        "id":1,
       "n_name": "Protien",
       "n_value": nutrition[1].split(' ')[0],
       "n_unit": "g"
     },
     {
        "id":2,
       "n_name": "Carbohydrate",
       "n_value": nutrition[2].split(' ')[0],
       "n_unit": "g"
     },
     {
        "id":3,
       "n_name": "Energy",
       "n_value": nutrition[3].split(' ')[0],
       "n_unit": "kcal"
     }]
    for i in range(len(weights)):
        variants_data= {
            'id':mock_id,
            'variant_name':weights[i],
            'price':price[i],
            'quantity':"",
            'sku':sku[i],

        }
        mock_id=mock_id+1
        variant_data.append(variants_data)
    #--------------------------------------------------------
    meta_fields_dict=[{
        'm_name':'Benefits',
        'm_value':single_prod_obj['benefits'] 
        },
        {
        'm_name':'Ingredients',
        'm_value':single_prod_obj['ingredients'] 
        },
        {
        'm_name':'How to use',
        'm_value':single_prod_obj['how_to_use'] 
        },
        {
        'm_name':'How we make it',
        'm_value':single_prod_obj['how_we_make_it'] 
        }
        ]
   

#-----------------------------------------------------------    
    res['images']=(single_prod_obj['image']).split(',')
    print((single_prod_obj['image']))
    res['name']=single_prod_obj['title']
    res['id']= single_prod_obj['id']
    res['status']=single_prod_obj['Status']
    res['category']=single_prod_obj['category']
    res['hsn']=single_prod_obj['HSN']
    res['variant_data']=variant_data
    res['sibling_product']=sibling_product
    res['nutritional_info']=nutritional_info
    res['meta_fields']=meta_fields_dict
    
    #----------------------------------------------------------
    prod_category=prods_obj.values('category','HSN').distinct()
    res['category_list']=prod_category
    res['ProductList']=sibling_prod_list


    #-------------------------------
    return Response(res)
@api_view((['POST']))
def admin_product_edit_view(request,format=None):
    data=request.data
    nutri=[]
    images=data['images']
    title=data['name']
    id=data['id']
    about=data['about']
    category=data['category']
    hsn=data['hsn']
    status=data['status']
    meta_fields=data['meta_fields']
    sibling_product=data['sibling_product']
    variant_data=data['variant_data']
    nutritional_info=data['nutritional_info']
    nutritional = list(map(itemgetter('n_value','n_unit'), nutritional_info))
   
    variant_name = list(map(itemgetter('variant_name'), variant_data))
    size = '|'.join(list(variant_name))
    price_get = (map(itemgetter('price'), variant_data))
    price = '|'.join(list(price_get))
    SKU_get = (map(itemgetter('sku'), variant_data))
    SKU = '|'.join(list(SKU_get))
    #----------------------------------------------------------
    meta_fieldss = dict(map(itemgetter('m_name','m_value'),meta_fields ))
    for i in nutritional:
        print(i)
        result=i[0]+" "+i[1]
        nutri.append(result)
    nutritional_info_list = '|'.join(list(nutri))

    
    try:
        Product_data.objects.filter(id=id).update(title=title,
                                                    category=category,
                                                    HSN=hsn,
                                                    about=about,
                                                    image=images,
                                                    Status=status,
                                                    benefits=meta_fieldss['Benefits'],
                                                    ingredients=meta_fieldss['Ingredients'],
                                                    how_to_use=meta_fieldss['How to use'],
                                                    how_we_make_it=meta_fieldss['How we make it'],
                                                    sibling_product=sibling_product['product_name'],
                                                    price=price,
                                                    size=size,
                                                    SKU=SKU,
                                                    nutrition=nutritional_info_list
            )
                                                
        
        res={
                    'status':True,
                    'message':"data updated successfully"
                }    
    except:
         res={
                    'status':False,
                    'message':"Sometthing went wrong"
                }    


    print(meta_fields)
    print(meta_fieldss)

   

    return Response(res)


@api_view(['GET'])
def siblingProductList(request,format=None):
    prod_list=[]
    prod_obj=Product_data.objects.values('id','title','image','category')
    for i in prod_obj:
        img=i['image'].split(',')
        prods={
            'id':i['id'],
            'title':i["title"],
            "image":img[0],
            "category":i["category"],
           
        }
        prod_list.append(prods)
    return Response(prod_list)


@api_view(['GET','PUT'])
def adminAddNewProduct(request,format=None):
    if request.method=='GET':
        category_obj=categoryy.objects.values_list('category',flat=True)
        res={
            'title' :"", 
            'category' :category_obj, 
            'about' :"", 
            'price' :"", 
            'discount' :"", 
            'image':"",
            'size' :"", 
            'benefits' :"", 
            'ingredients':"", 
            'how_to_use':"",
            'how_we_make_it' :"", 
            'nutrition':"", 
            'Status' :"", 
            'sibling_product':"",
            'HSN':"",
            'SKU':"",
            'tax' :"", 

        }
        return Response(res)
    if request.method=='PUT':
        data=request.data
        try:
            if data['title']=="":
                res={
                    'status':False,
                    'message':'Field Required'
                }
            else:
                title=data['title']
            if data['category']=="":
                res={
                    'status':False,
                    'message':'Field Required'
                }
            else:
                category=data['category']
            if data['about']=="":
                res={
                    'status':False,
                    'message':'Field Required'
                }
            else:
                about=data['about']

            if data['image']=="":
                res={
                    'status':False,
                    'message':'Field Required'
                }
            else:
                images=data['image']
              

            if data['price']=="":
                res={
                    'status':False,
                    'message':'Field Required'
                }
            else:
                price=data['price']

            if data['size']=="":
                res={
                    'status':False,
                    'message':'Field Required'
                }
            else:
                size=data['size']

            if data['discount']=="":
                res={
                    'status':False,
                    'message':'Field Required'
                }
            else:
                discount=data['discount']



            benefits=data['benefits']
            ingredients=data['ingredients']
            how_to_use=data['how_to_use']
            how_we_make_it=data['how_we_make_it']
            if data['nutrition']=="":
                res={
                    'status':False,
                    'message':'Field Required'

                }
                return Response(res)
               
            else:
                nutrition=data['nutrition']

            if data['Status']=="":
                res={
                    'status':False,
                    'message':'Field Required'

                }
                return Response(res)
            else:
                Status=data['Status']

            if data['sibling_product']=="":
                res={
                    'status':False,
                    'message':'Field Required'

                }
                return Response(res)
            else:
                sibling_product=data['sibling_product']

            if data['HSN']=="":
                res={
                    'status':False,
                    'message':'Field Required'

                }
                return Response(res)
            else:
                HSN=data['HSN']

            if data['SKU']=="":
                res={
                    'status':False,
                    'message':'Field Required'

                }
                return Response(res)
            else:
                SKU=data['SKU']

            if data['tax']=="":
                res={
                    'status':False,
                    'message':'Field Required'

                }
                return Response(res)
            else:
                tax=data['tax']

            new_obj= Product_data(
                                title=title,
                                category=category,
                                HSN=HSN,
                                about=about,
                                image=images,
                                Status=Status,
                                benefits=benefits,
                                discount=discount,
                                ingredients=ingredients,
                                how_to_use=how_to_use,
                                how_we_make_it=how_we_make_it,
                                sibling_product=sibling_product,
                                price=price,
                                size=size,
                                SKU=SKU,
                                nutrition=nutrition,
                                tax=tax
                                )
            new_obj.save()
          
            res={
                'message':"all good"
            }

        except:
            res={
                'message':"Something went wrong"
            }
        return Response(res)


@api_view(['POST'])
def newImageUpload(request,format=None):
    file = request.FILES['file']
    index = request.data['index']
    imageArray = request.data['image_array'].split(',')
  
    img_path = 'img/'
    upload_res = image_upload(file,img_path)
    updated_value = 'media/'+upload_res
   
    imageArray[int(index)] = updated_value
 
    return Response({'image_array':imageArray})

@api_view(['POST'])
def adminProductDelete(request,format=None):
   product_id=request.data['id']
   try:
    obj=Product_data.objects.get(id=product_id)
    obj.delete()
    prod_obj=Product_data.objects.values()

    res={
           'status':True,
           "Message":"Product deleted successfully !"
       }
   except:
       res={
           'status':False,
           "Message":"Something went wrong !"
       }
   return Response(prod_obj)


