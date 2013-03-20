from django.views.generic import TemplateView

#from timetableData.models import


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        context = None # compute what you want to pass to the template
        return self.render_to_response(context)
