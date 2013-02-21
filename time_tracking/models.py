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

from django.db import models
from django_extras.contrib.auth.models import SingleOwnerMixin
from django.contrib.auth.models import User
from django.utils import timezone


class Project(SingleOwnerMixin, models.Model):
    """
        Basic Project object that will group a selection of time records
        together.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    class Meta:
        unique_together = (('slug', 'owner'),)

    @models.permalink
    def get_absolute_url(self):
        return ('project_detail_view', (), {'project_slug': self.slug})

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """
        Category that will allow for the type of work to be documented.
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)


class Location(SingleOwnerMixin, models.Model):
    """
        Location that can be applied to records to show that the time was spent
        in a specific location.
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)
    location = models.CharField(max_length=255)


class Record(SingleOwnerMixin, models.Model):
    """
        Model object that will contain information about the start times of
        work on a project and the duration of the amount of time that the
        project was worked on.
    """
    project = models.ForeignKey(Project)
    brief_description = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    location = models.ForeignKey(Location, blank=True, null=True)

    def close(self):
        """
            Close the record as a completed activity, but only if the record
            doesn't already have an end time defined.
        """
        if self.end_time is None:
            self.end_time = timezone.now()
            self.save()

    def duration(self):
        """
            Determine the amount of time that has occurred in this record value
            in seconds
        """
        if self.end_time is None:
            return 0
        else:
            duration = self.end_time - self.start_time
            return duration.seconds + duration.microseconds / 1E6


