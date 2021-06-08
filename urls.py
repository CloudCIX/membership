from django.urls import path
from . import views

urlpatterns = [
    # Address
    path(
        'address/',
        views.AddressCollection.as_view(),
        name='address_collection',
    ),

    path(
        'address/<int:pk>/',
        views.AddressResource.as_view(),
        name='address_resource',
    ),

    path(
        'address/verbose/',
        views.VerboseAddressCollection.as_view(),
        name='verbose_address_collection',
    ),

    # AddressLink
    path(
        'address/<int:address_id>/link/',
        views.AddressLinkResource.as_view(),
        name='address_link_resource',
    ),

    # App Settings
    path(
        'app_settings/',
        views.AppSettingsCollection.as_view(),
        name='app_settings_collection',
    ),

    path(
        'app_settings/<int:pk>/',
        views.AppSettingsResource.as_view(),
        name='app_settings_resource',
    ),

    # Auth
    path(
        'auth/login/',
        views.AuthResource.as_view(),
        name='auth_resource',
    ),

    # Country
    path(
        'country/',
        views.CountryCollection.as_view(),
        name='country_collection',
    ),

    path(
        'country/<int:pk>/',
        views.CountryResource.as_view(),
        name='country_resource',
    ),

    # Currency
    path(
        'currency/',
        views.CurrencyCollection.as_view(),
        name='currency_collection',
    ),

    path(
        'currency/<int:pk>/',
        views.CurrencyResource.as_view(),
        name='currency_resource',
    ),

    # Department
    path(
        'department/',
        views.DepartmentCollection.as_view(),
        name='department_collection',
    ),

    path(
        'department/<int:pk>/',
        views.DepartmentResource.as_view(),
        name='department_resource',
    ),

    # EmailConfirmation
    path(
        'email_confirmation/<str:email_token>/',
        views.EmailConfirmationResource.as_view(),
        name='email_confirmation_resource',
    ),

    # Language
    path(
        'language/',
        views.LanguageCollection.as_view(),
        name='language_collection',
    ),

    path(
        'language/<int:pk>/',
        views.LanguageResource.as_view(),
        name='language_resource',
    ),

    # Member
    path(
        'member/',
        views.MemberCollection.as_view(),
        name='member_collection',
    ),

    path(
        'member/<int:pk>/',
        views.MemberResource.as_view(),
        name='member_resource',
    ),

    # MemberLink
    path(
        'member/<int:member_id>/link/',
        views.MemberLinkCollection.as_view(),
        name='member_link_collection',
    ),

    path(
        'member/<int:member_id>/link/<int:contra_member_id>/',
        views.MemberLinkResource.as_view(),
        name='member_link_resource',
    ),

    # Notification
    path(
        'address/<int:address_id>/notification/<int:transaction_type_id>/',
        views.NotificationCollection.as_view(),
        name='notification_collection',
    ),

    # Profile
    path(
        'profile/',
        views.ProfileCollection.as_view(),
        name='profile_collection',
    ),

    path(
        'profile/<int:pk>/',
        views.ProfileResource.as_view(),
        name='profile_resource',
    ),

    # Subdivision
    path(
        'country/<int:country_id>/subdivision/',
        views.SubdivisionCollection.as_view(),
        name='subdivision_collection',
    ),

    path(
        'country/<int:country_id>/subdivision/<int:pk>/',
        views.SubdivisionResource.as_view(),
        name='subdivision_resource',
    ),

    # Team
    path(
        'team/',
        views.TeamCollection.as_view(),
        name='team_collection',
    ),
    path(
        'team/<int:pk>/',
        views.TeamResource.as_view(),
        name='team_resource',
    ),

    # Territory
    path(
        'territory/',
        views.TerritoryCollection.as_view(),
        name='territory_collection',
    ),

    path(
        'territory/<int:pk>/',
        views.TerritoryResource.as_view(),
        name='territory_resource',
    ),

    # Transaction Type
    path(
        'transaction_type/',
        views.TransactionTypeCollection.as_view(),
        name='transaction_type_collection',
    ),

    path(
        'transaction_type/<int:pk>/',
        views.TransactionTypeResource.as_view(),
        name='transaction_type_resource',
    ),

    # TODO - Remove these after everything is Python3 (backwards compat urls)
    path(
        'transactiontype/',
        views.TransactionTypeCollection.as_view(),
        name='transaction_type_collection',
    ),

    path(
        'transactiontype/<int:pk>/',
        views.TransactionTypeResource.as_view(),
        name='transaction_type_resource',
    ),

    # User
    path(
        'user/',
        views.UserCollection.as_view(),
        name='user_collection',
    ),

    path(
        'user/<int:pk>/',
        views.UserResource.as_view(),
        name='user_resource',
    ),
]
