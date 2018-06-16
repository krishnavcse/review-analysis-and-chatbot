from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.http import Http404
from . amazon import *
import requests
import re
import string
import bcrypt
from django.http import HttpResponseRedirect
import pprint
from .models import *
from .revClassify import *
from .forms import ClassifyForm

plist = []
rdata = []
res = 0
resultt = 0


# the index function is called when root is visited
def index(request):
    request.session.flush()
    return render(request, 'main/index.html')


def register(request):
    errors = User.objects.nameValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            request.session['first_name'] = request.POST['first_name']
            request.session['last_name'] = request.POST['last_name']
            request.session['email'] = request.POST['email']
            return redirect('/')
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                            email=request.POST['email'], password=pwhash)
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        return redirect('/success')


def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
        request.session['last_name'] = User.objects.get(email=request.POST['email']).last_name
        return redirect('/success')


def success(request):
    if 'p_name' in request.GET:
        p_name = request.GET['p_name']
        p_index = request.GET['p_index']
        if p_name:
            request.session['p_cat'] = p_name
            ap = search_p(p_name)
            request.session['p_data'] = ap
            for i, (link, name) in enumerate(request.session['p_data']):
                try:
                    plist.append((i, name))
                except Exception as e:
                    print(e)
            request.session['p_list'] = plist
            l = len(request.session['p_data'])
            print("There are total ", l, " similar products")
        if p_index:
            p_index = int(p_index)
            p_ind = select_num(p_index, request.session['p_data'])
            request.session['p_review'], request.session['p_rth'], request.session['rating'], request.session['url'], \
            request.session['price'], request.session['pname'] = ParseReviews(p_ind)

    else:
        p_name = None
        p_index = None
    return render(request, 'main/success.html')

def sentimentanalysis(request):
    form2 = ClassifyForm()
    revs = []
    revSentimentPairs = []
    sentimentStats = ["N/A", "N/A"]
    loadResults = False
    percent_neg = "0"
    percent_pos = "0"
    text = ""
    textClassification = "none"
    if request.method == 'POST':
        form2 = ClassifyForm(request.POST)
        # pass the classified reviews to the page for populating the table
        if request.session['p_rth']:
            ap = request.session['p_rth']
            revSentimentPairs = classifyRevs(ap)
        sentimentStats = computeSentimentStats(revSentimentPairs)
        percent_neg = sentimentStats[0]
        percent_pos = sentimentStats[1]
        loadResults = True

        if form2.is_valid():
            textClassification = classifySentiment(form2.cleaned_data['text'])
            text = form2.cleaned_data['text']

    return render(request, 'main/sentimentanalysis.html',
                  context={'classifyForm': form2, 'text': text, 'textClassification': textClassification,
                           ' revs': revs, 'pairs': revSentimentPairs, 'percent_neg': percent_neg,
                           'percent_pos': percent_pos, 'loadResults': loadResults})


def previews(request):
    return render(request, 'main/previews.html')


def chat(request):
    request.session.flush()
    context = {}
    return render(request, 'main/chatbot.html', context)


def respond_to_websockets(message):
    greet = {
     'thankyou':    ["you're welcome", "not a problem", "mention not", "it's my pleasure"]
     }  

    result_message = {
        'type': 'text'
    }
    if 'product' in message['text']:
        ap = search_p(message['text'][8:])
        for i, (link, name) in enumerate(ap):
            try:
                plist.append((i, name))
            except Exception as e:
                print(e)
        result_message['text'] = plist
        return result_message
    elif 'return' in message['text']:
        result_message['text'] = "Amazon online returns center provides customers with help pages and details about how to contact them. If the customer wants to return a product, amazon will direct the customer to our online Returns center. Once the customer raises a return request, Amazon handle the customer returns."
        return result_message
    elif 'refund' in message['text']:
        result_message['text'] = "For products sold by you through the Amazon.in website, Customer Executives will process the customer refunds for product returns in accordance with Amazon.in returns policy, the FBA service terms and the selling on Amazon Service terms. Your selling on Amazon report will show these refunds."
        return result_message
    elif 'customer returned products' in message['text']:
        result_message['text'] = "If the technician determine the product is no longer sellable in the same condition as previously listed, amazon will flag it as damaged in your seller account and will hold it temporarily. If you do not tell us within 90 days whether you elect to dispose of the unit or have it returned to you, amazon may choose to dispose of or return it at our discretion."
        return result_message
    elif 'amazon prime' in message['text']:
        result_message['text'] = "Amazon Prime is a membership programme that will offer Amazon customers in over 100 cities unlimited free one-day and two-day delivery on lakhs of eligible products. Amazon Prime Members will also get discounted pricing on scheduled, same-day and morning delivery on thousands of items across 20 cities. In addition, Prime members get early access to top Lightning Deals every day, and exclusive deals on sought-after products."
        return result_message
    elif 'prime delivery' in message['text']:
        result_message['text'] = "All Amazon Prime members receive multiple benefits including FREE one-day and two-day delivery, discounted same-day and/or morning delivery at Rs.50, scheduled delivery at Rs.50 for Prime eligible items. For deliveries to cities not yet eligible for one-day or two-day delivery, members will receive free delivery with no minimum purchase."
        return result_message
    elif message['text'] in ['hi', 'hey', 'hello','hii']:
        result_message['text'] = "Hello to you too! What product do you want? Eg: Product Mobile"
        return result_message
    elif message['text'] in ['thanks', 'thankyou', 'thank you', 'thank', 'good']:
        result_message['text'] = random.choice(greet['thankyou'])
        return result_message
    else:
        result_message['text'] = "I don't know any responses for that. You can try responses out of this(product product_name, return, refund, customer returned products, amazon prime, prime delivery)"
        return result_message
    