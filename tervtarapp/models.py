from django.db import models

class Vonal(models.Model):
    vonalszam = models.CharField(primary_key=True, max_length=3)
    kezdo_allomas = models.CharField(max_length=50)
    vegallomas = models.CharField(max_length=50)

    def __str__(self):
        return str(self.vonalszam)

class Allomas(models.Model):
    allomasnev = models.CharField(primary_key=True, max_length=50)
    vonalszam = models.ForeignKey('Vonal', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.allomasnev)

class Egyseg(models.Model):
    megnevezes = models.CharField(primary_key=True, max_length=25)

    def __str__(self):
        return str(self.megnevezes)

class Dokumentumtipus(models.Model):
    megnevezes = models.CharField(primary_key=True, max_length=50)
    egyseg = models.ForeignKey('Egyseg', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.megnevezes)