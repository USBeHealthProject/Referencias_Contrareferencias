#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from medico.models import *
from django.contrib.auth.models import User, Group
from administrador.models import Usuario
from medico.models import Medico
from paciente.models import Historiadetriaje, Paciente
import datetime

dicDias = {'Monday':'Lunes','Tuesday':'Martes','Wednesday':'Miercoles',
            'Thursday':'Jueves','Friday':'Viernes','Saturday':'Sabado',
            'Sunday':'Domingo'}

def Conocer_dia(fecha):
    # fecha = datetime.date(anio,mes,dia)
    day = dicDias[fecha.strftime('%A')]
    return day


def volverElemlista(lista,ultimo):
    x = "'"
    indice= lista.index(x)
    if ultimo :
        return lista[indice+1:len(lista)-3]
    else :
        return lista[indice+1:len(lista)-2]


class Medico_EstudiosForm(forms.ModelForm):

    class Meta:
        model = Medico_Estudios
        exclude = ("medico",)


class Medico_LogrosForm(forms.ModelForm):

    class Meta:
        model = Medico_Logros
        exclude = ("medico",)


class Medico_PublicacionesForm(forms.ModelForm):

    class Meta:
        model = Medico_Publicaciones
        exclude = ("medico",)


class Medico_ExperienciasForm(forms.ModelForm):

    class Meta:
        model = Medico_Experiencias
        exclude = ("medico",)


class Medico_HabilidadesForm(forms.ModelForm):

    class Meta:
        model = Medico_Habilidades
        exclude = ("medico",)


class Medico_EventosForm(forms.ModelForm):

    class Meta:
        model = Medico_Eventos
        exclude = ("medico",)


class Medico_CitasForm(forms.ModelForm):

    class Meta:
        model = Medico_Citas
    #    exclude = ("medico",)
        fields = ['paciente','institucion', 'fecha','descripcion','especialidad','hora']
        # '__all__'

    def __init__(self, *args, **kwargs):
        self.medico = kwargs.pop('medico',None)
        super(Medico_CitasForm,self).__init__(*args,**kwargs)

    def clean(self):
        data = self.cleaned_data
        fecha = self.cleaned_data.get('fecha')
        hora = self.cleaned_data.get('hora')
        especialidad = self.cleaned_data.get('especialidad')
        inst = self.cleaned_data.get('institucion')
        institucion = Institucion.objects.get(name=inst)
        paciente = self.cleaned_data.get('paciente')
        user = User.objects.get(pk=self.medico)
        usuario = Usuario.objects.get(user=user)
        med = Medico.objects.get(usuario=usuario)
        medico = med.cedula
        num_paciente = Medico_Citas.objects.filter(paciente=paciente,fecha=fecha,
            hora=hora).count()
        dia= Conocer_dia(fecha)
        dia_hora=dia+hora
        cantidad = Medico_Especialidad.objects.filter(medico=medico,
            institucion=institucion.id,especialidad=especialidad).count()
        
        if cantidad > 0 :
            disponibilidad =Medico_Especialidad.objects.get(medico=medico,
                institucion=institucion.id,especialidad=especialidad)
            horario= disponibilidad.horario
            horario2=horario.split(', ')
            i = 0
            a = ''
            for x in horario2 :
                ulti = i == (len(horario2)-1)
                elem=volverElemlista(x,ulti)
                boo = (dia_hora == elem)
                a = a + elem + ', '
                if boo :
                    break
                i = i+1
            fecha_actual = datetime.datetime.now().date()
            if fecha < fecha_actual :
                msj = "La fecha de la cita no puede ser menor a la de hoy. "
                self.add_error('fecha',msj)

            if num_paciente == 1:
                msj="Cambie la hora y fecha de su consulta porque ya tiene otra cita a esa hora. "
                self.add_error('paciente',msj)

            if boo :
                num_citas = Medico_Citas.objects.filter(fecha=fecha, hora=hora,
                    especialidad=especialidad,medico=medico,institucion=institucion).count()
                if num_citas == 1 :
                    msj = "La fecha y hora solicitadas no se encuentran disponibles. Por favor elija algunas de estos horarios: "
                    # for x in horario :
                    #     msj = msj + str(x) + ', '
                    msj = msj + a
                    self.add_error('hora',msj)
                    # raise forms.ValidationError('La fecha y hora solicitadas no se encuentran disponibles. Por favor'+
                    #     ' elija algunas de estos horarios')
            else :
                msj = "El Medico no atiende ese dia a esa hora. Por favor elija algunas de estos horarios: "
                # for x in horario :
                #     msj = msj + str(x) + ', '
                msj = msj + a
                self.add_error('hora',msj)
                # raise forms.ValidationError('El Medico no atiende ese dia a esa hora.Por favor'+
                #         ' elija algunas de estos horarios')
                # raise forms.ValidationError('La fecha de la cita no puede ser menor a la de hoy')
        else :
            cantidad = Medico_Especialidad.objects.filter(medico=medico)
            especialidad = ''
            institucion = ''
            msj = "El Medico no atiende esta especialidad en esta institucion. Las especialidades que atiende "
            msj = msj + " en la correspondiente institucion son: "
            for c in cantidad :
                msj = msj + str(c.especialidad) + ' en ' + str(c.institucion) + ', '
            self.add_error('institucion',msj)

        return data


class HistoriaClinicaForm(forms.ModelForm):
    class Meta:
        model = Historiadetriaje
        fields = ["paciente", "medico_triaje", "antecedentes_personales", "antecedentes_familiares", "motivo_consulta",
                "enfermedad_actual", "peso", "talla", "signos_vitales", "piel", "ojos",
                "fosas_nasales", "conductos_auditivos", "cavidad_oral", "cuello",
                "columna", "torax", "abdomen", "extremidades", "genitales"]

        # widgets = {
        #     'antecedentes_personales': forms.Textarea(),
        #     'antecedentes_familiares': forms.Textarea()
        # }

    def __init__(self, *args, **kwargs):
        super(HistoriaClinicaForm, self).__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all()
        # self.fields['medico'].queryset = Paciente.objects.all()


class Medico_ConsultasForm(forms.ModelForm):

    class Meta:
        model = Medico_Citas
        fields = ("paciente", "institucion", "fecha")

        labels = {
            'paciente' : 'Paciente',
            'institucion' : 'Institución',
            'fecha' : 'Fecha',
        }


class Medico_HorariosForm(forms.ModelForm):

    class Meta:
        model = Medico_Especialidad
        fields = ["especialidad", "institucion"]

        labels = {
            'especialidad' : 'Especialidad',
            'institucion' : 'Institución',
            'horario' : 'Horarios de Consulta'
        }

    def __init__(self, *args, **kwargs):
        self.medico = kwargs.pop('medico',None)
        super(Medico_HorariosForm,self).__init__(*args,**kwargs)


    def clean(self):
        data = self.cleaned_data
        especialidad = self.cleaned_data.get('especialidad')
        institucion = self.cleaned_data.get('institucion')
        print(self.medico)
        user = User.objects.get(pk=self.medico)
        usuario = Usuario.objects.get(user=user)
        med = Medico.objects.get(usuario=usuario)
        medico = med.cedula
        inst = Institucion.objects.get(name=institucion)
        institucion = inst.id
        num_horarios = Medico_Especialidad.objects.filter(medico=medico,
            institucion=institucion, especialidad=especialidad).count()
        print(num_horarios)

        if num_horarios == 1:
            msj="Ya tiene horarios para esta especialidad en esta institución, seleccione otros por favor."
            self.add_error('especialidad',msj)

        return data


class Medico_HorariosFormEditar(forms.ModelForm):

    class Meta:
        model = Medico_Especialidad
        exclude = ["horario","especialidad","institucion","medico"]

        labels = {
            'especialidad' : 'Especialidad',
            'institucion' : 'Institución',
            'horario' : 'Horarios de Consulta'
        }



class Medico_RevisionForm(forms.ModelForm):

    class Meta:
        model = Medico_Revision
        exclude=("cita",)


class Medico_InformeForm(forms.ModelForm):

    class Meta:
        model = Medico_Informe
        exclude = ('medico_Revision',)

        widgets = {
            'desc_prediagnostico': forms.Textarea(attrs={'rows':5,
                                                        'cols':10,
                                                        'style': 'height: 9em;width:50em'})
        }


class ReferenciaForm(forms.ModelForm):

    class Meta:
        model = Referencia

        exclude = ('cita', 'paciente')

        widgets={
                'archivo':forms.FileInput (attrs={'class':'form-control','accept':'.pdf'})
                }

    # def validate_file_extension(value):
    #     if not value.name.endswith('.pdf'):
    #         raise ValidationError(u'Error message')

    # def __init__(self, *args, **kwargs):
    #     self.paciente = kwargs.pop('paciente',None)
    #     super(ReferenciaForm,self).__init__(*args,**kwargs)

    # def clean(self):
    #     data = self.cleaned_data
    #     fecha = self.cleaned_data.get('fecha')
    #     hora = self.cleaned_data.get('hora')
    #     especialidad = self.cleaned_data.get('especialidad')
    #     institucion = self.cleaned_data.get('institucion')
    #     medico = self.cleaned_data.get('medico')
    #     user = User.objects.get(pk=self.medico)
    #     usuario = Usuario.objects.get(user=user)
    #     med = Medico.objects.get(usuario=usuario)
    #     medico = med.cedula
    #     num_paciente = Medico_Citas.objects.filter(paciente=paciente,fecha=fecha,
    #         hora=hora).count()
    #     dia= Conocer_dia(fecha)
    #     dia_hora=dia+hora
    #     disponibilidad =Medico_Especialidad.objects.get(medico=medico,
    #         institucion=institucion,especialidad=especialidad)
    #     horario= disponibilidad.horario
    #     horario2=horario.split(', ')
    #     print(num_paciente)
    #     i = 0
    #     for x in horario2 :
    #         ulti = i == (len(horario2)-1)
    #         elem=volverElemlista(x,ulti)
    #         boo = (dia_hora == elem)
    #         if boo :
    #             break
    #         i = i+1
    #     print("boo es: "+str(boo))
    #     fecha_actual = datetime.datetime.now().date()
    #     if fecha < fecha_actual :
    #         msj = "La fecha de la cita no puede ser menor a la de hoy. "
    #         self.add_error('fecha',msj)

    #     if num_paciente == 1:
    #         msj="Cambie la hora y fecha de su consulta porque ya tiene otra cita a esa hora. "
    #         self.add_error('paciente',msj)

    #     if boo :
    #         num_citas = Medico_Citas.objects.filter(fecha=fecha, hora=hora,
    #             especialidad=especialidad,medico=medico,institucion=institucion).count()
    #         if num_citas == 1 :
    #             msj = "La fecha y hora solicitadas no se encuentran disponibles. Por favor elija algunas de estos horarios: "
    #             msj = msj + str(horario)
    #             self.add_error('hora',msj)
    #             self.add_error('fecha',msj)
    #             # raise forms.ValidationError('La fecha y hora solicitadas no se encuentran disponibles. Por favor'+
    #             #     ' elija algunas de estos horarios')
    #     else :
    #         msj = "El Medico no atiende ese dia a esa hora. Por favor elija algunas de estos horarios: "
    #         msj = msj + str(horario)
    #         self.add_error('hora',msj)
    #         self.add_error('fecha',msj)
    #         # raise forms.ValidationError('El Medico no atiende ese dia a esa hora.Por favor'+
    #         #         ' elija algunas de estos horarios')
    #         # raise forms.ValidationError('La fecha de la cita no puede ser menor a la de hoy')

    #     return data


class Medico_HistorialForm(forms.ModelForm):

    class Meta:
        model = Medico_Citas
        exclude = ("paciente","medico","institucion","fecha","descripcion",
            "hora","especialidad","revision","informe","es_referido",)
