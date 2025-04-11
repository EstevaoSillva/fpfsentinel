from django.db import models
from django.contrib.auth.models import AbstractUser

class ModelBase(models.Model):
    """
    Modelo base para fornecer campos de ID, data de criação e modificação para outros modelos.
    """
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')
    modified_at = models.DateTimeField(auto_now=True, db_column='modified_at')
    activate = models.BooleanField(db_column='activate', default=True, null=False)

    class Meta:
        abstract = True
        managed = True

class PersonType(models.TextChoices):
    COLABORATOR = 'COLABORATOR', 'Colaborador'
    VISITOR_PF = 'VISITOR_PF', 'Visitante - Pessoa Física'
    VISITOR_PJ = 'VISITOR_PJ', 'Visitante - Pessoa Jurídica'

class Person(AbstractUser):
    name = models.CharField(max_length=200, db_column='name', null=False, verbose_name='Nome')
    person_type = models.CharField(max_length=20, db_column='person_type', choices=PersonType.choices, default=PersonType.COLABORATOR)
    photo = models.CharField(upload_to='photos', db_column='photo', null=True)
    document = models.CharField(max_length=20, db_column='document', null=True, verbose_name='Documento') #Adicionado novamente

    def __str__(self):
        return self.name

class Employee(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True, db_column='person_id', null=False, verbose_name='Funcionário')
    registration = models.CharField(max_length=20, db_column='registration', null=False, verbose_name='Matrícula')
    job = models.CharField(max_length=200, db_column='job', null=False, verbose_name='Cargo')
    sector = models.CharField(max_length=200, db_column='sector', null=False, verbose_name='Setor')

    def __str__(self):
        return f"{self.person} - {self.registration}"

class Visitor(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True, db_column='person_id', verbose_name='Nome do Visitante')
    visit_location = models.CharField(max_length=200, db_column='visit_location', null=False, verbose_name='Local de Visita')
    cpf_individual = models.CharField(max_length=11, db_column='cpf', null=False, unique=True, verbose_name='CPF')
    company_name = models.CharField(max_length=200, db_column='company_name', null=False, verbose_name='Nome da Empresa')
    cnpj_company = models.CharField(max_length=14, db_column='cnpj', null=False, unique=True, verbose_name='CNPJ')

    def __str__(self):
        return f"{self.person} - {self.company}"
