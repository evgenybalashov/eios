#coding: utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from core.views import CommonContextMixin
from profiles.models import UserDetail

from .forms import DisciplineForm, DisciplineFormHelper, DisciplineFormset, EducationForm, \
                   ProfessorForm, WorkForm
from .models import Education, Professor, Studies, Work


class DeptStudentListView(CommonContextMixin, ListView):
    context_object_name = 'students'
    template_name = "profiles/students.html"
    paginate_by = 100

    def get_queryset(self):
        try:
            dept = User.objects.get(pk=self.kwargs['pk']).userdetail.professor.dept
        except Professor.DoesNotExist:
            raise Http404
        students = Education.objects.filter(status="IN").filter(dept=dept)
        return students


class DisciplineView(ListView):
    context_object_name = "disciplines"
    template_name = "education/discipline.html"

    def get_queryset(self):
        disciplines = Studies.objects.filter(leaner__user__pk=self.kwargs['pk'], leaner__status="IN")
        course = self.request.GET.get("course")
        semester = self.request.GET.get("semester")
        if course:
            disciplines = disciplines.filter(Q(course=course))
        if semester:
            disciplines = disciplines.filter(Q(semester=semester))
        return disciplines

    def get_context_data(self, **kwargs):
        context = super(DisciplineView, self).get_context_data(**kwargs)
        context['u'] = User.objects.get(pk=self.kwargs['pk'])
        context['edu'] = Education.objects.filter(user__pk=self.kwargs['pk'], status="IN").first()
        disciplines = Studies.objects.filter(leaner__user__pk=self.kwargs['pk'])
        course = self.request.GET.get("course")
        semester = self.request.GET.get("semester")
        context['courses'] = disciplines.order_by()\
            .values_list('course', flat=True)\
            .distinct().order_by('course')
        context['semesters'] = disciplines.order_by()\
            .values_list('semester', flat=True)\
            .distinct().order_by('semester')
        return context


class DisciplineCreateView(CreateView):
    form_class = DisciplineForm
    context_object_name = "u"
    template_name = "education/discipline_create.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.userdetail.is_professor:
            return HttpResponseForbidden()
        return super(DisciplineCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('discipline', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super(DisciplineCreateView, self).get_context_data(**kwargs)
        context['helper'] = DisciplineFormHelper
        context['edu'] = Education.objects.filter(user__pk=self.kwargs['pk'], status="IN").first()
        context['u'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(DisciplineCreateView, self).get_form_kwargs(**kwargs)
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form = DisciplineForm(self.request.POST)
        form = form.save(commit = False)
        form.leaner = Education.objects.get(user__pk=self.kwargs['pk'], status="IN")
        form.save()
        return super(DisciplineCreateView, self).form_valid(form)


class DisciplineUpdateView(UpdateView):
    model = Studies
    form_class = DisciplineForm
    context_object_name = "u"
    template_name = "education/discipline_update.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.userdetail.is_professor:
            return HttpResponseForbidden()
        try:
            return super(DisciplineUpdateView, self).dispatch(request, *args, **kwargs)
        except Studies.DoesNotExist:
            return redirect('discipline_create', self.kwargs['pk'])

    def get_object(self):
        return Studies.objects.get(leaner__user__pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('discipline', args=[self.kwargs['pk']])

    def get_context_data(self, **kwargs):
        context = super(DisciplineUpdateView, self).get_context_data(**kwargs)
        disciplines = Studies.objects.filter(leaner__user__pk=self.kwargs['pk'])
        course = self.request.GET.get("course")
        semester = self.request.GET.get("semester")
        context['courses'] = disciplines.order_by()\
            .values_list('course', flat=True)\
            .distinct().order_by('course')
        context['semesters'] = disciplines.order_by()\
            .values_list('semester', flat=True)\
            .distinct().order_by('semester')
        if course:
            disciplines = disciplines.filter(Q(course=course))
        if semester:
            disciplines = disciplines.filter(Q(semester=semester))
        formset = DisciplineFormset(queryset=disciplines)
        context['formset'] = formset
        context['helper'] = DisciplineFormHelper
        context['edu'] = Education.objects.filter(user__pk=self.kwargs['pk'], status="IN").first()
        context['u'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        formset = DisciplineFormset(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)


class EducationCreateView(CommonContextMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = "profiles/profile_update.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.userdetail.is_professor:
            return HttpResponseForbidden()
        return super(EducationCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form = EducationForm(self.request.POST)
        form = form.save(commit = False)
        form.user = User.objects.get(pk=self.kwargs['pk'])
        form.save()
        try:
            Application.objects.get(user__user__pk=self.kwargs['pk']).delete()
        except:
            pass
        return super(EducationCreateView, self).form_valid(form)


class EducationUpdateView(CommonContextMixin, UpdateView):
    form_class = EducationForm
    template_name = "profiles/profile_update.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            try:
                userdetail = request.user.userdetail
                if not userdetail.is_professor:
                    return HttpResponseForbidden()
            except:
                return HttpResponseForbidden()
        try:
            return super(EducationUpdateView, self).dispatch(request, *args, **kwargs)
        except Education.DoesNotExist:
            return redirect('education_create', self.kwargs['pk'])

    def get_object(self):
        return Education.objects.get(user__pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])


class HistoryView(CommonContextMixin, ListView):
    context_object_name = "history"
    template_name = "history.html"
    paginate_by = 10

    def get_queryset(self):
        return Education.objects.filter(user__pk=self.kwargs['pk'], status="OUT")


class JobCreateView(CommonContextMixin, CreateView):
    model = Professor
    form_class = ProfessorForm
    template_name = "profiles/profile_update.html"

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form = ProfessorForm(self.request.POST)
        form = form.save(commit = False)
        form.user = UserDetail.objects.get(user__pk=self.kwargs['pk'])
        form.save()
        return super(JobCreateView, self).form_valid(form)


class JobUpdateView(CommonContextMixin, UpdateView):
    form_class = ProfessorForm
    template_name = "profiles/profile_update.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            return super(JobUpdateView, self).dispatch(request, *args, **kwargs)
        except Professor.DoesNotExist:
            return redirect('job_create', self.kwargs['pk'])

    def get_object(self):
        return Professor.objects.get(user__pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse('profile', args=[self.kwargs['pk']])


class StudentListView(ListView):
    context_object_name = 'students'
    template_name = "education/students.html"
    paginate_by = 200

    def get_queryset(self):
        students = Education.objects.filter(status="IN", type=self.kwargs['type'])
        query = self.request.GET.get("q")
        if query:
            students = students.filter(
                Q(user__userdetail__last_name__icontains=query)|
                Q(user__userdetail__first_name__icontains=query)|
                Q(faculty__name__icontains=query)|
                Q(faculty__abbr__icontains=query)
                ).distinct()
        return students

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['edu'] = Education.objects.filter(status="IN", type=self.kwargs['type']).first()
        return context


class WorkListView(CommonContextMixin, ListView):
    context_object_name = "works"
    template_name = "education/works.html"
    paginate_by = 10

    def get_queryset(self):
        edu = Education.objects.filter(user__pk=self.kwargs['pk'], 
            status="IN").first()
        return Work.objects.filter(author=edu)


class WorkCreateView(CommonContextMixin, CreateView):
    model = Work
    form_class = WorkForm
    context_object_name = "work"
    template_name = "education/works_update.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.userdetail.is_professor:
            return HttpResponseForbidden()
        return super(WorkCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('works', args=[self.kwargs['pk']])

    def form_valid(self, form):
        form = WorkForm(self.request.POST, self.request.FILES)
        form = form.save(commit = False)
        form.author = Education.objects.get(user__pk=self.kwargs['pk'], status="IN")
        form.save()
        return super(WorksCreateView, self).form_valid(form)


class WorkUpdateView(CommonContextMixin, UpdateView):
    model = Work
    form_class = WorkForm
    context_object_name = "work"
    template_name = "education/works_update.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser or not request.user.userdetail.is_professor:
            return HttpResponseForbidden()
        return super(WorkUpdateView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        work = get_object_or_404(Work, author__user__pk=self.kwargs['pk'], pk=self.kwargs['number'])
        return work

    def get_success_url(self):
        return reverse('works', args=[self.kwargs['pk']])


