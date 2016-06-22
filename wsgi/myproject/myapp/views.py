
# Create your views here.
# -*- coding: utf-8 -*-
from cgi import escape
import datetime
import json
import cStringIO as StringIO
import os
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Permission
from django.core import serializers

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.template import Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from myapp.models import Customer
from myapp.models import Page
from werkzeug.debug import console

from myproject.settings import STATIC_ROOT
from myproject.settings import BASE_DIR


def home(request):

    x = Customer.objects.all()

    #y = Customer.objects.get(id=1)
    #print y.name


    return render(request,'home.html',{'data':x })


def test(request):
    if request.method=="POST":
      addname = request.POST['name']
      addaddress = request.POST['address']
      additem = request.POST['order']
      adddate = request.POST['order_date']
      #z = json.loads(request.body)

      file1 = request.FILES["upload"]
      contentOfFile = file1.read()
        # Other data on the request.FILES dictionary:
        #   filesize = len(file['content'])
        #   filetype = file['content-type']

      filename = file1.name
      imagefile = ["jpeg","jpg","gif","png","bmp"]
      mytypefile = file1.content_type.split('/')[1]
      maxsize = 1000000
      print mytypefile

      if int(file1.size) >= maxsize :
          return HttpResponse("error file size")
      elif mytypefile not in imagefile :
          return HttpResponse("error file type")

      else:
          fd = open('%s/%s' % (os.path.join(os.path.dirname(BASE_DIR), 'static'), filename), 'wb')
          fd.write(contentOfFile)
          fd.close()

          cus1 = Customer(name=addname,address=addaddress,order=additem,order_date=adddate,image=filename)
          cus1.save()
          responsedata = serializers.serialize('json', Customer.objects.all())
          return HttpResponse(responsedata, content_type='json')


    responsedata = serializers.serialize('json', Customer.objects.all())

    return HttpResponse(responsedata, content_type='json')

def recievecount(request):
    recievecount =  request.GET.get('count')
    dbcount = Page.objects.get(id=1)
    Page.objects.filter(id=1).update(counterload=int(recievecount)+dbcount.counterload)
    newcount = Page.objects.get(id=1).counterload
    return HttpResponse(newcount)

def deldata(request):
    datagetdel = request.GET['cid']
    Customer.objects.filter(id=datagetdel).delete()
    ad = serializers.serialize('json', Customer.objects.all())
    return HttpResponse(ad, content_type='json')

def page2(request):
    # page for test code
    u = User.objects.get(username='test')
    permission = Permission.objects.get(name='Can delete customer')
    u.user_permissions.add(permission)
    perm_tuple = [(x.id, x.name) for x in Permission.objects.filter(user=2)] # user 2 is test
    #print perm_tuple
    return render(request,'page2.html')

@ensure_csrf_cookie
@permission_required('myapp.change_customer')
def update(request):
    u = json.loads(request.body)
    #uorder = u['order']
    #udateobj = datetime.datetime.strptime(u['order_date'], "%d/%m/%Y").date()
    Customer.objects.filter(id=int(u['id'])).update(name=u['name'])
    Customer.objects.filter(id=int(u['id'])).update(address=u['address'])
    Customer.objects.filter(id=int(u['id'])).update(order=u['order'])
    Customer.objects.filter(id=int(u['id'])).update(order_date=u['order_date'])

    return HttpResponse('update success.')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

@ensure_csrf_cookie
def signin_view(request):
    signinData = json.loads(request.body)
    user = authenticate(username=signinData['signinUsername'], password=signinData['signinPassword'])
    if user is not None:
          if user.is_active:
            login(request, user)
            return HttpResponse("success")
            # Redirect to a success page.
          else:
            # Return a 'disabled account' error message
            return HttpResponse("error")
    else:
        return HttpResponse("error")


'''def generate_pdf_view(request):
    try:
        # create an API client instance
        client = pdfcrowd.Client("ninenox", "2e6dbe4c1ae886fbae8a10f96149b109")

        # convert a web page and store the generated PDF to a variable
        pdf = client.convertURI("http://www.google.com")

         # set HTTP response headers
        response = HttpResponse(content_type="application/pdf")
        response["Cache-Control"] = "max-age=0"
        response["Accept-Ranges"] = "none"
        response["Content-Disposition"] = "attachment; filename=google_com.pdf"

        # send the generated PDF
        response.write(pdf)
    except pdfcrowd.Error, why:
        response = HttpResponse(mimetype="text/plain")
        response.write(why)
    return response '''



