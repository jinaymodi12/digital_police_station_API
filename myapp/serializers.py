from rest_framework import serializers,fields
from .models import*
from django.contrib.auth.hashers import make_password


class AdduserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['roles','username','name','email','mobile','pincode','address','state','password']
    def create(self,validated_data):
        validated_data['password']=make_password(validated_data['password'])
        return super(AdduserSerializers,self).create(validated_data)
        
class Addlogin(serializers.ModelSerializer):
    username=serializers.CharField(max_length=100)
    class Meta:
        model=User
        fields=['username','password']

class Addcomplain(serializers.ModelSerializer):
    # date = fields.DateField(input_formats=['%Y-%m-%dT%H:%M:%S.%fZ'])
    class Meta:
        model=complain
        fields=['crime_category','detail','area']

class Listcomplain(serializers.ModelSerializer):
    class Meta:
        model=complain
        fields=['crime_category','detail','area','date']

class viewcomplainSerializers(serializers.ModelSerializer):
    class Meta:
        model=complain
        fields=['crime_category','detail','area','date','status']

class assigncomplainSerializers(serializers.ModelSerializer):
    class Meta:
        model = complain
        fields=['crime_category','detail','area','date','status','station']

class addpolicememberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Police
        fields=['salary','description','post','rank','station']

class addstationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields=['city','state','locality','name']

class addreviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields=['description']

class addcriminaldataSerializers(serializers.ModelSerializer):
    class Meta:
        model = Criminal_Record
        fields = ['jail','description','section','fine']

# class SearchSerializer(serializers.ModelSerializer):
#     search = serializers.CharField(required=True)

#     class Meta:
#         models = Criminal_Record
#         fields = ['criminal_name']
class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criminal_Record
        fields = ['criminal_name']