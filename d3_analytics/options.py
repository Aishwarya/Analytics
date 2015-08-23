from datetime import datetime, timedelta

from django import forms
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils import get_model_entries_graph_data
from utils import get_attribute_value_frequency_graph_data
from metrics.models import RequestLog

class AnalyticsModel(object):
    
    __metaclass__ = forms.MediaDefiningClass

    graph_type = 'line' # By default graph rendered is line
    ordering = None
    time_delta = 30 # By default data is aggregated by month
    title = None

    def __init__(self, model, analytics):
        self.model = model
        self.opts = model._meta
        self.analytics = analytics
        super(AnalyticsModel, self).__init__()

    def __str__(self):
        return "%s.%s" % (self.model._meta.app_label, self.__class__.__name__)

    def get_ordering(self):
        if self.ordering:
            return self.ordering
        else:
            return ()

    def wrap_view(self, view):
        def wrapper(request, *args, **kwargs):
            return view(request, *args, **kwargs)
        return wrapper


    def get_urls(self):
        from django.conf.urls import url
        info = (self.model._meta.app_label, self.model._meta.module_name)
        urlpatterns = [
            url(r'^(.+)$', self.wrap_view(self.analytics_view), name='%s_%s' % info),
        ]

        return urlpatterns

    def urls(self):
        return self.get_urls()
    urls = property(urls)

    def analytics_view(self, request, applabel):
        template = 'index.html'

        graph_meta = {
            'Model': self.model,
            'graph_start_datetime': datetime.now() - timedelta(weeks=15),
        }
        graph_data = get_model_entries_graph_data(graph_meta)

        ctx = {
            'graph_data': graph_data
        }

        ctx = RequestContext(request, ctx)
        return render_to_response(template, ctx)