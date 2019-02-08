from django.db.models import Manager, Q


class UserImageManager(Manager):

    def search(self, query=None, source_id=0, source_type=1, per_page=10, page=0):
        query_search = self.get_queryset()
        try:
            count_query = query_search.count()
        except:
            count_query = 0
            query_search = []
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(query_search.values('id', 'user__user__username', 'user__user__first_name', 'user__user__last_name',
                                        'user__user__email', 'user__user__password', 'user__user__is_active',
                                        'user__mobile', 'user__unit', 'user__group__name',
                                        'profile_image')), count_query
