def get_datatable_query(queries):
    search = queries.get('search[value]')
    per_page = int(queries.get('length'))
    per_page = per_page if per_page <= 100 else 100
    page = int(int(queries.get('start')) / per_page)

    return search, page, per_page


def get_datatable_results(results, count, search):
    # entities = list(results.values())
    entities = results
    result = {
        'data': entities,
        'recordsTotal': count,
        'recordsFiltered': len(entities) if len(search) > 0 else count
    }
    return result
