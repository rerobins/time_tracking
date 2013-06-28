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
from django.template.defaultfilters import slugify

from django.shortcuts import get_object_or_404

from time_tracking.views.forms import CategoryForm
from time_tracking.models import Project, Category


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
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(CategoryCreateView, self).get_context_data(**kwargs)

        context['project'] = self.project
        context['command'] = 'Add'
        context['add_category'] = True

        return context       


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

    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(CategoryEditView, self).get_context_data(**kwargs)

        context['project'] = self.project
        context['command'] = 'Edit'

        return context        


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
    
    def get_context_data(self, **kwargs):
        """
            Adding additional context to the view in order to show the
            deactivated projects as well.
        """
        context = super(CategoryDeleteView, self).get_context_data(**kwargs)

        context['project'] = self.project

        return context      


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
        context['project'] = self.project
        context['selected'] = self.object

        return context


