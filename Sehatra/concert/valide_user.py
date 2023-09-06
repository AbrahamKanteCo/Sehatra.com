from concert.models import Billet

user= []
for billet in Billet.objects.filter(valide=True):
    print (billet)

