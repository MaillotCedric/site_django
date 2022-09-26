from django.db import models

# Create your models here.
class Projet(models.Model):
    codePr = models.AutoField(primary_key=True)
    initial = models.CharField(max_length=10)
    url = models.TextField()

    def __str__(self):
        return self.initial

class Histo(models.Model):
    projetId = models.ForeignKey(Projet, on_delete=models.CASCADE, null=True)
    idHisto = models.AutoField(primary_key=True)
    dateRel = models.DateField()
    nbThreadsRel = models.BigIntegerField()
    nbCommRel = models.BigIntegerField()
    status = models.BooleanField(null=True)

    def __str__(self):
        return self.idHisto

class Threads(models.Model):
    projetId = models.ForeignKey(Projet, on_delete=models.CASCADE, null=True)
    idThread = models.AutoField(primary_key=True)
    nomThread = models.TextField()

    def __str__(self):
        return self.nomThread

class Comments(models.Model):
    threadId = models.ForeignKey(Threads,  on_delete=models.CASCADE, null=True)
    idCom = models.AutoField(primary_key=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment
