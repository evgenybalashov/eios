# coding: utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .forms import DocForm
from .models import Document, FlatPage
from education.models import Education
from profiles.models import UserDetail


class CommonContextMixin(ContextMixin):

	def get_context_data(self, **kwargs):
		context = super(CommonContextMixin, self).get_context_data(**kwargs)
		context['u'] = get_object_or_404(User, pk=self.kwargs['pk'])
		context['edu'] = Education.objects.filter(user__pk=self.kwargs['pk'], status="IN").first()
		return context


class HomeView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, **kwargs):
		context = super(HomeView, self).get_context_data(**kwargs)
		context['page'] = get_object_or_404(FlatPage, url=reverse('home'))
		return context


class UserListView(ListView):
	model = User
	context_object_name = "users"
	template_name = "users.html"
	paginate_by = 10


class DocsView(CommonContextMixin, ListView):
	context_object_name = "docs"
	template_name = "docs.html"
	paginate_by = 10

	def get_queryset(self):
		return Document.objects.filter(user__user__pk=self.kwargs['pk'])


class DocsCreateView(CommonContextMixin, CreateView):
	model = Document
	form_class = DocForm
	context_object_name = "doc"
	template_name = "docs_update.html"

	def get_success_url(self):
		return reverse('docs', args=[self.kwargs['pk']])

	def form_valid(self, form):
		form = DocForm(self.request.POST, self.request.FILES)
		form = form.save(commit = False)
		form.user = UserDetail.objects.get(user__pk=self.kwargs['pk'])
		form.save()
		return super(DocsCreateView, self).form_valid(form)


class DocsUpdateView(CommonContextMixin, UpdateView):
	model = Document
	form_class = DocForm
	context_object_name = "doc"
	template_name = "docs_update.html"

	def get_object(self):
		return get_object_or_404(Document, user__user__pk=self.kwargs['pk'], pk=self.kwargs['number'])

	def get_success_url(self):
		return reverse('docs', args=[self.kwargs['pk']])
