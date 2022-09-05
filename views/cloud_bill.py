"""
Read-only services for data on Currencies supported by CloudCIX
"""

# libs
from cloudcix_rest.exceptions import Http404
from cloudcix_rest.views import APIView
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
# local
from membership.models import Address, AddressLink
from membership.permissions.cloud_bill import Permissions

__all__ = [
    'CloudBillResource',
]


class CloudBillResource(APIView):
    """
    Handles the getting the details needed for CloudBill specific information
    """

    def get(self, request: Request, address_id: int, target_address_id: int) -> Response:
        """
        summary: Get the details required by CloudBill to run from an address to a target address

        description: |
            Attempt to read the Address Link between two IDs and return information required by CloudBill

        path_params:
            address_id:
                description: The id of the Address running CloudBill i.e. region
                type: integer
            target_address_id:
                description: The id of the Address being billed by the address
                type: integer

        responses:
            200:
                description: Cloudbill specific information
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                cloud_customer:
                                    description: |
                                        A flag stating if the target_address_id can build cloud resources in the
                                        address_id(region)
                                    type: boolean
                                customer:
                                    description: |
                                        A flag stating if the target_address_id is a customer of the region
                                    type: boolean
                                is_region:
                                    description: A flag stating if the address_id is a region.
                                    type: boolean
                                reseller_id:
                                    description: |
                                        ID of the Address that is the billing_address_id of the region (sent address_id)
                                        If None, it will default to the sent address_id in the request.
                                tax_rate:
                                    description: |
                                        ID of the TaxRate belonging to address_id to be used as the tax rate in biling.
                                    type: string
            404: {}
        """
        tracer = settings.TRACER

        with tracer.start_span('get_address_objects', child_of=request.span):
            try:
                address = Address.objects.get(pk=address_id)
                target_address = Address.objects.get(pk=target_address_id)
            except Address.DoesNotExist:
                return Http404(error_code='membership_cloud_bill_read_001')

        with tracer.start_span('checking_permissions', child_of=request.span):
            err = Permissions.read(request, address, target_address)
            if err is not None:
                return err

        with tracer.start_span('retrieving_requested_object', child_of=request.span):
            cloud_sellers = AddressLink.objects.filter(
                address__member=address.member,
                contra_address=target_address,
                cloud_customer=True,
            )
            if not cloud_sellers.exists():
                return Http404(error_code='membership_cloud_bill_read_002')
            cloud_seller = cloud_sellers.first()

        with tracer.start_span('get_data', child_of=request.span):
            data = {
                'cloud_customer': cloud_seller.cloud_customer,
                'customer': cloud_seller.customer,
                'is_region': address.cloud_region,
                # TODO: Remove as this is only required until functionality to select reseller is added to IAAS
                'reseller_id': cloud_seller.address.id,
                'tax_rate': cloud_seller.extra_reference1,
            }

        return Response({'content': data})
