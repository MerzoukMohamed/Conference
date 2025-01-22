
from django.views.generic import  DeleteView





from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from ..decorators import chercheur_required
from ..forms import ChercheurSignUpForm, From_Edite_Profile, ArticleForm
from ..models import User, Chercheur, Article, Topic, Conferance, Comment

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.forms import inlineformset_factory
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import SuccessMessageMixin


#+++++++++++++++++
from mybasic_app.filters import FilterClass


class ChercheurSignUpView(SuccessMessageMixin, CreateView):
	model = User
	form_class = ChercheurSignUpForm
	template_name = 'registration/signup.html'
	success_message = "You'r Profile was Create successfully"

	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'chercheur'

		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		user = form.save()
		login(self.request, user)
		return redirect('chercheur:dashboardchrch')


####################
@method_decorator([login_required, chercheur_required], name='dispatch')
class Edit_Myprofil(SuccessMessageMixin, UpdateView):
	template_name = 'Templchercheur/edite_myprofil.html'
	model = User
	form_class = From_Edite_Profile
	success_message = "  %(username)s You'r Profile was Updated successfully"

	def get_success_url(self):
		return reverse_lazy('chercheur:Profile')


@login_required
@chercheur_required
def AccedeauDoc_Aschrch(request):
	User = request.user
	chrch = Chercheur.objects.get(user=User)
	articles = Article.objects.filter(author_list=chrch) and Article.objects.filter(author=chrch)
	context = {'articles': articles}
	messages.info(request, "Etat d'articles au se moment  , From @Makani-CF- ")
	return render(request, 'Templchercheur/docs/documentation.html', context)


import datetime
# ++++++++++++++++++++++++ notification  1/06/2020
from Notification.models import Notification


@login_required
@chercheur_required
def profil_chrch(request):
	chrch = Chercheur.objects.get(user = request.user)
	conferances = Conferance.objects.all()
	Now = datetime.datetime.now()
	Help_articles = Article.objects.filter(author_list=chrch)
	article_principal =  Article.objects.filter(author=chrch)
	List_Articl_deja_evlueé= []
	Listreslt = []
	rusalt=Resultat.objects.filter(chrchr=chrch) 
	etat_artciles = Etat_Artcile.objects.filter(chrchr=chrch)
	for aa in etat_artciles:
		List_Articl_deja_evlueé.append(aa.article)

	for a in rusalt:
		Listreslt.append(a.article)	
	n = Notification.objects.filter(user=request.user, As_viewed=False)
	us = request.user

	context = {'chrch': chrch, 'Help_articles': Help_articles,'article_principal':article_principal,
	 'notifications': n,'conferances': conferances, 'Now': Now,'etat_artciles':etat_artciles,
	'List_Articl_deja_evlueé':List_Articl_deja_evlueé,'rusalt':rusalt,'Listreslt':Listreslt}
	return render(request, 'Templchercheur/profil_chrch.html', context)






@login_required
@chercheur_required
def Userchrch(request):
	us = request.user
	messages.info(request, " Hi  " + str(us) + " , From @Makani-CF- ")
	return render(request, 'Templchercheur/profile-page.html')


########################      12/07/2020        ###########


from random import randint
from email.message import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from learning_user import settings
@login_required
@chercheur_required
def CrArticle(request, pk):

	Uuuser = request.user 
	topic = Topic.objects.get(pk=pk)
	confer = Conferance.objects.filter(topic=topic).first()

	formset = ArticleForm()
	if request.method == 'POST':
		formset = ArticleForm(request.POST, request.FILES)

		ren = request.POST['amount']
		ren = int(ren)

		bros = set()

		print('++++++++++++++++++++++++++++')
		print(ren)
		print('++++++++++++++++++++++++++++')

		for x in range(0, ren ):
			first = request.POST.get(str(x) + "0", "y445")
			family = request.POST.get(str(x) + "1", "y41394")
			idnumber = request.POST.get(str(x) + "2", "143998")
			mail = request.POST.get(str(x) + "3", "y4315")
			number = request.POST.get(str(x) + "4", "3413")
			country = request.POST.get(str(x) + "5", "y4315")
			city = request.POST.get(str(x) + "6", "y43165")
			postal_code = request.POST.get(str(x) + "7", "4313")
			organization = request.POST.get(str(x) + "8", "43195")

			ussser = User.objects.create(username=randint(1, 1000), password="123456789", first_name=first,
			last_name=family, numbr_Identd=randint(1 , 9999999), email=mail,
			Phone=number, Country=country, City=city,
			Post_code=postal_code, Organization=organization)

			ussser.is_chercheur = True
			ussser.save()
			auth = Chercheur.objects.create(user=ussser, email=mail)
			auth.save()
			bros.add(auth)
		

		if formset.is_valid():
			article = formset.save(commit=False)
			article.date_posté
			article.author = Chercheur.objects.get(user=Uuuser)
			article.Conferance = confer
			article.topic = topic
			article.save()

			for chr_ancien in formset.cleaned_data['author_list']:
				bros.add(chr_ancien)


			for bro in bros:
				article.author_list.add(bro)
				article.save()

  
			for us in article.author_list.all():
				message = ' il existe une Partage de  article :  ' + str(article.name)  + ' avec Vous dans Confrance : '+ str(confer) +' \n,Votre compte tempriare \n \n Username  : ' + str(us.user.username) + 'et motpass  :  ' + str(us.user.password) + ''' \n
				 
				  \n
				   \n
						 \n \n \n
						 - mais attention il faut changer votre donne primeir pour bien sucriseé votre compte  : \n
				  clique ici >>> aprr ndiro lien
						   ***
						'''

				subject = f' vous avez particpee dans une depot article : , from Makani -CF-'
				sender = settings.EMAIL_HOST_USER
				recipients = str(us.email)
				print('*********** author *****************',recipients, '*********** author *****************')
				try:
					send_mail(subject, message, sender, [recipients], fail_silently=True)
				except BadHeaderError:
					return HttpResponse('Invalid header found,Attention')

			messages.success(request,"Your Article !!!,From @Makani-CF- ")
			return redirect('chercheur:tach_ARTCL')

	context = {'formset': formset }
	return render(request, 'Templchercheur/register-page.html' ,context)





@login_required
@chercheur_required
def Delete_list(request):
	conferances = Conferance.objects.all()
	Now = datetime.datetime.now()
	User = request.user
	researcher = Chercheur.objects.get(user=User)
	articles = Article.objects.filter(author = researcher)  # lazme tkon nta how mol article bch tnjm supprm
	myfilter=FilterClass(request.GET , queryset=articles)
	articles = myfilter.qs
	context = {'articles': articles ,'myfilter':myfilter,'conferances':conferances,'Now':Now}
	messages.warning(request,"Attention Si Clique L'article est supprimeé")
	return render(request, 'Templchercheur/Delete_List_Article.html' , context)










@login_required
@chercheur_required
def Update_detaille_list(request):
	conferances = Conferance.objects.all()
	Now = datetime.datetime.now()
	User = request.user 
	researcher = Chercheur.objects.get(user=User)
	articles = Article.objects.filter(author=researcher)
	comments = Comment.objects.filter(authorComment__chercheur=researcher)
	comments_All = Comment.objects.all()
	myfilter=FilterClass(request.GET , queryset=articles)
	articles = myfilter.qs
	context = {'articles': articles ,'myfilter':myfilter , 
	'comments':comments,'comments_All':comments_All ,'conferances':conferances,'Now':Now}
	
	return render(request, 'Templchercheur/les_articl_Detailles.html' , context)



@login_required
@chercheur_required
def Voir_All_m_Artcl(request):
	User = request.user 
	researcher = Chercheur.objects.get(user=User)
	articles = Article.objects.filter(author_list=researcher) or Article.objects.filter(author=researcher)
	comments = Comment.objects.filter(authorComment__chercheur=researcher)
	comments_All = Comment.objects.all()
	myfilter=FilterClass(request.GET , queryset=articles)
	articles = myfilter.qs
	context = {'articles': articles ,'myfilter':myfilter , 
	'comments':comments,'comments_All':comments_All}
	
	return render(request, 'Templchercheur/Voir_All_m_Artcl.html' , context)



@login_required
@chercheur_required
def Update(request ,pk ):

	User = request.user
	researcher = Chercheur.objects.get(user=User) ##+++++++++++++++  chkon li dar hada aartcile
	article = Article.objects.filter(author_list= User.id ) or Article.objects.filter(author= User.id )
	article = article.get(pk = pk)
	formset = ArticleForm(instance = article)
	
	if request.method == 'POST':
		formset = ArticleForm(request.POST , request.FILES  ,instance = article)
   
		if formset.is_valid():
			 article = formset.save(commit=False)
			 article.date_posté
			 article.author = Chercheur.objects.get(user=User)
			 article.Conferance.name = formset.cleaned_data['Conferance']
			 article.save()
			 messages.success(request,"Your Article was Update successfully !!! , From @Makani-CF-")

			 return redirect('chercheur:tach_ARTCL')

	context = {'formset': formset}
	return render(request, 'Templchercheur/modifèè.html' ,context)




 
# +++++++++++++++++++++++++++++++++++ 2020/05/15   +++++++++++++++++++++++++++++
import datetime
@method_decorator([login_required, chercheur_required], name='dispatch')
class topicList(SuccessMessageMixin,ListView):
   template_name = 'Templchercheur/All_Topics.html'
   model = Topic        
   paginate_by = 5


   def get_context_data(self, **kwargs):
   	context = super().get_context_data(**kwargs)
   	context['number'] = Topic.objects.all().count()
   	context['cf'] = Conferance.objects.all()
   	context['Now'] = datetime.datetime.now()
   	return context   



  
@login_required
@chercheur_required
def confList(request, pk):
	topic = Topic.objects.get(id = pk)
	conferance= Conferance.objects.filter(topic = topic).first()
	context = {'topic':topic, 'conferance':conferance}
	return render(request, 'Templchercheur/Detail_Conf_Poste_Artcl.html', context)








# ++++++++++++++++++++++++++++++  2020/06/05 ++++++++++++++++++++++++
from mybasic_app.forms import CommentForm
from mybasic_app.models import Comment,Chercheur,User
from django.shortcuts import get_object_or_404


  
@login_required
@chercheur_required
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

			return redirect('chercheur:tach_ARTCL')    #, pk=article.pk)
	else :
		form  = CommentForm()
	return render(request,'Commentaire/comment_form.html',{'form' : form})         




  
@login_required
def comment_approve(request,pk):
	comment = get_object_or_404(Comment,pk=pk)
	comment.approve()
	messages.success(request,"Your Comment off \n"+  str(comment) +" \n was Approved successfully !!! , From @Makani-CF-")
	return redirect('chercheur:tach_ARTCL')




  
@login_required
@chercheur_required
def comment_remove(request,pk):
	comment = get_object_or_404(Comment,pk=pk)
	article_pk =comment.article.pk
	comment.delete()
	messages.success(request,"Your Comment was Deleted  !!! , From @Makani-CF-")
	return redirect('chercheur:tach_ARTCL')





# ""# 24/06/2020 
from G__evaluation.models import Etat_Artcile,Resultat
import datetime

@login_required
@chercheur_required
def Etat_Mes_Articles(request):
	List_Articl_deja_evlueé= []
	chrchr = Chercheur.objects.get(user = request.user)
	articles = Article.objects.filter(author = chrchr)
	rusalt=Resultat.objects.filter(chrchr=chrchr)
	Now = datetime.datetime.now()  
	etat_artciles = Etat_Artcile.objects.filter(chrchr=chrchr)
	for aa in etat_artciles:
		List_Articl_deja_evlueé.append(aa.article)
	context = {'chrchr':chrchr , 'etat_artciles':etat_artciles,'articles':articles,
	'List_Articl_deja_evlueé':List_Articl_deja_evlueé,'rusalt':rusalt,'Now':Now}
	return render(request,'Templchercheur/Evaluation_Pour_chaq_Mes_articl.html' , context)


































@login_required
@chercheur_required
def Delete(request , pk):
	User = request.user
	researcher = Chercheur.objects.get(user=User)
	article = Article.objects.filter(author = researcher).get(pk = pk)
	article.delete()
	messages.error(request,"Your Article was Deleted successfully, From @Makani-CF- ")

	return redirect('chercheur:list_delete_Article')








	  
@login_required
def artDeleteView(request,pk):


	article = Article.objects.filter(pk = pk).first()
	context = {'article':article}
	return render(request,'Templchercheur/article_confirm_delete.html' , context)
   	


