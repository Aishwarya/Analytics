from django.shortcuts import render_to_response

# Create your views here.
def home(request):
    template = 'analytics/index.html'
    ctx = {}
    return render_to_response(template, ctx)