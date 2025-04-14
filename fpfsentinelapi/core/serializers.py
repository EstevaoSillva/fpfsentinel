from rest_framework import serializers

# Validação de email e senha
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext as _

# Importando o modelo
from core.models import GuardPost, AccessRegister, Visitor, Employee, PersonType

# Importando o modelo de usuário
from django.contrib.auth import get_user_model
GuardPost = get_user_model()


class GuardPostSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=GuardPost.objects.all(), message="Este email já está cadastrado.")],
        error_messages={
            'required': 'O email é obrigatório.',
            'invalid': 'Informe um endereço de email válido.',
        }
    )
    
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        label=_('Confirmação de Senha'),
        validators=[validate_password],
        error_messages={"required":_("A senha é obrigatória.")}
    )

    class Meta:
        model = GuardPost
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email', 
            'password', 
            'password_confirmation', 
            'registration_guard_post', 
            'shift_guard_post',
        ]  

    
    def validate(self, data):
        """
        Valida se as senhas coincidem.
        """
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError({"confirmacao_senha": "As senhas não coincidem."})
        
        return data
    
    def create(self, validated_data):
        """
        Cria o usuário corretamente, removendo a confirmação de senha.
        """
        validated_data.pop('password_confirmation')  # Removendo a confirmação de senha
        return GuardPost.objects.create_user(**validated_data)
    

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

    def validate(self, data):
        if not data.get('cpf_visitor') and not data.get('cnpj_visitor'):
            raise serializers.ValidationError("CPF ou CNPJ é obrigatório.")
        return data

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class AccessRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessRegister
        fields = [
            'id',
            'visitor',
            'guard_post',
            'date_access',
            'time_access',
        ]

    def validate(self, data):
        person_type = data.get('person_type')
        employee = data.get('id_employee')
        visitor = data.get('id_visitor')

        if person_type == PersonType.COLABORATOR and not employee:
            raise serializers.ValidationError("Colaborador é obrigatório para este tipo de pessoa.")
        if person_type in [PersonType.VISITOR_PF, PersonType.VISITOR_PJ] and not visitor:
            raise serializers.ValidationError("Visitante é obrigatório para este tipo de pessoa.")
        return data