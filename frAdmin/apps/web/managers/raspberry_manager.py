from django.db.models import Manager, Q


class RaspberryManager(Manager):
    def search(self, query=None, source_type=1, per_page=10, page=0):
        query_search = self.get_queryset().all()
        if query is not None:
            or_lookup = ((Q(name__icontains=query) |
                          Q(ip__icontains=query)))
            query_search = query_search.filter(or_lookup)
        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(
            query_search.values('name', 'dhcp', 'default_gateway', 'sub_netmask', 'status', 'ip', 'ftp_path',
                                'unkown_person','lock_status',
                                'id', 'video_intro')), count_query
