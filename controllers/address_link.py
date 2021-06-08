# stdlib
from decimal import Decimal, InvalidOperation
from typing import Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from membership.models import AddressLink, Territory

__all__ = [
    'AddressLinkCreateController',
    'AddressLinkUpdateController',
]


class AddressLinkCreateController(ControllerBase):
    """
    Validates User data used to create a new AddressLink record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this controller
        """
        model = AddressLink
        validation_order = (
            'credit_limit',
            'client',
            'compute',
            'customer',
            'note',
            'reference',
            'service_centre',
            'supplier',
            'territory_id',
            'warrantor',
        )

    def validate_credit_limit(self, credit_limit: Optional[str]) -> Optional[str]:
        """
        description: |
            The agreed credit limit for Financials given to the contra address by the address.
            If set, the credit owed by the contra address to the address cannot exceed this amount.
        type: string
        format: decimal
        required: false
        """
        # Credit limit is optional
        if credit_limit is None:
            self.cleaned_data['credit_limit'] = None
            return None
        # If it was sent, ensure it's a valid Decimal number
        try:
            self.cleaned_data['credit_limit'] = Decimal(credit_limit)
        except InvalidOperation:
            return 'membership_address_link_create_105'
        return None

    def validate_client(self, client: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a client of the Address
        type: boolean
        required: false
        """
        # Client is optional
        if client is None:
            self.cleaned_data['client'] = False
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(client, bool):
            return 'membership_address_link_create_106'
        self.cleaned_data['client'] = client
        return None

    def validate_compute(self, compute: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address can build cloud resources using the Address's infrastructure
        type: boolean
        required: false
        """
        # Compute is optional
        if compute is None:
            self.cleaned_data['compute'] = False
            return None

        # If it was sent, ensure it's a boolean
        if not isinstance(compute, bool):
            return 'membership_address_link_create_107'

        # Make sure the Address can offer compute services to the Contra Address
        if compute and not self.request.user.address['cloud_region']:
            return 'membership_address_link_create_108'
        self.cleaned_data['compute'] = compute
        return None

    def validate_customer(self, customer: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a customer for the Address
        type: boolean
        required: false
        """
        # Customer is optional
        if customer is None:
            self.cleaned_data['customer'] = False
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(customer, bool):
            return 'membership_address_link_create_109'
        self.cleaned_data['customer'] = customer
        return None

    def validate_note(self, note: Optional[str]) -> Optional[str]:
        """
        description: A much larger note about the linked Address to put in the Link record. No length limit.
        type: string
        required: false
        """
        self.cleaned_data['note'] = str(note).strip() if note else ''
        return None

    def validate_reference(self, reference: Optional[str]) -> Optional[str]:
        """
        description: A reference about the linked Address to put in the Link record. Max 20 characters.
        type: string
        required: false
        """
        if not reference:
            reference = ''
        reference = str(reference).strip()
        if len(reference) > self.get_field('reference').max_length:
            return 'membership_address_link_create_101'
        self.cleaned_data['reference'] = reference
        return None

    def validate_service_centre(self, service_centre: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a service centre for the Address
        type: boolean
        required: false
        """
        # Service Centre is optional
        if service_centre is None:
            self.cleaned_data['service_centre'] = False
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(service_centre, bool):
            return 'membership_address_link_create_110'
        self.cleaned_data['service_centre'] = service_centre
        return None

    def validate_supplier(self, supplier: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a supplier for the Address
        type: boolean
        required: false
        """
        # Supplier is optional
        if supplier is None:
            self.cleaned_data['supplier'] = False
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(supplier, bool):
            return 'membership_address_link_create_111'
        self.cleaned_data['supplier'] = supplier
        return None

    def validate_territory_id(self, territory_id: Optional[int]) -> Optional[str]:
        """
        description: The id of a Territory owned by the requesting User's Member to attach to the Link record.
        type: integer
        required: false
        """
        if not territory_id:
            return None
        try:
            territory = Territory.objects.get(pk=int(territory_id))
        except (TypeError, ValueError):
            return 'membership_address_link_create_102'
        except Territory.DoesNotExist:
            return 'membership_address_link_create_103'
        if str(territory.member.pk) != str(self.request.user.member['id']):
            return 'membership_address_link_create_104'
        self.cleaned_data['territory'] = territory
        return None

    def validate_warrantor(self, warrantor: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a warrantor for the Address
        type: boolean
        required: false
        """
        # Warrantor is optional
        if warrantor is None:
            self.cleaned_data['warrantor'] = False
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(warrantor, bool):
            return 'membership_address_link_create_112'
        self.cleaned_data['warrantor'] = warrantor
        return None


class AddressLinkUpdateController(ControllerBase):
    """
    Validates User data used to update an AddressLink record
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = AddressLink
        validation_order = (
            'credit_limit',
            'client',
            'compute',
            'customer',
            'note',
            'reference',
            'service_centre',
            'supplier',
            'territory_id',
            'warrantor',
        )

    def validate_credit_limit(self, credit_limit: Optional[str]) -> Optional[str]:
        """
        description: |
            The agreed credit limit for Financials given to the contra address by the address.
            If set, the credit owed by the contra address to the address cannot exceed this amount.
        type: string
        format: decimal
        required: false
        """
        # Credit limit is optional
        if credit_limit is None:
            self.cleaned_data['credit_limit'] = None
            return None
        # If it was sent, ensure it's a valid Decimal number
        try:
            self.cleaned_data['credit_limit'] = Decimal(credit_limit)
        except InvalidOperation:
            return 'membership_address_link_update_105'
        return None

    def validate_client(self, client: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a client of the Address
        type: boolean
        required: false
        """
        # Client is optional
        if client is None:
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(client, bool):
            return 'membership_address_link_update_106'
        self.cleaned_data['client'] = client
        return None

    def validate_compute(self, compute: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address can build cloud resources using the Address's infrastructure
        type: boolean
        required: false
        """
        # Compute is optional
        if compute is None:
            return None

        # If it was sent, ensure it's a boolean
        if not isinstance(compute, bool):
            return 'membership_address_link_update_107'

        # Make sure the Address can offer compute services to the Contra Address
        if compute and not self.request.user.address['cloud_region']:
            return 'membership_address_link_update_108'
        self.cleaned_data['compute'] = compute
        return None

    def validate_customer(self, customer: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a customer for the Address
        type: boolean
        required: false
        """
        # Customer is optional
        if customer is None:
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(customer, bool):
            return 'membership_address_link_update_109'
        self.cleaned_data['customer'] = customer
        return None

    def validate_note(self, note: Optional[str]) -> Optional[str]:
        """
        description: A much larger note about the linked Address to put in the Link record. No length limit.
        type: string
        required: false
        """
        self.cleaned_data['note'] = str(note).strip() if note else ''
        return None

    def validate_reference(self, reference: Optional[str]) -> Optional[str]:
        """
        description: A reference about the linked Address to put in the Link record. Max 20 characters.
        type: string
        required: false
        """
        if not reference:
            reference = ''
        reference = str(reference).strip()
        if len(reference) > self.get_field('reference').max_length:
            return 'membership_address_link_update_101'
        self.cleaned_data['reference'] = reference
        return None

    def validate_service_centre(self, service_centre: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a service centre for the Address
        type: boolean
        required: false
        """
        # Service Centre is optional
        if service_centre is None:
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(service_centre, bool):
            return 'membership_address_link_update_110'
        self.cleaned_data['service_centre'] = service_centre
        return None

    def validate_supplier(self, supplier: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a supplier for the Address
        type: boolean
        required: false
        """
        # Supplier is optional
        if supplier is None:
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(supplier, bool):
            return 'membership_address_link_update_111'
        self.cleaned_data['supplier'] = supplier
        return None

    def validate_territory_id(self, territory_id: Optional[int]) -> Optional[str]:
        """
        description: The id of a Territory owned by the requesting User's Member to attach to the Link record.
        type: integer
        required: false
        """
        if not territory_id:
            return None
        try:
            territory = Territory.objects.get(pk=int(territory_id))
        except (TypeError, ValueError):
            return 'membership_address_link_update_102'
        except Territory.DoesNotExist:
            return 'membership_address_link_update_103'
        if str(territory.member.pk) != str(self.request.user.member['id']):
            return 'membership_address_link_update_104'
        self.cleaned_data['territory'] = territory
        return None

    def validate_warrantor(self, warrantor: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Contra Address is a warrantor for the Address
        type: boolean
        required: false
        """
        # Warrantor is optional
        if warrantor is None:
            return None
        # If it was sent, ensure it's a boolean
        if not isinstance(warrantor, bool):
            return 'membership_address_link_update_112'
        self.cleaned_data['warrantor'] = warrantor
        return None
