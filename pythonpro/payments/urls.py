from django.urls import path

from pythonpro.payments import views

app_name = 'payments'
urlpatterns = [
    path('opcoes/', views.options, name='options'),
    path('obrigado/', views.thanks, name='thanks'),
    path('curso-completo-de-python', views.member_landing_page, name='member_landing_page'),
    path('lista-de-espera', views.waiting_list_ty, name='waiting_list_ty'),
    path('pytools/obrigado/', views.pytools_thanks, name='pytools_thanks'),
    path('pytools/captura/', views.pytools_capture, name='pytools_capture'),
    path('pytools/boleto/', views.pytools_boleto, name='pytools_boleto'),
    path('curso-de-python-intermediario', views.client_landing_page, name='client_landing_page'),
    path('pargarme/notificacao/<int:user_id>', views.pagarme_notification, name='pagarme_notification'),
]
