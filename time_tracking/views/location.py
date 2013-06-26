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

from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.views.generic import ListView
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from time_tracking.views.forms import LocationForm
from time_tracking.models import Location, Project

from django.shortcuts import get_object_or_404


class LocationListView(ListView):
    """
        List view that will display a list of all of the projects.
    """

    model = Location
    context_object_name = 'locations'

    def get_queryset(self):
        """
            Return the list of active projects to display.
        """
        return self.model.objects.filter(owner=self.request.user)


class LocationCreateView(CreateView):
    """
        Specialized view that will create new project objects.
    """
    form_class = LocationForm
    model = Location
    
    def post(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the post
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        self.initial['project'] = self.project
        return super(LocationCreateView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the get
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        self.initial['project'] = self.project
        return super(LocationCreateView, self).get(request, *args, **kwargs)


    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.project = self.project

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()

        return super(LocationCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(LocationCreateView, self).get_context_data(**kwargs)

        context['project'] = self.project
        context['command'] = 'Add'
        context['add_location'] = True

        return context 


class LocationEditView(UpdateView):
    """
        Specialized view that will edit project objects.
    """
    form_class = LocationForm
    model = Location
    slug_url_kwarg = 'location_slug'

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.owner = self.request.user

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()

        return super(LocationEditView, self).form_valid(form)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return self.model.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            project as well.
        """
        context = super(LocationEditView, self).get_context_data(**kwargs)

        context['project'] = self.project
        context['command'] = 'Edit'

        return context   


class LocationDeleteView(DeleteView):
    """
        Deletes a project.
    """
    model = Location
    slug_url_kwarg = 'location_slug'

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return self.model.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('location_list_view')


class LocationDetailView(DetailView):
    """
        Overriding the Detail View generic class to provide the record
        information that is to be displayed along with the rest of the
        project details.
    """

    model = Location
    slug_url_kwarg = 'location_slug'
    
    def get(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the get
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)

        return super(LocationDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return self.model.objects.filter(project=self.project)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            project as well.
        """
        context = super(LocationDetailView, self).get_context_data(**kwargs)

        context['project'] = self.project

        return context       
