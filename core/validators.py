from django.core.validators import RegexValidator

alpha = RegexValidator(r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]*$', 'Solo se permiten letras')

first_name = RegexValidator(
    r'^([a-zA-ZñÑáéíóúÁÉÍÓÚ])*(\s([a-zA-ZñÑáéíóúÁÉÍÓÚ])*){0,1}$', 'Solo se permiten dos nombres')

name = RegexValidator(r'^([a-zA-ZñÑáéíóúÁÉÍÓÚ])*(\s([a-zA-ZñÑáéíóúÁÉÍÓÚ])*)*$', 'Solo se permiten letras')

# adress = RegexValidator(r'^([a-zA-ZñÑáéíóúÁÉÍÓÚ0-9,.])*(\s([a-zA-ZñÑáéíóúÁÉÍÓÚ0-9,.])*)*$', 'Solo se permiten letras y números')

phone = RegexValidator(r'^[0-9]{10}$', 'Solo se permiten 10 números')

zip_code = RegexValidator(r'^[0-9]{5}$', 'Solo se permiten 5 números')

web_address = RegexValidator(r'^((http|https):\/\/)?(www\.)?([a-zA-Z0-9]+)\.([a-zA-Z]{2,5})$', 'Formato de dirección web inválido')