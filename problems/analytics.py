from d3_analytics import actions
from problems.models import Submission
from d3_analytics.options import AnalyticsModel

class SubmissionAnalytics(AnalyticsModel):
    graph_type = 'BAR'
    title = 'Submissions Report'

actions.register(Submission, SubmissionAnalytics)