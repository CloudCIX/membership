# stdlib
import re
from collections import deque
from typing import cast, Deque, Dict, List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from membership.models import (
    Address,
    Country,
    Currency,
    Language,
    Member,
    Subdivision,
)


__all__ = [
    'AddressListController',
    'AddressCreateController',
    'AddressUpdateController',
]

PHONE_PATTERN = re.compile(r'^(\(?\+?[0-9]*\)?)?[0-9_\- ()]*$')


class AddressListController(ControllerBase):
    """
    Validates User data used to filter a list of Address records
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        allowed_ordering = (
            'name',
            'address1',
            'address_link__credit_limit',
            'address_link__note',
            'address_link__reference',
            'address_link__territory__name',
            'city',
            'full_address',
            'id',
            'member_id',
            'member__name',
            'subdivision__english_name',
            'subdivision__country__english_name',
        )
        search_fields = {
            'address1': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'address2': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'address3': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'address_link__credit_limit': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'address_link__client': (),
            'address_link__compute': (),
            'address_link__customer': (),
            'address_link__note': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'address_link__reference': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'address_link__service_centre': (),
            'address_link__supplier': (),
            'address_link__territory__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'address_link__territory__id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'address_link__warrantor': (),
            'city': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'country_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'country__english_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'member_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'member__name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'member__self_managed': (),
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'postcode': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'cloud_region': (),
            'subdivision_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'subdivision__english_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }
        validation_order = ('linked', ) + ControllerBase.Meta.validation_order

    def validate_order(self, order: Optional[str]):
        """
        Extend the base order method by handling the unique `full_address` order parameter
        :param order: The order parameter sent by the user
        """
        # Just call the super version and then check the cleaned_data
        super(AddressListController, self).validate_order(order)
        cleaned_order: str = self.cleaned_data['order']
        if 'full_address' in cleaned_order:
            # Set up the initial list and then check if it is asc or desc
            new_order = [
                'name',
                'address1',
                'address2',
                'address3',
                'city',
                'postcode',
                'subdivision__english_name',
                'country__english_name',
            ]
            if cleaned_order == '-full_address':
                # Switch to desc
                new_order[0] = '-name'
        else:
            # Put the old order into a list so we can use a star param in view
            new_order = [cleaned_order]
        self.cleaned_data['order'] = new_order


class AddressCreateController(ControllerBase):
    """
    Data required to create a new Address
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Address
        validation_order = (
            'member_id',
            'name',
            'address1',
            'address2',
            'address3',
            'city',
            'country_id',
            'subdivision_id',
            'postcode',
            'phones',
            'email',
            'website',
            'gln',
            'vat_number',
            'language_id',
            'currency_id',
            'billing_address_id',
        )

    def validate_member_id(self, member_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Member that will own the Address
        type: integer
        """
        try:
            member = Member.objects.get(id=int(cast(int, member_id)))
        except (ValueError, TypeError):
            # member_id was not an int
            return 'membership_address_create_101'
        except Member.DoesNotExist:
            return 'membership_address_create_102'
        self.cleaned_data['member'] = member
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Address
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_address_create_103'
        if len(name) > self.get_field('name').max_length:
            return 'membership_address_create_104'
        self.cleaned_data['name'] = name
        return None

    def validate_address1(self, address: Optional[str]) -> Optional[str]:
        """
        description: The first line of the geographic address of the Address
        type: string
        """
        if address is None:
            address = ''
        address = str(address).strip()
        if len(address) == 0:
            return 'membership_address_create_105'
        if len(address) > self.get_field('address1').max_length:
            return 'membership_address_create_106'
        self.cleaned_data['address1'] = address
        return None

    def validate_address2(self, address: Optional[str]) -> Optional[str]:
        """
        description: The second line of the geographic address of the Address
        type: string
        required: false
        """
        if address is None:
            address = ''
        address = str(address).strip()
        if len(address) > self.get_field('address2').max_length:
            return 'membership_address_create_107'
        self.cleaned_data['address2'] = address
        return None

    def validate_address3(self, address: Optional[str]) -> Optional[str]:
        """
        description: The third line of the geographic address of the Address
        type: string
        required: false
        """
        if address is None:
            address = ''
        address = str(address).strip()
        if len(address) > self.get_field('address3').max_length:
            return 'membership_address_create_108'
        self.cleaned_data['address3'] = address
        return None

    def validate_city(self, city: Optional[str]) -> Optional[str]:
        """
        description: The city in which the Address is located
        type: string
        """
        if city is None:
            city = ''
        city = str(city).strip()
        if len(city) == 0:
            return 'membership_address_create_109'
        if len(city) > self.get_field('city').max_length:
            return 'membership_address_create_110'
        self.cleaned_data['city'] = city
        return None

    def validate_country_id(self, country_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Country in which the Address is located
        type: integer
        """
        try:
            country = Country.objects.get(id=int(cast(int, country_id)))
        except (ValueError, TypeError):
            return 'membership_address_create_111'
        except Country.DoesNotExist:
            return 'membership_address_create_112'
        self.cleaned_data['country'] = country
        return None

    def validate_subdivision_id(self, subdivision_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Subdivision in the specified Country in which the Address is located
        type: integer
        required: false
        """
        if subdivision_id is None or 'country' not in self.cleaned_data:
            # Optional
            self.cleaned_data['subdivision'] = None
            return None
        try:
            subdivision = Subdivision.objects.get(id=int(subdivision_id), country=self.cleaned_data['country'])
        except (ValueError, TypeError):
            return 'membership_address_create_113'
        except Subdivision.DoesNotExist:
            return 'membership_address_create_114'
        self.cleaned_data['subdivision'] = subdivision
        return None

    def validate_postcode(self, postcode: Optional[str]) -> Optional[str]:
        """
        description: The postcode of the location of the Address record
        type: string
        required: false
        """
        if postcode is None:
            postcode = ''
        postcode = str(postcode).strip()
        if len(postcode) > self.get_field('postcode').max_length:
            return 'membership_address_create_115'
        self.cleaned_data['postcode'] = postcode
        return None

    def validate_phones(self, phones: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """
        description: An array of named phone numbers that can be used to contact the Address
        type: array
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
        required: false
        """
        phones = phones or []
        if not isinstance(phones, list):
            return 'membership_address_create_116'
        numbers: Deque = deque()
        for i, phone in enumerate(phones):
            if not isinstance(phone, dict):
                return 'membership_address_create_117'
            name = phone.get('name', None)
            number = phone.get('number', None)
            if name is None or number is None:
                return 'membership_address_create_118'
            if not PHONE_PATTERN.match(number):
                return 'membership_address_create_119'
            key = {'name': name.strip(), 'number': number.strip()}
            if key not in numbers:
                numbers.append(key)
        self.cleaned_data['phones'] = list(numbers)
        return None

    def validate_email(self, email: Optional[str]) -> Optional[str]:
        """
        description: An email address that can be used to contact the Address
        type: string
        required: false
        """
        if email is None:
            email = ''
        email = email.strip()
        if len(email) > self.get_field('email').max_length:
            return 'membership_address_create_120'
        self.cleaned_data['email'] = email
        return None

    def validate_website(self, website: Optional[str]) -> Optional[str]:
        """
        description: The website of the Address
        type: string
        required: false
        """
        if website is None:
            website = ''
        website = str(website).strip()
        if len(website) > self.get_field('website').max_length:
            return 'membership_address_create_121'
        self.cleaned_data['website'] = website
        return None

    def validate_gln(self, gln: Optional[str]) -> Optional[str]:
        """
        description: The Global Location Number of the Address, minus the Member's GLN Prefix
        type: string
        required: false
        """
        if gln is None:
            gln = ''
        gln = str(gln).strip()
        if len(gln) > self.get_field('gln').max_length:
            return 'membership_address_create_122'
        self.cleaned_data['gln'] = gln
        return None

    def validate_vat_number(self, vat_number: Optional[str]) -> Optional[str]:
        """
        description: The vat number of the Address
        type: string
        required: false
        """
        if vat_number is None:
            vat_number = ''
        vat_number = str(vat_number).strip()
        if len(vat_number) > self.get_field('vat_number').max_length:
            return 'membership_address_create_123'
        self.cleaned_data['vat_number'] = vat_number
        return None

    def validate_language_id(self, language_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the main Language used by the Address
        type: integer
        """
        try:
            language = Language.objects.get(id=int(cast(int, language_id)))
        except (ValueError, TypeError):
            return 'membership_address_create_124'
        except Language.DoesNotExist:
            return 'membership_address_create_125'
        self.cleaned_data['language'] = language
        return None

    def validate_currency_id(self, currency_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the main Currency used by the Address
        type: integer
        """
        try:
            currency = Currency.objects.get(id=int(cast(int, currency_id)))
        except (ValueError, TypeError):
            return 'membership_address_create_126'
        except Currency.DoesNotExist:
            return 'membership_address_create_127'
        self.cleaned_data['currency'] = currency
        return None

    def validate_billing_address_id(self, billing_address_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Address record that will receive bills for the Address
        type: integer
        required: false
        """
        if billing_address_id is None or 'member' not in self.cleaned_data:
            return None
        try:
            address = Address.objects.get(id=int(billing_address_id), member=self.cleaned_data['member'])
        except (ValueError, TypeError):
            return 'membership_address_create_128'
        except Address.DoesNotExist:
            return 'membership_address_create_129'
        self.cleaned_data['billing_address'] = address
        return None


class AddressUpdateController(ControllerBase):
    """
    Validates User data used to update an Address record
    """

    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Address
        validation_order = (
            'name',
            'address1',
            'address2',
            'address3',
            'city',
            'country_id',
            'subdivision_id',
            'postcode',
            'phones',
            'email',
            'website',
            'gln',
            'vat_number',
            'language_id',
            'currency_id',
            'billing_address_id',
            'cloud_region',
        )

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Address
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'membership_address_update_101'
        if len(name) > self.get_field('name').max_length:
            return 'membership_address_update_102'
        self.cleaned_data['name'] = name
        return None

    def validate_address1(self, address: Optional[str]) -> Optional[str]:
        """
        description: The first line of the geographic address of the Address
        type: string
        """
        if address is None:
            address = ''
        address = str(address).strip()
        if len(address) == 0:
            return 'membership_address_update_103'
        if len(address) > self.get_field('address1').max_length:
            return 'membership_address_update_104'
        self.cleaned_data['address1'] = address
        return None

    def validate_address2(self, address: Optional[str]) -> Optional[str]:
        """
        description: The second line of the geographic address of the Address
        type: string
        required: false
        """
        if address is None:
            address = ''
        address = str(address).strip()
        if len(address) > self.get_field('address2').max_length:
            return 'membership_address_update_105'
        self.cleaned_data['address2'] = address
        return None

    def validate_address3(self, address: Optional[str]) -> Optional[str]:
        """
        description: The third line of the geographic address of the Address
        type: string
        required: false
        """
        if address is None:
            address = ''
        address = str(address).strip()
        if len(address) > self.get_field('address3').max_length:
            return 'membership_address_update_106'
        self.cleaned_data['address3'] = address
        return None

    def validate_city(self, city: Optional[str]) -> Optional[str]:
        """
        description: The city in which the Address is located
        type: string
        """
        if city is None:
            city = ''
        city = str(city).strip()
        if len(city) == 0:
            return 'membership_address_update_107'
        if len(city) > self.get_field('city').max_length:
            return 'membership_address_update_108'
        self.cleaned_data['city'] = city
        return None

    def validate_country_id(self, country_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Country in which the Address is located
        type: integer
        """
        try:
            country = Country.objects.get(id=int(cast(int, country_id)))
        except (ValueError, TypeError):
            return 'membership_address_update_109'
        except Country.DoesNotExist:
            return 'membership_address_update_110'
        self.cleaned_data['country'] = country
        return None

    def validate_subdivision_id(self, subdivision_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Subdivision in the specified Country in which the Address is located
        type: integer
        required: false
        """
        if subdivision_id is None:
            # Optional
            self.cleaned_data['subdivision'] = None
            return None
        country = self.cleaned_data.get('country', self._instance.country)
        try:
            subdivision = Subdivision.objects.get(id=int(subdivision_id), country=country)
        except (ValueError, TypeError):
            return 'membership_address_update_111'
        except Subdivision.DoesNotExist:
            return 'membership_address_update_112'
        self.cleaned_data['subdivision'] = subdivision
        return None

    def validate_postcode(self, postcode: Optional[str]) -> Optional[str]:
        """
        description: The postcode of the location of the Address record
        type: string
        required: false
        """
        if postcode is None:
            postcode = ''
        postcode = str(postcode).strip()
        if len(postcode) > self.get_field('postcode').max_length:
            return 'membership_address_update_113'
        self.cleaned_data['postcode'] = postcode
        return None

    def validate_phones(self, phones: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """
        description: An array of named phone numbers that can be used to contact the Address
        type: array
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
        required: false
        """
        phones = phones or []
        if not isinstance(phones, list):
            return 'membership_address_update_114'
        numbers: Deque = deque()
        for i, phone in enumerate(phones):
            if not isinstance(phone, dict):
                return 'membership_address_update_115'
            name = phone.get('name', None)
            number = phone.get('number', None)
            if name is None or number is None:
                return 'membership_address_update_116'
            if not PHONE_PATTERN.match(number):
                return 'membership_address_update_117'
            key = {'name': name.strip(), 'number': number.strip()}
            if key not in numbers:
                numbers.append(key)
        self.cleaned_data['phones'] = list(numbers)
        return None

    def validate_email(self, email: Optional[str]) -> Optional[str]:
        """
        description: An email address that can be used to contact the Address
        type: string
        required: false
        """
        if email is None:
            email = ''
        email = email.strip()
        if len(email) > self.get_field('email').max_length:
            return 'membership_address_update_118'
        self.cleaned_data['email'] = email
        return None

    def validate_website(self, website: Optional[str]) -> Optional[str]:
        """
        description: The website of the Address
        type: string
        required: false
        """
        if website is None:
            website = ''
        website = str(website).strip()
        if len(website) > self.get_field('website').max_length:
            return 'membership_address_update_119'
        self.cleaned_data['website'] = website
        return None

    def validate_gln(self, gln: Optional[str]) -> Optional[str]:
        """
        description: The Global Location Number of the Address, minus the Member's GLN Prefix
        type: string
        required: false
        """
        if gln is None:
            gln = ''
        gln = str(gln).strip()
        if len(gln) > self.get_field('gln').max_length:
            return 'membership_address_update_120'
        self.cleaned_data['gln'] = gln
        return None

    def validate_vat_number(self, vat_number: Optional[str]) -> Optional[str]:
        """
        description: The vat number of the Address
        type: string
        required: false
        """
        if vat_number is None:
            vat_number = ''
        vat_number = str(vat_number).strip()
        if len(vat_number) > self.get_field('vat_number').max_length:
            return 'membership_address_update_121'
        self.cleaned_data['vat_number'] = vat_number
        return None

    def validate_language_id(self, language_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the main Language used by the Address
        type: integer
        """
        try:
            language = Language.objects.get(id=int(cast(int, language_id)))
        except (ValueError, TypeError):
            return 'membership_address_update_122'
        except Language.DoesNotExist:
            return 'membership_address_update_123'
        self.cleaned_data['language'] = language
        return None

    def validate_currency_id(self, currency_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the main Currency used by the Address
        type: integer
        """
        try:
            currency = Currency.objects.get(id=int(cast(int, currency_id)))
        except (ValueError, TypeError):
            return 'membership_address_update_124'
        except Currency.DoesNotExist:
            return 'membership_address_update_125'
        self.cleaned_data['currency'] = currency
        return None

    def validate_billing_address_id(self, billing_address_id: Optional[int]) -> Optional[str]:
        """
        description: The id of the Address record that will receive bills for the Address
        type: integer
        required: false
        """
        if billing_address_id is None:
            return None
        try:
            address = Address.objects.get(id=int(billing_address_id), member=self._instance.member)
        except (ValueError, TypeError):
            return 'membership_address_update_126'
        except Address.DoesNotExist:
            return 'membership_address_update_127'
        self.cleaned_data['billing_address'] = address
        return None

    def validate_cloud_region(self, cloud_region: Optional[bool]) -> Optional[str]:
        """
        description: A flag stating if the Address has the role cloud_region.
        type: boolean
        required: false
        """
        # cloud_region is optional
        if cloud_region is None:
            self.cleaned_data['cloud_region'] = self._instance.cloud_region
            return None

        # If it was sent, ensure it's a boolean
        if not isinstance(cloud_region, bool):
            return 'membership_address_update_128'

        # Make sure the Address's Member is self managed
        if cloud_region and not self._instance.member.self_managed:
            return 'membership_address_update_129'

        self.cleaned_data['cloud_region'] = cloud_region
        return None
