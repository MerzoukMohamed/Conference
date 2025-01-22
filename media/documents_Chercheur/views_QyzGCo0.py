from django.shortcuts import render,redirect
from mybasic_app.models import User
from mybasic_app.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from mybasic_app.models import (User, Evaluateur, Chercheur,
                                Commite, Conferance, Article, Topic)
from django.http import HttpResponseRedirect

from django.db.models import Prefetch
from operator import attrgetter
from django.db.models import Q
from G__evaluation.models import Choosing_map




# hadi hiyaa li rahi t9l3naaa 

@login_required
@staff_member_required
def Update(request,pk):
        
    division(request,pk)

    labels = []
    data= []
    labels2 = []
    data2 = []
    labels3 = []
    data3 = []
    

    
    Conf = Conferance.objects.get(id = pk)
    comite = Conf.Comite_de_programme
    evl = comite.evaluteur_list.all()
    Art = Article.objects.filter(Conferance = Conf)
   
    for e in evl :
        labels2.append(e.user.username)
        d = e.artcl_a_corrige.filter(Conferance = Conf).count()
        data2.append(d)



    totalart = Art.count()
    #totalch = Chr.count()

    totalcorr = 0
    for e in evl:
        labels.append(e.user.username) 
        d = e.artcl_a_corrige.filter(Conferance = Conf).count()
        data.append(d)
        totalcorr = totalcorr + d

    totaleval = evl.count()
    

    return render(request, 'gConf/distribution_graph.html', {
        'conf_name':Conf,
        'labels2': labels2,
        'data2': data2,
        'totalcorr': totalcorr,
        'totaleval' : totaleval,
        'totalart' : totalart,
        #'totalch' :totalch,
    })





@login_required
@staff_member_required
def division(request,pk):

    conferance = Conferance.objects.get(id = pk)
    comite = conferance.Comite_de_programme
    evaluateurs = comite.evaluteur_list.all()
    articles= Article.objects.filter(Conferance = conferance)
    lart = list(articles)

    nb_evl = evaluateurs.count()
    nb_art = articles.count()
    
 
    

    #+++++++++++++++++++++++++++++++++ evite problem de duplication et ecrasment ::

    for evl in evaluateurs:
        print('eval articles :',evl , evl.artcl_a_corrige.all())
        for a in evl.artcl_a_corrige.all():  
            if a in articles:
                evl.artcl_a_corrige.remove(a)
                
        print('eval articles :',evl, evl.artcl_a_corrige.all())
        

    
    print(' articles :',articles)

    for art in articles :
        art.evaluteur_list.clear()


    list_of_evl_iN_cm = list(evaluateurs.only('user__id','artcl_a_corrige__id'))
    

            #only et id pour bien spicivee dans base de donne

    print('')
    print('///////////////*** les article par comite apre mth 1 + 2 ***/////////////////////')
    print('')

        
        #if Conf.Comite_de_programme.evaluteur_list is not None :
         #   evl_in_cm = Conf.Comite_de_programme.evaluteur_list.all()
       
    print('')
    print('///////////////*** Appel distribution == 3eme mth  ***/////////////////////')
    print('')
    

    Destribute(request, comite, articles)  #hadi  bach n3yte distrubue w nmdlhom par mth 3

     
    list_articl = []
    
    for a in lart:
        if a.evaluteur_list.all().count() < 3: 
            list_articl.append(a)

    nb_acl = len(list_articl)
            
                                                 
    #  n   evaluateurs dans chaque comite
    # si il n ya pas d'evaluateur !! on sort




    #------------------------> evaluateurs non choisi   nejbed choosing
    cho = Choosing_map.objects.select_related('evalu').only('id' , 'evalu__user__id' ,'point','prio' ).filter(comit = comite).only('id' , 'evalu__user__id' ,'point','prio' )
    chom = list(cho)
    e = [x for x in list_of_evl_iN_cm if(not(cho & x.choosing_map_set.all()))]  
    new_liste_eval = list(e)

    
    # ---------------------------> article non choisi 
    j = 0   # 0 --> n niveau eval article pris
    hell = chom
    Num_eval_in_Cm = 0
    num_eval_passe = []  # eval passé
    list_evalu_ini = []
    list_articl_a_supprimer = []
    list_evalu_supp = []
    list_evalu = []
    

    if len(hell) > 0: #random avec choix
    
        while (len(list_articl) > 0) : # rest articles a distribuer
            
           # ajouter evaluateur choix avec eval non choix ---> meme niveau (nb articles)
            

            
            
            while len(list_evalu_ini) > 0 :  #reinitializer la liste des eval 
                del list_evalu_ini[0]

            while len(list_evalu) > 0 :  #reinitializer la liste des eval 
                del list_evalu[0]

            while len(list_articl_a_supprimer) > 0 :  #reinitializer la liste des articles a supprimer
                del list_articl_a_supprimer[0]
            
            
            for ev in new_liste_eval:
                print('eval ', ev  ,' nivau ',ev.artcl_a_corrige.filter(Conferance = conferance).count())
                list_evalu.append(ev)

            
            for k in hell:
                print('eval ',k.evalu  ,' nivau ',k.evalu.artcl_a_corrige.filter(Conferance = conferance).count())
                list_evalu.append(k.evalu)
                    #ele = hell.index(k)
                    #hell.pop(ele)  #reduir la table des evaluateur a ajouter
                        
            
            
            j = min(list_evalu,conferance)
            print('niveau',j)
            

            for ev in list_evalu:
                if ev.artcl_a_corrige.filter(Conferance = conferance).count() == j : #list eval meme niveau
                    list_evalu_ini.append(ev)

            nbeval = len(list_evalu_ini)
            

            print('nb eval a distribuer ',nbeval)
            print('list articles', list_articl)


            if nbeval != 0 : # si il ya eval cas tous ont choisit
                
                for art in list_articl:    # article de comite no full #ou bien  for e in newlisteval
                    art_nb_eval= art.evaluteur_list.count()
                    print('nb eval de article ',art,' = ',art_nb_eval)

                    # si article pris par 3 evals , on le supprime
                    if art_nb_eval == 3 :   
                        list_articl_a_supprimer.append(art)
                    else :
                        tour = 0
                        while article_pris(request,art,list_evalu_ini,nbeval,Num_eval_in_Cm):  # article pris par evaluateur donc ne peut pas etre pris 2 fois par le meme eval
                            #ici probleme de decalage----------------------------------------------------------------------------------------------------                  
                            num_eval_passe.append(Num_eval_in_Cm)  # nwejdou eval li madach , yedi article l jay
                            Num_eval_in_Cm += 1   
                            if Num_eval_in_Cm >= nbeval : #si fin list eval , retourner au debut
                                Num_eval_in_Cm = 0
                                tour +=1
                            if tour == 2: #si tous les evals on pris l'artice , max 3 evals dans la liste , on passe a l'article suivant 
                                break


                              
                        if tour < 2:
                            if Num_eval_in_Cm < nbeval:    
                                list_evalu_ini[Num_eval_in_Cm].artcl_a_corrige.add(art)
                                art.evaluteur_list.add(list_evalu_ini[Num_eval_in_Cm])
                                print('Article ---> ',art.name ,'Distribué a -----> ',list_evalu_ini[Num_eval_in_Cm])
                                print('evaluateur : -----> ',list_evalu_ini[Num_eval_in_Cm],'a pris l''Article ---> ',art.name)
                        
                        

                        for ev in list_evalu_ini:
                            if ev.artcl_a_corrige.filter(Conferance = conferance).count() > j:
                                list_evalu_supp.append(ev)

                        

                        for e in list_evalu_supp :
                           ele = list_evalu_ini.index(e)
                           list_evalu_ini.pop(ele) 


                        nbeval = len(list_evalu_ini)


                        while len(list_evalu_supp) > 0 :  #reinitializer la liste des evals a supprimer
                            del list_evalu_supp[0]   
                        
                            
                            
                        if len(num_eval_passe) > 0 :     # ida mazal ba9i eval madach , yebdou bih marra jaya
                            Num_eval_in_Cm = num_eval_passe[0]
                            del num_eval_passe[0] 
                        else:
                            Num_eval_in_Cm +=1

                    if Num_eval_in_Cm >= nbeval:                          # sinon yrou7 eval li morah
                        Num_eval_in_Cm = 0
                                             

                for e in list_articl_a_supprimer :
                    ele = list_articl.index(e)
                    list_articl.pop(ele)    


    else : #randome noraml

        while (len(list_articl) > 0) : # rest articles a distribuer


            while len(list_articl_a_supprimer) > 0 :  #reinitializer la liste des articles a supprimer
                del list_articl_a_supprimer[0]

            
            #for ev in new_liste_eval:
                #print('eval ', ev  ,' nivau ',ev.artcl_a_corrige.filter(Conferance = conferance).count())
                        
            
            nbeval = len(new_liste_eval)
            #print('nb eval a distribuer ',nbeval)
            #print('list articles', list_articl)
            

            if nbeval != 0 : # si il ya eval cas tous ont choisit
               
                for art in list_articl:    # article de comite no full #ou bien  for e in newlisteval
                    art_nb_eval= art.evaluteur_list.count()
                    #print('nb eval de article ',art,' = ',art_nb_eval)

                    # si article pris par 3 evals , on le supprime
                    if art_nb_eval == 3 :   
                        list_articl_a_supprimer.append(art)
                    else :
                        while article_pris(request,art,new_liste_eval,nbeval,Num_eval_in_Cm):  # article pris par evaluateur donc ne peut pas etre pris 2 fois par le meme eval
                            #ici probleme de decalage----------------------------------------------------------------------------------------------------                  
                            num_eval_passe.append(Num_eval_in_Cm)  # nwejdou eval li madach , yedi article l jay
                            Num_eval_in_Cm += 1   
                            if Num_eval_in_Cm >= nbeval : #si fin list eval , retourner au debut
                                Num_eval_in_Cm = 0
                              

                        if Num_eval_in_Cm >= nbeval:  # ida mazal mandirou le tour te3 les evals 
                            Num_eval_in_Cm = 0

                        new_liste_eval[Num_eval_in_Cm].artcl_a_corrige.add(art)
                        art.evaluteur_list.add(new_liste_eval[Num_eval_in_Cm])
                        #print('Article ---> ',art.name ,'Distribué a -----> ',new_liste_eval[Num_eval_in_Cm])
                        #print('evaluateur : -----> ',new_liste_eval[Num_eval_in_Cm],'a pris l''Article ---> ',art.name)
                        
                        if len(num_eval_passe) > 0 :     # ida mazal ba9i eval madach , yebdou bih marra jaya
                            Num_eval_in_Cm = num_eval_passe[0]
                            del num_eval_passe[0] 
                        else:
                            Num_eval_in_Cm +=1

                        if Num_eval_in_Cm >= nbeval:                          # sinon yrou7 eval li morah
                            Num_eval_in_Cm = 0
                                             
                            
                   
                for e in list_articl_a_supprimer :
                    ele = list_articl.index(e)
                    list_articl.pop(ele)    


            else :  # nb eval = 0 !!
                break
    
    return render(request, 'Pour_Evaluaéé/mth_evluéé.html')







#///////////////////////////////////////////////////////////////////////////////////////////

def article_pris(request,article,liste_eval,nbeval,index):

    if index < nbeval :
        if article in liste_eval[index].artcl_a_corrige.all() :
            return True
        else :
            return False


def choix(point):
    if point == 0 :
        n = 0
    elif point in {1,2,4} :
        n = 1
    elif point in {3,5,6} :
        n = 2
    elif point == 7 :
        n = 3

    return n

def min(list_eval,conf):

    n = list_eval[0].artcl_a_corrige.filter(Conferance = conf).count()

    
    if len(list_eval) > 0:
        for e in list_eval:
            if n > e.artcl_a_corrige.filter(Conferance = conf).count():
                n = e.artcl_a_corrige.filter(Conferance = conf).count()

    return n








#///////////////////////////////////////////////////////////////////////////////////// 27/05/2020  and update in 10/06/2020





@login_required
@staff_member_required
def Destribute(request , comitee, qs):

    # update satis to the value of "0"  
    clean = Choosing_map.objects.only('pk' , 'point').update(point= 0)  
    clean = Choosing_map.objects.only('pk' , 'prio').update(prio= 0) 


    
    evals = comitee.evaluteur_list.only('user__id')

    # Retreive the "choices" made by those reviewers who take part within this comité

    cho = Choosing_map.objects.select_related('evalu').only('id' , 'evalu__user__id' ,'point','prio' ).filter(comit = comitee).only('id' , 'evalu__user__id' ,'point','prio' )
    chom = list(cho)
    
    # this comite's reviewers list

    EVE = evals 
    arti= Article.objects.none()
    EEV = Evaluateur.objects.none()
    cho_count = cho.count()

    #############################################"
    
    okey_ev_set = set()
    okey_ev1_set = set()
    okey_arti_set = set()
    okey_ar1_set = set()

    qss = list(qs)

     ############################################## for reduction purposes
     
    okey_ev_set = [x for x in EVE if ((x in [y.evalu for y in cho]))] 

    EV = list(okey_ev_set)


    bullshit = len(EV) # to be deleted 
     


    # second , get the choices made by the reviewers of this comit (look at first)

    okey_hell_set = [x for x in cho if (x.evalu in EV)]  

    hell = list(okey_hell_set)



    print(' ------------------------------------  ')


    # third , from the choices above get all the 3 choices articles in one list while avoiding duplicates (see second)

    for k in hell :
            art1 =  k.art1 
            art2 = k.art2 
            art3 = k.art3 
        
            ar0 = qs.select_related('author' , 'Conferance').filter( Q(pk = art1.pk) | Q(pk = art2.pk) | Q(pk = art3.pk) ).defer('description' , 'date_posté' ,'document' , 'uploaded_at')
            set3 = set(ar0)

            okey_arti_set =okey_arti_set.union(set3)

    arti = list(okey_arti_set)
    
    horsecrap = len(arti)         # to be deleted 
 
 ##############################################


    if hell :     # since we are always reducing the size of "hell" whenever one of them doesn't 
                 # fufill the condition , here we will be checking if the list is empty ,
                 # means if nothing fulfills those conditions

        while True :
            #j=0

            
               ######################################################################################

            # we retrieve the "choices" again in case a modification to the field "point" has been made .
            cho = Choosing_map.objects.select_related('evalu').only('id' , 'evalu__user__id' ,'point','prio' ).filter(comit = comitee).only('id' , 'evalu__user__id' ,'point','prio' )
            
            okey_hell_set = [x for x in cho if (x in hell)]  
            hell = list(okey_hell_set)
            
            


            # from the above choices get only those of which correspons to the reviewers who fulfills the conditions 
            



            # get the articles depending on the previous list of choices


            for k in hell :
                art1 = k.art1
                art2 = k.art2
                art3 = k.art3
                
                ar0 = qs.select_related('author' , 'Conferance').filter(Q(pk = art1.pk) | Q(pk = art2.pk) | Q(pk = art3.pk)).defer('description' , 'date_posté' ,'document' , 'uploaded_at')
                set4 = set(ar0)
                okey_ar1_set = okey_arti_set.union(set4)

            # why intersection ? 
            # 1 in case an article in list "arti" has been selected in a previous iteration , thus we don't want to treat it again in case another reviewer wants it 
            # 2 in case an article in list "arti" not choosen yet , BUT , however there is the case where a
            #           reviewer won't fufill the condition therefore that article won't be treated or taken into consideration
            #
            okey_arti_set = okey_arti_set.intersection(okey_ar1_set)
            

            
            print( '++++++++++++++++++++++++++++++++++++++')
            print( '<<<< mise a jour of article  >>>>' )
                    
                
               ######################################################################################

             # HOHO ! now this here is beautiful and simple , we will sort the list reviewers in an ascending order
             # according to their "satis" variable
             # "satis" means satisfaction ! so the group of reviewers with the least amount of satisfactions 
             #in each itereation would be treated !




             #  NOTE : i feel it can be improved .
            eev = sorted(hell, key=attrgetter('prio'),reverse=False)
            #print(eev[0].prio,'////', eev[1].prio) 
            


            # now we will iterate over that list of "bundle" that contains the list of
            # reviewers with the least amount of satisfaction 
            # here we will try to check different cases , and whether a reviewer 
            #has unfortunately been unable to get what he wants 
            # it happens which means our algorithm needs improvement but the current
            # edition would be suffscient for now . hopefully so .
            for oz in eev :
                

                    ero1 = qs.get(Q(pk = oz.art1.pk ))
                    ero2 = qs.get(Q(pk = oz.art2.pk ))
                    ero3 = qs.get(Q(pk = oz.art3.pk ))

                    if (ero1 in arti) and (ero1 not in oz.evalu.artcl_a_corrige.all()) :

                        #t9essem direct


                        #" this article , is for that reviewer" and simply create an instance 
                        #of model named "pair" that would hose that data . 

                        #pair = Pair.objects.create(comit = comitee , evalu = oz.evalu , arti = ero1)
                        

                        # " this article , is for that reviewer"  and soo we will add to the numbers of articles to that reviewer

                        this = EVE.get( pk =oz.evalu )

                        ero1.evaluteur_list.add(oz.evalu)
                        oz.evalu.artcl_a_corrige.add(ero1)
                        this.save()

                        sample = oz
                        sample.point += 1
                        
                        if sample.point == 3:
                            sample.prio = 3
                        elif sample.point == 1 :
                            sample.prio = 2
                        elif sample.point == 2 :
                            sample.prio = 1
                        print('er01',' eval ' ,oz.evalu ,' article a corrigé ',oz.evalu.artcl_a_corrige.all(),' prio = ' ,sample.prio)
                        print(' article pris par ' ,ero1.evaluteur_list.count())
                        sample.save()

                        # those will exclude a chosen article from 
                        #the list of "arti" so that it won't be treated again 
                        if ero1.evaluteur_list.count() >= 3 :
                            ele = arti.index(ero1)
                            arti.pop(ele)

                        

                        break



                    elif (ero2 in arti) and (ero2 not in oz.evalu.artcl_a_corrige.all()) : 


                        this = EVE.get( pk =oz.evalu )
                        ero2.evaluteur_list.add(oz.evalu)
                        oz.evalu.artcl_a_corrige.add(ero2)
                        this.save()

                        sample = oz
                        sample.point += 2

                        if sample.point == 3:
                            sample.prio = 3
                        elif sample.point == 2 :
                            sample.prio = 1
                        print('er02',' eval ' ,oz.evalu ,' article a corrigé ',oz.evalu.artcl_a_corrige.all(),' io = ' ,sample.prio)
                        print(' article pris par ' ,ero2.evaluteur_list.count())
                        sample.save()

                        if ero2.evaluteur_list.count() >= 3 :
                            ele = arti.index(ero2)
                            arti.pop(ele)

                        break


                    elif (ero3 in arti) and (ero3 not in oz.evalu.artcl_a_corrige.all()) :

                        

                        this = EVE.get( pk =oz.evalu  )
                        ero3.evaluteur_list.add(oz.evalu)
                        oz.evalu.artcl_a_corrige.add(ero3)
                        this.save()

                        sample = oz
                        sample.point += 4
                        sample.prio = 4
                        print('er03',' eval ' ,oz.evalu ,' article a corrigé ',oz.evalu.artcl_a_corrige.all(),' io = ' ,sample.prio)
                        print(' article pris par ' ,ero3.evaluteur_list.count())
                        sample.save()

                        # if 3rd article   , then delete this reviewer from the list "EV"
                        bye = EV.index(oz.evalu)
                        EV.pop(bye)

                        if ero3.evaluteur_list.count() >= 3  :
                            ele = arti.index(ero3)
                            arti.pop(ele)

                        break

                    else :# no article can possibly be given to this reviewers
                        bye = EV.index(oz.evalu)
                        EV.pop(bye)
                        okey_hell_set = [x for x in cho if (x.evalu in EV)]  
                        
                        hell = list(okey_hell_set)


                
                
             ##############################################################################

            if not arti :  
                break

            if not EV :
                break



    