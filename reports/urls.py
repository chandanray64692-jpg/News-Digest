from django.urls import path
from . import views

urlpatterns = [
    path("", views.reports_page, name="reports"),
    path("generate-pdf/", views.generate_pdf, name="generate_pdf"),
    path("executive-summary/", views.executive_summary, name="executive_summary"),
    path("sitrep/", views.sitrep, name="sitrep"),
    path("detail/<int:article_id>/",views.report_detail,name="report_detail"),
    

]