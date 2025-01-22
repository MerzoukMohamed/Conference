from django.forms import ModelForm
from django import forms

from G__evaluation.models import Resultat
from mybasic_app.models import Evaluateur, Chercheur,User,Conferance, Commite,Topic
from django.forms import ModelForm ,TextInput,Textarea

class EvalForm(ModelForm):
	class Meta:
		model = User
		fields = '__all__'


################## hnaa khasenha tmodifa apree pcq kyn 
#### les feildes rahom ybano ziyadaa  
##  hadi ___all___  aprr nspiicifoo hnaa
######## pcq kon tchofo ki tkhyre dok f template jayne tfecha  


class CherForm(ModelForm):
	class Meta:
		model = User
		fields = '__all__'



class ComiteForm(ModelForm):
	class Meta:
		model = Commite
		fields = '__all__'


class ContactCommitForm(forms.Form):
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	email = forms.EmailField(max_length=100)
	numbr_Identd=forms.IntegerField()
	Organization = forms.CharField(max_length=100)
	Phone  = forms.IntegerField()
	City = forms.CharField(max_length=100)
	Post_code = forms.CharField(max_length=20)
	Country = forms.CharField(max_length=100)




class EvaluationFinalForm(forms.ModelForm):
    class Meta:
        model = Resultat
        fields = ('Note_Final','Notation_Final',)

        widgets = {
        'Notation': Textarea(attrs={'class':'editable medium-editor-textarea'}) 
        }  



class topicForm(ModelForm):
	class Meta:
		model = Topic
		fields = '__all__'



class ConfForm(ModelForm):
	class Meta:
		model = Conferance
		fields = '__all__'
