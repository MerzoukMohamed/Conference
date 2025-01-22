from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import ProtectedError
from django.http import HttpResponse

from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, CreateView, UpdateView, RedirectView, DetailView, DeleteView, TemplateView

from .forms import EvalForm, CherForm,ConfForm, ComiteForm
from mybasic_app.models import User,Conferance,Article, Commite,Topic,Evaluateur

from mybasic_app.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required



from django.contrib import messages

  # donc ydkol SSi ykon Admin
@method_decorator([login_required, staff_member_required], name='dispatch')
class HomePageView(TemplateView): 
    template_name= "accounts/dashboard.html"


#///////////////////partie evaluateur////////////////////////////////// 
@method_decorator([login_required, staff_member_required], name='dispatch')
class evalList(ListView):
   template_name = 'accounts/liste_eval.html'
   model = User        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    context['number'] = User.objects.filter(is_evaluteur=True).count()
 
    return context


#///////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class EvalCreateView(CreateView):
    template_name = "accounts/addUser.html"
    form_class = EvalForm
        
    def form_valid(self, form):
        
       return super(EvalCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ges_eval')

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class EvalUpdateView(UpdateView):
    template_name = 'accounts/edit_user.html'
    model = User
    form_class = EvalForm
    

    def get_success_url(self):
        return reverse_lazy('ges_eval')

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class EvalDeleteView(DeleteView):
    model = User

    template_name = 'accounts/evaluateur_confirm_delete.html'

    def form_valid(self, form):       
        return super(EvalDeleteView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('ges_eval')





#///////////////////partie chercheur//////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class cherList(ListView):
   template_name = 'accounts/liste_cher.html'
   model = User        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['number'] = User.objects.filter(is_chercheur=True).count()
    return context

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class CherCreateView(CreateView):
    template_name = "accounts/addUser.html"
    form_class = CherForm
        
    def form_valid(self, form):
        
        return super(CherCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ges_cher')

#////////////////////////////////////////////////////////////////////////////////////////////////



@method_decorator([login_required, staff_member_required], name='dispatch')
class CherUpdateView(UpdateView):
    template_name = 'accounts/edit_user.html'
    model = User
    form_class = CherForm

    def get_success_url(self):
        return reverse_lazy('ges_cher')


#////////////////////////////////////////////////////////////////////////////////////////////////


@method_decorator([login_required, staff_member_required], name='dispatch')
class CherDeleteView(DeleteView):
    model = User
    template_name = 'accounts/chercheur_confirm_delete.html'

    def form_valid(self, form):
        
        return super(CherDeleteView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('ges_cher')



 
#################################################    Le 15/07/2020  Toooooooopic      ########################""""


from accounts.forms import topicForm


@method_decorator([login_required, staff_member_required], name='dispatch')
class TopicList(ListView):
   template_name = 'accounts/TopicList.html'
   model = Topic        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['number'] = Topic.objects.all().count()
    return context

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class TopicCreateView(CreateView):
    template_name = "accounts/TopicCreat.html"
    form_class = topicForm
        
    def form_valid(self, form):
        
        return super(TopicCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('confCreate')

#////////////////////////////////////////////////////////////////////////////////////////////////



@method_decorator([login_required, staff_member_required], name='dispatch')
class TopicUpdate(UpdateView):
    template_name = 'accounts/topicEdit.html'
    model = Topic
    form_class = topicForm

    def get_success_url(self):
        return reverse_lazy('ges_Topic')


#////////////////////////////////////////////////////////////////////////////////////////////////


@method_decorator([login_required, staff_member_required], name='dispatch')
class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'accounts/Topic_Confirm_delete.html'

    def form_valid(self, form):
        
        return super(TopicDeleteView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('ges_Topic')





#################################################################################
###########################    t3 Gconf ############################################"""

import datetime

@method_decorator([login_required, staff_member_required], name='dispatch')
class confList(ListView):
   template_name = 'gConf/list_Conf.html'
   model = Conferance        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['number'] = Conferance.objects.all().count()
    context['Now'] = datetime.datetime.now()
    return context
#///////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class ConfCreateView(CreateView):
    template_name = "gConf/add-conf.html"
    form_class = ConfForm
        
    def form_valid(self, form):
       return super(ConfCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ges_conf')

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class ConfUpdateView(UpdateView):
    template_name = 'gConf/edit_conf.html'
    model = Conferance
    form_class = ConfForm

    def get_success_url(self):
        return reverse_lazy('ges_conf')



#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class ConfDetailView(DetailView):
    template_name = 'gConf/edit_conf.html'
    model = Conferance


#///////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class Confmodifier(DetailView):
    template_name = 'gConf/modifier.html'
    model = Conferance



#//////////////////////////////////////////////////////////
@login_required
@staff_member_required
def ArticlList_Conf(request, pk):
    conferance = Conferance.objects.get(id = pk)
    articles= Article.objects.filter(Conferance = conferance)
    Nbr_Articl = articles.count()
    context = {'articles':articles, 'conferance':conferance, 'Nbr_Articl':Nbr_Articl}
    return render(request, 'gConf/Arctl_conf.html', context)


#//////////////////////////////////// 03/07/2020 ///////////////////////////////////////////////////////////
from django.core.mail import send_mail, BadHeaderError
from learning_user import settings 



@login_required
@staff_member_required
def Stop_Ou_Cont_Conf(request,pk):
    Conff = get_object_or_404(Conferance, pk=pk)
    Conff.Stop_contuneé_Conf()
    Conff.save()
    return redirect('ges_conf')




from email.message import EmailMessage
from random import randint
@login_required
@staff_member_required
def ComiteCreate(request):
    chairmen = request.user   # pcq li ydkhol hna how ciarmn li ycryiha
    form = ComiteForm()
    if request.method == 'POST':
        form = ComiteForm(request.POST)

        ren = request.POST['amount']
        ren = int(ren)

        bros= set()


        print('++++++++++++++++++++++++++++')
        print(ren)
        print('++++++++++++++++++++++++++++')
                                                ###  problem de username 
        for x in range(0 , ren) :
            first = request.POST.get(str(x) +"0", "y445")
            family = request.POST.get(str(x) +"1" , "y41394")
            idnumber = request.POST.get(str(x) +"2" ,"144098")
            mail =request.POST.get(str(x) +"3","y4315")
            number =request.POST.get(str(x) +"4","3413")
            country = request.POST.get(str(x) +"5","y4315")
            city = request.POST.get(str(x) +"6","y43165")
            postal_code = request.POST.get(str(x) +"7","4313")
            organization = request.POST.get(str(x) +"8","43195")
 
     #J       ussser = User.objects.create(username = randint(1 , 458) , password= "123456789" , first_name= first ,
       #     last_name=family  , numbr_Identd= idnumber , email= mail ,
        #    Phone= number , Country= country , City=  city ,
         #   Post_code=postal_code , Organization= organization)
      #      ussser.is_evaluteur=True
     #       ussser.save()

            ussser = User.objects.create(username = randint(1 , 1000) , password= "123456789" , first_name= first ,
            last_name=family  , numbr_Identd= randint(1 , 9999999), email= mail ,
            Phone= number , Country= country , City=  city ,
            Post_code=postal_code , Organization= organization)
            ussser.is_evaluteur=True
            ussser.save()





            evval = Evaluateur.objects.create(user = ussser , email=mail   ) 
            evval.save()
            bros.add(evval)
        
        if form.is_valid():
             comite = form.save(commit=False)
             comite.charmain = chairmen
             comite.save()


             for ev_ancien in  form.cleaned_data['evaluteur_list'] :
                bros.add(ev_ancien)


             for bro in bros :
                 comite.evaluteur_list.add(bro)
                 comite.save()

             for us in comite.evaluteur_list.all() :
                subject = f'validation de Comite pour vous: , from Makani -CF-' 

                      
                message = 'Vous avez ajoute dans comite   : '+str(comite.Name)+'  \n  Par le chairmaine    : '+str(comite.charmain)+'  \n Votre compte tempriare \n \n Username  : '+str(us.user.username)+'   ____ password  :  ' +str(us.user.password) +''' \n
           - mais attention il faut changer votre donne primeir pour bien sucriseé votre compte  : \n 
           clique ici >>> aprr ndiro lien 
                    \n
                          \n                 
                         \n \n \n   
                         , en attend votre repondre ,Merci !!!    , 
                           *** 
                    '''

                sender = settings.EMAIL_HOST_USER
                recipients = str(us.email)

                print('****************************',recipients,'****************************')
                
                try:
                    send_mail(subject, message, sender, [recipients], fail_silently=True)
                except BadHeaderError:
                    return HttpResponse('Invalid header found,Attention')


             messages.success(request,"Your Comite was Created successfully en attend la reponse de votre Mombre !!!,From @Makani-CF- ")
             return redirect('confCreate')
    
    context = {'form': form, 'charmain':chairmen}
    return render(request, 'gConf/add_comite.html' ,context)












#//////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class ComiteUpdateView(UpdateView):
    template_name = 'gConf/edit_comite.html'
    model = Commite
    form_class = ComiteForm
    
    def get_success_url(self):
        return reverse('modifier',kwargs={'pk': self.object.pk})




############################################################################
# +++++++++++++++++++  Statistique rusalt with charJs and django  03/06/2020 ++++++++++++++++++++         
from mybasic_app.models import (User,Conferance,Article, Commite,
Evaluateur,Chercheur,Commite)
from django.http import JsonResponse




def StatistiQue_Data_evl_artcl(request):
    Eval_data = []
    evl =Evaluateur.objects.all()
    for e in evl :
        d=0
        d=e.artcl_a_corrige.all().count()
        Eval_data.append({e.user.username:d})
    return JsonResponse(Eval_data,safe=False)




def StatistiQue_Data_comite_eval(request):
    Comite_data = []
    Cm = Commite.objects.all()

    for c in Cm :
        d=0
        for i in c.evaluteur_list.all():
            d+=1
        Comite_data.append({c.Name:d})
    return JsonResponse(Comite_data,safe=False)



def StatistiQue_Data_articl_chrch(request):
    Artcl_Data = []
    Art = Article.objects.all()
    Chr=Chercheur.objects.all()
    for ch in Chr:
        d=0
        for c in Art:
            if c.author == ch :
                d+=1    
        Artcl_Data.append({ch.user.username:d})
        
    return JsonResponse(Artcl_Data,safe=False)






def StatistiQue_Data_Conf_topic(request):
    Conf_Data = []
    Conf_Data.append({"":""})
    Conf = Conferance.objects.all()

    for c in Conf :
        for i in c.topic.all():
            Conf_Data.append({c.title:i.title})
        
    return JsonResponse(Conf_Data,safe=False)






def StatistiQue_Data_articl_Confreance(request):
    Artcl_Data = []
    Art = Article.objects.all()
    Conf = Conferance.objects.all()
    for cf in Conf:
        d=0
        for c in Art:
            if c.Conferance == cf :
                d+=1    
        Artcl_Data.append({cf.title:d})
        
    return JsonResponse(Artcl_Data,safe=False)





# >>>>>>>>>>>>>>>>>>>>>>>>>>< Le 16/07/2020    evaluation Final de chairmen !!!!!!!!!!!!!!

 
import datetime
from accounts.forms import EvaluationFinalForm
from G__evaluation.models import Etat_Artcile,Resultat
from django.shortcuts import get_object_or_404

@login_required
@staff_member_required
def All_Mes_Artcl(request):
    chairement = request.user
    etat_artciles = Etat_Artcile.objects.filter(chairement=chairement)    
    Now = datetime.datetime.now()
    context = { 'etat_artciles':etat_artciles,'Now':Now}
    return render(request,'gCommite/All_Article.html' , context)




@login_required
@staff_member_required
def Evalueé(request,pk):
    
    article = get_object_or_404(Article, pk=pk)
    etat_artciles=Etat_Artcile.objects.filter(article=article)

    if request.method == 'POST' :
        form = EvaluationFinalForm(request.POST )
        if form.is_valid():
            Resultat = form.save()
            Resultat.article=article
            Resultat.chairement=request.user
            Resultat.chrchr=article.author
            Resultat.save()
            article.evaluéé_Art()  
            
            return redirect('Mes_Evaluation')
    else :
        form  = EvaluationFinalForm()
    return render(request,'gCommite/Complte_Evaluation_Fial.html',{'form' : form,'article':article,'etat_artciles':etat_artciles})         








@login_required
@staff_member_required
def Mes_Evaluation(request):
    article = Article.objects.all()
    etat_artciles=Etat_Artcile.objects.filter(article=article)
    rusalt=Resultat.objects.filter(chairement=request.user)
    context = { 'etat_artciles':etat_artciles,'rusalt':rusalt}
    return render(request,'gCommite/Mes_Evaluation.html' , context)


