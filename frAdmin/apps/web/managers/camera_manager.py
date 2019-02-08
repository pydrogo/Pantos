from django.db.models import Manager, Q


class CameraManager(Manager):
    def search(self, query=None, per_page=10, page=0):
        query_search = self.get_queryset().filter(status=1).all()
        if query is not None:
            or_lookup = (Q(name__icontains=query))
            query_search = query_search.filter(or_lookup)
        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(query_search.values('name', 'status', 'ip', 'id', 'username', 'password','is_active')), count_query

