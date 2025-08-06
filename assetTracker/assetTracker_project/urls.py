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
from assetTracker_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [ 
      
      path('', views.index, name='index'),
      path('admin/', admin.site.urls),
     path('register-user/',views.register_user,name='register-user'),
     path('login-page/',views.login_page,name='login-page'),
     path('login_superadmin/',views.login_superadmin,name='login_superadmin'),
     path('login-page/',views.login_page,name='login-page'),
     path('dashboard/',views.dashboard,name='dashboard'),
     path('add-tool/',views.add_tool,name='add-tool'),
     path('add-tool12/',views.add_tool12,name='add-tool12'),
     path('view-tool/',views.view_tool,name='view-tool'),
     path('delete-tool/',views.delete_tool,name='delete-tool'),
     path('delete-tool12/',views.delete_tool12,name='delete-tool12'),
     path('edit-tool/',views.edit_tool,name='edit-tool'),
     path('edit-tool12/',views.edit_tool12,name='edit-tool12'),
     path('add-employee/',views.add_employee,name='add-employee'),
     path('add-employee12/',views.add_employee12,name='add-employee12'),
     path('view-employee/',views.view_employee,name='view-employee'),

     path('delete-employee12/',views.delete_employee12,name='delete-employee12'),
     path('edit-employee/',views.edit_employee,name='edit-employee'),
     path('edit-employee12/',views.edit_employee12,name='edit-employee12'),

     path('assign-tool/',views.assign_tool,name='assign-tool'),
     path('assign-tool12/',views.assign_tool12,name='assign-tool12'),

     path('unassign-tool/',views.unassign_tool,name='unassign-tool'),
     path('assign-new/',views.assign_new,name='assign-new'),
     path('assign-new12/',views.assign_new12,name='assign-new12'),
     path('history/',views.history,name='history'),
     path('search/',views.search,name='search'),
    
    path('employee-login/',views.employee_login,name='employee-login'),
    path('dashboard-emp/',views.dashboard_emp,name='dashboard-emp'),
        path('edit/',views.edit,name='edit'),
     path('edit12/',views.edit12,name='edit12'),
     path('inventory/',views.inventory,name='inventory'),
     path('assigned/',views.assigned,name='assigned'),
     path('categories/',views.categories,name='categories'),
     path('dashboard_super/',views.dashboard_super,name='dashboard_super'),
     path('change/',views.change,name='change'),
     path('asset-details/',views.asset_details,name='asset-details'),
     path('add-category/',views.add_category,name='add-category'),
     path('edit-category/',views.edit_category,name='edit-category'),
     path('unrepair-tool/',views.unrepair_tool,name='unrepair-tool'),
     path('add-repair/',views.add_repair,name='add-repair'),
     path('repair-table/',views.repair_table,name='repair-table'),
     path('remove-category/',views.remove_category,name='remove-category'),
     path('show-tools/',views.show_tools,name='show-tools'),
     path('add-repair-new/',views.add_repair_new,name='add-repair-new'),
     path('dashboard-redirection/',views.dashboard_redirection,name='dashboard-redirection'),
     path('dashboard-result/',views.dashboard_result,name='dashboard-result'),
     path('edit-category12/',views.edit_category12,name='edit-category12'),
     path('edit-category123/',views.edit_category123,name='edit-category123'),
     path('Addcategory',views.Addcategory,name='Addcategory'),
     path('search-repair/',views.search_repair,name='search-repair'),
     path('search-employee/',views.search_employee,name='search-employee'),
     path('login-all/',views.login_all,name='login-all'),
     path('edit-repair/',views.edit_repair,name='edit-repair'),
     path('edit-repair-id/',views.edit_repair_id,name='edit-repair-id'),
     path('repair-created-by-user',views.repair_created_by_user,name='repair_created_by_user'),
     path('createRepair/',views.createRepair,name= 'createRepair'),
     path('accounts/login-all/', admin.site.urls),
     path('logout/',views. custom_logout_view, name='logout'),
     path('filter-tool/',views.filter_tool,name='filter-tool'),
     path('repairUser/',views.repairUser,name='repairUser'),
     path('search-company/',views.search_company,name='search-company'),



                                    
     


        

     
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
