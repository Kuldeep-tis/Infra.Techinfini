from django.shortcuts import render, redirect
from django.contrib import messages
    # myapp/views.py
from django.http import HttpResponse
from django.core.serializers import serialize
    
import json
import datetime
from datetime import datetime
from django.db.models import Max
from django.http import JsonResponse
from .models import Employee,Tools,Details,superuser,Category,Repair,actions
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
import math
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from textblob import TextBlob

def validate(password):
    if len(password) < 8:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in password):
        return False
    return True

def index(request):
  
  return render(request,'landing.html')


def register_user(request):
    
    if request.method == 'POST':
        firstname=request.POST.get('firstname').strip()
        username = request.POST.get('username').strip()



        res = username.count(" ") > 0
        
        raw_password = request.POST.get('password').strip()
        con_password=request.POST.get('confirmpassword').strip()
        email=request.POST.get('email').strip()
        #check=validate(raw_password)

        dict={'firstname':firstname,'username':username,'email':email}
        if (firstname=="" or username=="" or raw_password=="" or con_password=="" or email=="" ):
            dict['msg']="all fields required"
            return render(request,'test_app/register.html',{'value':dict})
        #elif (check!=True):
         #   dict['msg']={"password must conatain 1 ucase lacse digit and of 8 letters"}
          #  return render(request,'test_app/login.html',{'value':dict})
            
        else:
            
            if (raw_password==con_password): 
                
                if User.objects.filter(username=username).exists() or superuser.objects.filter(username=username).exists():
                      dict['msg']="username already exist"
                      dict['username']=""
                      return render(request,'test_app/register.html',{'value':dict})
                elif (res>0):
                    dict['msg']=" username cannot contain space"
                    dict['username']=""
                    return render(request,'test_app/register.html',{'value':dict})
                elif User.objects.filter(email=email).exists():
                      dict['msg']="email already exist"
                      dict['email']=""
                      return render(request,'test_app/register.html',{'value':dict})

                else:
                   
                    
                    user = User(first_name=firstname,username=username,email=email , is_active = False)
                    user.set_password(raw_password)  

                   # user=superuser(username=username,password=raw_password)
                    user.save()
                    #messages.success(request,'registration successsfull')
                    request.session['registerMsg']="Registered Successfully"
                    return redirect('login-all') 
            
            else:
                dict['msg']="password and confirm password does not match"
                return render(request,'test_app/register.html',{'value':dict})
    return render(request, 'test_app/register.html')

def login_page(request):
    
    if request.method=='POST':

        
        username=request.POST.get('username')
        raw_password=request.POST.get('password')
        
    
        
        if (username=="" or raw_password==""):
            return render(request,'test_app/login.html',{'value':"All fields are required"})
        else:

            if CustomUser.objects.filter(username=username).exists():
            
                if CustomUser.objects.filter(username=username,password=raw_password,approved="True").exists():
                  

                  request.session['name']=username
                  return redirect('dashboard')
                elif CustomUser.objects.filter(username=username,password=raw_password,approved="False").exists():
                    
                    return render(request,'test_app/login.html',{'value':"please wait for approval"})
                else:
                 return render(request,'test_app/login.html',{'value':"enter correct username and password"})
            # elif superuser.objects.filter(username=supername).exists():
            #     if superuser.objects.filter(username=supername,password=raw_password).exists():
                  
            #       return redirect('dashboard_super')  
            #     else:
            #         messages.success(request,"wrong credentials")
            #         return redirect('login_superadmin')
            # elif (supername!="None"):
            #     messages.success(request,"wrong credentials")
            #     return redirect('login_superadmin')

            else:
                # messages.success(request,'wrong credentials')
                return render(request,"test_app/login.html",{'value':'wrong credentials'})
    value=request.session.get('registerMsg')
    return render (request,"test_app/login.html",{'value':value})

def login_all(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()



        
        try:
            user = User.objects.get(username=username)
            auth_user = authenticate(request, username=username, password=password)
            print(auth_user)
            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)
                    request.session['name'] = username
                    return redirect('dashboard')
                else:
                    return render(request, 'test_app/login.html', {'msg': "Please wait for approval"})
            else:
                return render(request, 'test_app/login.html', {'msg': "Incorrect username or password"})
        except User.DoesNotExist:
            pass  

        
        if superuser.objects.filter(username=username, password=password).exists():
            request.session['name'] = username
            return redirect('dashboard-super')

        
        if Employee.objects.filter(employee_code=username, employee_password=password).exists():
            request.session['employee_code'] = username
            return redirect('dashboard-emp')

       
        return render(request, 'test_app/login.html', {'msg': "Invalid credentials"})

    return render(request, 'test_app/login.html')

        
def login_superadmin(request):
    
    if request.method=='POST':
        supername=request.POST.get('supername')
        password=request.POST.get('password')
        print(supername)
        print(password)
        if (supername=="" or password==""):
            return render(request,'test_app/login_superadmin.html',{'value':"All fields are required"})
        else:

            if superuser.objects.filter(username=supername).exists():
            
                if superuser.objects.filter(username=supername,password=password).exists():
                  

                  
                  return redirect('dashboard_super')

                else:
                 return render(request,'test_app/login_superadmin.html',{'message':"enter correct username and password"})
            # elif superuser.objects.filter(username=supername).exists():
            #     if superuser.objects.filter(username=supername,password=raw_password).exists():
                  
            #       return redirect('dashboard_super')  
            #     else:
            #         messages.success(request,"wrong credentials")
            #         return redirect('login_superadmin')
            # elif (supername!="None"):
            #     messages.success(request,"wrong credentials")
            #     return redirect('login_superadmin')

            else:
                messages.success(request,'wrong credentials')
                return redirect("login_superadmin")

    return render(request,'test_app/login_superadmin.html')

@login_required
def dashboard(request):
        
             
             total_asset = Tools.objects.count() 
             print(total_asset)
             total_employee = Employee.objects.count() 
             assigned_tool = Tools.objects.filter(tool_avaliability="Assigned").count()
             repair_asset=Repair.objects.filter(repair_status = 'Repair Created').count()
             repair_alert=Tools.objects.filter(repair_status='Created By Employee').count()
             avaliable_asset=Tools.objects.filter(tool_avaliability="Avaliable").count()
             first=request.session.get('name')
             fullName=User.objects.filter(username=first).values('first_name')[0]['first_name']
             latest_action= actions.objects.order_by('-created_at')
             employee_count=Tools.objects.values('tool_assigned').distinct().count()
             print(employee_count)
             emp_no_asset=total_employee-employee_count+1
             latest_action= latest_action[:5]
             print(latest_action)
             return render(request,'test_app/dashboard.html',{'total_asset':total_asset,'total_employee':total_employee,'assigned_asset':assigned_tool,'avaliable_asset':avaliable_asset,
                                                              'repair_tool':repair_asset,
                                                             'fullname':fullName,"tab":"dashboard",'action':latest_action,'emp_no_asset':emp_no_asset ,'repair_alert':repair_alert , 'first':first})
        
@login_required
def add_tool(request):
 
    if request.method=='POST':
        category=request.POST.get('category')
        print(category)
        user=Category.objects.get(category_name=category)
        user1=user.device_name
        my_list = user1.split(',')
        
        default_value = None

        my_dict = dict.fromkeys(my_list, default_value)
        return render(request,'test_app/add_tool.html',{'data':category,'dict':my_dict,'disable':category})


    return render(request,'test_app/add_tool.html')


            
def add_tool12(request):
 if (request.session.get('name')):
    # id = 0
    last_object=Tools.objects.order_by('-id').first()
    if last_object :
      id = last_object.id +1
    else : 
        id = 1

    if request.method == 'POST':
     
   #  request.session['next_id']=166
    # id=request.session.get('next_id')
     #request.session['next_id']=id+1
     name=request.POST.get('tool_name').strip()
    #  print(last_object)
    #  last_object=last_object+1
    
     tool_id=f"TIS-CM- {id}"

     status=request.POST.get('status')
     category=request.POST.get('tool_category')
     
     
                                             #image=request.FILES.get('tool_image')
     company=request.POST.get('company').lower()
     model=request.POST.get('model')
     purchasedate=request.POST.get('purcahsedate')
     print("purchase")
     print(purchasedate)
     
     waraantydate=request.POST.get('warrantydate')
     print("waranty")
     print(waraantydate)
     if waraantydate !="":
       format_1 = "%Y-%m-%d"
       datetime_object = datetime.strptime(waraantydate, format_1)
       current_date = datetime.now() - timezone.timedelta(days=1)
       if (datetime_object<current_date):
          user=Category.objects.get(category_name=category)
          user1=user.device_name
          my_list = user1.split(',')
        
          default_value = None

          my_dict = dict.fromkeys(my_list, default_value)

            
          return render(request,'test_app/add_tool.html',{'category':category,'message':"Cannot give past dates",'dict':my_dict})
     else :
         waraantydate= 'Null'
         
     condition=request.POST.get('condition')
     price_input=request.POST.get('price')
     if price_input:
       price=int(price_input)
     else:
         price=None
     supplier=request.POST.get('supplier')
     invoice_input=request.POST.get('invoice')
     if invoice_input:
         invoice=invoice_input
     else:
         invoice=None
     assigndate=request.POST.get('asigneddate')
     location=request.POST.get('location').lower().strip()
     remark=request.POST.get('remark')


     if (name==""  ):
            messages.success(request,'you can not give name as empty field')
            return redirect('add-tool')

     else: 
         if Tools.objects.filter(tool_id=0).exists():
            messages.success(request,'tool code already exixts')
            return redirect('add-tool')
         

         else:   
            last_object=Tools.objects.filter(tool_id=0)
            if not last_object :      
                
            
                user= Tools(tool_name=name,tool_id=tool_id,tool_category=category,tool_avaliability=status,
                            tool_company=company,tool_model=model,tool_purchase=purchasedate,tool_warantty=waraantydate,
                            tool_condition=condition,tool_price=price,tool_supplier=supplier,tool_invoice=invoice,tool_assigneddate=assigndate,
                            tool_location=location,tool_remark=remark)  
                user.save()  
                
                user1=Details(asset_id=user.tool_id, asset_name=name,is_info="Asset Added")
                user1.save()
                curr= actions(unique_id=tool_id,name=name,is_info="Asset Added")
                curr.save()
                
                if (status=="Assigned"):
                    
                    request.session['already']= user.tool_id
                    return redirect('assigned')
                elif (status=="In-Repair"):
                    request.session['addRepair']= user.tool_id
                    return redirect('add-repair-new')


                
                else:
                   messages.success(request,'tool added succesfully')
                   return redirect('asset-details')
                
            else:
                messages.success(request,'giving same entry as before')
                return redirect('add-tool')
    
    return redirect('add_tool')
 else :
     return redirect(login-all)

@login_required
def view_tool(request):
  
     if request.method=='POST':
         
         searched_data=json.loads(request.body)
         get_name=searched_data.get('search').strip()
         print(get_name)
         if get_name=="":
           data_to_be_searched=Tools.objects.all()
           print(data_to_be_searched)
           filtered_data=list(data_to_be_searched.values('id','tool_name','tool_id','tool_assigned','tool_avaliability','tool_category','assigned_employee_id',))
           return JsonResponse(filtered_data,safe=False)
            
         else:  
        
           filtered_data=Tools.objects.filter(Q(tool_name__icontains=get_name)|Q(tool_name__iexact=get_name) |Q(tool_id__icontains=get_name)|
                                            Q(tool_id__iexact=get_name)|Q(tool_avaliability__icontains=get_name)|Q(tool_avaliability__iexact=get_name)
                                            |Q(tool_category__icontains=get_name)|Q(tool_category__iexact=get_name))
           print(filtered_data)
          # filtered_data=list(data_to_be_searched.values('id','tool_name','tool_id','tool_assigned','tool_avaliability','tool_category','assigned_employee_id',))
           return JsonResponse(filtered_data,safe=False)
     
     data = Tools.objects.all()
     items_per_page = 5 
     total_page=math.ceil(Tools.objects.all().count()/5)
     
     paginator = Paginator(data, items_per_page)
     page_number = request.GET.get('page')
     try:
        page_obj = paginator.get_page(page_number)
     except PageNotAnInteger:
        page_obj = paginator.page(1)
     except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
     context={'page_obj':page_obj,'view':"viewTool",'total':total_page}

    
     return render(request, 'test_app/view_tool.html', context)


def delete_tool(request,id):

    return render(request,'test_app/delete_tool.html')


def delete_tool12(request):
    if request.method=='POST':
       
       idLoad=json.loads(request.body)
       id=idLoad.get('tool_id')
       print(id)
       
   
       curr_asset = Tools.objects.get(tool_id = id)
       

       curr_repair=Repair.objects.filter(repair_tool_id=id)
     
    
       new_entry = Details(asset_id=curr_asset.tool_id, asset_name=curr_asset.tool_name ,
                        employee_id=curr_asset.assigned_employee_id,employee_name=curr_asset.tool_assigned,is_info="Asset Deleted")
       curr=actions(unique_id=curr_asset.tool_id,name=curr_asset.tool_name,is_info='Asset Deleted')
       curr.save()
       new_entry.save()
       curr_asset.delete()
       curr_repair.delete()
       data = Tools.objects.all()
       
       return JsonResponse({'message':'Deleted Successfully'})

@login_required
def edit_tool(request):
    
     if request.method=='POST':
         id= request.POST.get('tool_id')
         request.session['func']=id
         print("id")
         print(id)
     tools=Tools.objects.get(tool_id=id)
     return render(request,'test_app/edit_tool.html',{'tool':tools})


@login_required
def edit_tool12(request):
  
    value=request.session.get('func')
    print(value)

    if request.method == 'POST':
     print('hello')
     new_asset_name=request.POST.get('tool_name').strip()
     print(new_asset_name)
     id=request.POST.get('tool_quantity').strip()
     new_company=request.POST.get('company').lower()
     new_location=request.POST.get('location').lower().strip()
     print(new_location)
     blob = TextBlob(new_company)
     corrected_input = str(blob.correct())
     print("this is correct input")
     print(corrected_input)
     
     new_waraantydate=request.POST.get('warrantydate')
     if new_waraantydate !="":
       format_1 = "%Y-%m-%d"
       datetime_object = datetime.strptime(new_waraantydate, format_1)
       current_date = datetime.now() - timezone.timedelta(days=1)  
               #    if (datetime_object<current_date):
               #         tools=Tools.objects.get(tool_id=value)
               #         return render(request,'test_app/edit_tool.html',{'tool':tools,'message':"Cannot give past dates"})
     else :
         new_waraantydate = 'Null'
     new_status=request.POST.get('status')
     new_price_input=request.POST.get('price')
     if new_price_input:
         new_price=new_price_input
     else:
         new_price=None
     
     new_purchase=request.POST.get('Purchasedate')
     new_assigndate=request.POST.get('asigneddate')
     
     new_remark=request.POST.get('remark')
     tool=Tools.objects.get(tool_id=id)
     if(new_asset_name=="" ):
         messages.success(request,'Name Field Is Required')
         return redirect('edit-tool')
     
         

     else:
     
         Tools.objects.filter(tool_id=id).update(tool_name=new_asset_name,
                            tool_company=new_company,tool_location=new_location, tool_warantty=new_waraantydate,
                            tool_price=new_price,tool_purchase=new_purchase,
                            tool_remark=new_remark)  
         curr_asset = Tools.objects.get(tool_id = value)
         curr_details=Details(asset_id=curr_asset.tool_id,asset_name=curr_asset.tool_name,employee_id=curr_asset.assigned_employee_id,
                              employee_name=curr_asset.tool_assigned,is_assigned=curr_asset.tool_avaliability,is_info="Tool Edited")
         
         curr_action=actions(unique_id=curr_asset.tool_id,name=curr_asset.tool_name,is_info='Asset Edited')
         curr_action.save()
         curr_details.save()
         data = Tools.objects.all()

         messages.success(request,'Tool Edited Succesfully')
         return redirect('asset-details')
    else:
        
     return render(request,'test_app/edit_tool.html')
 

@login_required
def add_employee(request):
  
    return render(request,'test_app/add_employee.html')
 

@login_required
def add_employee12(request):
  
    last_object=Employee.objects.order_by('-unique_id').first()
    if not last_object :
       emp_id = 1
    else  :
     emp_id = last_object.unique_id +1
    print(emp_id)
    if request.method == 'POST':
        id=request.session.get('emp_id')
        #request.session['emp_id']=id+1
      
    
        id=f"TIS-EMP-{emp_id}"



        name=request.POST.get('employee_name').strip()
      #  id=request.POST.get('employee_code').strip()
        contact=request.POST.get('employee_contact').strip()
        mail=request.POST.get('employee_email').strip()
        team=request.POST.get('team_name').strip()
        password=request.POST.get('employee_password')
        department=request.POST.get('employee_department')
        dict={'name':name,'id':id , 'contact':contact, 'mail':mail, 'team':team,'department':department}
        
        if(name=="" or mail=="" or team=="" or password=="" or contact=="" ):
            dict['msg']="all fields required"
            return render(request,'test_app/add_employee.html',{'value': dict})
     


        else:
            k=len(contact)
            use=Employee.objects.filter(employee_code=id).exists()
            use1=Employee.objects.filter(employee_email=mail).exists()
            use2=Employee.objects.filter(employee_contact=contact).exists()
            use3=Employee.objects.filter(employee_password=password).exists()

            if (k!=10 ):
                dict['msg']="enter correct mobile number"
                return render(request,'test_app/add_employee.html',{'value':dict})
            else:
                if use:
                    dict['msg']='employee code already exists'
                    dict['id']=""
                    print(dict)
                    return render(request,'test_app/add_employee.html',{'value':dict})
                elif use1:
                    dict['mail']=""
                    dict['msg']='employee mail already exists'
                    return render(request,'test_app/add_employee.html',{'value':dict})
                elif use2:
                    dict['contact']=""
                    print(dict)
                    dict['msg']='employee contact already exists'
                    return render(request,'test_app/add_employee.html',{'value':dict})
                elif use3:
                    dict['msg']="please give unique passsword"
                    return render(request,'test_app/add_employee.html',{'value':dict})
            
                else:
                 
                    user= Employee(employee_name=name,employee_code=id,employee_email=mail,employee_contact=contact,team_name=team,
                                   employee_password=password,employee_department=department)
                    user.save()  
                    currDetails=Details(employee_name=name,employee_id=id,is_info="Employee Added")
                    curr_action=actions(unique_id=id,name=name,is_info="Employee Added")
                    curr_action.save()
                    currDetails.save()
                    
                    messages.success(request,'Employee Added Successfully')
                    return redirect('view-employee')
                    
    return render(request,'test_app/add_employee.html')

    
@login_required  
def view_employee(request):
     if request.method=='POST':
            print("inside")
            a=json.loads(request.body)
            searched_name = a.get('filter')
            
            

            data=Employee.objects.filter(Q(employee_name__icontains=searched_name) | Q(employee_name__iexact=searched_name) |
                                          Q(employee_code__icontains= searched_name)| Q(employee_department__iexact=searched_name)
                                          |Q(team_name__iexact=searched_name)) 
            print(data)
            searched_data = list(data.values('employee_name','employee_code','employee_contact','employee_email','team_name','employee_department'))
            length= len(searched_data)
            response_data = {
                'searched_data': searched_data,
                'length' : length,
                'filterValue':searched_name,
            }
            
            return JsonResponse(response_data,safe=False)

     data = Employee.objects.all()
     total_page = math.ceil(Employee.objects.all().count()/5)
     
     items_per_page = 5 
     
     paginator = Paginator(data, items_per_page)
     page_number = request.GET.get('page')
     try:
        page_obj = paginator.get_page(page_number)
     except PageNotAnInteger:
        page_obj = paginator.page(1)
     except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

  

     context={'page_obj':page_obj,'emp':'employee','total':total_page}
     return render(request, 'test_app/view_employee.html',context)


def delete_employee12(request):
  if(request.session.get('name')):
    if request.method=='POST':
       
       load_details=json.loads(request.body)

       id=load_details.get('employee_id')
       print(id)
       curr_asset = Employee.objects.filter(employee_code = id)

       curr_delete=Tools.objects.filter(assigned_employee_id=id)
    
       if (len(curr_delete)==0):
         print('inside if')
         b=Employee.objects.get(employee_code=id)
         new_entry = Details(
                employee_id=b.employee_code,employee_name=b.employee_name,is_info="Employee Deleted",is_assigned="Avaliable")
        
         new_entry.save()  
         curr_action=actions(unique_id=b.employee_code,name=b.employee_name,is_info='Employee Deleted')
         curr_action.save()   
       else :
        print('inside else')
    
        for i in curr_delete: 
          curr_tool_id = i.tool_id
          print(curr_tool_id)
          a=Tools.objects.get(tool_id=curr_tool_id)
          b=Employee.objects.get(employee_code=id)

          new_entry = Details(asset_id=a.tool_id, asset_name=a.tool_name ,
                        employee_id=b.employee_code,employee_name=b.employee_name,is_info="Employee Deleted",is_assigned="Avaliable")

          new_entry.save()
       Tools.objects.filter(assigned_employee_id=id).update(assigned_employee_id=None,tool_assigned=None,tool_avaliability="Avaliable")
       curr_asset.delete()
       
       response_data = {
            'success': "success",
            'message': 'Operation completed successfully!',
            'redirect_url': '/view-employee/' 
        }
       return JsonResponse(response_data)
  else :
      return redirect(login-all)    

@login_required
def edit_employee(request):
 
    if request.method=='POST':
      id= request.POST.get('employee_id')
      print(id)
      request.session['edit']=id
    employee=Employee.objects.get(employee_code=id)
    return render(request,'test_app/edit_employee.html',{'employee':employee})


@login_required
def edit_employee12(request):
 
    value=request.session.get('edit')

    print(value)

    if request.method == 'POST':
     
     new_name=request.POST.get('employee_name').strip()
     
     new_mail=request.POST.get('employee_email').strip()
     new_contact=request.POST.get('employee_contact').strip()
     new_team=request.POST.get('team_name').strip()
     new_department=request.POST.get('employee_department')
     k=len(new_contact)
     

     if(new_name=="" or new_mail=="" or new_team==""  ):
        employee=Employee.objects.get(employee_code=value)

        
        return render(request,'test_app/edit_employee.html',{'employee':employee,'msg':"All fields required"})
     elif(Employee.objects.exclude(employee_code=value).filter(employee_contact=new_contact)):
        employee=Employee.objects.get(employee_code=value)

        
        return render(request,'test_app/edit_employee.html',{'employee':employee,'msg':"Contact already exists"})
     elif(Employee.objects.exclude(employee_code=value).filter(employee_email=new_mail)):
        employee=Employee.objects.get(employee_code=value)

        
        return render(request,'test_app/edit_employee.html',{'employee':employee,'msg':"Email already exists"})
     else:
        if(k!=10):
             print("Number is not valid")
             employee=Employee.objects.get(employee_code=value)

             messages.success(request, 'phone number not correct')
             return redirect('edit-employee')
        else :
            
               

            Employee.objects.filter(employee_code=value).update(employee_name=new_name, employee_code=value,employee_email=new_mail,employee_contact=new_contact,
                                                                team_name=new_team,employee_department=new_department)
            user=Tools.objects.filter(assigned_employee_id=value).exists()
            user1=Tools.objects.filter(assigned_employee_id=value)
            curr_action=actions(unique_id=value,name=new_name,is_info="Employee Edited")
            curr_action.save()
            if user :
                  curr=Tools.objects.filter(assigned_employee_id=value).update(tool_assigned=new_name)
                  for i in user1: 
                    tools_id = i.tool_id
                    print(tools_id)
                    a=Tools.objects.get(tool_id=tools_id)
                    new_entry = Details(asset_id=a.tool_id, asset_name=a.tool_name ,
                    employee_id=a.assigned_employee_id,employee_name=a.tool_assigned,is_info="Employee Edited",is_assigned="avaliable")
        
                    new_entry.save()               
            

            messages.success(request,'employee edited successfully')
            return redirect('view-employee')


def unassign_tool(request):
   if request.method=='POST':
    id=request.POST.get('tool_id') 
    message = request.POST.get('message')

    Tools.objects.filter(id=id).update(tool_assigned=None,assigned_employee_id=None)
    Tools.objects.filter(id=id).update(tool_avaliability='Avaliable')
    curr=Tools.objects.get(id=id)
    new_entry = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
                        employee_id=None,employee_name=None,is_info="Asset Unassigned",is_assigned="Avaliable")
    curr_action=actions(unique_id=id,name=curr.tool_name,is_info="Asset Unassigned")
    curr_action.save()
    new_entry.save() 
    data = Tools.objects.all()
    if message == 'view tool':

      messages.success(request,'Asset Unassigned')
      return redirect('view-tool')
    elif message == 'assigned' :
      messages.success(request,'Asset Unassigned')
      return redirect('dashboard-result')

@login_required
def assign_tool(request):

  if request.method=='POST':

    id=request.POST.get('tool_id')
    message = request.POST.get('message')
    request.session['assigned']=id
    
    tool_data=Tools.objects.get(tool_id=id)
    tool=tool_data.tool_id
    
    tool_name=tool_data.tool_name
    data=Employee.objects.all()
    # request.session['tool']=tool
    # request.session['tool_name']=tool_name
    a=1
    request.session['flag']=a

    #return redirect('assign_new')
    return render(request,'test_app/assign_tool.html',{'employee':data,'tool':tool,'tool_name':tool_name,'flag':'flag', 'message' : message})
  id = request.session.get('assigned')
  tool_data=Tools.objects.get(tool_id=id)
  tool=tool_data.tool_id
  tool_name=tool_data.tool_name
  data=Employee.objects.all()
  return render(request,'test_app/assign_tool.html',{'employee':data,'tool':tool,'tool_name':tool_name,'flag':'view tool','message':'view tool'})

@login_required
def assign_tool12(request):

    value = request.session.get('assigned')

    if request.method=='POST':
        
        assigned_to=request.POST.get('employee_code')
        k=assigned_to
        message = request.POST.get('message')
        print(message)
        if k == None :
            messages.success(request,'Employee Id is Required')
            return redirect('assign-tool')
        print(k)
        user1 = Employee.objects.filter(employee_code=assigned_to)

        user = Employee.objects.filter(employee_code=assigned_to).exists()
        ans=Employee.objects.filter(employee_code=assigned_to).values('employee_name')
        print(ans[0])
        name=ans[0]['employee_name']
        
        if user :
          
          Tools.objects.filter(tool_id=value).update(tool_assigned=name)
          Tools.objects.filter(tool_id=value).update(tool_avaliability='Assigned')
          Tools.objects.filter(tool_id=value).update(assigned_employee_id=k)
          curr=Tools.objects.get(tool_id=value)
          curr1=Tools.objects.filter(tool_id=value).values('tool_assigned')
          print(curr1)
          

          new_entry = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
                        employee_id=curr.assigned_employee_id,employee_name=curr.tool_assigned,is_info="Asset Assigned",is_assigned="assigned")
          curr_action=actions(unique_id=curr.tool_id,name=curr.tool_name,is_info="Asset Assigned",emp_name=curr.tool_assigned,emp_code=curr.assigned_employee_id)
          curr_action.save()
          new_entry.save() 


          data = Tools.objects.all()
          if message == 'view tool':
            messages.success(request,'Asset Assigned')
            return redirect('view-tool')
          elif message == 'avaliable':
            messages.success(request,'Asset Assigned')
            return redirect('dashboard-result')
        else:
            
            return render(request,'test_app/assign_tool.html',{'value':"this employee is not in our database"})
   

@login_required
def assign_new(request):

    tool=Tools.objects.exclude(tool_avaliability ='In-Repair')
    employee=Employee.objects.all()
    # tool1=request.session.get('tool')

    return render(request,'test_app/assign_new.html',{'tool':tool,'employee':employee ,'assign':"assign"})

@login_required
def assign_new12(request):

    if request.method=='POST':
        tool_id=request.POST.get('tool_assign')
        print(tool_id)
        employee_id=request.POST.get('employee_code')
        print(employee_id)
        if (employee_id == None) :
            messages.success(request, 'Employee Id is Required')
            return redirect ('assign-new')
        employee_name=Employee.objects.get(employee_code=employee_id)
        name=employee_name.employee_name
        date=request.POST.get('date')
        k=employee_id
        i=tool_id
        print(i)

        Tools.objects.filter(tool_id=tool_id).update(tool_assigned=name)
        Tools.objects.filter(tool_id=tool_id).update(tool_avaliability="Assigned")
        Tools.objects.filter(tool_id=tool_id).update(assigned_employee_id=k)
        Tools.objects.filter(tool_id=tool_id).update(tool_assigneddate=date)

        curr=Tools.objects.get(tool_id=i)
        new_entry = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
                        employee_id=curr.assigned_employee_id,employee_name=curr.tool_assigned,is_info="Asset Assigned",is_assigned="assigned")
        curr_action=actions(unique_id=curr.tool_id,name=curr.tool_name,is_info="Asset Assigned",emp_name=curr.tool_assigned,emp_code=curr.assigned_employee_id)
        curr_action.save()
        new_entry.save() 
        data = Tools.objects.all()
        messages.success(request,'Asset Assigned')
        return redirect('assign-new')

@login_required
def history(request):

  if request.method=='POST':
     id=request.POST.get('tool_id')
     back=request.POST.get('back')
     k=id
     user=Details.objects.filter(asset_id=id).order_by('-created_at')
     if back :
              return render(request,'test_app/history.html',{'data':user,'back':back})

     return render(request,'test_app/history.html',{'data':user})


@login_required
def search(request):

   if request.method=='POST':
      employee_id=request.POST.get('tool_id')
      disable=request.POST.get('disable')
      print(disable)
      
      user=Tools.objects.filter(assigned_employee_id=employee_id)
      if disable :

        return render(request,'test_app/search.html',{'data':user,'disable':disable})
      else :
        
        return render(request,'test_app/search.html',{'data':user})



def employee_login(request):
    
    if request.method=='POST':
        
        
        code=request.POST.get('code')
        request.session['employee_code']=code
        
        raw_password=request.POST.get('password').strip()
        

        if (code=="" or raw_password==""):
            return render(request,'test_app/login.html',{'value':"All fields are required"})
        else:

            if Employee.objects.filter(employee_code=code).exists():
            
                if Employee.objects.filter(employee_code=code,employee_password=raw_password).exists():
            
                  return redirect('dashboard-emp')
                else:
                 return render(request,'test_app/employee_login.html',{'value':"enter correct username and password"}) 
            else:
                return render(request,'test_app/employee_login.html',{'value':"you are not our employee"}) 
    return render (request,"test_app/employee_login.html")


def dashboard_emp(request):
       
       employee_code=request.session.get('employee_code')
       print(employee_code)
       if request.method=='POST':
           load_toolCode=json.loads(request.body)
           get_toolCode=load_toolCode.get('damage')
           print(get_toolCode)
           curr=Tools.objects.get(tool_id=get_toolCode)
           a=curr.assigned_employee_id
           print(a)
        #    new_entry = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
        #                 employee_id=curr.assigned_employee_id,employee_name=curr.tool_assigned,is_info="Under Repair",is_assigned="In-Repair")
        #    new_entry.save()
           Tools.objects.filter(tool_id=get_toolCode).update(repair_status="Created By Employee")
        #    new_entry=Repair(name=curr.tool_name,repair_tool_id=get_toolCode,
        #                  tool_user=curr.tool_assigned,tool_user_id=curr.assigned_employee_id,repair_created_by="Employee")
        #    new_entry.save()
           data_to_be_sent=Tools.objects.filter(assigned_employee_id=curr.assigned_employee_id)
           filtered_data=list(data_to_be_sent.values('id','tool_name','tool_id','tool_category','tool_avaliability','repair_status'))
           return JsonResponse(filtered_data,safe=False)


       user=Tools.objects.filter(assigned_employee_id=employee_code)
       user1=Employee.objects.filter(employee_code=employee_code)
       repair_data=Repair.objects.filter(tool_user_id=employee_code)
       
       if user:
                  return render(request,'test_app/search_emp.html',{'data':user,'value':employee_code,'data1':user1,'repair_data':repair_data})
       else:
            return render(request,'test_app/search_emp.html',{'ans':1,'value':employee_code,'data1':user1})


def edit(request):
  if (request.session.get('name')) :
    if request.method=='POST':
      id= request.POST.get('employee_id')
      print(id)
      request.session['employeedit']=id
      
      
    employee=Employee.objects.get(employee_code=id)
    return render(request,'test_app/edit.html',{'employee':employee})
  else :
     return redirect(login-all)


def edit12(request):
 if (request.session.get('name')) :
    
    value=request.session.get('employeedit')
    print(value)
    
    
    

    if request.method == 'POST':
     
     new_name=request.POST.get('employee_name')
     new_code=request.POST.get('employee_code')
     print(new_code)
     
     new_mail=request.POST.get('employee_email')
     new_contact=request.POST.get('employee_contact')
     new_team=request.POST.get('team_name')
     k=len(new_contact)
     

     if(new_name=="" or new_mail=="" or new_team==""  ):
        employee=Employee.objects.get(employee_code=value)

        messages.success(request,'all fields required')
        return redirect('edit-employee')
     
     else:
        if(k!=10):
             print("Number is not valid")
             employee=Employee.objects.get(employee_code=value)

             messages.success(request, 'phone number not correct')
             return redirect('edit-employee')
        else :
            print("value")
            print(value)
            print("new code")
            print(new_code)

            Employee.objects.filter(employee_code=value).update(employee_name=new_name,employee_email=new_mail,employee_contact=new_contact,team_name=new_team)
            user=Tools.objects.filter(assigned_employee_id=value).exists()
            user1=Tools.objects.filter(assigned_employee_id=value)

            answers=list(user1)
            if user :
                  curr=Tools.objects.filter(assigned_employee_id=value).update(tool_assigned=new_name)
                  for i in answers: 
                    tools_id = i.tool_id
                
                    a=Tools.objects.get(tool_id=tools_id)
                
                    new_entry = Details(asset_id=a.tool_id, asset_name=a.tool_name ,
                    employee_id=a.assigned_employee_id,employee_name=a.tool_assigned,is_info="Employee Edited",is_assigned=a.tool_avaliability)
        
                    new_entry.save()      
            

            messages.success(request,'employee edited successfully')
            return redirect('dashboard-emp')
 else :
    return redirect(login-all)

@login_required
def inventory(request):
  
    data=Category.objects.all()
    return render(request,'test_app/categories.html',{'value':data , 'invent':"invent"})



def assigned(request):
  
    if request.method=='POST':
        
        tool_id=request.POST.get('tool_id')
        print(tool_id)
        employee_id=request.POST.get('employee_code')
        date=request.POST.get('date')
        k=employee_id
        employee_name=Employee.objects.get(employee_code=employee_id)
        name=employee_name.employee_name
        
        Tools.objects.filter(tool_id=tool_id).update(tool_assigned=name)
        Tools.objects.filter(tool_id=tool_id).update(tool_avaliability="Assigned")
        Tools.objects.filter(tool_id=tool_id).update(assigned_employee_id=k)
        Tools.objects.filter(tool_id=tool_id).update(tool_assigneddate=date)
        curr=Tools.objects.get(tool_id=tool_id)
        new_entry = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
                        employee_id=curr.assigned_employee_id,employee_name=curr.tool_assigned,is_info="Asset Assigned",is_assigned="assigned")
        new_entry.save() 
        data = Tools.objects.all()
        messages.success(request,'asset assigned')
        return redirect('view-tool')
    
    employee=Employee.objects.all()
    already=request.session.get('already')
    print(already)
    return render (request,'test_app/assigned.html',{'employee':employee,'data':already})


@login_required
def categories(request):
  
    if request.method=='POST':
        loadName=json.loads(request.body)
        get_name=loadName.get('categoryName')
        request.session['categoryName']=get_name
        return JsonResponse({"message":"success"})
        
        
        # tools=Tools.objects.filter(tool_category=name)
        # return render(request,'test_app/inventory.html',{'data':tools,'value':name})
    return redirect('inventory')


@login_required
def Addcategory(request):
  
    category_name=request.session.get('categoryName') 
    tools=Tools.objects.filter(tool_category=category_name)
    return render(request,'test_app/inventory.html',{'data':tools,'value':category_name})


def dashboard_super(request):
    user=User.objects.all()
    return render(request,'test_app/dashboard_super.html',{'data':user})


def change(request):
  
    if request.method=='POST':
        ans=request.POST.get('approved')
        username=request.POST.get('username')
        
        print(ans)
        if(ans=="False"):
          
          User.objects.filter(username=username).update(is_active=True)
          password=User.objects.get(username=username).password

          

          return redirect('dashboard_super')
        else:
                      User.objects.filter(username=username).update(is_active=False)
                      return redirect('dashboard-super')
 

@login_required
def asset_details(request):
 
  if request.method=='POST':
      searched_data=json.loads(request.body)
      get_name=searched_data.get('search')
      print(get_name)
      if get_name=="":
          filtered_data=Tools.objects.all()
          
          data_to_be_sent=list(filtered_data.values('tool_name','tool_id','tool_category','tool_assigned','assigned_employee_id','tool_avaliability',
                                                'tool_company','tool_model','tool_purchase','tool_warantty','tool_condition',
                                                'tool_price','tool_supplier','tool_invoice','tool_location','tool_remark','tool_assigneddate','tool_type'))
          response_data = {
                'searched_data': data_to_be_sent

            }
          return JsonResponse(response_data,safe=False)
      else:
         filtered_data=Tools.objects.filter(Q(tool_name__icontains=get_name)|Q(tool_name__iexact=get_name) |Q(tool_id__icontains=get_name)|
                                            Q(tool_id__iexact=get_name)|Q(tool_avaliability__icontains=get_name)|Q(tool_avaliability__iexact=get_name)
                                            |Q(tool_category__icontains=get_name)|Q(tool_category__iexact=get_name))
        
         data_to_be_sent=list(filtered_data.values('id','tool_name','tool_id','tool_category','tool_assigned','assigned_employee_id','tool_avaliability',
                                                'tool_company','tool_model','tool_purchase','tool_warantty','tool_condition',
                                                'tool_price','tool_supplier','tool_invoice','tool_location','tool_remark','tool_assigneddate','tool_type'))
         response_data = {
                'searched_data': data_to_be_sent

            }
         return JsonResponse(response_data,safe=False)
  data=Tools.objects.all()

  items_per_page = 5
  total_page = math.ceil(Tools.objects.all().count()/items_per_page)

  paginator = Paginator(data, items_per_page)
  page_number = request.GET.get('page')

  try:
         page_obj = paginator.get_page(page_number)

  except PageNotAnInteger:
         page_obj = paginator.page(1)


  except EmptyPage:
         page_obj = paginator.page(paginator.num_pages)

  data = Category.objects.all()
  value= data.values('device_name')
  category=data.values('category_name')
  location = Tools.objects.values('tool_location').distinct()
  company = Tools.objects.values('tool_company').distinct()
  max_ = Tools.objects.aggregate(Max('tool_price'))
  print("max_price")
  max_price = max_['tool_price__max']
  if max_price == None :
      max_price = 0
  

  
  
  a=0
  b=0
  c=0
  d=0
  e=0
  my_list =[]
  category_list= []
  location_list = []
  company_list = []
  condition = ['New' , 'Average' , 'Bad']
  avaliability = ['Avaliable' , 'Assigned' , 'In-Repair']

  

  for k in company :
      user = company[d]['tool_company']
      d=d+1
      company_list.append(user)
  
#   company_list.remove('')
  company_list.sort()

  for l in category :
    user = category[b]['category_name']
    b = b+1  
    category_list.append(user) 

 
  for j in value :
     
    user = value[a]['device_name']
    a= a+1  
    my_list.append(user.split(',')) 
 
  tool_list = []
  for sublist in my_list:
    for item in sublist:
        tool_list.append(item)
 
  top_five_tools = tool_list[:5]
  top_five_category = category_list[:5]
 
  top_five_company = company_list[:5]
  print(top_five_company)

  for i in location :
     user = location[c]['tool_location']
     c = c+1
     location_list.append(user)
#   location_list.remove('')
  len_of_tool_list = len(tool_list)
  len_of_tool_category =len(category_list)
  len_of_location = len(location_list)
  len_of_company = len(company_list)
  top_five_location = location_list[:5]
  print(top_five_location)
  context={'page_obj':page_obj, 'details':'details','total':total_page,'tool_list':tool_list,'tool_category':category_list ,
            'top_five_tools':top_five_tools , 'location_list' : location_list , 'len_of_tools' : len_of_tool_list , 
            'len_of_category' : len_of_tool_category , 'len_of_location' : len_of_location ,
             'condition' : condition , 'top_five_category' : top_five_category , 'top_five_location' : top_five_location  ,
             'avaliability' :  avaliability , 'tool_company' : company_list , 'top_five_company' : top_five_company ,
               'len_of_company': len_of_company , 'max_price' : max_price}
  return render(request,'test_app/asset_details.html' ,context)


@login_required
def add_category(request):
  
    if request.method=='POST':
        category=request.POST.get('add_category').strip()
        
        device_input=request.POST.get('device_name').strip()
        if device_input[-1]==',':
            device_input=device_input[:-1]
        
        lower_category=category.capitalize()
        if device_input=="" or category=="" :
            return render(request,'test_app/add_category.html',{'msg':"All fields are required"})

    
        input_device=[]
        my_devices=device_input.split(',')
        for i in my_devices:
            a=i.lower()
            input_device.append(a)
        
        
        if len(my_devices)==0:
            return render(request,'test_app/add_category.html',{'msg':"all fields are required"})
        existingDevice=set()
        all_devices=Category.objects.all()
        
        for i in all_devices:
           # i_devices=[d.strip().lower() for d in i.device_name.split(',') if d.strip()]
           ll=[]
           all_list=i.device_name.split(',') 
           print(all_list)
           for j in all_list:
            
               a=j.lower()
               ll.append(a)

               existingDevice.update(ll)
           
        
        common = set(input_device) & existingDevice
        
        commanString = ", ".join(common)
        
        
   
        if len(common)>0:
                return render(request,'test_app/add_category.html',{'msg':commanString,'msg1':" are already in different category",'category_name':category,'device_name':device_input})

        
        if Category.objects.filter(category_name=lower_category).exists():
            
            return render (request,'test_app/add_category.html',{'msg':"Category Name Already Exists"})
        else :
         user=Category(category_name=lower_category,device_name=device_input)
         user1= Details(asset_name=lower_category ,is_info='Category Added')
         curr= actions(name=lower_category ,is_info='Category Added')
         curr.save()
         user.save()
         user1.save()
         messages.success(request,'Category Added Successfully')
         return redirect('inventory')
    return render (request,'test_app/add_category.html')

@login_required
def edit_category12(request) :

    if request.method=='POST':
        
        categoryLoad=json.loads(request.body)
        getCategory=categoryLoad.get('categoryName')
        print(getCategory)
        request.session['categoryName']=getCategory
        print("yes")
        redirect_url='/edit_category/'
        return JsonResponse({"message": "success"})


@login_required
def edit_category(request):

    
    device_input=request.session.get('categoryName')
    deviceName=Category.objects.filter(category_name=device_input).values('device_name')[0]['device_name']
    return render(request,'test_app/edit_category.html',{'categories':device_input,'deviceName':deviceName})


@login_required
def edit_category123(request):

     if request.method=='POST':
        extract_details=json.loads(request.body)
        category=extract_details.get('category').strip()
        original_category=extract_details.get('orgname')
        device_input=extract_details.get('device').strip()
        lower_category=category.capitalize()
        if device_input[-1]==',':
            device_input=device_input[:-1]

        if (Category.objects.exclude(category_name=original_category).filter(category_name=lower_category).exists()):
            response_data = {
            'success': False,
            
            'message':"Category name already exists",
            
        }
            return JsonResponse(response_data)
        
        input_device=[]
        my_devices=device_input.split(',')
        for i in my_devices:
            a=i.lower()
            input_device.append(a)
        
        print(input_device)

        if device_input=="" or category=="":
            
            response_data = {
            'success': False,
            
            'message':"All Fields Are Required",
            
        }
            return JsonResponse(response_data)
        existingDevice=set()
        all_devices=Category.objects.all()
        
        for i in all_devices:
           
           if i.category_name==original_category:
              continue
           else:
                ll=[]
                all_list=i.device_name.split(',') 
                print(all_list)
                for j in all_list:
            
                    a=j.lower()
                    ll.append(a)
                    existingDevice.update(ll)
                print(ll)
        
        common = set(input_device) & existingDevice
        commanString = ", ".join(common)
        print(common)
        if len(common)>0:
                print("inside if")
                response_data = {
            'success': False,
            'common_tools':commanString,
            'message':" are already there",
            
        }
                return JsonResponse(response_data)
                # return render(request,'test_app/add_category.html',{'msg':common,'msg1':"These Device are already there"}) 
    
        else:
 
            Category.objects.filter(category_name=original_category).update(category_name=lower_category,device_name=device_input)
            curr = actions(name=original_category,is_info='Category Edited')
            curr.save()
            response_data = {
            'success': True,
            'message': 'Operation completed successfully!',
            'redirect_url': '/inventory/' 
        }
            return JsonResponse(response_data)
            



        
  #  all_categories=Category.objects.all()

   # return render(request,'test_app/edit_category.html',{'categories':all_categories})

@login_required
def unrepair_tool(request):
  
    if request.method=='POST':
        loadTool=json.loads(request.body)
        tool_id=loadTool.get('tool_id')
        
        print(tool_id)
        # form_tool_id=request.POST.get('tool_id')
        # if form_tool_id == 'None':
        #     tool_id=form_tool_id
        # else :
        #     tool_id=form_tool_id
        flag=loadTool.get('flag')
        print(flag)
        values=Tools.objects.filter(tool_id=tool_id)
        
        toolDetails=Tools.objects.get(tool_id=tool_id)
        status=toolDetails.tool_assigned
        

        if(status== None):
           Tools.objects.filter(tool_id=tool_id).update(tool_avaliability='Avaliable', repair_status = 'Not In Repair')
        else:
           Tools.objects.filter(tool_id=tool_id).update(tool_avaliability='Assigned',repair_status="Not In Repair")


        Repair.objects.filter(repair_tool_id=tool_id).update(repair_status='Not In Repair')
        
        curr=Tools.objects.get(tool_id=tool_id)
        new_entry = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
                        employee_id=curr.assigned_employee_id,employee_name=curr.tool_assigned,is_info="Repair Done",is_assigned="Avaliable")
        curr_action=actions(unique_id=curr.tool_id,name=curr.tool_name,is_info="Repair Done")
        curr_action.save()
        new_entry.save() 
        if flag:
            response_data = {
            'success': "success",
            'message': 'Operation completed successfully!',
            'redirect_url': '/repair-table/' 
              }
            return JsonResponse(response_data)
        else :
           response_data = {
            'success': "success",
            'message': 'Operation completed successfully!',
            'redirect_url': '/view_tool/' 
              }
           return JsonResponse(response_data)
        # else:
        #   messages.success(request,'Repair done successfully')

        #   return redirect('repair_table')


@login_required
def add_repair(request):
  
    if request.method=='POST':

        tool_id=request.POST.get('tool_id')
        print(tool_id)
        if tool_id == None:
            return render(request,'test_app/repair.html',{'msg':"Enter a valid Tool Id"})
        cost=request.POST.get('cost')
        return_date=request.POST.get('date')
        format_1 = "%Y-%m-%d"
        datetime_object = datetime.strptime(return_date, format_1)
        current_date = datetime.now() - timezone.timedelta(days=1)
        repair_person=request.POST.get('repair_person').strip()
        curr_repair_user=Tools.objects.get(tool_id=tool_id)       
        tool_name=curr_repair_user.tool_name
        employee_id=curr_repair_user.assigned_employee_id
        employee_name=curr_repair_user.tool_assigned
        if (datetime_object<current_date):
            data=Tools.objects.exclude(tool_avaliability="In-Repair")
            addRepair=request.session.get('addRepair')
            return render(request,'test_app/repair.html',{'data':data,'tool_name':addRepair,'msg':"Cannot give past dates",'repair_person':repair_person,'cost':cost,})
        elif (int(cost)<0):
            data=Tools.objects.exclude(tool_avaliability="In-Repair")
            addRepair=request.session.get('addRepair')
            return render(request,'test_app/repair.html',{'data':data,'tool_name':addRepair,'msg':"Cannot enter negative cost",'repair_person':repair_person,'date_time':datetime_object })
        elif (repair_person==''):
            data=Tools.objects.exclude(tool_avaliability="In-Repair")
            addRepair=request.session.get('addRepair')
            return render(request,'test_app/repair.html',{'data':data,'tool_name':addRepair,'msg':"Repair Person Name Is Required",'repair_person':repair_person,'date_time':datetime_object,'cost':cost})

        else :
            curr=Tools.objects.get(tool_id=tool_id)
            new_entry = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
                            employee_id=curr.assigned_employee_id,employee_name=curr.tool_assigned,is_info="Under Repair",is_assigned="In-Repair")
            curr_action=actions(unique_id=curr.tool_id,name=curr.tool_name,is_info="Repair Created")
            curr_action.save()
            new_entry.save() 
            
            Tools.objects.filter(tool_id=tool_id).update(tool_avaliability="In-Repair",repair_status="Repair Created By Admin")

            new_entry=Repair(name=tool_name,repair_tool_id=tool_id,repair_cost=cost,return_date=return_date,repair_person=repair_person,
                            tool_user=employee_name,tool_user_id=employee_id,repair_status="Repair Created",repair_created_by="Admin")
            new_entry.save()
            messages.success(request,'Repair Created Successfully')

            return redirect('repair-table')
    data=Tools.objects.exclude(tool_avaliability="In-Repair")
    addRepair=request.session.get('addRepair')
    print(addRepair)
    return render(request,'test_app/repair.html',{'data':data,'tool_name':addRepair})


@login_required
def repair_table(request):

    if request.method=='POST':
        loadsearch=json.loads(request.body)
        searched_name=loadsearch.get('filter')
        curr =Repair.objects.filter(repair_status="Repaired")
        curr.delete()
        data=Repair.objects.filter((Q(name__icontains=searched_name) | Q(name__iexact=searched_name) |
                                          Q(repair_tool_id__icontains= searched_name)| Q(repair_tool_id__iexact=searched_name)
                                          |Q(repair_person__iexact=searched_name) | Q(repair_person__icontains=searched_name)) ,repair_status= "Repair Created")
        print(data)
        #searched_data = list(data.values('name','repair_tool_id','repair_cost','return_date',' tool_user','tool_user_id','repair_person','repair_created_at '))
        searched_data=list(data.values('name','repair_tool_id','repair_cost','return_date','tool_user','tool_user_id','repair_person','repair_created_at','repair_created_by'))
        
            
        return JsonResponse(searched_data,safe=False)
  
     
  





    data=Repair.objects.filter(repair_status="Repair Created",repair_created_by='Admin').order_by('-repair_created_at')
    total_page = math.ceil(data.count()/7)
    items_per_page = 7 
    paginator = Paginator(data, items_per_page)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    print(data)
    msg=request.session.get('repair_msg')
    context={'page_obj':page_obj,'msg':msg , 'table' : 'table' , 'total' : total_page}
    return render(request,'test_app/repair_table.html',context)


@login_required
def remove_category(request):
   
  
   if request.method=='POST':
     
     load_category=json.loads(request.body)
     category_name=load_category.get('categoryName')
     print(load_category)
     current_delete=Category.objects.filter(category_name=category_name)
     current_delete.delete()
     curr= actions(name=load_category,is_info='Category Removed')
     curr.save()
     response_data = {
            'success': True,
            'message': 'Operation completed successfully!',
            'redirect_url': '/inventory/'
        }
     return JsonResponse(response_data)
 




   all_categories=Category.objects.all()

   return render(request,'test_app/remove_category.html',{'categories':all_categories})

@login_required
def show_tools(request):
  
    if request.method=='POST':
        all_tool=json.loads(request.body)
        category_name=all_tool.get('category')
        all_tool_name=Category.objects.filter(category_name=category_name)
    
        all_tool_list=list(all_tool_name.values('device_name'))

        return JsonResponse(all_tool_list,safe=False)


@login_required
def add_repair_new(request):
  
    if request.method=='POST':
        tool_id=request.POST.get('tool_id')
        tool_name=Tools.objects.get(tool_id=tool_id).tool_name
        cost=request.POST.get('cost')
        return_date=request.POST.get('date')
        format_1 = "%Y-%m-%d"
        datetime_object = datetime.strptime(return_date, format_1)
        current_date = datetime.now()
        repair_person=request.POST.get('repair_person')
        if (datetime_object<current_date):
            return render(request,'test_app/add_repair_new.html',{'msg':"Cannot give past dates"})

        new_entry=Repair(name=tool_name,repair_tool_id=tool_id,repair_cost=cost,return_date=return_date,repair_person=repair_person,
                         repair_status="In-Repair")
        new_repair = Details(asset_id=curr.tool_id, asset_name=curr.tool_name ,
                            employee_id=curr.assigned_employee_id,employee_name=curr.tool_assigned,is_info="Under Repair",is_assigned="In-Repair")
        new_entry.save() 
        new_repair.save()
        return redirect('asset-details')
    tool_id=request.session.get('addRepair')
    return render(request,'test_app/add_repair_new.html',{'tool_id':tool_id})


@login_required
def dashboard_redirection(request):
  
    if request.method=='POST':
        load_status=json.loads(request.body)
        status=load_status.get('tool_status')
        print(status)
        request.session['status']=status
        redirect_url='/dashboard-result/'
        return JsonResponse({'redirect_url': redirect_url})



@login_required
def dashboard_result(request):
  
    status = request.session.get('status')
    print(status)

    data = Tools.objects.filter(tool_avaliability=status)

    return render(request, 'test_app/dashboard_redirection.html', {
        'data': data,
        'status': status
    })


@login_required
def search_repair(request):
  if request.method == 'POST' :
    load_value=json.loads(request.body)
    get_value=load_value.get('search')
    print(get_value)
    filtered_data=Tools.objects.exclude(tool_avaliability='In-Repair').filter(Q(tool_id__icontains=get_value) | Q(tool_id__iexact=get_value) | Q(tool_name__icontains=get_value) | Q(tool_name__iexact=get_value))
    print(filtered_data)
    data_to_be_sent=list(filtered_data.values('tool_id','tool_name'))
    return JsonResponse(data_to_be_sent,safe=False)


@login_required
def search_employee(request):
  if request.method == 'POST':
    load_value=json.loads(request.body)
    get_value=load_value.get('search')
    print(get_value)
    filtered_data=Employee.objects.filter(Q(employee_code__icontains=get_value) | Q(employee_code__iexact=get_value) | Q(employee_name__icontains=get_value) | Q(employee_name__iexact=get_value))
    print(filtered_data)
    data_to_be_sent=list(filtered_data.values('employee_code','employee_name'))
    return JsonResponse(data_to_be_sent,safe=False)

@login_required
def edit_repair_id(request):
  
    if request.method=='POST':
        tool_id=request.POST.get('tool_id')
        request.session['tool_id']=tool_id  
        data=Repair.objects.get(repair_tool_id=tool_id, repair_status = 'Repair Created')
        return render(request,'test_app/edit_repair.html',{'tool':data})



@login_required
def edit_repair(request):
  if (request.session.get('name')) :
    if request.method == 'POST':
        tool_id=request.POST.get('tool_id')
        print(tool_id)
        new_cost=request.POST.get('cost')
        new_returndate=request.POST.get('return_date')
        format_1 = "%Y-%m-%d"
        datetime_object = datetime.strptime(new_returndate, format_1)
        current_date = datetime.now() - timezone.timedelta(days=1)
        new_repair_person=request.POST.get('repair_person')
        if (new_cost=="" or new_repair_person==""):
            data=Repair.objects.get(repair_tool_id=tool_id)

            return render (request,'test_app/edit_repair.html',{'tool':data,'msg':"All fields are Required"})
        elif (int(new_cost)<0):
            data=Repair.objects.get(repair_tool_id=tool_id)

            return render (request,'test_app/edit_repair.html',{'tool':data,'msg':"Cannot Give Negative Cost"})
        elif (datetime_object<current_date):
            data=Repair.objects.get(repair_tool_id=tool_id)

            return render (request,'test_app/edit_repair.html',{'tool':data,'msg':"Cannot Give Back Date"})
            
        else:


           Repair.objects.filter(repair_tool_id=tool_id).update(repair_cost=new_cost,return_date=new_returndate,repair_person=new_repair_person)
        
           return redirect('repair-table')
  else :
      return redirect(login-all)    

@login_required
def repair_created_by_user(request):
  
    repair_data=Tools.objects.filter( repair_status='Created By Employee')
    print(repair_data)
    return render (request,'test_app/repairUser.html',{'repair_data':repair_data})


@login_required
def createRepair(request) :

    if request.method == 'POST':
        tool_id = request.POST.get('tool_id')
        name=Tools.objects.get(tool_id = tool_id).tool_name
        return render (request , 'test_app/repair.html', {'tool_id' : tool_id , 'flag':'flag', 'name':name})




def custom_logout_view(request):
    # username = request.GET.get('username')
    # print(username)
    value= request.session.get('name')
    print(value)
    print('hello')

    logout(request)

    # request.session.clear()
    return redirect('login-all')


def filter_tool(request):
   print('hello')
   if request.method == 'POST':
      load_filter_value = json.loads(request.body)
      name = load_filter_value.get('name')
      if(len(name)<1) :
         name=""
      company = load_filter_value.get('company')
      print(company)
      if(len(company) < 1):
          company = ""
      avaliability = load_filter_value.get('avaliablity')
      if(len(avaliability)<1) :
         avaliability=""
      price = load_filter_value.get('price')
      
      condition= load_filter_value.get('condition')
      if(len(condition)<1) :
         condition=""
      category= load_filter_value.get('category')
      if(len(category)<1):
         category=""
      print (category)
      location= load_filter_value.get('location')
      if (len(location) <1) :
         location = ""
      waranty = load_filter_value.get('waranty')
      print(waranty)
      if (len(waranty) < 1) :
           waranty = ""


      print(company)

      if(waranty == "" and price == '0' ):
        data = Tools.objects.filter( (Q(tool_name__icontains = name) | Q(tool_name__in = name) ), (Q(tool_condition__icontains = condition) | Q(tool_condition__in =condition)),
                                    (Q(tool_avaliability__icontains = avaliability) | Q(tool_avaliability__in = avaliability)),
                                    (Q(tool_category__in = category) | Q(tool_category__icontains = category)),
                                    (Q(tool_location__icontains = location) | Q(tool_location__in = location)),
                                   (Q (tool_company__icontains = company) | Q(tool_company__in = company))
                                  )
  
      elif (waranty == "" ):
         print(price)
         data = Tools.objects.filter( (Q(tool_name__icontains = name) | Q(tool_name__in = name) ), (Q(tool_condition__icontains = condition) | Q(tool_condition__in =condition)),
                                    (Q(tool_avaliability__icontains = avaliability) | Q(tool_avaliability__in = avaliability)),
                                    (Q(tool_category__in = category) | Q(tool_category__icontains = category)) , (Q(tool_company__icontains = company) | Q(tool_company__in = company)),
                                    (Q(tool_location__icontains = location) | Q(tool_location__in = location)) ,  tool_price__lt = price)
      
      elif (price == '0')  :   
         data = Tools.objects.filter( (Q(tool_name__icontains = name) | Q(tool_name__in = name) ), (Q(tool_condition__icontains = condition) | Q(tool_condition__in =condition)),
                                    (Q(tool_avaliability__icontains = avaliability) | Q(tool_avaliability__in = avaliability)),
                                    (Q(tool_category__in = category) | Q(tool_category__icontains = category)) , (Q(tool_company__icontains = company) | Q(tool_company__in = company)),
                                      (Q(tool_location__icontains = location) | Q(tool_location__in = location)), 
                                     tool_warantty__lt = waranty )
      
           

      else :     
        
         data = Tools.objects.filter( (Q(tool_name__icontains = name) | Q(tool_name__in = name) ), (Q(tool_condition__icontains = condition) | Q(tool_condition__in =condition)),
                                    (Q(tool_avaliability__icontains = avaliability) | Q(tool_avaliability__in = avaliability)),
                                    (Q(tool_category__in = category) | Q(tool_category__icontains = category)) , (Q(tool_company__icontains = company) | Q(tool_company__in = company)),
                                      (Q(tool_location__icontains = location) | Q(tool_location__in = location)) ,
                                    (Q(tool_warantty__icontains = waranty) | Q( tool_warantty__lt = waranty )) , tool_price__lt = price)
      print(data)
      data_to_be_sent=list(data.values('tool_name','tool_id','tool_category','tool_assigned','assigned_employee_id','tool_avaliability',
                                                'tool_company','tool_model','tool_purchase','tool_warantty','tool_condition',
                                                'tool_price','tool_supplier','tool_invoice','tool_location','tool_remark','tool_assigneddate','tool_type'))
      response_data = {
                'searched_data': data_to_be_sent

            }
      return JsonResponse(response_data,safe=False)

def repairUser(request):
    if request.method == 'POST' :
        print('hello')
        loadsearch=json.loads(request.body)
        searched_name=loadsearch.get('filter')
        print(searched_name)

        data=Tools.objects.filter((Q(tool_name__icontains=searched_name) | Q(tool_name__iexact=searched_name) |
                                          Q(tool_id__icontains= searched_name)| Q(tool_id__iexact=searched_name)
                                          ) ,repair_status= "Created By Employee")
        print(data)
        searched_data=list(data.values('tool_name','tool_id','tool_assigned','assigned_employee_id'))
        print(searched_data)
        
            
        return JsonResponse(searched_data,safe=False)

def search_company(request):
    if request.method == 'POST' :
      print('hello')
      loadText = json.loads(request.body)
      text = loadText.get('tool_filter').strip()
      message  = loadText.get('message').strip()
      if message == 'searchCompany' :      

          print(text)
          company_list = []
          company = Tools.objects.values('tool_company').distinct()
          print(company)
          d=0
          for k in company :
            user = company[d]['tool_company']
            if  user.startswith(text) :
              print(user)
              company_list.append(user)
            d= d+1
          if '' in company_list :
              company_list.remove('') 
          company_list.sort()
          data_to_be_sent = {
              'filtered_data' : company_list,
              'message' : 'company'

              
          }
          return JsonResponse(data_to_be_sent , safe=False)
    if message == 'searchLocation' : 
          print(text)
          location_list = []
          location = Tools.objects.values('tool_location').distinct()
          
          d=0
          for k in location :
            user = location[d]['tool_location']
            if user.startswith(text) :
              print(user)
              location_list.append(user)
            d= d+1
          if '' in location_list :
              location_list.remove('') 
          location_list.sort()
          data_to_be_sent = {
              'filtered_data' : location_list,
              'message' : 'location'

              
          }
          return JsonResponse(data_to_be_sent , safe=False)

    
    

