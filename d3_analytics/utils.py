from collections import Counter
import datetime
import json


def get_datetime_frequency_list(entries_list, strf_string):
    formatted_list= []
    for entry in entries_list:
        formatted_list.append(entry.strftime(strf_string))

    frequency_list = Counter(formatted_list)
    return sorted(frequency_list.items())


def get_model_entries_graph_data(graph_meta):
    """
    Receives timedelta ('DAILY', 'MONTHLY', 'YEARLY') and a Model object, and
    returns the graph data on the basis of frequency of entries.
    """
    time_delta = graph_meta.get('time_delta')
    if time_delta == 'YEARLY':
        days_timedelta = datetime.timedelta(days=365)
    elif time_delta == 'MONTHLY':
        days_timedelta = datetime.timedelta(days=30)
    elif time_delta == 'WEEKLY':
        days_timedelta = datetime.timedelta(days=7)
    else:
        # timedelta defaults to DAILY
        days_timedelta = datetime.timedelta(days=1)


    query_kwargs = {}
    if 'start_datetime' in graph_meta:
        query_kwargs['timestamp__gte'] = graph_meta['start_datetime']

    if 'end_datetime' in graph_meta:
        query_kwargs['timestamp__lte'] = graph_meta['end_datetime']


    Model = graph_meta.get('Model')
    entries = list(Model.objects.filter(**query_kwargs).values_list(
        'timestamp', flat=True))

    if not entries:
        graph_data = {'graph': False}
        return graph_data

    time_delta = graph_meta.get('time_delta')
    if time_delta == 'YEARLY':
        strftime_string = "%Y"
    elif time_delta == 'MONTHLY':
        strftime_string = "%Y-%m"
    else:
        # timedelta defaults to DAILY
        strftime_string = "%Y-%m-%d"

    frequency_list = get_datetime_frequency_list(entries, strftime_string)
    data_points = []
    for data in frequency_list:
        data_points.append({
            'x_value': data[0],
            'y_value': data[1],
        })

    graph_data = {
        "graph": True,
        "meta": {
                "y_label": "Table Entries",
                "strftime_string": strftime_string,
                "svg_div_id": "model-entries-graph",
                "svg_div_container": "model-entries-graph-container",
            },
        "data_points": data_points,
    }

    return graph_data


def get_attribute_value_frequency_graph_data(graph_meta):
    """
    Receives a model attribute and returns the graph data with frequency of its
    values.
    """

    query_kwargs = {}
    if 'start_datetime' in graph_meta:
        query_kwargs['timestamp__gte'] = graph_meta['start_datetime']

    if 'end_datetime' in graph_meta:
        query_kwargs['timestamp__lte'] = graph_meta['end_datetime']

    Model = graph_meta.get('Model')
    model_attribute = graph_meta.get('model_attribute')
    print query_kwargs
    entries = Model.objects.filter(**query_kwargs).values_list(
            model_attribute, flat=True)

    if not entries:
        graph_data = {'graph': False}
        return graph_data

    frequency_dict = Counter(entries).items()

    data_points = []
    for data in frequency_dict:
        data_points.append({
            'x_value': str(data[0]),
            'y_value': data[1]
        })

    graph_data = {
        "graph": True,
        "meta": {
                "x_label": model_attribute,
                "y_label": "Table Entries",
                "svg_div_id":"attribute-value-frequency-id",
                "svg_div_container": "attribute-value-frequency-graph-container",
            },
        "data_points": data_points,
    }

    return graph_data    