#coding: UTF-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.views.generic import FormView, View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView

from core.models import Document
from core.views import CommonContextMixin
from education.models import Education, Studies, Work
from profiles.models import UserDetail

from .forms import DeptQueryForm, UserForm, UserDetailForm, UserDetailShortForm
from .models import UserDetail


def profile_redirect(request):
    return HttpResponseRedirect(reverse('profile', args=[request.user.pk]))


class ProfileView(DetailView):
    model = User
    context_object_name = "u"
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        user_docs = Document.objects.filter(user__user__pk=self.kwargs['pk'])
        context['deptqueryform'] = DeptQueryForm()
        try:
            dept = self.request.user.userdetail.professor.dept
            context['querylist'] = UserDetail.objects.filter(application__dept=dept)
        except:
            pass
        context['edu'] = Education.objects.filter(user__pk=self.kwargs['pk'], status="IN").first()
        context['edu_docs'] = user_docs.filter(type="Документ об образовании")
        context['orders'] = user_docs.filter(type="Приказ").order_by('issue_date')
        context['works'] = Work.objects.filter(author__user__pk=self.kwargs['pk'],
            author__status="IN")
        context['disciplines'] = Studies.objects.filter(leaner__user__pk=self.kwargs['pk'], leaner__status="IN")
        return context


class ConfirmQueryView(View):

    def get(self, *args, **kwargs):
        raise Http404()

    def post(self, *args, **kwargs):
        pk = self.request.POST.get('person')
        u = UserDetail.objects.get(user__pk=pk)
        if self.request.POST.get('query_response') == 'student':
            return redirect('education_create', pk)
        elif self.request.POST.get('query_response') == 'professor':
            u.is_professor = True
            u.save()
        u.application.delete()
        return redirect('profile', self.kwargs['pk'])

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form = DeptQueryForm(self.request.POST)
        form = form.save(commit = False)
        form.user = UserDetail.objects.get(user__pk=self.kwargs['pk'])
        form.save()
        return super(DeptQueryView, self).form_valid(form)


class DeptQueryView(FormView, SingleObjectMixin):
    template_name = "profiles/profile.html"
    form_class = DeptQueryForm

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form = DeptQueryForm(self.request.POST)
        form = form.save(commit = False)
        form.user = UserDetail.objects.get(user__pk=self.kwargs['pk'])
        form.save()
        return super(DeptQueryView, self).form_valid(form)


class ProfileCreateView(CommonContextMixin, CreateView):
    model = UserDetail
    template_name = "profiles/profile_update.html"

    def get_form_class(self):
        if self.request.user.is_superuser:
            return UserDetailForm
        return UserDetailShortForm

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])

    def form_valid(self, form):
        if self.request.user.is_superuser:
            form = UserDetailForm(self.request.POST, self.request.FILES)
        else:
            form = UserDetailShortForm(self.request.POST, self.request.FILES)
        form = form.save(commit = False)
        form.user = User.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super(ProfileCreateView, self).form_valid(form)


class ProfileUpdateView(CommonContextMixin, UpdateView):
    template_name = "profiles/profile_update.html"
    model = UserDetail

    # def dispatch(self, request, *args, **kwargs):
    #     try:
    #         u = UserDetail.objects.get(user__pk=self.kwargs['pk'])
    #     except UserDetail.DoesNotExist:
    #         return redirect('profile_create', self.kwargs['pk'])
    #     return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if self.request.user.userdetail.is_professor:
            return UserDetailForm
        return UserDetailShortForm

    def get_object(self, queryset=None):
        return UserDetail.objects.get(user__pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])


class EmailUpdateView(CommonContextMixin, UpdateView):
    form_class = UserForm
    template_name = "profiles/profile_update.html"

    def get_object(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])