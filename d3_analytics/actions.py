from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.text import capfirst
from django.core.urlresolvers import reverse

global analytics_registry;
analytics_registry = {}

class Analytics(object):

    site_url = '/'    
    def __init__(self, name='d3_analytics'):
        #self._registry = {}
        self.name = name


    def register(self, model, analytics_class):
        if model._meta.abstract:
            raise ImproperlyConfigured('The model %s is abstract, so it '
                  'cannot be registered.' % model.__name__)

        if model in analytics_registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__name__)

        # Instantiate the admin class to save in the registry
        analytics_registry[model] = analytics_class(model, self)

    def wrap_view(self, view):
        def wrapper(request, *args, **kwargs):
            return view(request, *args, **kwargs)
        return wrapper


    def get_urls(self):
        from django.conf.urls import url, include

        # Analytics views.
        urlpatterns = [
            url(r'^$', self.wrap_view(self.index), name='index'),
        ]

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        for model, model_analytics in analytics_registry.items():

            urlpatterns += [
                url(r'^%s/' % (model._meta.module_name),
                    include(model_analytics.urls))
            ]
        return urlpatterns


    @property
    def urls(self):
        return self.get_urls(), 'analytics', self.name


    def get_registered_apps(self):

        app_dict = {}

        models = analytics_registry
        for model, analytic_model in models.items():
            app_label = model._meta.app_label
            info = (model._meta.app_label, model._meta.module_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'analytics_url' : reverse('d3_analytics:%s_%s' % info, current_app=self.name, args=[model._meta.module_name])
            }

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': app_label.title(),
                    'models': [model_dict],
                }

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])

        return app_list

    def each_context(self):
        return {
            'site_url': self.site_url,
            'available_apps': self.get_registered_apps(),
        }


    def index(self, request, extra_context=None):
        template = 'index1.html'
        #app_list = self.get_registered_apps()

        app_dict = {}

        models = analytics_registry
        for model, analytic_model in models.items():
            app_label = model._meta.app_label
            info = (model._meta.app_label, model._meta.module_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'analytics_url' : reverse('d3_analytics:%s_%s' % info, current_app=self.name, args=[model._meta.module_name])
            }

            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': app_label.title(),
                    'models': [model_dict],
                }

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])


        ctx = dict(
            self.each_context(),
            app_list=app_list,
        )

        ctx = RequestContext(request, ctx)
        return render_to_response(template, ctx)

analytics = Analytics()

def register(model, analyticsClass):
    analytics.register(model, analyticsClass)
