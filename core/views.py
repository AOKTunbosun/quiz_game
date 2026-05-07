from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid

from .models import Subject, Topic

# Create your views here.
User = get_user_model()


class LandingPage(View):
    def get(self, request):
        context = {}
        return render(request, 'core/landing.html', context)
    

class SignupPage(View):
    def get(self, request):
        context = {}
        return render(request, 'core/signup.html', context)
    
    def post(self, request):
        first_name = request.POST.get('first_name').strip().capitalize()
        last_name = request.POST.get('last_name').strip().capitalize()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password').strip()
        current_class = request.POST.get('class_level').strip()
        school_name = request.POST.get('school_name').strip()
        mother_name = request.POST.get('mother_name').strip()
        father_name = request.POST.get('father_name').strip()
        phone_number = request.POST.get('student_phone').strip()
        parent_phone_number = request.POST.get('parent_phone').strip()
        parent_email = request.POST.get('parent_gmail').strip()
        home_address = request.POST.get('address').strip()

        username = email.split('@')[0] + str(uuid.uuid4())[:10]

        if password != confirm_password:
            messages.error(request, 'Password and confirm password must be the same')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
                messages.error(request, 'Email has already been used')
                return redirect('signup')
        try:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    phone_number=phone_number,
                    password=password,
                    current_class=current_class,
                    school_name=school_name,
                    mother_name=mother_name,
                    father_name=father_name,
                    parent_phone_number=parent_phone_number,
                    parent_email=parent_email,
                    home_address=home_address                    
                )

                login(request, user)
                return redirect('dashboard')

        except Exception as e:
            print(e)
            messages.error(request, 'Error trying to create your account')
            return redirect('signup')


class LoginPage(View):
    def get(self, request):
        context = {}
        return render(request, 'core/login.html', context)
    
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)


        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        remember_me = request.POST.get('remember_me')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(
                request, message='User does not exist, try signing up')
            return redirect('login')

        except User.MultipleObjectsReturned:
            messages.error(
                request, message='Multiple accounts found for this email')
            return redirect('login')

        user = authenticate(request, username=user.username, password=password)

        if not remember_me:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(60*60*24*30)

            
        login(request, user)
        return redirect('dashboard')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


class DashboardPage(View):
     @method_decorator(login_required)
     def get(self, request):
          context = {'student': {
               'class_level': request.user.current_class,
               'school_name': request.user.school_name,
          },
          'total_quizzes_taken': 15,
          'average_score': 78,
          'best_score': 95,
          'pending_quizzes': 8,
          'recommended_topics': [
               {
                    'id': 1, 
                    'name': 'Computer Hardware',
                    'description': 'Learn about CPT, RAM and storage',
                    'difficulty': 'medium'
               },
               {
                    'id': 2, 
                    'name': 'Networking Basics',
                    'description': 'Understanding LAN, WAN, and internet protocols',
                    'difficulty': 'hard'
               }
          ],
          'available_quizzes': [
               {
                    'id': 1,
                    'title': 'Introduction to Computers',
                    'icon': 'fa-desktop',
                    'time_minutes': 15,
                    'question_count': 20,
               },
               {
                    'id': 2,
                    'title': 'Computer Hardware Quiz',
                    'icon': 'fa-microchip',
                    'time_minutes': 20,
                    'question_count': 25,
               }
          ]
          }
          return render(request, 'core/dashboard.html', context)
     
     def post(self, request):
          pass
     

class SubjectsPage(View):
    def get(self, request):
        subjects = Subject.objects.all()

        context = {'subjects': subjects}
        return render(request, 'core/subjects.html', context)


class TopicsPage(View):
    def get(self, request, subject_id):
        topics = Topic.objects.filter(subject=subject_id)

        topic = topics.first()
        
        if topic is None:
            subject = Subject.objects.get(id=subject_id)
            print(subject)
            subject_info = {
                'id': subject.id,
                'name': subject.name,
                'description': subject.description,
                'icon': subject.icon
                }
        
        else:
            subject_info = {
                'id': topic.subject.id,
                'name': topic.subject.name,
                'description': topic.subject.description,
                'icon': topic.subject.icon
                }


        topics_list = []
        for each in topics:
            each_topic = {
                    'id': each.id,
                    'name': each.name,
                    'short_description': each.description,
                    'estimated_minutes': each.estimated_minutes,
                    'question_count': each.question_count,
                }
            topics_list.append(each_topic)

        context = {
            'subject': subject_info,
            'topics': topics_list
            }
        
        return render(request, 'core/topics.html', context)
    

class TopicInfoPage(View):
    def get(self, request, subject_id, topic_id):
        context = {
            'subject': {
                'id': 1,
                'name': 'Computer Studies',
            },
            'topic': {
                'id': 1,
                'name': 'Computer Hardware',
                'icon': 'fa-microchip',
                'estimated_minutes': 20,
                'question_count': 25,
            },
            'topic_info': {
                'short_note': 'Computer hardware refers to the physical components that make up a computer system. These include the CPU (Central Processing Unit), RAM (Random Access Memory), storage devices (HDD/SSD), motherboard, power supply, and input/output devices like keyboard, mouse, and monitor.',
                'learning_objectives': 'By the end of this topic, you will be able to:',
                'objectives_list': [
                    'Identify and name the major hardware components of a computer',
                    'Explain the function of the CPU and how it processes data',
                    'Differentiate between RAM and ROM',
                    'List various input and output devices',
                    'Understand storage devices and their capacities'
                ],
                'key_points': 'Remember: Hardware is physical (you can touch it). The CPU is the "brain" of the computer. RAM is temporary memory, storage is permanent.',
            }
        }
        return render(request, 'core/topics_info.html', context)
    

class QuizPage(View):
    def get(self, request, subject_id, topic_id):
        context = {
            'subject': {
                'id': 1,
                'name': 'Computer Studies',
            },
            'topic': {
                'id': 1,
                'name': 'Computer Hardware',
                'question_count': 3,
            },
            'total_minutes': 20,
            'questions': [
                {
                    'id': 1,
                    'question_text': 'What does CPU stand for?',
                    'option_a': 'Central Processing Unit',
                    'option_b': 'Computer Personal Unit',
                    'option_c': 'Central Program Utility',
                    'option_d': 'Core Processing Union',
                },
                {
                    'id': 2,
                    'question_text': 'Which of the following is an input device?',
                    'option_a': 'Monitor',
                    'option_b': 'Printer',
                    'option_c': 'Keyboard',
                    'option_d': 'Speaker',
                },
                {
                    'id': 3,
                    'question_text': 'What is RAM?',
                    'option_a': 'Readily Available Memory',
                    'option_b': 'Random Access Memory',
                    'option_c': 'Rapid Access Module',
                    'option_d': 'Read Access Memory',
                },
            ]
        }
        return render(request, 'core/quiz.html', context)


    def post(self, request, subject_id, topic_id):
        pass


class ResultsPage(View):
    def get(self, request):
        context = {
            'total_quizzes': 8,
            'average_score': 72,
            'best_score': 95,
            'total_correct': 142,
            'results': [
                {
                    'id': 1,
                    'topic_name': 'Computer Hardware',
                    'completed_at': '2026-05-01',
                    'score': 18,
                    'total_questions': 20,
                    'percentage': 90,
                },
                {
                    'id': 2,
                    'topic_name': 'Computer Software',
                    'completed_at': '2026-04-28',
                    'score': 15,
                    'total_questions': 20,
                    'percentage': 75,
                },
                {
                    'id': 3,
                    'topic_name': 'Networking Basics',
                    'completed_at': '2026-04-25',
                    'score': 10,
                    'total_questions': 20,
                    'percentage': 50,
                },
                {
                    'id': 4,
                    'topic_name': 'History of Computers',
                    'completed_at': '2026-04-20',
                    'score': 8,
                    'total_questions': 20,
                    'percentage': 40,
                },
            ]
        }
        return render(request, 'core/results.html', context)


class ProfileSettingsPage(View):
    def get(self, request):
        context = {
            'student': {
                'class_level': 'SS2',
                'school_name': 'Springfield High School',
                'student_phone': '08012345678',
                'mother_name': 'Mrs. Jane Doe',
                'father_name': 'Mr. John Doe',
                'parent_phone': '08098765432',
                'parent_gmail': 'parent@gmail.com',
                'address': '123 Main Street, Lagos, Nigeria',
            }
        }
        return render(request, 'core/profile_settings.html', context)

    def post(self, request):
        pass