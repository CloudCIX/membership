"""
Management of a Member's Departments
"""

# stdlib
from datetime import datetime
# libs
from cloudcix_rest.exceptions import Http400, Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import (
    DepartmentCreateController,
    DepartmentListController,
    DepartmentUpdateController,
)
from membership.models import Department
from membership.permissions.department import Permissions
from membership.serializers import DepartmentSerializer

__all__ = [
    'DepartmentCollection',
    'DepartmentResource',
]


class DepartmentCollection(APIView):
    """
    Handles methods regarding department records that don't require an id to be specified
    """

    def get(self, request: Request) -> Response:
        """
        summary: Retrieve a list of Department records

        description: |
            Retrieve a list of Department records for the requesting User's Member.

            Departments are one way to group Users in a Member, the others being Profiles and Teams.

        responses:
            200:
                description: A list of Department records, filtered and ordered by the User
        """
        tracer = settings.TRACER

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = DepartmentListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        order = controller.cleaned_data['order']
        warnings = controller.warnings
        with tracer.start_span('retrieving_objects', child_of=request.span):
            # Because the only field in Department is name and name is a char field, there is no possible way this fails
            objs = Department.objects.filter(
                member_id=request.user.member['id'],
                **controller.cleaned_data['search'],
            ).exclude(
                **controller.cleaned_data['exclude'],
            ).order_by(
                order,
            )

        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            metadata = {
                'page': page,
                'limit': limit,
                'order': order,
                'total_records': total_records,
                'warnings': warnings,
            }
            objs = objs[page * limit:(page + 1) * limit]

        with tracer.start_span('serializing_data', child_of=request.span) as span:
            span.set_tag('num_objects', objs.count())
            data = DepartmentSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})

    def post(self, request: Request) -> Response:
        """
        summary: Create a new Department record

        description: |
            Create a new Department record in the requesting User's Member, using the data supplied by the User.

        responses:
            201:
                description: Department record was created successfully
            400: {}
            403: {}
        """
        tracer = settings.TRACER

        # Have Permission checks as early as possible
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.create(request)
            if err is not None:
                return err

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = DepartmentCreateController(data=request.data, request=request, span=span)
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.member_id = request.user.member['id']
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = DepartmentSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_201_CREATED)


class DepartmentResource(APIView):
    """
    Handles methods regarding department records that do require an id to be specified, i.e. read, update, delete
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        summary: Read the details of a specified Department record

        description: |
            Attempt to read a Department record in the requesting User's Member by the given `pk`, returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Department record to be read
                type: integer

        responses:
            200:
                description: Department record was read successfully
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_department_object', child_of=request.span):
            try:
                obj = Department.objects.get(id=pk, member_id=request.user.member['id'])
            except Department.DoesNotExist:
                return Http404(error_code='membership_department_read_001')

        with tracer.start_span('serializing_data', child_of=request.span):
            data = DepartmentSerializer(instance=obj).data

        return Response({'content': data})

    def put(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        summary: Update the details of a specified Department record

        description: |
            Attempt to update a Department record in the requesting User's Member by the given `pk`, returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Department record to be updated
                type: integer

        responses:
            200:
                description: Department record was updated successfully
            400: {}
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        # Have Permission checks as early as possible
        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.update(request)
            if err is not None:
                return err

        with tracer.start_span('retrieving_department_object', child_of=request.span):
            try:
                obj = Department.objects.get(id=pk, member_id=request.user.member['id'])
            except Department.DoesNotExist:
                return Http404(error_code='membership_department_update_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = DepartmentUpdateController(
                instance=obj,
                data=request.data,
                request=request,
                partial=partial,
                span=span,
            )
            if not controller.is_valid():
                return Http400(errors=controller.errors)

        with tracer.start_span('saving_object', child_of=request.span):
            controller.instance.save()

        with tracer.start_span('serializing_data', child_of=request.span):
            data = DepartmentSerializer(instance=controller.instance).data

        return Response({'content': data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, pk: int) -> Response:
        """
        Attempt to partially update a department record
        """
        return self.put(request, pk, True)

    def delete(self, request: Request, pk: int):
        """
        summary: Delete a specified Department record

        description: |
            Attempt to delete a Department record in the requesting User's Member by the given `pk`, returning a 404 if
            it does not exist

        path_params:
            pk:
                description: The id of the Department record to delete
                type: integer

        responses:
            204:
                description: Department record was deleted successfully
            403: {}
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_department_object', child_of=request.span):
            try:
                obj = Department.objects.get(id=pk, member_id=request.user.member['id'])
            except Department.DoesNotExist:
                return Http404(error_code='membership_department_delete_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.delete(request, obj)
            if err is not None:
                return err

        with tracer.start_span('saving_object', child_of=request.span):
            obj.deleted = datetime.now()
            obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
