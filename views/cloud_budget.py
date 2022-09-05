"""
Services for obtaining information on the budgets given to a particular Address(es)
"""
from typing import Dict, Optional
# libs
from cloudcix_rest.exceptions import Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.models import Address, AddressLink

__all__ = [
    'CloudBudgetResource',
]
EXTRA_FIELDS = ['approved_increase', 'external_cost']


class CloudBudgetResource(APIView):
    """
    Get cloud seller budget details
    """

    def get(self, request: Request, address_id: int) -> Response:
        """
        summary: Get the budget information for all of the User's Addresses, from a specific Address

        description: |
            Get the budget information for all of the requesting User's Addresses.
            If the requesting User is local, this method will only return the details for their own Address.
            If they are global, it will return the details for all Addresses in their Member.

        path_params:
            address_id:
                description: The id of the Address to check budgets with (i.e. reseller address)
                type: integer

        responses:
            200:
                description: |
                     Cloud Budget Details in the form of the address_id as the key and budget amount as the value
                     which can be null.
                content:
                    application/json:
                        schema:
                            type: object
                            additionalProperties:
                                type: object
                                properties:
                                    budget:
                                        type: integer
                                    external_cost:
                                        type: integer
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('get_addresses', child_of=request.span):
            try:
                target_address = Address.objects.get(pk=address_id)
            except Address.DoesNotExist:
                return Http404(error_code='membership_cloud_budget_read_001')

            if request.user.is_global:
                addresses = Address.objects.filter(member_id=request.user.member['id'])
            else:
                addresses = [Address.objects.get(pk=request.user.address['id'])]

        data: Dict[int, Dict[str, Optional[str]]] = {}
        with tracer.start_span('retrieving_address_link_details', child_of=request.span):
            for address in addresses:
                address_data: Dict[str, Optional[str]] = {}
                try:
                    link = AddressLink.objects.get(address=address, contra_address=target_address)
                    contra_link = AddressLink.objects.get(address=target_address, contra_address=address)
                    if link.credit_limit is None and contra_link.credit_limit is None:
                        address_data['budget'] = None
                    else:
                        address_data['budget'] = str(min([
                            link.credit_limit or float('inf'),
                            contra_link.credit_limit or float('inf'),
                        ]))

                    # Get the fields from the extra map
                    for field in EXTRA_FIELDS:
                        address_data[field] = str(
                            link.extra.get('cloud_bill', {}).get(field, 0)
                            + contra_link.extra.get('cloud_bill', {}).get(field, 0),
                        )
                except AddressLink.DoesNotExist:
                    pass

                data[address.id] = address_data

        return Response({'content': data})
