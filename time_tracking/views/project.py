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

from django.shortcuts import get_object_or_404

from time_tracking.views.forms import ProjectForm
from time_tracking.models import Project, Record, Category, Location


class ProjectListView(ListView):
    """
        List view that will display a list of all of the projects.
    """

    model = Project
    context_object_name = 'active_projects'

    def get_queryset(self):
        """
            Return the list of active projects to display.
        """
        return Project.objects.filter(template=False, owner=self.request.user)

    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(ProjectListView, self).get_context_data(**kwargs)

        deactive_projects = Project.objects.filter(template=True,
            owner=self.request.user)

        context['templates'] = deactive_projects

        return context


class ProjectCreateView(CreateView):
    """
        Specialized view that will create new project objects.
    """
    form_class = ProjectForm
    model = Project

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.owner = self.request.user

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()

        return super(ProjectCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
            Override the get so that the initial object's owner can be set to
            the request user.
        """
        self.initial['owner'] = request.user
        return super(ProjectCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post so that the initial object's owner can be set to
            the request user.
        """
        self.user = request.user
        self.initial['owner'] = request.user
        return super(ProjectCreateView, self).post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(ProjectCreateView, self).get_context_data(**kwargs)

        context['command'] = 'Add'

        return context


class ProjectEditView(UpdateView):
    """
        Specialized view that will edit project objects.
    """
    form_class = ProjectForm
    model = Project
    slug_url_kwarg = 'project_slug'

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.owner = self.request.user

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()

        return super(ProjectEditView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
            Override the get so that the initial object's owner can be set to
            the request user.
        """
        self.user = request.user
        self.initial['owner'] = request.user
        return super(ProjectEditView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post so that the initial object's owner can be set to
            the request user
        """
        self.user = request.user
        self.initial['owner'] = request.user
        return super(ProjectEditView, self).post(request, *args, **kwargs)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Project.objects.filter(owner=self.user)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(ProjectEditView, self).get_context_data(**kwargs)
        
        context['edit_project'] = True
        context['command'] = 'Edit'

        return context    


class ProjectDeleteView(DeleteView):
    """
        Deletes a project.
    """
    model = Project
    slug_url_kwarg = 'project_slug'

    def post(self, request, *args, **kwargs):
        """
            Wants to fetch the project that the record is supposed to be
            associated with.
        """
        self.owner = request.user
        return super(ProjectDeleteView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Wants to fetch the project that the record is supposed to be
            associated with.
        """
        self.owner = request.user
        return super(ProjectDeleteView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Project.objects.filter(owner=self.owner)

    def get_success_url(self):
        return reverse('project_list_view')
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(ProjectDeleteView, self).get_context_data(**kwargs)
        
        context['delete_project'] = True

        return context      


class ProjectCopyView(CreateView):
    """
        Specialized view that will create new project objects.
    """
    form_class = ProjectForm
    model = Project
    template_name = "time_tracking/project_copy.html"

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.owner = self.request.user

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()

        for category in self.source_project.category_set.all():
            new_category = Category()
            new_category.name = category.name
            new_category.slug = category.slug
            new_category.project = self.object
            new_category.save()

        return super(ProjectCopyView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
            Override the get so that the initial object's owner can be set to
            the request user.
        """
        self.initial['owner'] = request.user
        self.source_project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=request.user)
        return super(ProjectCopyView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post so that the initial object's owner can be set to
            the request user.
        """
        self.user = request.user
        self.initial['owner'] = request.user
        self.source_project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=request.user)
        return super(ProjectCopyView, self).post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(ProjectCopyView, self).get_context_data(**kwargs)

        context['project'] = self.source_project
        context['copy_project'] = True
        context['command'] = 'Copy'

        return context
    

class ProjectDetailView(DetailView):
    """
        Overriding the Detail View generic class to provide the record
        information that is to be displayed along with the rest of the
        project details.
    """

    model = Project
    slug_url_kwarg = 'project_slug'

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Project.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        """
            Adding additional context for:
                Closed Records - records that have an end time
                Open Records - records that do not have an ned time.
        """
        context = super(ProjectDetailView, self).get_context_data(**kwargs)

        ## Need to fetch the records that are associated with this project.
        open_records = Record.objects.filter(project=self.object,
            end_time=None)

        closed_records = Record.objects.filter(
            project=self.object
        ).exclude(
            end_time=None)

        context['closed_records'] = closed_records
        context['open_records'] = open_records
        context['project_overview'] = True
        context['locations'] = Location.objects.filter(project=self.object)
        
        categories = {}
        for record in closed_records:
            record_duration = (record.end_time-record.start_time).total_seconds()
            if record.category in categories:
                categories[record.category] += record_duration
            else:
                categories[record.category] = record_duration
                
        context['categories'] = categories

        return context




