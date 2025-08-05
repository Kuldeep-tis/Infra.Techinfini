"""
URL configuration for test_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from test_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
      
      path('', views.index, name='index'),
      path('admin/', admin.site.urls),
     path('register_user/',views.register_user,name='register_user'),
     path('login_page/',views.login_page,name='login_page'),
     path('login_superadmin/',views.login_superadmin,name='login_superadmin'),
     path('login_page/',views.login_page,name='login_page'),
     path('dashboard/',views.dashboard,name='dashboard'),
     path('add_tool/',views.add_tool,name='add_tool'),
     path('add_tool12/',views.add_tool12,name='add_tool12'),
     path('view_tool/',views.view_tool,name='view_tool'),
     path('delete_tool/',views.delete_tool,name='delete_tool'),
     path('delete_tool12/',views.delete_tool12,name='delete_tool12'),
     path('edit_tool/',views.edit_tool,name='edit_tool'),
     path('edit_tool12/',views.edit_tool12,name='edit_tool12'),
     path('add_employee/',views.add_employee,name='add_employee'),
     path('add_employee12/',views.add_employee12,name='add_employee12'),
     path('view_employee/',views.view_employee,name='view_employee'),

     path('delete_employee12/',views.delete_employee12,name='delete_employee12'),
     path('edit_employee/',views.edit_employee,name='edit_employee'),
     path('edit_employee12/',views.edit_employee12,name='edit_employee12'),

     path('assign_tool/',views.assign_tool,name='assign_tool'),
     path('assign_tool12/',views.assign_tool12,name='assign_tool12'),

     path('unassign_tool/',views.unassign_tool,name='unassign_tool'),
     path('assign_new/',views.assign_new,name='assign_new'),
     path('assign_new12/',views.assign_new12,name='assign_new12'),
     path('history/',views.history,name='history'),
     path('search/',views.search,name='search'),
    
    path('employee_login/',views.employee_login,name='employee_login'),
    path('dashboard_emp/',views.dashboard_emp,name='dashboard_emp'),
        path('edit/',views.edit,name='edit'),
     path('edit12/',views.edit12,name='edit12'),
     path('inventory/',views.inventory,name='inventory'),
     path('assigned/',views.assigned,name='assigned'),
     path('categories/',views.categories,name='categories'),
     path('dashboard_super/',views.dashboard_super,name='dashboard_super'),
     path('change/',views.change,name='change'),
     path('asset_details/',views.asset_details,name='asset_details'),
     path('add_category/',views.add_category,name='add_category'),
     path('edit_category/',views.edit_category,name='edit_category'),
     path('unrepair_tool/',views.unrepair_tool,name='unrepair_tool'),
     path('add_repair/',views.add_repair,name='add_repair'),
     path('repair_table/',views.repair_table,name='repair_table'),
     path('remove_category/',views.remove_category,name='remove_category'),
     path('show_tools/',views.show_tools,name='show_tools'),
     path('add_repair_new/',views.add_repair_new,name='add_repair_new'),
     path('dashboard_redirection/',views.dashboard_redirection,name='dashboard_redirection'),
     path('dashboard_result/',views.dashboard_result,name='dashboard_result'),
     path('edit_category12/',views.edit_category12,name='edit_category12'),
     path('edit_category123/',views.edit_category123,name='edit_category123'),
     path('Addcategory',views.Addcategory,name='Addcategory'),
     path('search_repair/',views.search_repair,name='search_repair'),
     path('search_employee/',views.search_employee,name='search_employee'),
     path('login-all/',views.login_all,name='login-all'),
     path('edit-repair/',views.edit_repair,name='edit-repair'),
     path('edit-repair-id/',views.edit_repair_id,name='edit-repair-id'),
     path('repair-created-by-user',views.repair_created_by_user,name='repair_created_by_user'),
     path('createRepair/',views.createRepair,name= 'createRepair'),
     path('accounts/login-all/', admin.site.urls),
     path('logout/',views. custom_logout_view, name='logout'),
     path('filter-tool/',views.filter_tool,name='filter-tool'),
     path('repairUser/',views.repairUser,name='repairUser'),



                                    
     


        

     
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
