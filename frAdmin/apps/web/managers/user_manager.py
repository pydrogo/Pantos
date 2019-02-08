from django.db.models import Manager, Q


class UserManager(Manager):

    def search(self, query=None, per_page=10, page=0):
        query_search = self.get_queryset().all()
        if query is not None:
            or_lookup = (Q(user__username__icontains=query))
            query_search = query_search.filter(or_lookup)
        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(query_search.values('id', 'user__username', 'last_pass', 'user__first_name', 'user__last_name',
                                        'user__email', 'pass_limitation', 'user__is_active', 'mobile', 'unit',
                                        'group__name','black_list')), count_query
