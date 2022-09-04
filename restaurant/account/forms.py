from django import forms
from .models import MyUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class RegisterForm(forms.ModelForm):
    """
    The default 

    """
    id_user = 0 #para el autogenerador de id's en base de datos
    """
    Validación faltante
    """
    password = forms.CharField(widget=forms.PasswordInput) 
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    """
    seleccion de roles al registrar usuario
    """
    ENUM_ROL = (
        ('', 'Elija rol'),
        ('adm','Administrador'),
        ('fin','Finanza'),
        ('coc','Cocina'),
        ('bod','Bodega'),
        )
    """
    definiendo el modelo a usar para el registro
    """
    class Meta:
        model = MyUser
        fields = ('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido','nombre_usuario','correo','password','rol')
        
        widgets = {
            'rol': forms.RadioSelect(
                attrs= {'class':'otro'}
                ),
        }

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('correo')
        qs = MyUser.objects.filter(correo=correo)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data
