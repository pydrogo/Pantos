from django.db.models import Manager, Q
from frAdmin.apps.web.models.alarms import Alarms

class GroupManager(Manager):
    def search(self, query=None, per_page=10, page=0):
        query_search = self.get_queryset().filter(status=1)
        if query is not None:
            or_lookup = (Q(name__icontains=query))
            query_search = query_search.filter(or_lookup)

        count_query = query_search.count()
        start_row = int(per_page * page)
        query_search = query_search[start_row:start_row + per_page]
        result = []
        temp = {}
        alarm_list = Alarms.objects.all()
        for item in query_search:
            temp['id'] = item.id
            temp['name'] = item.name
            temp['welcome_voice'] = str(item.welcome_voice)
            temp['active_rele_time'] = item.active_rele_time
            for alarm in alarm_list:
                if (alarm in list(item.alarm.all())) :
                    temp[alarm.name] = True
                else:
                    temp[alarm.name] = False
            result.append(temp)
            temp={}

        return list(result), count_query
