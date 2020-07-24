from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Bb, Rubric
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import RedirectView, FormView, ArchiveIndexView, DateDetailView, ListView, UpdateView, DeleteView
from .forms import BbForm
from django.urls import reverse


class BbIndexView(ArchiveIndexView):
    template_name = 'bboard/index.html'
    model = Bb
    date_field = 'published'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbDetailView(DateDetailView):
    model = Bb
    date_field = 'published'
    month_format = '%m'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbByRubricView(SingleObjectMixin, ListView):
    template_name = 'bboard/by_rubric.html'
    pk_url_kwarg = 'rubric_id'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Rubric.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.object.bb_set.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        context['bbs'] = context['object_list']
        return context

class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})

class BbEditView(UpdateView):
    template_name = 'bboard/bb_form.html'
    model = Bb
    form_class = BbForm
    success_url = '/bboard/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbDeleteView(DeleteView):
    template_name = 'bboard/bb_confirm_delete.html'
    model = Bb
    success_url = '/bboard/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class BbRedirectView(RedirectView):
    url = '/detail/%(pk)d/'