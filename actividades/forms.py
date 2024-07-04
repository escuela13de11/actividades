from django import forms

class SistemaNumeracionForm(forms.Form):
    respuesta_a = forms.CharField(widget=forms.Textarea, label='a) ¿Qué puntaje obtuvo en total? Mostrá cómo lo pensaste.')
    respuesta_b = forms.CharField(widget=forms.Textarea, label='b) Julieta en una vuelta hizo 403.120 puntos. Si tiró 10 tapitas, ¿cuántas embocó en cada vaso?')
    respuesta = forms.CharField(max_length=255, label='Respuesta')

# actividades/forms.py
from django import forms

class MultiplosDivisoresForm(forms.Form):
    respuestas_1 = forms.MultipleChoiceField(choices=[('160', '160'), ('161', '161'), ('320', '320'), ('322', '322'), ('480', '480'), ('488', '488')], widget=forms.CheckboxSelectMultiple, required=False)
    respuestas_2a = forms.CharField(max_length=100, required=False)
    respuestas_2b = forms.MultipleChoiceField(choices=[('600', '600'), ('540', '540'), ('542', '542'), ('122', '122'), ('204', '204'), ('240', '240')], widget=forms.CheckboxSelectMultiple, required=False)
    respuesta_3 = forms.CharField(max_length=100, required=False)
    respuesta_4 = forms.CharField(max_length=100, required=False)
    respuestas_5 = forms.MultipleChoiceField(choices=[('1351', '1351'), ('1456', '1456'), ('6356', '6356'), ('4727', '4727'), ('5467', '5467'), ('2465', '2465')], widget=forms.CheckboxSelectMultiple, required=False)
    respuesta_6a = forms.CharField(max_length=100, required=False)
    respuesta_6b = forms.CharField(max_length=100, required=False)
    respuesta_7 = forms.CharField(max_length=100, required=False)
    respuesta_8a = forms.CharField(max_length=100, required=False)
    respuesta_8b = forms.CharField(max_length=100, required=False)
    respuesta_8c = forms.CharField(max_length=100, required=False)
    respuesta_8d = forms.CharField(max_length=100, required=False)
