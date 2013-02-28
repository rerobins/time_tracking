"""
time_tracking provides time tracking capabilities to be used in the
django framework.
Copyright (C) 2013 Robert Robinson rerobins@meerkatlabs.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from time_tracking.views import ProjectCreateView, ProjectDetailView
from time_tracking.views import ProjectEditView, ProjectDeleteView
from time_tracking.views import ProjectListView, ProjectCopyView
from time_tracking.views import CategoryCreateView, CategoryDetailView
from time_tracking.views import CategoryEditView, CategoryDeleteView
from time_tracking.views import RecordCreateView, RecordDeleteView
from time_tracking.views import RecordCloseView, RecordEditView
from time_tracking.views import LocationCreateView, LocationDetailView
from time_tracking.views import LocationEditView, LocationDeleteView
from time_tracking.views import LocationListView

urlpatterns = patterns('',

    ## House keeping
    url(r'^license/',
        TemplateView.as_view(template_name="time_tracking/license.html")),

    ## Project manipulation
    url(r'^projects/$', login_required(ProjectListView.as_view()),
        name='project_list_view'),
    url(r'^add/project/$', login_required(
        ProjectCreateView.as_view()),
            name='project_create_view'),
    url(r'^project/(?P<project_slug>[^/]+)/$', login_required(
        ProjectDetailView.as_view()),
        name='project_detail_view'),
    url(r'^edit/project/(?P<project_slug>[^/]+)/$', login_required(
        ProjectEditView.as_view()),
        name='project_edit_view'),
    url(r'^delete/project/(?P<project_slug>[^/]+)/$', login_required(
        ProjectDeleteView.as_view()),
        name='project_delete_view'),
    url(r'^copy/project/(?P<project_slug>[^/]+)/$', login_required(
        ProjectCopyView.as_view()),
        name='project_copy_view'),

    ## Record manipulation
    url(r'^project/(?P<project_slug>[^/]+)/add/$',
        login_required(RecordCreateView.as_view()),
        name='record_create_view'),
    url(r'^project/(?P<project_slug>[^/]+)/delete/(?P<pk>\d+)/$',
        login_required(RecordDeleteView.as_view()),
        name='record_delete_view'),
    url(r'^project/(?P<project_slug>[^/]+)/close/(?P<pk>\d+)/$',
        login_required(RecordCloseView.as_view()),
        name='record_close_view'),
    url(r'^project/(?P<project_slug>[^/]+)/edit/(?P<pk>\d+)/$',
        login_required(RecordEditView.as_view()),
        name='record_edit_view'),

    ## Category manipulation
    url(r'^add/project/(?P<project_slug>[^/]+)/category/$', login_required(
        CategoryCreateView.as_view()),
            name='category_create_view'),
    url(r'^project/(?P<project_slug>[^/]+)/category/'
        + '(?P<category_slug>[^/]+)/$', login_required(
        CategoryDetailView.as_view()),
        name='category_detail_view'),
    url(r'^edit/project/(?P<project_slug>[^/]+)/category/'
        + '(?P<category_slug>[^/]+)/$', login_required(
        CategoryEditView.as_view()),
        name='category_edit_view'),
    url(r'^delete/project/(?P<project_slug>[^/]+)/category/'
        + '(?P<category_slug>[^/]+)/$', login_required(
        CategoryDeleteView.as_view()),
        name='category_delete_view'),

    ## Location manipulation
    url(r'^locations/$', login_required(LocationListView.as_view()),
        name='location_list_view'),
    url(r'^add/location/$', login_required(
        LocationCreateView.as_view()),
            name='location_create_view'),
    url(r'^location/(?P<location_slug>[^/]+)/$', login_required(
        LocationDetailView.as_view()),
        name='location_detail_view'),
    url(r'^edit/location/(?P<location_slug>[^/]+)/$', login_required(
        LocationEditView.as_view()),
        name='location_edit_view'),
    url(r'^delete/location/(?P<location_slug>[^/]+)/$', login_required(
        LocationDeleteView.as_view()),
        name='location_delete_view'),

    ## Reports per Project


)
