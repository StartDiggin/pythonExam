# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from ..login_app.models import User
from .models import List
from django.contrib import messages


# Route to index --> /friend/
def index(request):
    if not 'id' in request.session:
        messages.error(request,'Please log in again!')
        return redirect('/')


    context={
    'user': User.objects.get(id=request.session['id']),
    'otherUsers': User.objects.exclude(id=request.session['id']),
    'userFriends': List.objects.all(),
    # 'userFriends': List.objects.filter(userfriend__id=request.session['id']),
    }

    return render(request,'friend_app/index.html',context)

# Route to show user profile --> /friend/show/{{id}}
def show(request, id):
    if not 'id' in request.session:
        messages.error(request,'Please log in again!')
        return redirect('/')
    return render(request,'friend_app/friend.html',{'user':User.objects.get(id=id)})

# Route to add a user to friend list --> /friend/add/{{id}}
def add(request, id):
    user = User.objects.get(id=id)
    cur_user = User.objects.get(id=request.session['id'])
    list1 = List.objects.create(friend=cur_user)
    list1.userfriend.add(user)

    return redirect('/friend/')

# Route to remove a user --> /friend/remove/{{id}}
def remove(request, id):
    List.objects.get(id=id).delete()
    return redirect('/friend')
