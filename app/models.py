from unittest.util import _MAX_LENGTH
from django.db import models


class Infraction(models.Model):
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom   
  
class Penalite(models.Model):
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nom    

# -----------------------------    Constat  ------------------------------
class Contrat(models.Model):
    date_creation = models.DateTimeField(auto_add_now=True)
    reference = models.CharField('N° Référence',max_length=100)
    matricule = models.CharField('Matricule du Policier',max_length=100)
    
    infraction = models.ForeignKey(Infraction,on_delete=models.CASCADE)
    penalite = models.ForeignKey(Penalite,on_delete=models.CASCADE)
    montant = models.CharField('Montant à Payer',max_length=100)
    
    conducteur = models.CharField(max_length=100)
    immatriculation = models.CharField('Véhicule',max_length=100)
    lieu = models.CharField('Lieu',max_length=100)
    #geolocal = models.CharField("Géolocalisation",max_length=200)

    def __str__(self):
        return self.photographie