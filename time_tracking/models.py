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
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
import pytz


class Project(models.Model):
    """
        Basic Project object that will group a selection of time records
        together.
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = (('slug', 'owner'),)
        ordering = ['name']

    def get_absolute_url(self):
        """
            Return the URL for the project.
        """
        return reverse('project_detail_view',
            kwargs={'project_slug': self.slug})

    def get_edit_url(self):
        """
            Return URL for editing a project.
        """
        return reverse('project_edit_view',
            kwargs={'project_slug': self.slug})

    def get_delete_url(self):
        """
            Return URL for deleting a project.
        """
        return reverse('project_delete_view',
            kwargs={'project_slug': self.slug})

    def get_add_category_url(self):
        """
            Return URL for adding a category to this project.
        """
        return reverse('category_create_view',
            kwargs={'project_slug': self.slug})

    def get_copy_project_url(self):
        """
            Return URL for copying the project to a new value.
        """
        return reverse('project_copy_view',
            kwargs={'project_slug': self.slug})

    def __unicode__(self):
        """
            Human readable strin representing the project.
        """
        return self.name


class Category(models.Model):
    """
        Category that will allow for the type of work to be documented.
    """
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    class Meta:
        unique_together = (('slug', 'project'),)
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('category_detail_view',
            kwargs={'project_slug': self.project.slug,
                    'category_slug': self.slug})

    def __unicode__(self):
        return self.name


class Location(models.Model):
    """
        Location that can be applied to records to show that the time was spent
        in a specific location.
    """
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)
    location = models.CharField(max_length=255)

    class Meta:
        unique_together = (('owner', 'slug'),)
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('location_detail_view',
            kwargs={'location_slug': self.slug})

    def __unicode__(self):
        return self.name

# Time zone choices for all of the record date time values.
timezone_choices = [(time_zone, time_zone)
    for time_zone in pytz.common_timezones]


class Record(models.Model):
    """
        Model object that will contain information about the start times of
        work on a project and the duration of the amount of time that the
        project was worked on.
    """
    project = models.ForeignKey(Project)
    brief_description = models.CharField(max_length=255, blank=True)
    start_time = models.DateTimeField()
    start_time_tz = models.CharField(max_length=50, choices=timezone_choices)
    end_time = models.DateTimeField(null=True, blank=True)
    end_time_tz = models.CharField(max_length=50, choices=timezone_choices,
        blank=True)
    category = models.ForeignKey(Category, null=True, blank=True,
                on_delete=models.SET_NULL)
    location = models.ForeignKey(Location, blank=True, null=True,
                on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['start_time', 'end_time']

    def close(self):
        """
            Close the record as a completed activity, but only if the record
            doesn't already have an end time defined.
        """
        if self.end_time is None:
            self.end_time = timezone.now()
            self.end_time_tz = timezone.get_current_timezone()

            if self.end_time >= self.start_time:
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

    def get_edit_url(self):
        return reverse('record_edit_view',
            kwargs={'project_slug': self.project.slug,
                    'pk': self.pk})

    def get_delete_url(self):
        return reverse('record_delete_view',
            kwargs={'project_slug': self.project.slug,
                    'pk': self.pk})

    def get_close_url(self):
        return reverse('record_close_view',
            kwargs={'project_slug': self.project.slug,
                    'pk': self.pk})


def convert_time(time_value, timezone_value):
    """
        Converts the time value into the time zone value provided.
    """
    time = timezone.make_naive(time_value, timezone.get_current_timezone())
    time = timezone.make_aware(time, timezone_value)
    return time
