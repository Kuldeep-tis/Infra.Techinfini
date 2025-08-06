    # my_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class superuser(models.Model):
     username=models.CharField(max_length=150)
     password=models.CharField(max_length=150)

# class UserData(AbstractUser):
#     firstname=models.CharField(max_length=150,null=True)
#     role=models.CharField(max_length=250,null=True)
#     approved=models.BooleanField(max_length=250 , default=False)

    


class Employee(models.Model):
      
      employee_name=models.CharField(max_length=150)
      employee_code=models.CharField(max_length=100)
      employee_email=models.CharField(max_length=150, default=1)
      team_name=models.CharField(max_length=150,default=1)
      employee_contact=models.IntegerField(max_length=10, default=1)
      employee_password=models.CharField(max_length=20, default=1)
      employee_department=models.CharField(max_length=150,default=1)
      unique_id = models.AutoField(max_length=150,unique=True, auto_created=True,primary_key=True)
    
      def __str__(self):
          return self.employee_name

class Tools(models.Model):
        
        tool_name = models.CharField(max_length=200)
        
        tool_id= models.CharField(max_length=100, null=True, blank=True )
        tool_category=models.CharField(max_length=150)
       # tool_assigned = models.ForeignKey(Employee, null=True, on_delete=models.SET_NULL,blank=True, default=None)
       
        tool_assigned=models.CharField(max_length=150,null=True)
        assigned_employee_id=models.CharField(max_length=150,null=True)
        tool_avaliability=models.CharField(max_length=10, default='Avaliable')
        tool_company=models.CharField(max_length=150,null=True,default='--')
        tool_model=models.CharField(max_length=150,null=True,default='--')

        tool_purchase=models.CharField(max_length=150,null=True)

        tool_warantty=models.CharField(max_length=150,null=True)
        tool_condition=models.CharField(max_length=150,null=True)
        tool_price=models.IntegerField(max_length=150,null=True, default = -1)
        tool_supplier=models.CharField(max_length=150,null=True)
        tool_invoice=models.IntegerField(max_length=150,null=True)
        tool_location=models.CharField(max_length=150,null=True, default='--')
        tool_remark=models.CharField(max_length=150,null=True, default='--')
        tool_assigneddate=models.DateField(null=True)
        tool_type=models.CharField(max_length=150,null=True,default=1)
        repair_status=models.CharField(max_length=150,null=True, default="Not In Repair")

        
     #    def save(self):
     #     if not self.tool_id:
     #        i
            

     #        last_object=Tools.objects.order_by('-id').first()
     #        next_id= i
     #        i=i+1

            
     #        self.tool_id = f"TIS-CM-{next_id:03d}"  
     #     super().save()




#image = models.ImageField(upload_to='images/', blank=True, null=True, default=None) 
class Details(models.Model):
       asset_id=models.CharField(max_length=150, null=True, default=None)
       asset_name=models.CharField(max_length=150, default= None , null=True)
       employee_id=models.CharField(max_length=150, null=True, default=None)
       employee_name=models.CharField(max_length=150, default=None, null=True)
       is_info=models.CharField(max_length=150, default=None, null=True)
       is_assigned=models.CharField(max_length=150, default="avaliable")
       created_at = models.DateTimeField(auto_now_add=True)
       def __str__(self):
          return self.employee_name
       
class Category(models.Model):
     category_name=models.CharField(max_length=150)
     device_name=models.CharField(max_length=150)
     def __str__(self):
          return self.device_name
     

class Repair(models.Model):
     name=models.CharField(max_length=150)
     repair_tool_id=models.CharField(max_length=150)
     repair_cost=models.CharField(max_length=100,null=True,default='--')
     return_date=models.DateField(null=True)
     tool_user=models.CharField(max_length=150, null=True)
     tool_user_id=models.CharField(max_length=150, null=True)
     repair_person=models.CharField(max_length=150)
     repair_status=models.CharField(max_length=150, default=1)
     repair_created_at = models.DateField(auto_now_add=True)
     repair_created_by=models.CharField(max_length=150,null=True)

class actions(models.Model):
     unique_id=models.CharField(max_length=150,null=True)
     name=models.CharField(max_length=150,null=True)
     is_info=models.CharField(max_length=150,null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     emp_name=models.CharField(max_length=150,null=True)
     emp_code=models.CharField(max_length=150,null=True)


