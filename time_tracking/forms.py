# -*- coding: utf-8 *-*
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from time_tracking.models import Project, Record


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
        fields = ('name',)


class RecordForm(ModelForm):
    """
        Form that will allow for the manipulation of the record objects.
    """

    class Meta:
        model = Record
        fields = ('start_time', 'end_time', 'brief_description', 'categories',
            'location')
