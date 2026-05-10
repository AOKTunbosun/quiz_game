from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid

from .models import *

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
        results_query = QuizResult.objects.filter(student=request.user)

        results = []
        for each in results_query:
            result_record = {
                'score': each.score,
                'total_questions': each.total_questions,
                'percentage': round(each.score/each.total_questions * 100, 2),
            }
            results.append(result_record)
        
        each_score = []
        for each in results:
            each_score.append(each['percentage'])
        
        total = 0
        for each in each_score:
            total += each

        try:
            average_score = total/len(each_score)
        except:
            average_score = 0

        print(results)
        print(each_score)
        print(total)
        print(average_score)
        print(max(results, key=lambda x: x['percentage'])['percentage'])



        context = {'student': {
               'class_level': request.user.current_class,
               'school_name': request.user.school_name,
          },
          'total_quizzes_taken': len(results),
          'average_score': round(average_score, 2),
          'best_score': max(results, key=lambda x: x['percentage'])['percentage'] if results else 0,
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
        topic = Topic.objects.select_related('topic_info').get(id=topic_id)
        
        if topic is None:
            subject = Subject.objects.get(id=subject_id)
            subject_info = {
                'id': subject.id,
                'name': subject.name
                }
        
        else:
            subject_info = {
                'id': topic.subject.id,
                'name': topic.subject.name
                }


        context = {
            'subject': subject_info,
            'topic': {
                'id': topic.id,
                'name': topic.name,
                'icon': topic.subject.icon,
                'estimated_minutes': topic.estimated_minutes,
                'question_count': topic.question_count,
            },
            'topic_info': {
                'short_note': topic.topic_info.short_note,
                'learning_objectives': topic.topic_info.learning_objectives,
                'key_points': topic.topic_info.key_points.split(' | '),
            }
        }
        return render(request, 'core/topics_info.html', context)
    

class QuizPage(View):
    def get(self, request, subject_id, topic_id):
        topic = Topic.objects.get(id=topic_id)
        quiz_questions = QuizQuestion.objects.filter(topic=topic).order_by('order')

        questions = []
        for question in quiz_questions:
            each = {
                    'id': question.order,
                    'question_text': question.question_text,
                    'option_a': question.option_a,
                    'option_b': question.option_b,
                    'option_c': question.option_c,
                    'option_d': question.option_d,
                }
            questions.append(each)


        context = {
            'subject': {
                'id': topic.subject.id,
                'name': topic.subject.name,
            },
            'topic': {
                'id': topic.id,
                'name': topic.name,
                'question_count': topic.question_count,
            },
            # 'total_minutes': 20,
            'questions': questions
        }
        return render(request, 'core/quiz.html', context)


    def post(self, request, subject_id, topic_id):
        topic = Topic.objects.get(id=topic_id)
        quiz_questions = QuizQuestion.objects.filter(topic=topic).order_by('order')


        score = 0
        correct_answers = 0
        for x, y in zip(range(1, topic.question_count+1), quiz_questions):
            option = request.POST.get(f'question_{x}').lower()
            question = y
            if option == question.correct_answer.lower():
                score += 1
                correct_answers += 1
        
        QuizResult.objects.create(
            student=request.user,
            topic=topic,
            score=score,
            total_questions=topic.question_count,
            correct_answers=correct_answers
        )

        return redirect('results')


class ResultsPage(View):
    def get(self, request):
        results_query = QuizResult.objects.filter(student=request.user)

        results = []
        for each in results_query:
            result_record = {
                'id': each.id,
                'topic_name': each.topic.name,
                'completed_at': each.completed_at,
                'score': each.score,
                'total_questions': each.total_questions,
                'percentage': round(each.score/each.total_questions * 100, 2),
            }
            results.append(result_record)

        
        total_correct = 0
        for each in results_query:
            total_correct += each.correct_answers

        each_score = []
        for each in results:
            each_score.append(each['percentage'])
        
        total = 0
        for each in each_score:
            total += each

        try:
            average_score = total/len(each_score)
        except:
            average_score = 0

        context = {
            'total_quizzes': len(results),
            'average_score': round(average_score, 2),
            'best_score': max(results, key=lambda x: x['percentage'])['percentage'] if results else 0,
            'total_correct': total_correct,
            'results': results
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