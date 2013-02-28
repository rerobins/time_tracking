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

from django.forms import ModelForm
from django.core.exceptions import ValidationError
from time_tracking.models import Project, Record, Category


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
        try:
            Project.objects.get(name=cleaned_data['name'],
                owner=self.initial['owner'])
        except:
            pass
        else:
            raise ValidationError("Project with this name already exists")

        return cleaned_data

    class Meta:
        model = Project
        fields = ('name', 'active', )


class RecordForm(ModelForm):
    """
        Form that will allow for the manipulation of the record objects.
    """

    class Meta:
        model = Record
#        fields = ('start_time', 'end_time',
#                    'brief_description', 'categories',
#                    'location')
        fields = ('start_time', 'end_time', 'brief_description', 'category')


class CategoryForm(ModelForm):
    """
        Form that will allow for the manipulation of the category objects.
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
        try:
            Category.objects.get(name=cleaned_data['name'],
                project=self.initial['project'])
        except:
            pass
        else:
            raise ValidationError("Category with this name already exists")

        return cleaned_data

    class Meta:
        model = Category
        fields = ('name',)
