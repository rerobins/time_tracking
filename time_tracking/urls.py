from django.conf.urls import patterns, url
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required

from time_tracking.models import Project
from time_tracking.views import ProjectCreateView, ProjectDetailView
from time_tracking.views import RecordCreateView, RecordDeleteView
from time_tracking.views import RecordCloseView, RecordEditView

urlpatterns = patterns('',

    ## House keeping
    url(r'^license/',
        TemplateView.as_view(template_name="time_tracking/license.html")),

    ## Project manipulation
    url(r'^projects/$', login_required(ListView.as_view(model=Project)),
        name='project_list_view'),
    url(r'^add/project/$', login_required(
        ProjectCreateView.as_view()),
            name='project_create_view'),
    url(r'^projects/(?P<project_slug>[^/]+)/$', login_required(
        ProjectDetailView.as_view()),
        name='project_detail_view'),

    ## Record manipulation
    url(r'^projects/(?P<project_slug>[^/]+)/add/$',
        login_required(RecordCreateView.as_view()),
        name='record_create_view'),
    url(r'^projects/(?P<project_slug>[^/]+)/delete/(?P<pk>\d+)/$',
        login_required(RecordDeleteView.as_view()),
        name='record_delete_view'),
    url(r'^projects/(?P<project_slug>[^/]+)/close/(?P<pk>\d+)/$',
        login_required(RecordCloseView.as_view()),
        name='record_close_view'),
    url(r'^projects/(?P<project_slug>[^/]+)/edit/(?P<pk>\d+)/$',
        login_required(RecordEditView.as_view()),
        name='record_edit_view'),

    ## Category manipulation

    ## Location manipulation

    ## Reports per Project


)
