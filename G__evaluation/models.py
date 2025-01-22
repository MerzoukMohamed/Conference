from django.db import models
from mybasic_app.models import Evaluateur,Article,Commite,Chercheur



class Choosing_map(models.Model):
    comit = models.ForeignKey(Commite ,null=True,  on_delete=models.CASCADE)
    evalu = models.ForeignKey(Evaluateur ,null=True,  on_delete=models.CASCADE)
    point = models.PositiveIntegerField(default=0)
    prio = models.PositiveIntegerField(default=0)
    # by the way it's fucking useless that way , rather then the whole packet of Article objects i want something like a queryset 
    
    # also i should check the case when two fields map to the same article ( a repeat ) probalbly i can add conditions the prevents that 
    art1 = models.ForeignKey(Article ,null=True,  on_delete=models.CASCADE , related_name='art1')
    art2 = models.ForeignKey(Article ,null=True,  on_delete=models.CASCADE , related_name='art2')
    art3 = models.ForeignKey(Article ,null=True,  on_delete=models.CASCADE , related_name='art3')



    def __int__(self):
        return self.evalu.user.id

    def save(self, *args, **kwargs):
        if self.art1==self.art2 or self.art1==self.art3 or self.art2 == self.art3:
          return #any person can only be a mum or a dad, not both   # ++++++  erreur
        else:
          super(Choosing_map, self).save(*args, **kwargs)



## donc evaluateur radi ydir note 
#  bss7 meme article yedouh plusier evals 
# radi ykoun ex: article 1 3andah 3 notes
# min radi njibhom ? sa7a radi nwerik evaluation kich tessra 
 

##################################################################
from django.utils import timezone
from mybasic_app.models import User


class Etat_Artcile(models.Model): 

    ETAT = (
    ("SA","Strong Accepted"),
    ("A","Accepted"),
    ("AWC","Accepted With Conditions"),                                         
    ("W","Week"),
    ("R","Refuse"),
    ("SR","Strong Refuse"),
        )
                                                                               
### etat   === note     w   Ntation == remarque  hadoo f Dgrm de class 

    etat = models.CharField(max_length =20 , choices = ETAT,null=True) #note first
    Notation = models.TextField() 
    article = models.ForeignKey(Article,null=True ,on_delete=models.SET_NULL) 
    chrchr = models.ForeignKey(Chercheur, null=True ,on_delete=models.SET_NULL)
    chairement = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)                                                                       

    ###### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  First evaluation 
    evaluteur_list = models.ManyToManyField(Evaluateur,null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.article




class Resultat(models.Model): 

    ETAT = (
    ("SA","Strong Accepted"),
    ("A","Accepted"),
    ("AWC","Accepted With Conditions"),                                         
    ("W","Week"),
    ("R","Refuse"),
    ("SR","Strong Refuse"),
        )
    article = models.ForeignKey(Article,null=True ,on_delete=models.SET_NULL) 
    chairement = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)                                                                       
    Note_Final = models.CharField(max_length =20 , choices = ETAT,null=True) #note final 
    chrchr = models.ForeignKey(Chercheur, null=True ,on_delete=models.SET_NULL)
    Notation_Final = models.TextField() 
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.article