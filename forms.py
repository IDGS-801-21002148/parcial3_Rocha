from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, SelectMultipleField, IntegerField, DateField
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(message="Este campo es obligatorio"),
        Length(min=3, max=15, message="Debe tener entre 3 y 15 caracteres")
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired(message="Este campo es obligatorio")
    ])
    submit = SubmitField("Iniciar Sesión")
    
    
class RegisterForm(FlaskForm):
    username = StringField("Usuario", validators=[
        DataRequired(),
        Length(min=3, max=15)
    ])
    password = PasswordField("Contraseña", validators=[
        DataRequired()
    ])
    submit = SubmitField("Registrarse")

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre Completo', validators=[DataRequired(), Length(max=255)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=255)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=100)])
    fecha_pedido = DateField('Fecha de Pedido', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Registrar Cliente')

class PizzaForm(FlaskForm):
    tamaño = RadioField('Tamaño de Pizza', choices=[('Chica', 'Chica $40'), ('Mediana', 'Mediana $80'), ('Grande', 'Grande $120')], default='Chica')
    ingredientes = SelectMultipleField('Ingredientes', choices=[('Jamón', 'Jamón $10'), ('Piña', 'Piña $10'), ('Champiñones', 'Champiñones $10')],
                                       option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    cantidad = IntegerField('Número de Pizzas', validators=[DataRequired()])
    submit = SubmitField('Agregar Pizza')

class ConsultaVentasForm(FlaskForm):
    periodo = RadioField('Periodo', choices=[('ninguno', 'Ninguno'), ('dia', 'Día'), ('mes', 'Mes')], default='ninguno', validators=[DataRequired()])
    fecha = StringField('Fecha')  
    submit = SubmitField('Consultar')