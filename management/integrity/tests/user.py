# libs
from django.db import connections
# local
from membership.management.integrity.runner import register, output_errors


__all__ = [
    'address_and_member_match',
    'users_deleted_from_member',
]


@register
def address_and_member_match(file=None):
    """
    Check that the member_id of a User match the member_id of the User's Address
    """
    results = dict()
    membership_db = connections['membership']
    with membership_db.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM "user"')
        results['records_inspected'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT "user".id, "user".member_id, "user".address_id FROM "user"
            LEFT JOIN address ON "user".address_id = address.id
            LEFT JOIN member ON ("user".member_id = member.id AND address.member_id = member.id)
            WHERE
                member.id IS NULL
                AND "user".deleted IS NULL
                AND address.deleted IS NULL
                AND member.deleted IS NULL
            ORDER BY
                "user".id
        """)
        invalid_records = cursor.fetchall()

    results['errors_found'] = len(invalid_records)
    if len(invalid_records) > 0:
        error_header = (
            'The following Users have an invalid combination of Member and Address IDs:\n'
            '   ID   | Member | Address\n'
        )
        output_errors(file, error_header, invalid_records)

    return results


@register
def users_deleted_from_member(file=None):
    """
    Check that if a Member is deleted, the Users in that Member are also deleted
    """
    results = dict()
    membership_db = connections['membership']
    with membership_db.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM "user"')
        results['records_inspected'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT "user".id, member_id from "user"
            LEFT JOIN member ON "user".member_id = member.id
            WHERE
                "user".deleted IS NULL
                AND member.deleted IS NOT NULL
            ORDER BY
                "user".id
        """)
        not_deleted_users = cursor.fetchall()

    results['errors_found'] = len(not_deleted_users)
    if len(not_deleted_users) > 0:
        error_header = (
            'The following Users were not deleted even though their Member have been deleted:\n'
            '  User  | Member \n'
        )
        output_errors(file, error_header, not_deleted_users)

    return results
