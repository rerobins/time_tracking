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

from django.template.defaultfilters import slugify
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from time_tracking.models import Project, Record, Category, Location
from time_tracking.models import convert_time
import pytz


class ProjectForm(ModelForm):
    """
        Form that will allow for the project object to have its slug overridden
    """

    def clean(self):
        """
            Overriden to validate the model before it is saved to the database,
            want to make sure that there are not two projects owned by the same
            user that have the same name.
        """
        cleaned_data = self.cleaned_data

        ## Make sure that there isn' already a project with the name requested
        ## owned by that user.

        test_slug = slugify(cleaned_data['name'])

        ## Make sure that there isn't already a project with the name requested
        ## owned by that user.
        try:
            project = Project.objects.get(slug=test_slug,
                owner=self.initial['owner'])
        except:
            pass
        else:
            if self.instance.pk and not project.pk == self.instance.pk:
                raise ValidationError("Project with this name already exists")

        return cleaned_data

    class Meta:
        model = Project
        fields = ('name', 'template', 'description', )


class RecordEditForm(ModelForm):
    """
        Form that will allow for the manipulation of the record objects.
    """

    def clean(self):
        cleaned_data = self.cleaned_data

        end_time_tz = timezone.get_current_timezone()

        if 'end_time' in cleaned_data and cleaned_data['end_time'] != None:
            start_time = convert_time(cleaned_data['start_time'],
                pytz.timezone(cleaned_data['start_time_tz']))

            if cleaned_data['end_time_tz']:
                end_time_tz = pytz.timezone(cleaned_data['end_time_tz'])

            end_time = convert_time(cleaned_data['end_time'],
                end_time_tz)

            if end_time < start_time:
                raise ValidationError("End time cannot be before start time")

        return cleaned_data

    class Meta:
        model = Record
        fields = ('start_time', 'start_time_tz', 'end_time', 'end_time_tz',
            'brief_description', 'category', 'location', 'description')
        widgets = {
            'start_time': forms.SplitDateTimeWidget(),
            'end_time': forms.SplitDateTimeWidget(),
        }


class RecordCreateForm(ModelForm):
    """
        Form that will allow for the manipulation of the record objects.
    """

    def clean(self):
        cleaned_data = self.cleaned_data

        end_time_tz = timezone.get_current_timezone()

        if 'end_time' in cleaned_data and cleaned_data['end_time'] != None:
            start_time = convert_time(cleaned_data['start_time'],
                pytz.timezone(cleaned_data['start_time_tz']))

            if cleaned_data['end_time_tz']:
                end_time_tz = pytz.timezone(cleaned_data['end_time_tz'])

            end_time = convert_time(cleaned_data['end_time'],
                end_time_tz)

            if end_time < start_time:
                raise ValidationError("End time cannot be before start time")

        return cleaned_data

    class Meta:
        model = Record
        fields = ('start_time', 'start_time_tz', 'end_time', 'end_time_tz',
            'brief_description', 'category', 'location', 'description')
        widgets = {
            'start_time': forms.SplitDateTimeWidget(),
            'end_time': forms.SplitDateTimeWidget(),
        }

class CategoryForm(ModelForm):
    """
        Form that will allow for the manipulation of the category objects.
    """

    def clean(self):
        """
            Overriden to validate the model before it is saved to the database,
            want to make sure that there are not two categories owned by the
            same user that have the same name.
        """
        cleaned_data = self.cleaned_data

        test_slug = slugify(cleaned_data['name'])

        ## Make sure that there isn' already a project with the name requested
        ## owned by that user.
        try:
            Category.objects.get(slug=test_slug,
                project=self.initial['project'])
        except:
            pass
        else:
            raise ValidationError("Category with this name already exists")

        return cleaned_data

    class Meta:
        model = Category
        fields = ('name', 'description', )


class LocationForm(ModelForm):
    """
        Form that will allow for the location object to have its slug
        overridden
    """

    def clean(self):
        """
            Overriden to validate the model before it is saved to the database,
            want to make sure that there are not two locations owned by the
            same user that have the same name.
        """
        cleaned_data = self.cleaned_data

        test_slug = slugify(cleaned_data['name'])

        ## Make sure that there isn' already a location with the name requested
        ## owned by that user.
        try:
            Location.objects.get(slug=test_slug,
                project=self.initial['project'])
        except:
            pass
        else:
            raise ValidationError("Location with this name already exists")

        return cleaned_data

    class Meta:
        model = Location
        fields = ('name', 'address', 'description', ) 
