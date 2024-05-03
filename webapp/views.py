import numpy as np
from django.shortcuts import render, redirect
from django.db.models import Count



import matplotlib.pyplot as plt


# Create your views here.
def home(request):
    return render(request, 'index.html')


def alogin(request):
    return render(request, 'admin.html')


def ulogin(request):
    return render(request, 'user.html')


def usrreg(request):
    return render(request, 'signup.html')


def signupaction(request):
    email = request.POST['mail']
    pwd = request.POST['pwd']
    zip = request.POST['zip']
    name = request.POST['name']
    age = request.POST['age']
    gen = request.POST['gen']

    d1 = user.objects.filter(email__exact=email).count()
    if d1 > 0:
        return render(request, 'signup.html', {'msg': "Email ALSTMeady Registered"})
    else:
        d = user(name=name, email=email, pwd=pwd, zip=zip, gender=gen, age=age)
        d.save()
        return render(request, 'signup.html', {'msg': "Register Success, You can Login.."})

    return render(request, 'signup.html', {'msg': "Register Success, You can Login.."})


def uloginaction(request):
    if request.method == 'POST':
        uid = request.POST['mail']
        pwd = request.POST['pwd']
        d = user.objects.filter(email__exact=uid).filter(pwd__exact=pwd).count()

        if d > 0:
            d = user.objects.filter(email__exact=uid)
            request.session['email'] = uid

            request.session['name'] = d[0].name
            return render(request, 'user_home.html', {'data': d[0]})

        else:
            return render(request, 'user.html', {'msg': "Login Fail"})

    else:
        return render(request, 'user.html')


def adminlogindef(request):
    if request.method == 'POST':
        uid = request.POST['uid']
        pwd = request.POST['pwd']

        if uid == 'admin' and pwd == 'admin':
            request.session['adminid'] = 'admin'
            return render(request, 'admin_home.html')

        else:
            return render(request, 'admin.html', {'msg': "Login Fail"})

    else:
        return render(request, 'admin.html')


def uhome(request):
    if "email" in request.session:
        uid = request.session["email"]
        d = user.objects.filter(email__exact=uid)
        return render(request, 'user_home.html', {'data': d[0]})

    else:
        return render(request, 'user.html')


def ulogout(request):
    try:
        del request.session['email']
    except:
        pass
    return render(request, 'user.html')


def adminhome(request):
    if "adminid" in request.session:

        return render(request, 'admin_home.html')

    else:
        return render(request, 'user.html')


def trainingpage(request):
    return render(request, 'trainingpage.html')


def cnn(request):
    from .Train_CNN import dl_evaluation_process


    
    acc, precsn, recall, f1score=dl_evaluation_process()
    d=accuracysc.objects.filter(algo='CNN')
    d.delete()
    d=accuracysc(algo='CNN',  accuracyv=acc, prec=precsn, recall=recall, f1sc=f1score)
    d.save()
        
    
    return render(request, 'trainingpage.html', {'msg': "CNN Classifier Training & Testing Completed Successfully"})


def ann(request):
    from .Train_ANN import dl_evaluation_process


    acc, precsn, recall, f1score=dl_evaluation_process()
    d=accuracysc.objects.filter(algo='ANN')
    d.delete()
    d=accuracysc(algo='ANN',  accuracyv=acc, prec=precsn, recall=recall, f1sc=f1score)
    d.save()
    
    
    return render(request, 'trainingpage.html', {'msg': "ANN Classifier Training & Testing Completed Successfully"})
    

def lstm(request):
    from .Train_LSTM import dl_evaluation_process


    acc, precsn, recall, f1score=dl_evaluation_process()
    d=accuracysc.objects.filter(algo='LSTM')
    d.delete()
    d=accuracysc(algo='LSTM',  accuracyv=acc, prec=precsn, recall=recall, f1sc=f1score)
    d.save()
    
    
    return render(request, 'trainingpage.html', {'msg': "LSTM Classifier Training & Testing Completed Successfully"})




def accuracyview(request):
    if "adminid" in request.session:
        d = accuracysc.objects.all()
        accuracygraph()
        precgraph()
        recallgraph()
        f1graph()

        return render(request, 'viewaccuracy.html', {'data': d})
    else:
        return render(request, 'admin.html')




def viewgraphs(request):
    if "adminid" in request.session:
        accuracygraph()
        precgraph()
        recallgraph()
        f1graph()


        return render(request, 'viewgraph.html')
    else:
        return render(request, 'admin.html')








def accuracygraph():
    if True:
        data = {}
        row = accuracysc.objects.filter(algo='CNN')
        rlist = []
        for r in row:
            rlist.append(r.accuracyv)
        data['CNN']=rlist



        row = accuracysc.objects.filter(algo='ANN')
        rlist = []
        for r in row:
            rlist.append(r.accuracyv)
        data['ANN']=rlist



        row = accuracysc.objects.filter(algo='LSTM')
        rlist = []
        for r in row:
            rlist.append(r.accuracyv)
        data['LSTM']=rlist


        from .bargraph import bargraph
        bargraph.view(data,'acc.jpg', 'Accuracy')
      

def precgraph():
    if True:
        data = {}
        row = accuracysc.objects.filter(algo='CNN')
        rlist = []
        for r in row:
            rlist.append(r.prec)
        data['CNN']=rlist



        row = accuracysc.objects.filter(algo='LSTM')
        rlist = []
        for r in row:
            rlist.append(r.prec)
        data['LSTM']=rlist



        row = accuracysc.objects.filter(algo='ANN')
        rlist = []
        for r in row:
            rlist.append(r.prec)
        data['ANN']=rlist


        from .bargraph import bargraph
        bargraph.view(data,'prec.jpg', 'Precision')
          

def recallgraph():
    if True:
        data = {}
        row = accuracysc.objects.filter(algo='CNN')
        rlist = []
        for r in row:
            rlist.append(r.recall)
        data['CNN']=rlist



        row = accuracysc.objects.filter(algo='LSTM')
        rlist = []
        for r in row:
            rlist.append(r.recall)
        data['LSTM']=rlist



        row = accuracysc.objects.filter(algo='ANN')
        rlist = []
        for r in row:
            rlist.append(r.recall)
        data['ANN']=rlist

        from .bargraph import bargraph
        bargraph.view(data,'recall.jpg', 'Recall')
          


def f1graph():
    if True:
        data = {}
        row = accuracysc.objects.filter(algo='CNN')
        rlist = []
        for r in row:
            rlist.append(r.f1sc)
        data['CNN']=rlist



        row = accuracysc.objects.filter(algo='LSTM')
        rlist = []
        for r in row:
            rlist.append(r.f1sc)
        data['LSTM']=rlist



        row = accuracysc.objects.filter(algo='ANN')
        rlist = []
        for r in row:
            rlist.append(r.f1sc)
        data['ANN']=rlist


        from .bargraph import bargraph
        bargraph.view(data,'f1sc.jpg', 'F1 Score')
          

def search(request):
    import sys,tweepy,re
    

    if request.method=='POST':
        keys=request.POST['keys']
        from .TweetSearch import TweetSearch
        l=TweetSearch.search(keys)
        print(l,'><<<<<<<<<<<<<<<<<<<<<<<<')
        ii=1
       

        from .LSTM import get_predictions
        res=get_predictions(l)
   
        
        print("res=",res)

        t=tweets.objects.all()
        t.delete()


        
        print(l)
        for l1 in range(len(res)):
            try:
                r=tweets(sno=ii,tweet=l[l1], sentiment=res[l1])
                r.save()
            except:
                pass
            ii=ii+1

        data=tweets.objects.all()
        print("data=",data)

    
        return render(request, 'tweetsresults.html',{'data':data})


    else:
        return render(request, 'search.html')

def sentiresults(request):
    from .Freq import CountFrequency
    from .Graphs import viewg

    senti=[]
 

    if "email" in request.session:
        data=tweets.objects.all()
        for d1 in data:
            senti.append(d1.sentiment)

        d=CountFrequency(senti)
        viewg(d)
            

    
        return render(request, 'tweetsresults2.html',{'data':data})


    else:
        return render(request, 'user.html')



def viewgraph2(request):
    if "email" in request.session:

        from PIL import Image 

        im = Image.open(r"g1.jpg") 
          
        im.show()
        
        

        return redirect('sentiresults')


