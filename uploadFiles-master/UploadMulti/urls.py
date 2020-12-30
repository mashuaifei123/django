from django.conf.urls import url

from . import views

app_name = 'UploadMulti'

urlpatterns = [
    url(r'^clear/$', views.clear_database, name='clear_database'),
    url(r'^cleartsm/$', views.clear_database_tsm, name='clear_database_tsm'),
    url(r'^clearspss/$', views.clear_database_ss, name='clear_database_ss'),
    url(r'^clearxzx/$', views.clear_database_xzx, name='clear_database_xzx'),
    url(r'^clearword/$', views.clear_database_word, name='clear_database_word'),


    url(r'^pngtoc/$', views.Png_to_csv, name='png_to_c'),
    url(r'^tsmtocode/$', views.tsmtocode, name='tsmtocode'),
    url(r'^tocode2612/$', views.tocode2612, name='tocode2612'),
    url(r'^tocode6236/$', views.tocode6236, name='tocode6236'),
    url(r'^tocode3512/$', views.tocode3512, name='tocode3512'),
    url(r'^tocode2515/$', views.tocode2515, name='tocode2515'),
    # url(r'^wordtopdf/$', views.Word_to_pdf, name='word_to_pdf'),
    url(r'^xueya/$', views.xueya_csv_xlsx, name='xueya_csv_xlsx'),
    url(r'^xindian/$', views.xindian_xlsx_xlsx, name='xindian_xlsx_xlsx'),
    # url(r'^U/(?P<username>[a-zA-Z0-9]+)/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),

    url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    url(r'^tsm-upload/$', views.TsmUploadView.as_view(), name='tsm_upload'),
    url(r'^spss-upload/$', views.SpssUploadView.as_view(), name='spss_upload'),
    url(r'^xzx-upload/$', views.XzxUploadView.as_view(), name='xzx_upload'),
    url(r'^word-upload/$', views.WordUploadView.as_view(), name='word_upload'),
    # url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),

    url(r'^xianzhuxing11/$', views.xianzhuxing11, name='xianzhuxing11'),
    url(r'^xianzhuxing12$', views.xianzhuxing12, name='xianzhuxing12'),
    url(r'^xianzhuxing13$', views.xianzhuxing13, name='xianzhuxing13'),

    url(r'^spss_excel/$', views.spss_excel, name='spss_excel'),
    url(r'^excel_form/$', views.excel_form, name='excel_form'),
    url(r'^search-post$', views.search_post),
    url(r'^get_word$', views.get_word, name='get_word')
]
