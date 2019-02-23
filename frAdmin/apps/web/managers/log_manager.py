from django.db.models import Manager, Q


class LogManager(Manager):

    def search(self, query=None, per_page=10, page=0):
        query_search = self.get_queryset().all()
        if query is not None:
            or_lookup = (Q(username__username__icontains=query))
            query_search = query_search.filter(or_lookup)
        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(
            query_search.values('id', 'username__username', 'date', 'description', 'action',
                                'result,username__UserProfile__last_snapshot')), count_query

    def dashboardsearch(self, query=None, per_page=10, page=0):
        query_search = self.get_queryset().all().order_by('-date')[:10]
        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(
            query_search.values('id', 'username__username', 'username__UserProfile__last_snapshot', 'date',
                                'action')), count_query
