from d3_analytics import actions
from hackathon.models import Event
from d3_analytics.options import AnalyticsModel

class EventAnalytics(AnalyticsModel):
    graph_type = 'Line'
    time_delta = 'weekly'
    title = 'Event Creation'
    ordering = ('-timestamp',)
    

actions.register(Event, EventAnalytics)