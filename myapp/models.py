from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator

# Create your models here.
class User(AbstractUser):
    choice=(
        ('policecommissioner','policecommissioner'),
        ('police_inspector','police_inspector'),
        ('police_superintendent','police_superintendent'),
        ('users','users'),
    )
    roles = models.CharField(choices=choice,max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50,unique=True)
    phone = models.CharField(max_length=10,unique=True)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
    pincode = models.CharField(max_length=6,default='395006')
    address = models.CharField(max_length=120)
    state = models.CharField(max_length=125)
    password = models.CharField(max_length=100)
    
    # USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = []
    # objects = UserManager()
    # def __str__(self):
    #     return self.email+''+self.roles

class UserToken(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    token = models.CharField(null=True, max_length=500)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return str(self.user)
        
class Station(models.Model):
	city=models.CharField(default="New Delhi",max_length=100)
	state=models.CharField(max_length=100)
	locality=models.CharField(max_length=100)
	name=models.CharField(max_length=100)
	slug=models.SlugField(primary_key=True,blank=True)
	# def __str__(self):
	# 	return self.name
	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=slugify(self.name)
		super(Station,self).save(*args,**kwargs)

class complain(models.Model):
    choice=(
        ('Ahmedabad','Ahmedabad'),
        ('Vadodra','Vadodra'),
        ('Surat','Surat'),
        ('Amreli','Amreli'),
    )
    crime = (
        ('Theft','Theft'),
        ('Murder','Murder'),
        ('Kidnapp','Kidnapp'),
        ('Cyber_crime','Cyber_crime'),
    )
    status = (
        ('pending','pending'),
        ('viewed','viewed'),
        ('solved','solved'),
        ('fake','fake'),
        ('working','working'),
       

    )
    name = models.ForeignKey(User,on_delete=models.CASCADE,related_name='names')
    crime_category = models.CharField(choices=crime,max_length=50)
    detail = models.TextField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    area = models.CharField(choices=choice,max_length=100)
    station = models.ForeignKey(Station,on_delete=models.CASCADE)
    resolve_by = models.CharField(max_length=100)
    status = models.CharField(choices=status,max_length=200,default='pending')


class Police(models.Model):
	user=models.ForeignKey('User',on_delete=models.CASCADE)
	salary=models.IntegerField()
	description=models.TextField()
	post=models.CharField(max_length=30,default="Inspector")
	rank=models.IntegerField(default=5)
	station=models.ForeignKey(Station,on_delete=models.CASCADE)
	def __str__(self):
		return self.user.username

class Review(models.Model):
	id=models.AutoField(primary_key=True)
	description=models.TextField()
	civilian=models.ForeignKey(User,on_delete=models.CASCADE)
	date_posted=models.DateTimeField()
	station=models.ForeignKey(Station,on_delete=models.CASCADE)


# class Area(models.Model):
#     area = models.CharField(max_length=100)

class Criminal_Record(models.Model):
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        station=models.ForeignKey(Station,on_delete=models.CASCADE)
        criminal_name=models.CharField(max_length=100)
        jail=models.IntegerField(default=0)
        description=models.TextField()
        section=models.TextField()
        fine=models.IntegerField(default=0)



# class PhoneOTP(models.Model):
#      username = models.CharField(max_length=254, unique=True, blank=True, default=False)
#      phone_regex = RegexValidator( regex = r'^\+?1?\d{9,14}$', message = "Phone number must be entered in the form of +919999999999.")
#      name = models.CharField(max_length=254, blank=True, null=True)
#      phone = models.CharField(validators = [phone_regex], max_length=17)
#      otp = models.CharField(max_length=9, blank=True, null=True)
#      count = models.IntegerField(default=0, help_text = 'Number of opt_sent')
#      validated = models.BooleanField(default=False, help_text= 'if it is true, that means user have validate opt correctly in seconds')

#      def __str__(self):
#          return str(self.phone) + ' is sent ' + str(self.otp)