from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing'),
    path('signup/', views.SignupPage.as_view(), name='signup'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('dashboard/', views.DashboardPage.as_view(), name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path('subjects/', views.SubjectsPage.as_view(), name='subjects'),
    path('topics/<int:subject_id>/', views.TopicsPage.as_view(), name='topics'),
    path('topic-info/<int:subject_id>/<int:topic_id>/', views.TopicInfoPage.as_view(), name='topic-info'),
    path('quiz/<int:subject_id>/<int:topic_id>/', views.QuizPage.as_view(), name='quiz-page'),
    path('results/', views.ResultsPage.as_view(), name='results'),
    path('profile/', views.ProfileSettingsPage.as_view(), name='profile')
]
