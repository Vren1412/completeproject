from django.contrib import admin
from django.urls import path,include
from MRECWBOOK import views as mainView
from users import views as usr
from admins import views as admins
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path("", mainView.index, name='index'),
    path("index/", mainView.index, name="index"),
    path("UserLogin/", mainView.UserLogin, name="UserLogin"),
    path("AdminLogin/", mainView.AdminLogin, name="AdminLogin"),
    path("UserRegister/", mainView.UserRegister, name="UserRegister"),

    path("UserRegisterAction/", mainView.UserRegisterAction, name="UserRegisterAction"),
    path("UserLoginAction/", mainView.UserLoginAction, name="UserLoginAction"),
    path("AdminLoginActions/", mainView.AdminLoginActions, name="AdminLoginActions"),

    path("logout/", mainView.logout, name="logout"),
    path("base/", mainView.base, name="base"),

    #user  
    path("UserHome/", usr.UserHome, name="UserHome"),
    path('SearchBooks/', usr.SearchBooks,name='SearchBooks'),
    path('viewBooks/', usr.viewBooks,name='viewBooks'),
    path('AddToCart/', usr.AddToCart,name='AddToCart'),
    path('ViewCart/', usr.ViewCart,name='ViewCart'),
    path('DeleteCartItem/<int:id>/', usr.DeleteCartItem, name='DeleteCartItem'),
    path('IncreaseQty/<int:id>/', usr.IncreaseQty, name='IncreaseQty'),
    path('DecreaseQty/<int:id>/', usr.DecreaseQty, name='DecreaseQty'),

    path('CheckOut/', usr.CheckOut,name='CheckOut'),
    path('CheckOutAction/', usr.CheckOutAction, name='CheckOutAction'),


    path('Payment/', usr.Payment,name='Payment'),
    path('OrderDetails/', usr.OrderDetails,name='OrderDetails'),
    path('UserLogout/', usr.UserLogout,name='UserLogout'),

    #admin 
    path("AdminHome/", admins.AdminHome, name="AdminHome"),
    path("ViewRegisteredUsers/", admins.ViewRegisteredUsers, name="ViewRegisteredUsers"),
    path("AdminActivaUsers/", admins.AdminActivaUsers, name="AdminActivaUsers"),
    path("AdminDeleteUsers/", admins.AdminDeleteUsers, name="AdminDeleteUsers"),
    path("AddBooks/", admins.AddBooks, name="AddBooks"),
    path("AddBookAction/", admins.AddBookAction, name="AddBookAction"),
    path("ViewBooks/", admins.ViewBooks, name="ViewBooks"),
    


    


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
