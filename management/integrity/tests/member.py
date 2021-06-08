# libs
from django.db import connections
from django.db.models import Count
# local
from membership.management.integrity.runner import register, output_errors
from membership.models.member_link import MemberLink


__all__ = [
    'member_links_have_reciprocals',
    'member_links_not_duplicated',
]


@register
def member_links_have_reciprocals(file=None):
    """
    For every Member Link ensure that a Member Link going in the opposite direction exists
    """
    results = dict()
    membership_db = connections['membership']
    with membership_db.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM member_link')
        results['records_inspected'] = cursor.fetchone()[0]

        cursor.execute("""
            SELECT l.id, l.member_id, l.contra_member_id FROM member_link as l
            LEFT JOIN member_link as r
            ON
                l.member_id = r.contra_member_id
                AND l.contra_member_id = r.member_id
            WHERE
                r.member_id IS NULL
                OR r.deleted IS NOT NULL
        """)
        unbalanced_links = cursor.fetchall()

    results['errors_found'] = len(unbalanced_links)
    if len(unbalanced_links) > 0:
        error_header = (
            'The following Member Links were found without reciprocals:\n'
            '   ID   | Member | Contra Member\n'
        )
        output_errors(file, error_header, unbalanced_links)
    return results


@register
def member_links_not_duplicated(file=None):
    """
    Ensure no Member Link is duplicated
    """
    results = dict()
    duplicates = MemberLink.objects.values_list('member_id', 'contra_member_id')\
        .annotate(Count('id'))\
        .order_by()\
        .filter(id__count__gt=1)

    results.update({
        'results_inspected': MemberLink.objects.all().count(),
        'errors_found': len(duplicates),
    })
    if len(duplicates) > 0:
        error_header = (
            'The following Member Links were duplicated:\n'
            ' Member | Contra Member | Duplicates Found\n'
        )
        output_errors(file, error_header, duplicates)
    return results
