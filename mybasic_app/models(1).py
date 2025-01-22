from django.db import models
from  django.contrib.auth.models import AbstractUser
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.conf import settings
from  django.contrib.auth.models import AbstractUser
from PIL import Image


      

class User(AbstractUser):
    is_chercheur = models.BooleanField(default=False)
    is_evaluteur = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_on']

     
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    numbr_Identd = models.PositiveIntegerField(default=0,unique=True) # pour cree ou nn compt pcq nbridntd jami chnge
    email = models.EmailField(unique=True)
    Organization = models.CharField(max_length=100)
    Phone  = models.CharField(max_length=20,unique=True,blank=True)
    City = models.CharField(max_length=100)
    Post_code = models.CharField(max_length=20)
    Country = models.CharField(blank=False,max_length=100)
    Address_line_principale = models.CharField(max_length=200,blank=True)
    Address_line = models.CharField(max_length=200,blank=True)
    profile_pict = models.ImageField(upload_to='profile_piccs',blank=True
        ,default='photodflt.png')
    site_Personnel = models.URLField(blank=True)


    def get_absolute_url(self):
        return reverse('EditeProfile', kwargs={'pk': self.pk})

    


###############

class Evaluateur(models.Model):
    #is_evaluteur = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    email = models.EmailField(unique=True)
    artcl_a_corrige = models.ManyToManyField('Article', blank=True)
    
    ## Choix 
    C_bn_Choix = models.BooleanField(default=False)
    count_pair_temporaire = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('editEval', kwargs={'pk':self.id})

 


    def __str__(self):
        return  ' Le Evaluteur :' + self.user.username + ' |  | ' + ' et Sont email : ' + self.user.email





################
class Chercheur(models.Model):
    #is_chercheur = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return  ' Le Chercheur :' + self.user.username + ' |  | ' + 'et sont  email : ' + self.user.email


    def get_absolute_url(self):
        return reverse('editCher', kwargs={'pk':self.id})





#######""""/////////////////////////////////////////////////////////////////////////////
class Commite(models.Model):
    #Evl_Of_Cm = models.ForeignKey('Evl_Of_Cm',on_delete=models.CASCADE,blank=True)
    # rani supprm w drteh f comite kifkif pcq con 1 = comite 1 w charimn il how
    # chairement = Admin 2 dans adminstaration et le rsponsable sur Conf
    charmain = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    evaluteur_list = models.ManyToManyField(Evaluateur, blank=True, null=True)
    Organizationof_Commite = models.CharField('Commite dans le theme',max_length=200)
    autre_Info = models.CharField(max_length=200)
    Name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.Name

    class Meta:  # bch tsmiha haka f partie adminstration t3k 
        verbose_name = "Commites"


'''
class Evl_Of_Cm(models.Model):
    evaluteur_confrm = models.ForeignKey(Evaluateur,on_delete=models.SET_NULL,
        related_name="evaluteur_confrm",null=True)
    Exist_CM = models.BooleanField(default=False)
'''






class ToDolist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , 
    	related_name="todolist" , null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
    	return self.name



class Item(models.Model):
	todolist = models.ForeignKey(ToDolist,on_delete=models.CASCADE)
	text = models.CharField(max_length=300)
	complete = models.BooleanField()

	def __str__(self):
		return self.text



#######""""/////////////////////////////////////////////////////////////////////////////

class Topic(models.Model):
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.title



class Conferance(models.Model):

    title = models.CharField(max_length=200, null=True,unique=True)
    # rani supprm w drteh f comite kifkif pcq con 1 = comite 1 w charimn il how
     # chairement = Admin 2 dans adminstaration et le rsponsable sur Conf
    email = models.EmailField(unique=True, null=True)
    topic = models.ManyToManyField(Topic) ## M2M
    Comite_de_programme = models.ForeignKey(Commite,null=True, on_delete=models.SET_NULL)
    # Comite_de_Organizations = les user extren ++ qlq detille comme photo ... 
    Comite_de_Organizations = models.ManyToManyField(User,related_name='Comite_de_Organizations')
    pay = models.PositiveIntegerField(null=True,default=0) 
    stop = models.BooleanField(default=False) #pause ou non cette conf 
    link = models.URLField(blank=True)
    location = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    postal_code = models.PositiveIntegerField(null=True)
    description = models.TextField(max_length=200, null=True)
    ##############>>>>>>>>>>>>>>>>>>>>>>>>  les dates
    ### date de conf hadi nennjmo ngolo tmetel Suivi de article mli nthete hata desicion final
    date_Start_conf = models.DateTimeField(auto_now_add = False , null=True)
    date_Fin_conf = models.DateTimeField(auto_now_add = False,null=True)
    # ystaha9oha les evlltr 
    date_Start_Notification  = models.DateField(auto_now_add = False,null=True)
    date_Fin_Notification= models.DateField(auto_now_add = False,null=True)
    
    date_Start_Eval_Artcl_First = models.DateField(auto_now_add = False,null=True)
    date_Fin_Eval_Artcl_First  = models.DateField(auto_now_add = False,null=True)
    # hadi lele charmain min ydire desecion final 
    date_Start_Eval_Artcl_FinaaaL = models.DateField(auto_now_add = False,null=True)
    date_Fin_Eval_Artcl_FinaaaL = models.DateField(auto_now_add = False,null=True)
    # ystaha9oha chrchrr  
    date_Start_poste_Artcl = models.DateField(auto_now_add = False,null=True)
    date_Fin_poste_Artcl = models.DateField(auto_now_add = False,null=True)
    updated = models.DateTimeField(auto_now=True)
    
         
    class Meta:
        ordering = ['-date_Start_conf','updated']


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('confEdit', kwargs={'pk':self.id})

  # pour bien comppernde hadi conf rahi Stop w non pcq delete connfe mknch  
    def Stop_contuneé_Conf(self):
        if self.stop == False :
            self.stop = True
        else :
            self.stop = False
        self.save()

 


class Article(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = RichTextField(blank=True )
    Mots_Cleé = models.CharField(max_length=50, blank=True)
    author = models.ForeignKey(Chercheur, null=True,   on_delete=models.SET_NULL)
    #  author_list pour les autre authorr
    author_list = models.ManyToManyField(Chercheur, blank=True , related_name="author_Add")
    date_posté = models.DateTimeField(auto_now_add=True)
    Conferance = models.ForeignKey(Conferance,null=True,on_delete=models.SET_NULL)
    topic = models.ForeignKey(Topic,null=True,on_delete=models.SET_NULL)
    document = models.FileField(upload_to='documents_Chercheur/',null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # Deja_evaluéé >>>>>>>>>>>>>>>>>> hadi ki tkon shihaa sayi m3naha kmlna pvq t3 chairmen   
    Deja_evaluéé = models.BooleanField(default=False)

#  evaluteur_list pour les evl machi chairmein
    evaluteur_list = models.ManyToManyField(Evaluateur,null=True, blank=True) 
    
    class Meta:
        ordering = ['-date_posté','updated']

  # pour bien comppernde ou est qe hada article evluee w nn par chairmen FinaaaaaaaaaaaL
    def evaluéé_Art(self):
        self.Deja_evaluéé = True
        self.save()


    def __str__(self):
        return self.name




# +++++++++++++++++++++++++++++++++++++++   2020 / 05 / 06 
from django.utils import timezone


class Comment(models.Model):
    article = models.ForeignKey(Article,null=True ,on_delete=models.SET_NULL)
    authorComment = models.ForeignKey(User, null=True ,on_delete=models.SET_NULL)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comments = True
        self.save()

    
    def __str__(self):
        return self.text     


