from django.db.models import Manager, Q


class AuthorizedtimeManager(Manager):
    def search(self,date_id_list=-1, source_id=0, source_type=1, per_page=10, page=0):
        query_search = self.get_queryset().filter(authorized_day__date_id__in=date_id_list).all()
        # if query is not None:
        #             # or_lookup = ((Q(left_operand_value__icontains=query) |
        #             #               Q(right_operand_value__icontains=query)) & Q(status=1) & Q(source_id=source_id) & Q(source_type=source_type)
        #             #              )
        #             # query_search = query_search.filter(or_lookup)

        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        return list(query_search.values('start_hour','end_hour','authorized_day')), count_query

