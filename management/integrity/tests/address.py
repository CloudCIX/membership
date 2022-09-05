# libs
from django.db import connections
from django.db.models import Count
# local
from membership.management.integrity.runner import register, output_errors
from membership.models.address_link import AddressLink


__all__ = [
    'address_has_member',
    'address_links_have_reciprocals',
    'address_links_not_duplicated',
]


@register
def address_has_member(file=None):
    """
    Check that each Address has a Member
    """
    results = dict()
    membership_db = connections['membership']
    with membership_db.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM address')
        results['records_inspected'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT address.id, address.member_id FROM address
            LEFT JOIN member
            ON
                address.member_id = member.id
            WHERE
                (member.id IS NULL OR member.deleted IS NOT NULL)
                AND address.deleted IS NULL
            ORDER BY
                address.member_id;
        """)
        missing_members = cursor.fetchall()

    results['errors_found'] = len(missing_members)
    if len(missing_members) > 0:
        error_header = (
            'The following Addresses belong to missing Members\n'
            'Member ID| Address ID\n'
        )
        output_errors(file, error_header, missing_members)
    return results


@register
def address_links_have_reciprocals(file=None):
    """
    For every Address Link check that an Address Link going in the opposite direction exists
    """
    results = dict()
    membership_db = connections['membership']
    with membership_db.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM address_link')
        results['records_inspected'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT l.id, l.address_id, l.contra_address_id FROM address_link as l
            LEFT JOIN address_link as r
            ON
                l.address_id = r.contra_address_id
                AND l.contra_address_id = r.address_id
            WHERE
                (r.address_id IS NULL OR r.deleted IS NOT NULL)
                AND l.deleted IS NULL
            ORDER BY
                l.address_id;
        """)
        unbalanced_links = cursor.fetchall()

    results['errors_found'] = len(unbalanced_links)
    if len(unbalanced_links) > 0:
        error_header = (
            'The following Address Links were found without reciprocals:\n'
            '   ID    | Address | Contra Address\n'
        )
        output_errors(file, error_header, unbalanced_links)
    return results


@register
def address_links_not_duplicated(file=None):
    """
    Check if any Address Links are duplicated
    """
    results = dict()
    duplicates = AddressLink.objects.values('address_id', 'contra_address_id') \
        .annotate(Count('id')) \
        .order_by() \
        .filter(id__count__gt=1)

    results['records_inspected'] = AddressLink.objects.all().count()
    results['errors_found'] = len(duplicates)
    if len(duplicates) > 0:
        error_header = (
            'The following combinations of Address ID and Contra Address ID are duplicated:\n'
            'Address ID | Contra Address ID | Duplicates Found\n'
        )
        output_errors(file, error_header, duplicates)
    return results
