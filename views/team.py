"""
Manage a Member's Teams
"""

# stdlib
from datetime import datetime
from typing import Optional
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
# local
from membership.controllers import TeamCreateController, TeamListController, TeamUpdateController
from membership.models import Team, TeamUser
from membership.permissions.team import Permissions
from membership.serializers import TeamSerializer

__all__ = [
    'TeamCollection',
    'TeamResource',
]


class TeamCollection(APIView):
    """
    Handles methods regarding Member records that do not require an id to be specified, i.e. list, create
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Team records

        description: |
            Retrieve a list of Team records for the requesting User's Member.

            Teams are one way to group Users in a Member, the others being Departments and Profiles.
            Unlike Departments and Profiles however, a User can be a part of multiple Teams.

        responses:
            200:
                description: A list of Team records, filtered and ordered by the User
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = TeamListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        # No possible way for an error to be thrown here
        with tracer.start_span('retrieving_requested_objects', child_of=request.span):
            objs = Team.list_objects.filter(
                member_id=request.user.member['id'],
                **controller.cleaned_data['search'],
            ).exclude(
                **controller.cleaned_data['exclude'],
            ).order_by(
                controller.cleaned_data['order'],
            )

        with tracer.start_span('generating_metadata', child_of=request.span):
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            metadata = {
                'page': page,
                'limit': limit,
                'order': controller.cleaned_data['order'],
                'total_records': objs.count(),
            }
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = TeamSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Team record

        description: |
            Create a new Team record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Team record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = TeamCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        users: Optional[QuerySet] = controller.cleaned_data.pop('users', None)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        with tracer.start_span('adding_users_to_team', child_of=request.span):
            if users is not None and users.count() > 0:
                TeamUser.objects.bulk_create(
                    (
                        TeamUser(
                            team=controller.instance,
                            user=user,
                        )
                        for user in users.iterator()
                    ),
                    ignore_conflicts=True,
                )

        with tracer.start_span('serializing_data', child_of=request.span):
            data = TeamSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class TeamResource(APIView):
    """
    Handles methods regarding Member records that do require an id to be specified, i.e. read, update, delete
    """
    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Team record

        description: |
            Attempt to read a Team record in the requesting User's Member by the given `pk`, returning a 404 if it does
            not exist

        path_params:
            pk:
                description: The id of the Team record to be read
                type: integer

        responses:
            200:
                description: Team record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Team.objects.get(pk=pk, member_id=request.user.member['id'])
            except Team.DoesNotExist:
                return Http404(error_code='membership_team_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = TeamSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial=False) -> Response:
        """
        summary: Update the details of a specified Team record

        description: |
            Attempt to update a Team record in the requesting User's Member by the given `pk`, returning a 404 if it
            does not exist

        path_params:
            pk:
                description: The id of the Team record to be updated
                type: integer

        responses:
            200:
                description: Team record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Team.objects.get(pk=pk, member_id=request.user.member['id'])
            except Team.DoesNotExist:
                return Http404(error_code='membership_team_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = TeamUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        users: Optional[QuerySet] = controller.cleaned_data.pop('users', None)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('adding_users_to_team', child_of=request.span):
            if users is not None:
                controller.instance.users.clear()
                TeamUser.objects.bulk_create(
                    TeamUser(
                        team=controller.instance,
                        user=user,
                    )
                    for user in users.iterator()
                )

        with tracer.start_span('serializing_data', child_of=request.span):
            data = TeamSerializer(instance=controller.instance).data

        return Response({'content': data})

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempts to partially update a Team
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int) -> Response:
        """
        summary: Delete a specified Team record

        description: |
            Attempt to delete a Team record in the requesting User's Member by the given `pk`, returning a 404 if it
            does not exist

            Unlike Department or Profile, a Team *can* be deleted if there are Users in it, and these Users will be
            removed from it when this happens.

        path_params:
            pk:
                description: The id of the Team record to delete
                type: integer

        responses:
            204:
                description: Team record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                obj = Team.objects.get(pk=pk, member_id=request.user.member['id'])
            except Team.DoesNotExist:
                return Http404(error_code='membership_team_delete_001')

        with tracer.start_span('saving_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        # Remove the Users linked to this team
        with tracer.start_span('removing_users_from_team', child_of=request.span):
            obj.users.clear()

        return Response(status=status.HTTP_204_NO_CONTENT)
