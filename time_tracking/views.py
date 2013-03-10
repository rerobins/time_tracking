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
from django.views.generic import View, ListView
from django.views.generic.detail import SingleObjectMixin
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


from django.shortcuts import get_object_or_404

from time_tracking.forms import ProjectForm, RecordForm, CategoryForm
from time_tracking.forms import LocationForm
from time_tracking.models import Project, Record, Category, Location

from django.utils import timezone


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
        return Project.objects.filter(active=True, owner=self.request.user)

    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(ProjectListView, self).get_context_data(**kwargs)

        deactive_projects = Project.objects.filter(active=False,
            owner=self.request.user)

        context['deactive_projects'] = deactive_projects

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


class ProjectCopyView(CreateView):
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

        return context


class RecordCreateView(CreateView):
    """
        Overrideing the create view in order to store and retrieve the context
        data of the project that the record belongs to.
    """
    form_class = RecordForm
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
        self.initial['start_time'] = timezone.now()
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
        return super(RecordCreateView, self).form_valid(form)


class RecordEditView(UpdateView):
    """
        Overrideing the create view in order to store and retrieve the context
        data of the project that the record belongs to.
    """
    form_class = RecordForm
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
        self.initial['start_time'] = timezone.now()
        return super(RecordEditView, self).get(request, *args, **kwargs)

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        form = super(RecordEditView, self).get_form(form_class)

        form.fields['category'].queryset = Category.objects.filter(
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

        print "%s" % self.owner

        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)

        print "Found Project."

        return self.close(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    """
        Overrideing the create view in order to store and retrieve the context
        data of the project that the record belongs to.
    """
    form_class = CategoryForm
    model = Category

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
        return super(CategoryCreateView, self).post(request, *args, **kwargs)

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
        return super(CategoryCreateView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.project = self.project

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryEditView(UpdateView):
    """
        Overrideing the create view in order to store and retrieve the context
        data of the project that the record belongs to.
    """
    form_class = CategoryForm
    model = Category
    slug_url_kwarg = 'category_slug'

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
        return super(CategoryEditView, self).post(request, *args, **kwargs)

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
        return super(CategoryEditView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Category.objects.filter(project=self.project)

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.project = self.project

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()
        return super(CategoryEditView, self).form_valid(form)


class CategoryDeleteView(DeleteView):
    """
        Deletes a record from a project.
    """
    model = Category
    slug_url_kwarg = 'category_slug'

    def post(self, request, *args, **kwargs):
        """
            Wants to fetch the project that the record is supposed to be
            associated with.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        return super(CategoryDeleteView, self).post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
            Wants to fetch the project that the record is supposed to be
            associated with.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)
        return super(CategoryDeleteView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Category.objects.filter(project=self.project)

    def get_success_url(self):
        return self.project.get_absolute_url()


class CategoryDetailView(DetailView):
    """
        Overriding the Detail View generic class to provide the record
        information that is to be displayed along with the rest of the
        project details.
    """

    model = Category
    slug_url_kwarg = 'category_slug'

    def get(self, request, *args, **kwargs):
        """
            Adding the project object to the base of this view when the get
            is called.
        """
        self.owner = request.user
        self.project = get_object_or_404(Project,
            slug=self.kwargs.get('project_slug', None),
            owner=self.owner)

        return super(CategoryDetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return Category.objects.filter(project=self.project)

    def get_context_data(self, **kwargs):
        """
            Adding additional context for:
                Closed Records - records that have an end time
                Open Records - records that do not have an ned time.
        """
        context = super(CategoryDetailView, self).get_context_data(**kwargs)

        ## Need to fetch the records that are associated with this category.
        open_records = self.object.record_set.filter(end_time=None)

        closed_records = self.object.record_set.exclude(end_time=None)

        context['closed_records'] = closed_records
        context['open_records'] = open_records

        return context


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

    def form_valid(self, form):
        """
            Sets the slug to the correct value based on the name of the object
            that was just created.
        """
        form.instance.owner = self.request.user

        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.name)

        self.object.save()

        return super(LocationCreateView, self).form_valid(form)


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

    def get_queryset(self):
        """
            Limiting the requests to only the objects that are owned by the
            user that is making the request.
        """
        return self.model.objects.filter(owner=self.request.user)
