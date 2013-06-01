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

from time_tracking.models import Project, Location


def time_tracker(request):
    """
        Adds context values for the templates that are provided by the
        application.
    """

    return_value = {}

    if request.user.is_authenticated():
        projects = Project.objects.filter(owner=request.user, active=True)
        return_value['active_projects'] = projects
        
        locations = Location.objects.filter(owner=request.user)
        return_value['locations'] = locations
        
        

    return return_value

