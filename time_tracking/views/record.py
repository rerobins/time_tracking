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

from django.views.generic import CreateView, DeleteView, UpdateView
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin
from django.http import HttpResponseRedirect
import pytz

from django.shortcuts import get_object_or_404

from time_tracking.views.forms import RecordEditForm
from time_tracking.views.forms import convert_time, RecordCreateForm
from time_tracking.views.project import ProjectDetailView
from time_tracking.models import Project, Record, Category, Location

from django.utils import timezone


class RecordCreateView(CreateView):
    """
        Overrideing the create view in order to store and retrieve the context
        data of the project that the record belongs to.
    """
    form_class = RecordCreateForm
    model = Record

    def post(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the post
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        return super(RecordCreateView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the get
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        #self.initial['start_time'] = timezone.now()
        self.initial['start_time_tz'] = timezone.get_current_timezone()
        self.initial['end_time_tz'] = timezone.get_current_timezone()

        return super(RecordCreateView, self).get(request, *args, **kwargs)

    def get_form(self, form_class):
        """
            Returns an instance of the form to be used in this view.  Overriden
            to limit the categories that are going to be used to the ones that
            are allowed in the currently edited project.
        """
        form = super(RecordCreateView, self).get_form(form_class)

        form.fields['category'].queryset = Category.objects.filter(
            project=self.project)
        form.fields['location'].queryset = Location.objects.filter(
            project=self.project)

        return form

    def get_success_url(self):
        """
            Want the display to be sent back to the URL of the project on
            success.
        """
        return self.project.get_absolute_url()

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.project = self.project

        time = form.instance.start_time
        form.instance.start_time = convert_time(time,
            pytz.timezone(form.instance.start_time_tz))

        if not form.instance.end_time_tz:
            form.instance.end_time_tz = str(timezone.get_current_timezone())

        if form.instance.end_time:
            time = form.instance.end_time
            form.instance.end_time = convert_time(time,
                pytz.timezone(form.instance.end_time_tz))

        return super(RecordCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(RecordCreateView, self).get_context_data(**kwargs)

        context['project'] = self.project
        context['add_new_record'] = True
        context['command'] = 'Add'

        return context    


class RecordEditView(UpdateView):
    """
        Overrideing the create view in order to store and retrieve the context
        data of the project that the record belongs to.
    """
    form_class = RecordEditForm
    model = Record

    def post(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the post
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        return super(RecordEditView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the get
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        return super(RecordEditView, self).get(request, *args, **kwargs)

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form = super(RecordEditView, self).get_form(form_class)

        form.fields['category'].queryset = Category.objects.filter(
            project=self.project)
        form.fields['location'].queryset = Location.objects.filter(
            project=self.project)

        return form

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Record.objects.filter(project=self.project)

    def get_success_url(self):
        """
            Want the display to be sent back to the URL of the project on
            success.
        """
        return self.project.get_absolute_url()

    def form_valid(self, form):
        time = form.instance.start_time
        form.instance.start_time = convert_time(time,
            pytz.timezone(form.instance.start_time_tz))

        if not form.instance.end_time_tz:
            form.instance.end_time_tz = str(timezone.get_current_timezone())

        if form.instance.end_time:
            time = form.instance.end_time
            form.instance.end_time = convert_time(time,
                pytz.timezone(form.instance.end_time_tz))

        return super(RecordEditView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(RecordEditView, self).get_context_data(**kwargs)

        context['project'] = self.project
        context['command'] = 'Edit'

        return context    



class RecordDeleteView(DeleteView):
    """
        Deletes a record from a project.
    """
    model = Record

    def post(self, request, *args, **kwargs):
        """
            Wants to fetch the project that the record is supposed to be
            associated with.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        return super(RecordDeleteView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Wants to fetch the project that the record is supposed to be
            associated with.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        return super(RecordDeleteView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Record.objects.filter(project=self.project)

    def get_success_url(self):
        return self.project.get_absolute_url()
    
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(RecordDeleteView, self).get_context_data(**kwargs)

        context['project'] = self.project

        return context   


class RecordCloseView(View, SingleObjectMixin):
    """
        View that will close the record by placing the end_time into the record
        value.
    """
    model = Record
    return_view = ProjectDetailView

    def get_queryset(self):
        """
            Return the query set that will only return the records owned by the
            current user and referenced by the project.
        """
        return Record.objects.filter(project=self.project)

    def get_redirect_url(self, **kwargs):
        """
            After done manipulating the object want to redirect back to the
            url of the project that was originally being displayed.
        """
        return self.project.get_absolute_url()

    def close(self, request, *args, **kwargs):
        """
            Close the record and return the redirect back to the project that
            fired off the event.
        """
        self.object = self.get_object()
        self.object.close()
        return HttpResponseRedirect(self.project.get_absolute_url())

    def get(self, request, *args, **kwargs):
        """
            Set up some additional class values, and then close the record
            object before redirecting back to the service.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)

        return self.close(request, *args, **kwargs)
