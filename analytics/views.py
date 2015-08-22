from django.shortcuts import render_to_response
from django.template import RequestContext

from utils import get_model_entries_graph_data
from utils import get_attribute_value_frequency_graph_data
from metrics.models import RequestLog

# Create your views here.
def home(request):
    template = 'index.html'

    model_entries_graph_meta = {
        'timedelta': 'DAILY',
        'Model': RequestLog
    }
    model_entries_graph_data = get_model_entries_graph_data(model_entries_graph_meta)


    attribute_value_frequency_meta_1 = {
        'Model': RequestLog,
        'model_attribute': 'request_method',
    }
    attribute_value_frequency_meta_2 = {
        'Model': RequestLog,
        'model_attribute': 'http_host',
    }
    attribute_value_frequency_meta_3 = {
        'Model': RequestLog,
        'model_attribute': 'query_string',
    }


    attribute_value_frequency_attrs = [
            'request_method', 'http_host', 'query_string'
    ]
    attribute_value_frequency_graph_data_1 = get_attribute_value_frequency_graph_data(
            attribute_value_frequency_meta_1)
    attribute_value_frequency_graph_data_2 = get_attribute_value_frequency_graph_data(
            attribute_value_frequency_meta_2)
    attribute_value_frequency_graph_data_3 = get_attribute_value_frequency_graph_data(
            attribute_value_frequency_meta_3)
    attribute_value_frequency_containers = []
    for attr in attribute_value_frequency_attrs:
        attribute_value_frequency_containers.append({
                'container_class': '{0}-attribute-value-frequency-graph-container'.format(attr),
                'id': '{0}-attribute-value-frequency-id'.format(attr)
        })



    ctx = {
        'model_entries_graph_data': model_entries_graph_data,
        'attribute_value_frequency_graph_data_1': attribute_value_frequency_graph_data_1,
        'attribute_value_frequency_graph_data_2': attribute_value_frequency_graph_data_2,
        'attribute_value_frequency_graph_data_3': attribute_value_frequency_graph_data_3,
        'attribute_value_frequency_containers': attribute_value_frequency_containers
    }
    ctx = RequestContext(request, ctx)
    return render_to_response(template, RequestContext(request, ctx))
