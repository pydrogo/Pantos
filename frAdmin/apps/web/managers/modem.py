from django.db.models import Manager, Q


class ModemManager(Manager):

    def search(self, query=None, per_page=10, page=0):
        query_search = self.get_queryset().all()
        if query is not None:
            or_lookup = (Q(ssid__icontains=query))
            query_search = query_search.filter(or_lookup)
        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(query_search.values('id', 'ssid', 'password', 'raspberry__name')), count_query
