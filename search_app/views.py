from pages.models import Template
from django.views.generic import ListView
from django.db.models import Q

class SearchResultsListView(ListView):
    model = Template
    context_object_name = 'template_list'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print('search query',query)
        return Template.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    
    def get_context_data(self, **kwargs):
        context = super(SearchResultsListView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context 
