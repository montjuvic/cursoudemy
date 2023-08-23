from django.shortcuts import redirect
from .models import Page
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from .forms import PageForm
from django.urls import reverse_lazy

# Create your views here.

class StaffRequiredMixin(object):
    #Este mixin requerira que el usuario sea miembro del staff
    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        #if not request.user.is_staff:
            #return redirect(reverse_lazy('admin:login'))
        return super(StaffRequiredMixin, self).dispatch(request, *args,**kwargs) 

class PageListView(ListView):
    model = Page #Que modelo gestionara?
    #def pages(request):
    #pages = get_list_or_404(Page)
    #return render(request, 'pages/pages.html', {'pages':pages})

class PageDetailView(DetailView):
    model = Page 


@method_decorator(staff_member_required, name="dispatch")
class PageCreateView(CreateView):

    model = Page
    form_class = PageForm
    success_url = reverse_lazy('pages:pages') #para redirccionar a pages una vez se crea una nueva, si no se hace dara error

      #def get_succes_url(self):
        #return reverse('pages:pages') Esta manera es a la antigua... debes importar reverse


        
@method_decorator(staff_member_required, name="dispatch")    
class PageUpdateView(UpdateView):
    model = Page
    form_class = PageForm
    
    template_name_suffix = "_update_form"
    #success_url = reverse_lazy('pages:pages') aca no se puede usar este metodo de esta manera <
    def get_success_url(self):
        return reverse_lazy('pages:update', args=[self.object.id]) + '?ok'
    
@method_decorator(staff_member_required, name="dispatch")
class PageDeleteView(DeleteView):
    model = Page
    
    success_url = reverse_lazy("pages:pages")