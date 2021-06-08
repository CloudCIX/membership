"""
CloudCIX Membership is an API that is capable of managing CloudCIX Members, and relationships between those Members.
It also allows for the management and authentication of a Member's Users.


Membership manages your membership and your relationships with your partner Members. It gives the ability for
multi-tenanted operations, which allow you to transact, and securely share information, with your partner Members.

Members can be self-managed or not. Being self-managed means that the Users in the Member are in charge of running it,
not self-managed means that Users in a different Member are in charge of running it.


CloudCIX is a business network. Membership is designed to manage data for Organisations, as well as transactions between
Addresses of these Organisations.


An Organisation is a CloudCIX Member, and any locations the Organisation is situated in are Addresses.
Links in CloudCIX are between Addresses.


Users are employees of a Member and are associated with an Address. Users may be global, which allows them to change
what Address they are associated with themselves.


Membership also manages tokens, which are used to authenticate requests to any of the CloudCIX APIs.

## Tokens

Membership requires that an email address is unique within a Member. However, the email address may be in use by the
same person in multiple Members. A token must be associated with a User and a Member, which is why the Member's API key
must be sent in requests to generate new tokens.
"""

__version__ = '1.0.0'
