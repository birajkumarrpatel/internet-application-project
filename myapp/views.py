# Import necessary classes
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.defaultfilters import upper
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from .models import Topic, Course, Student, Order
from .forms import SearchForm, OrderForm, ReviewForm
import operator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list,
                                                'last_login': request.session.get('last_login', False)})


def about(request):
    visits = request.COOKIES.get('about_visits')
    if visits:
        visits = int(visits) + 1
    else:
        visits = 1
    response = render(request, 'myapp/about.html', {'visits': visits})
    response.set_cookie('about_visits', visits, expires=300)
    return response


def detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'myapp/detail.html', {'topic': topic})


def findcourses(request):
    # breakpoint()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            courselist = Course.objects.filter(price__lte=max_price)
            if length:
                courselist = courselist.filter(topic__length=length)
            return render(request, 'myapp/results.html', {'courselist': courselist, 'name': name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=False)
            student = order.student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order,
                                                                 'student': student})
        else:
            return render(request, 'myapp/place_order.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if rating < 1 or rating > 5:
                form.add_error('rating', 'You must enter a rating between 1 and 5!')
                return render(request, 'myapp/review.html', {'form': form})
            review = form.save()
            course = Course.objects.get(id=review.course.id)
            course.num_reviews += 1
            course.save()
            return redirect('myapp:index')
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(timezone.now().isoformat('T', 'seconds'))
                request.session.set_expiry(3600)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myaccount(request):
    if request.user.is_staff:
        return render(request, 'myapp/myaccount.html', {"is_student": False})
    user = Student.objects.get(id=request.user.id)
    return render(request, 'myapp/myaccount.html',
                  {"is_student": True, "name": user, "courses": user.registered_courses.all(),
                   "interested_in": user.interested_in.all()})
