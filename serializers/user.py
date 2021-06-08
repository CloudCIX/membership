# libs
import serpy
# local
from membership.serializers.address import AddressSerializer
from membership.serializers.department import DepartmentSerializer
from membership.serializers.language import LanguageSerializer
from membership.serializers.member import MemberSerializer
from membership.serializers.transaction_type import TransactionTypeSerializer
from membership.serializers.profile import ProfileSerializer


class UserSerializer(serpy.Serializer):
    """
    address:
        $ref: '#/components/schemas/Address'
    administrator:
        description: A flag stating whether or not the User is an administrator for the Member
        type: boolean
    department:
        $ref: '#/components/schemas/Department'
    email:
        description: The email address of the User
        type: string
    expiry_date:
        description: The expiry date of the User in ISO format
        type: string
    external_notifications:
        description: An array of Transaction Types the User is set up to receive external Notifications for
        type: array
        items:
            $ref: '#/components/schemas/TransactionType'
    first_name:
        description: The first name of the User
        type: string
    first_otp:
        description: A number between 100000 and 999999 inclusive that is used in otp authentication
        type: interger
    email_validated:
        description: A flag stating wheter the users email has been confirmed
        type: boolean
    global_active:
        description: A flag stating whether the User is currently acting as a global User
        type: boolean
    global_user:
        description: A flag stating whether the User has the ability to act as a global User
        type: boolean
    id:
        description: The id of the User
        type: integer
    image:
        description: The URL of the image of the User
        type: string
    internal_notifications:
        description: An array of Transaction Types the User is set up to receive internal Notifications for
        type: array
        items:
            $ref: '#/components/schemas/TransactionType'
    is_private:
        description: A flag stating whether a user is is_private to thier own Member only or public to partner Members.
        type: boolean
    job_title:
        description: The User's job title
        type: string
    language:
        $ref: '#/components/schemas/Language'
    last_login:
        description: The last time the User logged in
        type: string
    member:
        $ref: '#/components/schemas/Member'
    otp:
        description: A flag stating whether the User is using 2fa or not
        type: boolean
    phones:
        description: An array of named phone numbers used by the User
        type: array
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
    profile:
        $ref: '#/components/schemas/Profile'
    robot:
        description: A flag stating whether a User is a robot for a cloud region
        type: boolean
    signature:
        description: The User's email signature
        type: string
    start_date:
        description: The date the User started working in their Member, in ISO format
        type: string
    surname:
        description: The surname of the User
        type: string
    timezone:
        description: The timezone that the User is currently situated in
        type: string
    uri:
        description: The absolute URL of the User that can be used to perform `Read` and `Update` operations on it
        type: string
    """
    address = AddressSerializer()
    administrator = serpy.Field()
    department = DepartmentSerializer(required=False)
    email = serpy.Field()
    email_validated = serpy.Field()
    expiry_date = serpy.Field(attr='expiry_date.isoformat', call=True)
    external_notifications = TransactionTypeSerializer(attr='get_external_notifications', call=True, many=True)
    first_name = serpy.Field()
    first_otp = serpy.Field(required=False)
    global_active = serpy.Field()
    global_user = serpy.Field()
    id = serpy.Field()
    image = serpy.Field(required=False)
    internal_notifications = TransactionTypeSerializer(attr='get_internal_notifications', call=True, many=True)
    is_private = serpy.Field()
    job_title = serpy.Field()
    language = LanguageSerializer()
    last_login = serpy.Field(required=False)
    member = MemberSerializer()
    otp = serpy.Field()
    phones = serpy.Field()
    profile = ProfileSerializer(required=False)
    robot = serpy.Field()
    signature = serpy.Field()
    start_date = serpy.Field(attr='start_date.isoformat', call=True)
    surname = serpy.Field()
    timezone = serpy.Field()
    uri = serpy.Field(attr='get_absolute_url', call=True)

    # Backwards Compatibility
    old_address_id = serpy.Field(attr='address_id', label='idAddress')
    old_department_id = serpy.Field(attr='department_id', label='idDepartment')
    old_email = serpy.Field(attr='email', label='username')
    old_expiry_date = serpy.Field(attr='expiry_date.isoformat', call=True, label='expiryDate')
    old_first_name = serpy.Field(attr='first_name', label='firstName')
    old_global_active = serpy.Field(attr='global_active', label='globalActive')
    old_global_user = serpy.Field(attr='global_user', label='globalUser')
    old_id = serpy.Field(attr='id', label='idUser')
    old_job_title = serpy.Field(attr='job_title', label='jobTitle')
    old_language_id = serpy.Field(attr='language_id', label='idLanguage')
    old_last_login = serpy.Field(attr='last_login', label='lastLogin')
    old_member_id = serpy.Field(attr='member_id', label='idMember')
    old_notifications = TransactionTypeSerializer(
        attr='get_external_notifications',
        call=True,
        many=True,
        label='notifications',
    )
    old_profile_id = serpy.Field(attr='profile_id', label='idProfile')
    old_start_date = serpy.Field(attr='start_date.isoformat', call=True, label='startDate')
