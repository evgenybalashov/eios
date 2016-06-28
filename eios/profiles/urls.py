from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from core.views import DocsView, DocsCreateView, DocsUpdateView
from profiles.views import ConfirmQueryView, DeptQueryView, EmailUpdateView, profile_redirect, \
                            ProfileCreateView, ProfileUpdateView, ProfileView
from education.views import DeptStudentListView, DisciplineView, DisciplineCreateView, \
                            DisciplineUpdateView, EducationCreateView, EducationUpdateView, \
                            HistoryView, JobCreateView, JobUpdateView, WorkListView, \
                            WorkCreateView, WorkUpdateView


urlpatterns = [    
    url(r'^$', profile_redirect),
    url(r'^(?P<pk>\d+)/$', login_required(ProfileView.as_view()), name='profile'),
    url(r'^(?P<pk>\d+)/create/$', login_required(ProfileCreateView.as_view()), name='profile_create'),
    url(r'^(?P<pk>\d+)/update/$', login_required(ProfileUpdateView.as_view()), name='profile_update'),
    url(r'^(?P<pk>\d+)/dept-query/$', login_required(DeptQueryView.as_view()), name='dept_query_form'),
    url(r'^(?P<pk>\d+)/confirm-query/$', login_required(ConfirmQueryView.as_view()), name='confirm_query_form'),
    url(r'^(?P<pk>\d+)/education/create/$', login_required(EducationCreateView.as_view()), name='education_create'),
    url(r'^(?P<pk>\d+)/education/update/$', login_required(EducationUpdateView.as_view()), name='education_update'),
    url(r'^(?P<pk>\d+)/job/create/$', login_required(JobCreateView.as_view()), name='job_create'),
    url(r'^(?P<pk>\d+)/job/update/$', login_required(JobUpdateView.as_view()), name='job_update'),
    url(r'^(?P<pk>\d+)/email/update/$', login_required(EmailUpdateView.as_view()), name='email_update'),
    url(r'^(?P<pk>\d+)/discipline/$', login_required(DisciplineView.as_view()), name='discipline'),
    url(r'^(?P<pk>\d+)/discipline/create/$', login_required(DisciplineCreateView.as_view()), name='discipline_create'),
    url(r'^(?P<pk>\d+)/discipline/update/$', login_required(DisciplineUpdateView.as_view()), name='discipline_update'),
    url(r'^(?P<pk>\d+)/works/$', login_required(WorkListView.as_view()), name='works'),
    url(r'^(?P<pk>\d+)/works/create/$', login_required(WorkCreateView.as_view()), name='works_create'),
    url(r'^(?P<pk>\d+)/works/update/(?P<number>\d+)/$', login_required(WorkUpdateView.as_view()), name='works_update'),
    url(r'^(?P<pk>\d+)/docs/$', login_required(DocsView.as_view()), name='docs'),
    url(r'^(?P<pk>\d+)/docs/create/$', login_required(DocsCreateView.as_view()), name='docs_create'),
    url(r'^(?P<pk>\d+)/docs/update/(?P<number>\d+)/$', login_required(DocsUpdateView.as_view()), name='docs_update'),
    url(r'^(?P<pk>\d+)/history/$', login_required(HistoryView.as_view()), name='history'),
    url(r'^(?P<pk>\d+)/students/$', login_required(DeptStudentListView.as_view()), name='dept_students')
]