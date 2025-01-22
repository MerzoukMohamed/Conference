from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import evaluteur_required
from ..forms import  EvaluteurSignUpForm,From_Edite_Profile,EvaluationForm
from ..models import  User,Evaluateur,Article,Conferance,Commite

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.messages.views import SuccessMessageMixin




##################################################"""""" hadi rahi ziyada pcq galk eval ma inscreach nta t3ytlehe 

class EvaluteurSignUpView(SuccessMessageMixin,CreateView):
    model = User
    form_class = EvaluteurSignUpForm
    template_name = 'registration/signup.html'
    success_message = "You'r Profile was Create successfully as Evaluateur"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'evaluteur'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        #if Evaluteur.Code_Eval =="makani" :
        user = form.save()
        login(self.request, user)
        return redirect('evaluteur:dashboardeval')         # hadi dashboard en genralle ga33
        #else :
            #return HttpResponseRedirect(reverse('homme'))
            
#########################################################################################################################""



# ++++++++++++++++++++++++ notification  1/06/2020
from Notification.models import Notification
@login_required
@evaluteur_required
def profil_eval(request):
    n=Notification.objects.filter(user=request.user,As_viewed=False)
    usrr=request.user
    messages.info(request,'Hi '+ str(usrr)+'  , From Makni-CF-')
    return render(request,'Templevaluteur/Dachboardeval.html',{'notifications':n})





# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
@login_required
@evaluteur_required
def Usereval(request):
    usrr=request.user
    messages.info(request,'Hi '+ str(usrr)+'  , From Makni-CF-')
    return render(request,'Templevaluteur/ProfileEval.html')





####################
@method_decorator([login_required, evaluteur_required], name='dispatch')
class Edit_Myprofil_As_Eval(SuccessMessageMixin,UpdateView):
    template_name = 'Templevaluteur/Eval_edite_myprofile.html'
    model = User
    form_class = From_Edite_Profile
    success_message = "You'r Profile was Updated successfully as Evaluateur"
    
    def get_success_url(self):
        return reverse_lazy('evaluteur:Profile')
     



#+++++++++++++++++++++++++++++++++++++
@method_decorator([login_required, evaluteur_required], name='dispatch')
class Liste_All_Artcl(ListView):
    model = Article
    template_name = 'Templevaluteur/All_Artcles.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrArctl'] = Article.objects.all().count()
        return context




@method_decorator([login_required, evaluteur_required], name='dispatch')
class Liste_All_Confrence(ListView):
    model = Conferance
    template_name = 'Templevaluteur/All_Conf.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrConf'] = Conferance.objects.all().count()
        return context        



@method_decorator([login_required, evaluteur_required], name='dispatch')
class All_Etat_Du_Cherchr(ListView):
    model = User
    template_name = 'Templevaluteur/All_chercheur.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrchrch'] = User.objects.filter(is_chercheur=True).count()
        return context        




@method_decorator([login_required, evaluteur_required], name='dispatch')
class All_Commite(ListView):
    model = Commite
    template_name = 'Templevaluteur/All_Commite.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrCommite'] = Commite.objects.all().count()
        return context        







@login_required
@evaluteur_required
def Info_T(request):
    return render(request,'Templevaluteur/info_Ttt.html')





#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
############################################### choix


from ..forms import ChoosingForm      
from G__evaluation.models import Choosing_map        
from django import forms                                                 


@login_required
@evaluteur_required
def Specefic(request , pk):

    conf = Conferance.objects.get(Comite_de_programme = pk)
    comit = Commite.objects.get( pk = pk )
    qs_articles = Article.objects.filter(Conferance = conf)
    address = ChoosingForm(conf)
    evalu = Evaluateur.objects.get(user = request.user)
    print('ccccccccccc',evalu.C_bn_Choix)
 



    if request.method == 'POST' and  evalu.C_bn_Choix == False :  # mzal makhyreche 

                address = ChoosingForm(conf , request.POST )
                

                if address.is_valid()  :

                    Choix_auncien = Choosing_map.objects.filter(evalu__user=request.user ,comit=pk)

                    for choix in Choix_auncien :
                        choix.delete()           # pour evite les auncien choix et ecrase tjr active avec nvvv
                                          
                    address = address.save(commit=False)
                    address.evalu = Evaluateur.objects.get(user = request.user)
                    address.comit = comit
                    address.save()
                    evalu.C_bn_Choix = True
                    evalu.save()

                    messages.info(request,' les 3 articles sont pris en charge pour vous en attend le rustat par adminstration Bon courag   , From Makni-CF-')
                    return redirect('evaluteur:Mes_article_Final')

    else :
        messages.warning(request,' Impossible  !   Vous avez deja choisi !! , From Makni-CF-')


    context = { 'articles' : qs_articles ,
                'add' : address 
               }

    return render(request,'Templevaluteur/single_comite.html' , context)



@login_required
@evaluteur_required
def Mon_Commite(request ):
    evalu = Evaluateur.objects.get(user = request.user)
    comits = Commite.objects.filter( evaluteur_list= evalu )
    context = { 'comits' : comits }

    return render(request,'Templevaluteur/selected_comite.html' , context)




@login_required
@evaluteur_required
def final(request ): # hna rahi final mli li bghaahhhom brk mchi final pcq mth 1 + 2 9adeere tzidehe des artcl
    evalu = Evaluateur.objects.get(user = request.user)
    mylist_off_article_Deja_eval= []
    
    etat_artciles = Etat_Artcile.objects.filter(evaluteur_list=evalu)
    comits = Commite.objects.filter( evaluteur_list= evalu )
    Choisi = Choosing_map.objects.filter(evalu=evalu)


    for aa in etat_artciles:
        mylist_off_article_Deja_eval.append(aa.article)


    context = { 'comits' : comits ,'Choisi':Choisi, 'evalu':evalu,'mylist_off_article_Deja_eval':mylist_off_article_Deja_eval }
    messages.warning(request,'Votre article !!!   , From Makni-CF-')

    return render(request,'Templevaluteur/Mes_artcl_a_Corrige.html' , context)




def Just_Notification(request):
    n=Notification.objects.filter(user=request.user,As_viewed=False)
    usrr=request.user
    messages.info(request,' Notifieé : Hi '+ str(usrr)+' , From Makni-CF-')
    return render(request,'Templevaluteur/Just_Notification.html',{'notifications':n})





@login_required
@evaluteur_required
def final_detailles(request ):
    mylist_off_article_Deja_eval = []
    evalu = Evaluateur.objects.get(user = request.user)
    etat_artciles = Etat_Artcile.objects.filter(evaluteur_list=evalu)
    comits = Commite.objects.filter( evaluteur_list= evalu )
    Now = datetime.datetime.now()

    for aa in etat_artciles:
        mylist_off_article_Deja_eval.append(aa.article)

    comments = Comment.objects.filter(authorComment__evaluateur=evalu)
    context = {'evalu':evalu , 'comments':comments,'Now':Now,
    'etat_artciles':etat_artciles,'mylist_off_article_Deja_eval':mylist_off_article_Deja_eval} 
    return render(request,'Templevaluteur/Mes_article_Final_detailles.html' , context)









# ++++++++++++++++++++++++++++++  2020/06/05 ++++++++++++++++++++++++
from mybasic_app.forms import CommentForm
from mybasic_app.models import Comment,Evaluateur,User
from django.shortcuts import get_object_or_404


@login_required
@evaluteur_required
def add_comment_to_Article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    User = request.user
    if request.method == 'POST' :
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment = form.save(commit=False)
            Comment.article = article
            Comment.authorComment=User
            Comment.save()
            messages.success(request,"Your Comment was Create successfully !!! , From @Makani-CF-")

            return redirect('evaluteur:Mes_evl_Comment')    #, pk=article.pk)
    else :
        form  = CommentForm()
    return render(request,'Commentaire/comment_form.html',{'form' : form})         





  
@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    messages.success(request,"Your Comment off \n"+  str(comment) +" \n was Approved successfully !!! , From @Makani-CF-")
    return redirect('evaluteur:Mes_evl_Comment')




  
@login_required
@evaluteur_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    article_pk =comment.article.pk
    comment.delete()
    messages.success(request,"Your Comment was Deleted  !!! , From @Makani-CF-")
    return redirect('evaluteur:Mes_evl_Comment')




@login_required
@evaluteur_required
def Mes_Comment(request ): 
    evalu = Evaluateur.objects.get(user = request.user)
    comits = Commite.objects.filter( evaluteur_list= evalu )
    comments = Comment.objects.filter(authorComment__evaluateur=evalu)
    comments_All = Comment.objects.all()
    context = {'evalu':evalu , 'comments':comments,'comments_All':comments_All}
    return render(request,'Templevaluteur/Commen_chaq_Mes_articl.html' , context)







# +++++++++++++++++++++++++++++++++++++++++++++ 23/06 /2020 
# attention ki evluue mknch dak chkil t3 suprrm wla modifiee sayii   

from G__evaluation.models import Etat_Artcile
from mybasic_app.forms import EvaluationForm
                             # ni dayer evaluation donc kol eval ydkhol 3ndehe swalhehe unique 

@login_required
@evaluteur_required
def evaluéé(request,pk):
    article = get_object_or_404(Article, pk=pk) 
    evalu = Evaluateur.objects.get(user = request.user)
   
    if request.method == 'POST' :
        form = EvaluationForm(request.POST)
        if form.is_valid():
            Etat_Artcile = form.save()
            Etat_Artcile.article = article

        
                        ########### fel parcourere Etat_Artcile.article.evaluteur_list.add(evalu)
            Etat_Artcile.chrchr = article.author
            Etat_Artcile.evaluteur_list.add(evalu)
            chairement = article.Conferance.Comite_de_programme.charmain
            Etat_Artcile.chairement = chairement 
            Etat_Artcile.save()
            messages.success(request,"Your evluation was successfully ADD !!! , From @Makani-CF-")
  
            return redirect('evaluteur:MesEvaluation')

    else :
        form  = EvaluationForm()
    return render(request,'Evaluationn/Evaluation.html',{'form' : form,'article':article,})         








import datetime
@login_required
@evaluteur_required
def List_MesEvaluation(request ): 
    mylist_off_article_Deja_eval = []
    evalu = Evaluateur.objects.get(user = request.user)
    comits = Commite.objects.filter( evaluteur_list= evalu )
    Now = datetime.datetime.now()
    etat_artciles = Etat_Artcile.objects.filter(evaluteur_list=evalu)
    for aa in etat_artciles:
        mylist_off_article_Deja_eval.append(aa.article)
    context = {'evalu':evalu , 'etat_artciles':etat_artciles,'Now':Now,'mylist_off_article_Deja_eval':mylist_off_article_Deja_eval}
    return render(request,'Evaluationn/Evaluation_Pour_chaq_Mes_articl.html' , context)








