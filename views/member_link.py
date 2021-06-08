"""
Management of links between Members (DEPRECATED)
"""

# libs
from cloudcix_rest.exceptions import Http404, Http400
from cloudcix_rest.views import APIView
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.controllers import MemberLinkListController
from membership.models import Member, MemberLink
from membership.serializers import MemberLinkSerializer

__all__ = [
    'MemberLinkCollection',
    'MemberLinkResource',
]


class MemberLinkCollection(APIView):

    def get(self, request: Request, member_id: int) -> Response:
        """
        summary: Retrieve a list of Member Link records for a given Member

        description: |
            Retrieve a list of Member Link objects that involve the specified Member

        path_params:
            member_id:
                description: The id of the Member to fetch link records for
                type: integer

        responses:
            200:
                description: |
                    A list of Member Link records that include the specified Member, filtered and ordered by the User
            400: {}
            404: {}

        deprecated: true
        """
        tracer = settings.TRACER

        with tracer.start_span('retrieving_requested_member_object', child_of=request.span):
            try:
                member = Member.objects.get(id=member_id)
            except Member.DoesNotExist:
                return Http404(error_code='membership_member_link_list_001')

        with tracer.start_span('validating_controller', child_of=request.span) as span:
            controller = MemberLinkListController(data=request.GET, request=request, span=span)
            controller.is_valid()

        with tracer.start_span('retrieving_member_link_objects', child_of=request.span):
            order = controller.cleaned_data['order']
            kw = controller.cleaned_data['search']
            kw['member'] = member
            # will need to change idAddress when new api server is made :)
            if str(request.user.address['id']) != '1':
                kw['member_id'] = request.user.member['id']
            try:
                objs = MemberLink.objects.filter(
                    **kw,
                ).exclude(
                    **controller.cleaned_data['exclude'],
                ).order_by(
                    order,
                )
            except (ValueError, ValidationError):
                return Http400(error_code='membership_member_link_list_002')

        with tracer.start_span('generating_metadata', child_of=request.span):
            total_records = objs.count()
            page = controller.cleaned_data['page']
            limit = controller.cleaned_data['limit']
            warnings = controller.warnings
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
            data = MemberLinkSerializer(instance=objs, many=True).data

        return Response({'content': data, '_metadata': metadata})


class MemberLinkResource(APIView):

    def get(self, request: Request, member_id: int, contra_member_id: int) -> Response:
        """
        summary: Check that a link exists between two specified Members

        description: |
            Return a HTTP 200 if a link exists between the Members with the specified ids, or a 404 or one or both of
             the ids do not correspond to a Member, or a link doesn't exist between the Members

        path_params:
            member_id:
                description: The id of the first Member in the link
                type: integer
            contra_member_id:
                description: The id of the second Member in the link
                type: integer

        responses:
            200:
                description: The two specified Members are linked
                content: none
            404: {}

        deprecated: true
        """
        tracer = settings.TRACER

        # Try to get a MemberLink record between the two specified members
        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            try:
                MemberLink.objects.get(member_id=member_id, contra_member_id=contra_member_id)
            except MemberLink.DoesNotExist:
                return Http404(error_code='membership_member_link_read_001')

        # The response code of 200 shows that there is a link between the two members
        return Response()
