from django.shortcuts import render
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import*
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.permissions import *
from .authentication import*
from .utils import*
# from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from .models import User
import base64
from rest_framework.views import APIView
import random
# Create your views here.
@api_view(['GET'])
def index(request):
    api_url={
        # '':'/list_pizza/',
        # 'edit_pizza':'/edit_pizza/',
        # 'add_pizza':'/add_pizza/',
        # 'delete_pizza':'/delete_pizza/',
        'user_register':'/registration/',
        # 'login':'/login/',
        # 'verify':'/verify/id',
        # 'seller_verification':'/seller_verification/id',
        # 'user-edit-profile':'/user-edit-profile/',
        # 'user-delete':'/user-delete/id',
        # # 'admin-index':'/admin-index/',
        # # 'edit-profile':'/edit-profile/',
        # # 'seller-index':'/seller-index/',
        # 'add-product':'/add-product/',
        # 'my-product':'/my-product/',
        # 'edit-product':'/edit-product/id',
        # 'delete-product':'/delete-product/id',
        # 'buyer-index':'/buyer-index/',
        # # 'one-product':'/one-product/',
        # 'add-cart':'/add-cart/product-id',
        # 'my-cart':'/my-cart/',
        # 'edit-cart':'/edit-cart/id',
        # 'delete-cart':'/delete-cart/id',
        # 'checkout':'/checkout/',
        # # 'buy-product/':'/buy-product/product-id',
        # 'my-buy':'/my-buy/',
        # 'status':'/status/',
    }
    return Response(api_url)

class registrationViews(GenericAPIView):
    serializer_class=AdduserSerializers

    def post(self,request):
        serializer = AdduserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status':200,"Message":'Registeration Done SuccessFully','Results':serializer.data})
        else:
            print(serializer.errors)
            return Response({'Status':404,"Message":'Error'})

class loginViews(GenericAPIView):
    serializer_class = Addlogin
    queryset = User.objects.all()

    def post(self,request):
       serializer=Addlogin(data=request.data)
       if serializer.is_valid():
        email = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        user = authenticate(request,username=email,password=password)
        print(user)
        if user:
            if user.roles =='users' or 'policecommissioner' or 'police_inspector' or 'police_superintendent':
                payload = {
                            'id':user.id,
                            'email':user.email
                        }
                jwt_token = {'token': jwt.encode(payload, "SECRET_KEY",algorithm='HS256')}
                print(jwt_token)
                UserToken.objects.create(user=user,token=jwt_token)
                
                return Response({'Status':200,'Message':'login SuccessFully!','Token':jwt_token,'Results':serializer.data})
            else:
                return Response({'msg':'Invalid Data'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class createcomplainViews(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Addcomplain

    def post(self,request):
        serializer = Addcomplain(data=request.data)
        if serializer.is_valid():
            area = serializer.validated_data.get('area')
            station=Station.objects.get(city=area)
            print(station)
            serializer.save(name=request.user,station=station)
            return Response({'Status':200,'Messages':'Complain Send To Respected Police Station',"Results":serializer.data})
        else:
            print(serializer.errors)
            return Response({'Status':404,'Messages':'Error'})

class listcomplainViews(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = Listcomplain

    def get(self,request):
        uid = complain.objects.filter(user=request.user)
        serializer = Listcomplain(uid,many=True)
        return Response({'Status':200,'Messages':'Complain As Below','Results':serializer.data})

class viewcomplainViews(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = viewcomplainSerializers

    def get(self,request):
        uid = complain.objects.filter(status='pending')
        serializer = viewcomplainSerializers(uid,many=True)
        return Response({'Status':200,'Results':serializer.data})

class AssigncomplainViews(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = assigncomplainSerializers

    def post(self,request,pk):
        uid = Station.objects.get(id=pk)
        serializer = assigncomplainSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(name=request.user,station=uid)
            return Response({'Status':200,'Messages':'Complain Assigned','Results':serializer.data})
        else:
            return Response('Error')

class AddpoliceViews(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = addpolicememberSerializers

    def post(self,request,pk):
        police=police.objects.get(id=pk)
        serializer = addpolicememberSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,Station=police)
            return Response({'Status':200,'Message':'Member Added','Results':serializer.data})
        else:
            return Response('Error')

class AddstationViews(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = addstationSerializers

    def post(self,request):
        serializer = addstationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Status':200,'Message':'Station Added','Results':serializer.data})
        else:
            return Response('Error')

class addreviewViews(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,pk):
        station = station.objects.get(id=pk)
        serializer = addreviewSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(civilian=request.user,station=station)
            return Response({'Status':200,'Messages':'Review Add SuceessFully','Results':serializer.data})
        else:
            return Response('Error')
    
class addcrimialViews(GenericAPIView):
    permission_classes = [IsAdminUser]

    def post(self,request,pk):
        station = Station.objects.get(id=pk)
        serializer = addcriminaldataSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,station=station)
            return Response({'Status':200,'Mesages':'Add data successfully','Results':serializer.data})
        else:
            return Response('Error')

class searchViews(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class=SearchSerializer

    def get(self,request):
        serializer = SearchSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(data={"Status": status.HTTP_400_BAD_REQUEST,
                                  "Message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        query = serializer.validated_data['criminal_name']

        search = Criminal_Record.objects.filter(criminal_name__icontains=query)
        print(search)
        a=[]
        if search:
            for i in search:
                print(i)
                b=i.criminal_name
                print(b)
                a.append(b)
            return Response({'Status':200,'Results':a})
        else:
            return Response('Error')
        
# class generateKey:
#     @staticmethod
#     def returnValue(phone):
#         return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"
    
# class getPhoneNumberRegistered(APIView):
#     # Get to Create a call for OTP
#     @staticmethod
#     def get(request, phone):
#         try:
#             Mobile = User.objects.get(mobile=phone)  # if Mobile already exists the take this else create New One
#         except ObjectDoesNotExist:
#             User.objects.create(
#                 mobile=phone,
#             )
#             Mobile = User.objects.get(mobile=phone)  # user Newly created Model
#         Mobile.counter += 1  # Update Counter At every Call
#         Mobile.save()  # Save the data
#         keygen = generateKey()
#         key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
#         OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
#         print(OTP.at(Mobile.counter))
#         # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
#         return Response({"OTP": OTP.at(Mobile.counter)}, status=200)
       



# class ValidatePhoneSendOTP(APIView):
#     permission_classes = (permissions.AllowAny, )
#     def post(self, request, *args, **kwargs):
#         name = request.data.get('name' , False)
#         phone_number = request.data.get('phone')
#         if phone_number:
#             phone  = str(phone_number)
#             user = User.objects.filter(phone__iexact = phone)

#             if user.exists():
#                 return Response({
#                     'status' : False,
#                     'detail' : 'Phone number already exists.'
#                     })
#             else:
#                 key = send_otp(phone)

#                 if key:
#                     old =User.objects.filter(phone__iexact = phone)
#                     if old.exists():
#                         old  = old.first()
#                         count = old.count
#                         # if count > 20:
#                         #     return Response({
#                         #         'status': False,
#                         #         'detail' : 'Sending otp error. Limit Exceeded. Please contact customer support.'
#                         #         })
#                         old.count = count + 1
#                         old.save()
#                         print('Count Increase', count)
#                         return Response({
#                             'status' : True,
#                             'detail' : 'OTP sent successfully.'
#                             })
#                     else:
#                         PhoneOTP.objects.create(
#                             # name = name,
#                             phone = phone,
#                             otp = key,

#                             )
#                         link = f'API-urls'
#                         requests.get(link)
#                         return Response({
#                             'status' : True,
#                             'detail' : 'OTP sent successfully.'
#                             })



#                 else:
#                     return Response({
#                         'status' : False,
#                         'detail' : 'Sending OTP error.'
#                         })

#         else:
#             return Response({
#                 'status' : False,
#                 'detail' : 'Phone number is not given in post request.'
#                 })


# def send_otp(phone):
#     if phone:
#         key = random.randint(999,9999)
#         print(key)
#         return key
#     else:
#         return False


# class ValidateOTP(APIView):
#     permission_classes = (permissions.AllowAny, )
#     def post(self, request, *args, **kwargs):
#         phone = request.data.get('phone' , False)
#         otp_sent = request.data.get('otp', False)

#         if phone and otp_sent:
#             old = PhoneOTP.objects.filter(phone__iexact = phone)
#             if old.exists():
#                 old = old.first()
#                 otp = old.otp
#                 if str(otp_sent) == str(otp):
#                     old.validated = True
#                     old.save()
#                     return Response({
#                         'status' : True,
#                         'detail' : 'OTP mactched. Please proceed for registration.'
#                         })

#                 else: 
#                     return Response({
#                         'status' : False,
#                         'detail' : 'OTP incorrect.'
#                         })
#             else:
#                 return Response({
#                     'status' : False,
#                     'detail' : 'First proceed via sending otp request.'
#                     })
#         else:
#             return Response({
#                 'status' : False,
#                 'detail' : 'Please provide both phone and otp for validations'
#                 })

