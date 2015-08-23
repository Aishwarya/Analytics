from datetime import datetime, timedelta

from django import forms
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils import get_model_entries_graph_data
from utils import get_attribute_value_frequency_graph_data
from metrics.models import RequestLog

class AnalyticsModel(object):
    """Encapsulates all analytics options and functionality for a model.
    """
    
    __metaclass__ = forms.MediaDefiningClass

    graph_type = 'LINE' # By default graph rendered is line
    ordering = None
    time_delta = 'WEEKLY' # By default data is aggregated by month
    title = None
    start_datetime = None #
    end_datetime = None
    is_attribute = False # set to True, if graph to be rendered for a specific attribute
    model_attribute = None #Mandatory, if is_attribute is set to True.
    weeks = 30

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


    def get_graph_title(self):
        if self.title:
            return self.title
        else:
            return '%s %s' %(self.model._meta.module_name, 'Analytics')

    def analytics_view(self, request, applabel):
        """View to render graph for a registered model
        """
        template = 'index.html'

        graph_meta = { 'Model': self.model }

        start_datetime = getattr(self, 'start_datetime')
        if start_datetime:
            graph_meta['start_datetime'] = self.start_datetime

        end_datetime = getattr(self, 'end_datetime')
        if end_datetime:
            graph_meta['end_datetime'] = self.end_datetime

        if start_datetime is None and end_datetime is None:
            graph_meta['start_datetime'] = datetime.now() - timedelta(weeks=self.weeks)

        graph_meta['time_delta'] = self.time_delta

        is_attribute = getattr(self, 'is_attribute')

        if is_attribute and self.model_attribute:
            graph_meta['model_attribute'] = self.model_attribute
            graph_data = get_attribute_value_frequency_graph_data(
                    graph_meta)
        else:
            graph_data = get_model_entries_graph_data(
                    graph_meta)

        ctx = {'title': self.get_graph_title()}
        is_graph = graph_data.pop('graph', None)
        if is_graph:
            graph_type = self.graph_type

            ctx.update({
                'graph_data': graph_data,
                'graph_type': graph_type,
                
            })
        else:
            template = 'empty_state.html'
        ctx = RequestContext(request, ctx)
        return render_to_response(template, ctx)
