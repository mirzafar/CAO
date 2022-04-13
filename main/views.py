from django.shortcuts import render
from main.models import *
import requests
from django.shortcuts import redirect
import re
from datetime import datetime
import os, uuid
from mysite.settings import BASE_DIR
from django.http.response import JsonResponse
import base64
from django.core.files.base import ContentFile
from django.db.models import Q


def indexHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    if active_user != None:
        users = SiteUser.objects.filter(id=user_id)
    else:
        users = SiteUser.objects.all()

    return render(request, 'index.html', {'users': users,
                                          "user_id": user_id,
                                          "active_user": active_user
                                          })


def overheadAddHandler(request, us_id):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    item = SiteUser.objects.get(id=int(us_id))
    citys = City.objects.all()

    errors = []
    if request.POST:
        action = request.POST.get('action', '')
        from_city = int(request.POST.get('from_city', 0))
        to_city = int(request.POST.get('to_city', 0))
        day = int(request.POST.get('day', 0))
        sum = float(request.POST.get('sum', 0))
        rate_dollar = float(request.POST.get('rate_dollar', 0))
        date = request.POST.get('date', '')
        if action == 'ADD':
            oh = Overhead()
            if from_city:
                oh.from_city_id = from_city
            else:
                errors.append('From city not found ')
            if to_city:
                oh.to_city_id = to_city
            else:
                errors.append('To city not found ')
            if day:
                oh.day = day
            else:
                errors.append('Day not found ')
            if sum:
                oh.sum = sum
            else:
                errors.append('Sum not found ')
            if rate_dollar:
                oh.rate_dollar = rate_dollar
            else:
                errors.append('Rate dollar not found ')
            if date:
                oh.date = date
            else:
                errors.append('Date not found ')
            oh.user_id = us_id
            if not errors:
                oh.save()
                response = JsonResponse({'status': True}, status=200)
            else:
                response = JsonResponse({'status': False, 'errors': errors}, status=200)
            return response

    return render(request, "overhead-add.html", {"citys": citys,
                                                 "item": item,
                                                 "user_id": user_id,
                                                 "active_user": active_user,
                                                 "errors": errors
                                                 })


def overheadHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    oc_user_id = int(request.GET.get('oc_user_id', 0))

    if oc_user_id:
        overheads = Overhead.objects.filter(user__id=int(oc_user_id))
    else:
        if active_user != None:
            overheads = Overhead.objects.filter(user__id=user_id)
        else:
            overheads = Overhead.objects.all()

    yr = []
    for i in range(2015, 2025):
        yr.append(i)

    day1 = request.POST.get('day1', None)
    month1 = request.POST.get('month1', None)
    year1 = int(request.POST.get('year1', 0))
    day2 = request.POST.get('day2', None)
    month2 = request.POST.get('month2', None)
    year2 = int(request.POST.get('year2', 0))

    if request.POST:
        action = request.POST.get('action', '')
        ohid = int(request.POST.get('id', 0))
        dd = int(request.POST.get('dd', 0))

        if action == 'del_overhead':
            hh = Overhead.objects.get(id=ohid)
            hh.delete()
            if dd != 0:
                return redirect(f'/overhead/?oc_user_id={dd}')
            else:
                return redirect('/overhead/')
        elif action == 'srch':
            start, end = None, None

            try:
                a = str(year1) + "-" + str(month1) + "-" + str(day1)
                b = str(year2) + "-" + str(month2) + "-" + str(day2)

                start = datetime.strptime(a, '%Y-%m-%d')
                end = datetime.strptime(b, '%Y-%m-%d')
            except:
                pass

            if start and end:
                if oc_user_id:
                    overheads = Overhead.objects.filter(user__id=int(oc_user_id)).filter(date__range=[start, end])
                else:
                    if active_user != None:
                        overheads = Overhead.objects.filter(user__id=user_id).filter(date__range=[start, end])
                    else:
                        overheads = Overhead.objects.filter(date__range=[start, end])

    return render(request, "overhead.html", {"overheads": overheads,
                                             "user_id": user_id,
                                             "active_user": active_user,
                                             "oc_user_id": oc_user_id,
                                             "yr": yr,
                                             "day1": day1,
                                             "day2": day2,
                                             "month1": month1,
                                             "month2": month2,
                                             "year1": year1,
                                             "year2": year2
                                             })


def overheadInfoHandler(request, overhead_id):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = SiteUser.objects.get(id=int(user_id))

    overheads = Overhead.objects.get(id=int(overhead_id))
    citys = City.objects.all()
    expensess = Expenses.objects.all()
    overhead_charges = OverheadCharges.objects.filter(overhead__id=overhead_id)

    total = 0
    for summ in overhead_charges:
        total += summ.sum
    total = round(total, 2)


    errors = []
    if request.POST:
        action = request.POST.get('action', '')
        from_city = int(request.POST.get('from_city', 0))
        to_city = int(request.POST.get('to_city', 0))
        day = request.POST.get('day', '')
        sum = request.POST.get('sum', '')
        rate_dollar = request.POST.get('rate_dollar', '')
        date = request.POST.get('date', '')
        state = request.POST.get('state', '')

        expenses = int(request.POST.get('expenses', 0))
        emount = request.POST.get('emount', '')
        cost = float(request.POST.get('cost', 0))
        sum2 = float(request.POST.get('sum', 0))

        oc_id = int(request.POST.get('oc_id', 0))

        if action == 'EDIT':
            oh = Overhead.objects.get(id=int(overhead_id))
            oh.from_city = City.objects.get(id=int(from_city))
            oh.to_city = City.objects.get(id=int(to_city))
            oh.day = day
            oh.sum = sum
            oh.rate_dollar = rate_dollar
            oh.date = date
            oh.state = state
            oh.save()
            return redirect(f'/overhead/{overhead_id}/')

        elif action == 'add_exp':
            oc = OverheadCharges()
            oc.overhead = Overhead.objects.get(id=int(overhead_id))
            if expenses:
                oc.expenses = Expenses.objects.get(id=int(expenses))
            else:
                errors.append('Expenses not found ')
            if cost:
                oc.cost = cost
            else:
                errors.append('Cost not found ')
            if emount:
                oc.emount = emount
            else:
                errors.append('Emount not found ')
            if sum2:
                oc.sum = sum2
            else:
                errors.append('Sum not found ')
            if not errors:
                oc.save()
                response = JsonResponse({'status': True}, status=200)
            else:
                response = JsonResponse({'status': False, 'errors': errors}, status=200)
            return response

        elif action == 'del_oc':
            hh = OverheadCharges.objects.get(id=oc_id)
            hh.delete()
            return redirect(f'/overhead/{overhead_id}/#section2')

    return render(request, "overheadinfo.html", {"overheads": overheads,
                                                 "citys": citys,
                                                 "expensess": expensess,
                                                 "overhead_charges": overhead_charges,
                                                 "total": total,
                                                 "user_id": user_id,
                                                 "active_user": active_user,
                                                 "errors": errors
                                                 })


def loginHandler(request):
    post_error = ''
    if request.POST:
        login = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if login and password:
            site_user = SiteUser.objects.filter(login=login).filter(password=password)
            if site_user:
                site_user = site_user[0]
                request.session['user_id'] = site_user.id
                return redirect('/')
            else:
                post_error = 'USER_NOT_FOUND'
        else:
            post_error = 'ERROR_ARGUMENTS'

    return render(request, 'login.html', {'post_error': post_error})


def logoutHandler(request):
    request.session['user_id'] = None
    return redirect('/')


