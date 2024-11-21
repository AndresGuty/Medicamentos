# Clase para manejar la información del medicamento
from enum import Enum
import datetime
import time
from datetime import date

class Tipo(Enum):
    NUMERICO = 1
    TEXTO = 2
    FECHA = 3
    HORA = 4

class Field:
    titulo: str
    id: str
    tipo: Tipo
    default: str
    formato: str
    
    
    def __init__(self, etiqueta, nombre, tipo, default):
        self.titulo = etiqueta
        self.id = nombre
        self.tipo = tipo
        self.default = default
        
    def __str__(self):
        return f"{self.titulo}{self.id}{self.tipo}{self.default}{self.formato}"
    
    
class Captura:
    fields: list = []
    values: dict = {}
    
    def __init__(self):
        self.fields = []
        self.values = {}
        
        
    def add(self, field):
        self.fields.append(field)
        
    def ejecutar(self):

        for field in self.fields:
            while True:
                texto = "{}"
                if field.default is not None:
                    texto += " [{}]"
                    
                texto +=":"
                self.values[field.id] = input(texto.format(field.titulo, field.default))
                try:

                    if len(self.values) == 0 or self.values[field.id].strip() == "":
                        if field.default is None:
                            raise ValueError("El campo es obligatorio.")
                        else:
                            self.values[field.id] = field.default

                    if field.tipo is Tipo.TEXTO:
                        if self.values[field.id].isnumeric():
                            raise ValueError("El campo debe ser alfanumerico.")                                
                    
                    if field.tipo is Tipo.HORA:
                        try:
                            datetime.datetime.strptime(self.values[field.id], "%H:%M").time()
                        except ValueError:
                            raise ValueError("Formato de hora inicio incorrecto. Intente nuevamente en formato HH:MM.")

                    if field.tipo is Tipo.FECHA:
                        try:
                            datetime.datetime.strptime(self.values[field.id], "%Y-%m-%d").time()
                        except ValueError as e:
                            print(e)
                            raise ValueError(f"Formato de hora inicio incorrecto ({self.values[field.id]}). Intente nuevamente en formato YYYY-MM-DD.")
                        
                        
                    if field.tipo is field.tipo.NUMERICO and not self.values[field.id].isnumeric():
                        raise ValueError('El valor debe ser numerico')
                        
                    break
                except ValueError as e:
                    print(e)
                    
        return self.values
