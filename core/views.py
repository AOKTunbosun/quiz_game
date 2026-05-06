from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid

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