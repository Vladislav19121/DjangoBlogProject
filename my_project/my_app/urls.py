from django.urls import path
from . import views
urlpatterns = [ 
                
                path('', views.home, name='home'),
                path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
                path('delete_rating/<int:rating_id>/', views.delete_rating, name='delete_rating'),
                path('comment/<int:comment_id>/reply/', views.add_reply, name = 'add_reply'),
                path('reply/delete/<int:reply_id>/', views.delete_reply, name='delete_reply'),
                path('post/<int:post_id>/rate/', views.rating_for_post, name='rating_for_post'),
                path('login/', views.login_view, name = 'login'),
                path('logout/', views.logout_view, name = 'logout'),
                path('registration/', views.registration, name='registration'),
                path('create/', views.create_post, name='create_post'),
                path('post/<int:post_id>/', views.post, name='post'),
                path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
                path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
                path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
               ]