from import_statements import *

# Create your views here.

@api_view(['POST'])
def adminLogin(request,format=None):
    email = request.data['email']
    password = request.data['password']

    try:
        user = admin_login.objects.get(email = email)
        if check_password(password,user.password):
            res = {
                    'status':True,
                    'message':'login successfull',
                    'token':user.token
            }
        else:
            res = {
                    'status':False,
                    'message':'Invalid Credentials',
                  }
        return Response(res)
    except:
        res = {
                    'status':False,
                    'message':'Invalid Credentials',
                  }
        return Response(res)