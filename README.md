# Membership

Membership is the central CloudCIX Application, which controls Company and User details and provides access to them via an API.

## Requirements

- cloudcix/pgsqlapi:latest
- osixia/openldap

## Membership Environment Variables

### framework
- See [here](https://github.com/CloudCIX/framework#framework-environment-variables)

### `PGSQL_USER`
- Name of superuser owner of the API Postgres Database.

### `PGSQL_PASSWORD`
- Password for the superuser owner of the API Postgres Database.

### `POD_NAME`
- Name of POD for this COP (Central Organization Platform). This is used to set the URL for membeship api e.g. membership.`POD_NAME`.`ORGANIZATION_URL`, membership.pod.example.com

### `ORGANIZATION_URL`
- Domain of the URL of the Organization owner of this COP. This is used to set the URL for membeship api e.g. membership.`POD_NAME`.`ORGANIZATION_URL`, membership.pod.example.com

### `MEMBERSHIPLDAP_DC`
- The name of the Server responsible security authentication requests
- If the server name is `example.com`,then the Domain controler is `dc=example,dc=com`

### `MEMBERSHIPLDAP_PASSWORD`
- LDAP Admin password for Membership LDAP

### `PAM_NAME`
- The name of the PAM pod monitoring this COP.

### `PAM_ORGANIZATION_URL`
- The URL of the organization of the PAM pod monitoring this COP.

### `SENTRY_URL` (optional)
- If CloudCIX Limited are providing support to your COP this will be supplied.

## Framework Volumes

### `/application_framework/private-key.rsa`
- Map private-key to membership docker container via volumes., This key is used to encode JSON Web tokens (JWT).

## Email Templates
Templates for emails are located /templates/email for the following:
- Admin Expiry Reminder: An email sent to administrators in a member to notify them that users in their account will expire within 30 days
- Email Confirmation: An email sent to new users to validate their email address
- Non Self Managed Expiry: An email sent to administrators in a member to notify them that users in their non self managed partner members will expire within 30 days
