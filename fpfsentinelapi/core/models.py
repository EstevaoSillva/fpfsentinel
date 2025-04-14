from django.db import models
from django.contrib.auth.models import AbstractUser

class ModelBase(models.Model):
    """
    Base model
    """
    id = models.BigAutoField(primary_key=True, db_column='id')
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

class ReasonLeaving(models.TextChoices):
    PERSONAL = 'PERSONAL', 'Pessoal'
    TECHNICAL_VISIT = 'TECHNICAL_VISIT', 'Visita Técnica'
    DEPARTURE_LUNCH = 'DEPARTURE_LUNCH', 'Saída para Almoço'
    END_SHIFT = 'END_SHIFT', 'Fim de Turno'
    OTHER = 'OTHER', 'Outro'

class Shift(models.TextChoices):
    MORNING = 'MORNING', 'Matutino'
    AFTERNOON = 'AFTERNOON', 'Vespertino'
    NIGHT = 'NIGHT', 'Noturno'
    FULL_TIME = 'FULL_TIME', 'Integral'

class GuardPost(AbstractUser, ModelBase):
    """
    Posto de Trabalho
    """
    first_name = models.CharField(max_length=100, db_column='name')
    last_name = models.CharField(max_length=100, db_column='last_name')
    registration_guard_post = models.CharField(max_length=20, db_column='registration_guard_post', verbose_name='Matrícula do Colaborador')
    shift_guard_post = models.CharField(max_length=20, choices=Shift.choices, default=Shift.FULL_TIME, verbose_name='Turno do Colaborador')
    email = models.EmailField(max_length=100, unique=True, db_column='email', verbose_name='Email do Colaborador')
    password = models.CharField(max_length=128, db_column='password', verbose_name='Senha do Colaborador')

    USERNAME_FIELD = 'email' # Assuming email is the unique identifier for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name', 'shift_guard_post']

    def __str__(self):
        return f"Posto de Trabalho: {self.first_name}, Matrícula: {self.registration_guard_post}"

class Visitor(ModelBase):
    name_visitor = models.CharField(max_length=100, db_column='name')
    cpf_visitor = models.CharField(max_length=11, db_column='cpf_visitor', verbose_name='CPF Visitante')
    cnpj_visitor = models.CharField(max_length=14, db_column='cnpj_visitor', verbose_name='CNPJ Visitante')
    reason_visit = models.CharField(max_length=200, db_column='reason_visit', verbose_name='Motivo da Visita')
    place_visit = models.CharField(max_length=200, db_column='place_visit', verbose_name='Local da Visita')

    def __str__(self):
        return f"Visitante: {self.name_visitor}"

class Employee(ModelBase):

    name_employee = models.CharField(max_length=100, db_column='name', verbose_name='Nome do Colaborador')
    cpf_employee = models.CharField(max_length=11, db_column='cpf_employee', verbose_name='CPF Colaborador')
    registration_employee = models.CharField(max_length=20, db_column='registration_employee', verbose_name='Matrícula Colaborador')
    sector_employee = models.CharField(max_length=40, db_column='sector_employee', verbose_name='Setor Colaborador')
    position_employee = models.CharField(max_length=40, db_column='position_employee', verbose_name='Cargo Colaborador')
    leaving_employee = models.BooleanField(max_length=20, choices=ReasonLeaving.choices, default=ReasonLeaving.PERSONAL, verbose_name='Motivo de Saída')

    def save(self, *args, **kwargs):
        # Check if the employee is leaving
        if self.reason_leaving != ReasonLeaving.END_SHIFT:
            self.leaving_employee = True
        else:
            self.leaving_employee = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Funcionário: {self.pk}, Motivo de Saída: {self.reason_leaving}" 

class AccessRegister(ModelBase):


    id_guard_post = models.ForeignKey('core.GuardPost', on_delete=models.CASCADE, db_column='id_guard_post')
    id_visitor = models.ForeignKey('core.Visitor', on_delete=models.CASCADE, db_column='id_visitor', null=True, blank=True) 
    id_employee = models.ForeignKey('core.Employee', on_delete=models.CASCADE, db_column='id_employee', null=True, blank=True) 
    person_type = models.CharField(max_length=20,choices=PersonType.choices,default=PersonType.COLABORATOR,verbose_name='Tipo de Pessoa')
    date_visitation = models.DateTimeField('core.date_visit', db_column='date_visit')

    def save(self, *args, **kwargs):
        if self.person_type == PersonType.COLABORATOR:
            self.employee_register = True
            self.visitor_register = False
        elif self.person_type in [PersonType.VISITOR_PF, PersonType.VISITOR_PJ]:
            self.employee_register = False
            self.visitor_register = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Registro de Acesso: {self.person_type}"
