from django.views.generic import DetailView
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from bricks.models import Page


class PageDetailView(DetailView):
    context_object_name = 'page'
    context_content_object_name = 'object'
    model = Page
    #FIXME: published!
    queryset = Page.objects.all()
    slug_field = 'slug'
    context_object_name = None
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(PageDetailView, self).get_context_data(**kwargs)
        context[self.context_content_object_name] = self.object.content_object
        return context

    def get_template_names(self):
        return self.content_object.get_template_names(self.kwargs.get('path'))

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        path = self.kwargs.get('path', None)
        if path:
            path_elements = [p for p in path.split('/')]
            tie = None
            f = {}
            for (i, slug) in enumerate(path_elements):
                l = '__'.join(['parent'] * (len(path_elements) - 1 - i))
                a = lambda a: '__'.join([l, a]) if l else a
                f.update({a('slug'): slug, a('level'): i})
            queryset = queryset.filter(**f)
        else:
            raise ImproperlyConfigured

        try:
            tie = queryset.get()
        except ObjectDoesNotExist:
            raise Http404(_(u"No %(verbose_name)s found matching the query") % {'verbose_name': queryset.model._meta.verbose_name})
        self.content_object = tie.content_object
        return tie

    def get_queryset(self):
        #TODO
        return super(PageDetailView, self).get_queryset()


tie_detail = PageDetailView.as_view()
