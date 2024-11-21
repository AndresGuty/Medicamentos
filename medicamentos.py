# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/142ZFkoNH3WDGILkqbyXLbXOjbMr7cY7N
"""

import datetime
import json
import time
from datetime import date, timedelta
from capturaDatos import  *


# Clase para manejar la información del medicamento
class Medicamento:
    def __init__(self, nombre, dosis, horario, tomado=False):
        self.nombre = nombre  # Nombre del medicamento
        self.dosis = dosis  # Dosis del medicamento
        self.horario = horario  # Horario para tomar el medicamento
        self.tomado = tomado  # Estado de si se ha tomado o no

    def __str__(self):
        estado = "Tomado" if self.tomado else "No tomado"
        return f"{self.nombre} - Dosis: {self.dosis}, Horario: {self.horario}, Estado: {estado}"


# Clase para el sistema de seguimiento de medicamentos
class SeguimientoMedicamentos:
    ruta = 'medicamentos.json'
    medicamentos = []

    def __init__(self):
        try:
            with open(self.ruta, "r") as f:
                result = json.loads(f.read())
                for row in result:
                    data = {
                        **row,
                        "horario": datetime.datetime.strptime(row["horario"], "%Y-%m-%d %H:%M")
                    }
                    self.medicamentos.append(Medicamento(**data))
        except FileNotFoundError:
            self.medicamentos = []

    def grabar_data(self):
        result = map(lambda x: {
            **x.__dict__,
            "horario": x.horario.strftime('%Y-%m-%d %H:%M')
        }, self.medicamentos)

        with open(self.ruta, "w") as archivo:
            json_object = json.dumps(list(result), indent=2)
            archivo.write(json_object)

    def programar(self, medicamento):
        self.medicamentos.append(medicamento)
        self.grabar_data()
        print(f"Medicamento {medicamento.nombre} agregado correctamente.")
        
    def agregar_medicamento(self, medicamento):
        self.medicamentos.append(medicamento)
        self.grabar_data()

    def inicializar(self):
        self.medicamentos = []
        with open(self.ruta, "w") as archivo:
            archivo.write("")
        print("Medicamentos inicializados correctamente.")

    def mostrar_medicamentos(self):
        if not self.medicamentos:
            print("No hay medicamentos registrados.")
        else:
            print("Medicamentos registrados:")
            for med in self.medicamentos:
                print(med)

    def editar_medicamento(self, nombre):
        for med in self.medicamentos:
            if med.nombre == nombre:
                nueva_dosis = input(f"Ingrese la nueva dosis para {med.nombre} (actual: {med.dosis}): ")
                nuevo_horario_str = input(f"Ingrese el nuevo horario para {med.nombre} (actual: {med.horario} en formato HH:MM): ")
                try:
                    nuevo_horario = datetime.datetime.strptime(nuevo_horario_str, "%H:%M").time()
                    med.dosis = nueva_dosis
                    med.horario = nuevo_horario
                    self.grabar_data()
                    print(f"{med.nombre} ha sido actualizado.")
                except ValueError:
                    print("Formato de hora incorrecto. Intente nuevamente en formato HH:MM.")
                return
        print(f"Medicamento {nombre} no encontrado.")

    def eliminar_medicamento(self, nombre):
        for med in self.medicamentos:
            if med.nombre == nombre:
                self.medicamentos.remove(med)
                self.grabar_data()
                print(f"Medicamento {nombre} eliminado.")
                return
        print(f"Medicamento {nombre} no encontrado.")

    def buscar_medicamento(self, nombre):
        for med in self.medicamentos:
            if med.nombre.lower() == nombre.lower():
                print(med)
                return
        print(f"Medicamento {nombre} no encontrado.")

    def marcar_tomado(self, nombre):
        for med in self.medicamentos:
            if med.nombre.lower() == nombre.lower():
                med.tomado = True
                self.grabar_data()
                print(f"✅ {med.nombre} marcado como tomado.")
                return
        print(f"Medicamento {nombre} no encontrado.")

    def medicamentos_no_tomados(self):
        no_tomados = [med for med in self.medicamentos if not med.tomado]
        if no_tomados:
            print("🚨 Medicamentos no tomados:")
            for med in no_tomados:
                print(med)
        else:
            print("🎉 Todos los medicamentos han sido tomados.")

    def comprobar_recordatorios(self):
        ahora = datetime.datetime.now()
        print(f"Hora actual: {ahora.strftime('%H:%M:%S')}")  # Muestra la hora actual

        # Definir el margen de tolerancia de 5 minutos
        margen_tolerancia = datetime.timedelta(minutes=5)

        recordatorios_activos = False  # Bandera para saber si hay recordatorios

        for med in self.medicamentos:
            # Calcular el rango de tiempo para el recordatorio
            inicio = (med.horario - margen_tolerancia).time()
            fin = (med.horario + margen_tolerancia).time()

            # Verificar si el medicamento está dentro del rango de tiempo y no ha sido tomado
            if inicio <= ahora.time() <= fin and not med.tomado:
                if not recordatorios_activos:
                    print("\n⏰ ¡Hay recordatorios para los siguientes medicamentos! ⏰")
                    recordatorios_activos = True
                print(f"🔔 Recordatorio: Es hora de tomar tu medicamento '{med.nombre}'.")

        if not recordatorios_activos:
            print("🎉 No hay medicamentos pendientes por tomar en este momento.")


# Función para preguntar si el usuario desea continuar
def continuar_o_salir():
    while True:
        opcion = input("¿Deseas regresar al menú principal? (s/n): ").strip().lower()
        if opcion == 's':
            return True
        elif opcion == 'n':
            print("Saliendo del sistema...")
            return False
        else:
            print("Opción no válida. Por favor, ingresa 's' o 'n'.")


# Función principal
def main():
    sistema = SeguimientoMedicamentos()
    while True:
        print("\nOpciones:")
        print("1. Agregar medicamento")
        print("2. Mostrar medicamentos")
        print("3. Editar medicamento")
        print("4. Eliminar medicamento")
        print("5. Buscar medicamento")
        print("6. Comprobar recordatorios")
        print("7. Ver medicamentos no tomados")
        print("8. Marcar medicamento como tomado")
        print("9. Inicializar medicamentos")
        print("10. Crear Tratamiento")
        print("11. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del medicamento: ")
            dosis = input("Ingrese la dosis: ")
            while True:
                horario_str = input("Ingrese el horario (HH:MM) para tomar el medicamento: ")
                
                try:
                    now = datetime.datetime.now()
                    horario = datetime.datetime.strptime(f"{now.strftime('%Y-%m-%d')} {horario_str}", "%Y-%m-%d %H:%M")
                    break
                except ValueError as e:
                    print(e)
                    print("Formato de hora incorrecto. Intente nuevamente en formato HH:MM.")
            medicamento = Medicamento(nombre, dosis, horario)
            sistema.agregar_medicamento(medicamento)
            print(f"Medicamento {medicamento.nombre} agregado correctamente.")
            

        elif opcion == "2":
            sistema.mostrar_medicamentos()

        elif opcion == "3":
            nombre = input("Ingrese el nombre del medicamento a editar: ")
            sistema.editar_medicamento(nombre)

        elif opcion == "4":
            nombre = input("Ingrese el nombre del medicamento a eliminar: ")
            sistema.eliminar_medicamento(nombre)

        elif opcion == "5":
            nombre = input("Ingrese el nombre del medicamento a buscar: ")
            sistema.buscar_medicamento(nombre)

        elif opcion == "6":
            sistema.comprobar_recordatorios()

        elif opcion == "7":
            sistema.medicamentos_no_tomados()

        elif opcion == "8":
            nombre = input("Ingrese el nombre del medicamento a marcar como tomado: ")
            sistema.marcar_tomado(nombre)

        elif opcion == "9":
            sistema.inicializar()

        elif opcion == "10":
            formulario = Captura()
            now = datetime.datetime.now()
            campos = [
                ("Medicamento", "medicamento", Tipo.TEXTO, None),
                ("Dosis", "dosis", Tipo.TEXTO, None),
                ("Cantidad", "cantidad", Tipo.NUMERICO, None),
                ("Tomar cada (Horas)", "regularidad", Tipo.NUMERICO, None),
                ("Fecha Inicial", "fecha_inicial", Tipo.FECHA, now.strftime('%Y-%m-%d')),
                ("Hora Inicial", "hora_inicial", Tipo.HORA, now.strftime('%H:%M'))
            ]
            for item in campos:
                campo = Field(*item)
                formulario.add(campo)
            
            values = formulario.ejecutar()
            start = datetime.datetime.strptime("{} {}".format(values['fecha_inicial'], values['hora_inicial']), "%Y-%m-%d %H:%M")
            for n in range(int(values["cantidad"])):
                horario = start
                parametros = (values["medicamento"], values["dosis"], horario)
                medicamento = Medicamento(*parametros)
                sistema.agregar_medicamento(medicamento)
                start += timedelta(hours=int(values["regularidad"]))
                    
                    
        elif opcion == "11":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida. Por favor, elige otra opción.")

        if not continuar_o_salir():
            break


# Ejecutar el programa
if __name__ == "__main__":
    main()
