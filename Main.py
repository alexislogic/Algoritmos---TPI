import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Constantes Globales ---
COSTO_ENTRADA = 12000
FILE_TURNOS = "turnos.txt"
FILE_RESERVAS = "reservas.txt"
FILE_PROXIMO_ID = "proximo_id.txt" # Archivo para el contador de reservas
HORARIOS_PARQUE = ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']

# --- Estructura de Archivos---
#   Funcionamiento:
    # 1. turnos.txt
    #    - Propósito: Almacena los cupos disponibles por cada turno.
    #    - Formato: CSV (Valores Separados por Coma)
    #    - Estructura: fecha,horario,cupos_disponibles
    #    - Ejemplo:
    #      2025-11-15,11:00,80
    #      2025-11-15,12:00,100
    #
    # 2. reservas.txt
    #    - Propósito: Log de todas las reservas confirmadas.
    #    - Formato: CSV (Valores Separados por Coma)
    #    - Estructura: id_reserva,fecha_turno,horario_turno,dni_resp,nombre_resp,cant_total,total_pagado,medio_pago,detalle_asistentes
    #    - 'detalle_asistentes' es un string separado por '|'
    #    - Ejemplo:
    #      R1001,2025-11-15,11:00,30123456,Alexis Peralta,2,24000,Tarjeta de Crédito,(18;Si)|(10;No)
    #
    # 3. proximo_id.txt
    #    - Propósito: Almacena el próximo número de ID de reserva.
    #    - Formato: Texto plano (un solo número)
    #    - Ejemplo:
    #      1001
#   Alcances Gestionar (Se crean durante el programa):
    # Solicitud de turno (Nro Solicitud, DatosResponsable, DatosAcompañantes, FechaTurno, HoraTurno, Cantidad de personas, Importe, FechaSolicitud, HoraSolicitud,  Estado)
    # Constancia de pago (Nro Solicitud, Importe, Medio de pago, FechaPago, HoraPago)
    # Cancelacion (Nro Solicitud, ImporteTotal, ImporteDevuelto, FechaCancelación, HoraCancelación, Motivo, Estado)
#
    #Alcances Administrar (Ya deben estar cargados):
    # Roles (Nro Rol, Descripción)
    # Personal (DNI, nombre, apellido, rol, telefono, email)
    # Metodo de pago (Nro MedioDePago, Descripción)
    # Tarifas (Nro Operación, Descripción, Costo)

class AppLagosPark(tk.Tk):
    
    def __init__(self):
        super().__init__()

        self.title("TPI Algoritmos - Venta de Entradas 'Lagos Park'")
        self.geometry("900x700")
        self.resizable(False, False)
        
        # Estilos
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'))
        self.style.configure('Small.TLabel', font=('Arial', 8, 'italic'))

        # Variables de estado
        self.costo_total = tk.DoubleVar(value=0.0)
        
        self.cargar_datos_iniciales()
        self.crear_widgets()

    def cargar_datos_iniciales(self):
        """
        Verifica si los archivos de datos existen. Si no, los crea.
        Usa try/except FileNotFoundError ya que no podemos importar 'os'.
        """
        try:
            # 1. Verificar turnos.txt
            with open(FILE_TURNOS, 'r') as f:
                pass # El archivo existe, no hacer nada
        except FileNotFoundError:
            self.crear_archivo_turnos_default()
            
        try:
            # 2. Verificar reservas.txt
            with open(FILE_RESERVAS, 'r') as f:
                pass
        except FileNotFoundError:
            self.crear_archivo_vacio(FILE_RESERVAS)
            
        try:
            # 3. Verificar proximo_id.txt
            with open(FILE_PROXIMO_ID, 'r') as f:
                pass
        except FileNotFoundError:
            self.crear_archivo_vacio(FILE_PROXIMO_ID, "1001") # Empezar contador en 1001

    def crear_archivo_vacio(self, nombre_archivo, contenido_inicial=""):
        """Crea un archivo vacío o con contenido inicial."""
        try:
            with open(nombre_archivo, 'w') as f:
                f.write(contenido_inicial)
        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudo crear {nombre_archivo}: {e}")

    def crear_archivo_turnos_default(self):
        """
        Crea un archivo 'turnos.txt' con cupos fijos para fechas de ejemplo.
        (No usamos datetime, así que son fechas estáticas).
        """
        lineas_turnos = [
            # Datos para el 15 de Nov
            "2025-11-15,11:00,100",
            "2025-11-15,12:00,80",
            "2025-11-15,13:00,50",
            "2025-11-15,14:00,10", # Pocos cupos
            "2025-11-15,15:00,0",  # Agotado
            "2025-11-15,16:00,90",
            "2025-11-15,17:00,100",
            "2025-11-15,18:00,100",
            "2025-11-15,19:00,100",
            # Datos para el 16 de Nov
            "2025-11-16,11:00,100",
            "2025-11-16,12:00,100",
            "2025-11-16,13:00,100",
            "2025-11-16,14:00,100",
            "2025-11-16,15:00,100",
            "2025-11-16,16:00,100",
            "2025-11-16,17:00,100",
            "2025-11-16,18:00,100",
            "2025-11-16,19:00,100"
        ]
        try:
            with open(FILE_TURNOS, 'w') as f:
                for linea in lineas_turnos:
                    f.write(linea + "\n")
        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudo crear {FILE_TURNOS}: {e}")

    def crear_widgets(self):
        """Crea todos los componentes de la interfaz gráfica."""
        
        # --- Frame Principal ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Frame Izquierdo (Formulario) ---
        form_frame = ttk.Frame(main_frame, width=450)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        form_frame.pack_propagate(False)

        # 1. Sección Consulta
        frame_consulta = ttk.LabelFrame(form_frame, text="1. Consultar Turno", padding="10")
        frame_consulta.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_consulta, text="Cantidad de Personas:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_cantidad = ttk.Entry(frame_consulta, width=10)
        self.entry_cantidad.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_consulta, text="Fecha (AAAA-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_fecha = ttk.Entry(frame_consulta, width=15)
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5)
        self.entry_fecha.insert(0, "2025-11-15") # Fecha de ejemplo

        self.btn_verificar = ttk.Button(frame_consulta, text="Verificar Disponibilidad", command=self.on_verificar_disponibilidad)
        self.btn_verificar.grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.EW)

        ttk.Label(frame_consulta, text="Horarios Disponibles:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_horario = ttk.Combobox(frame_consulta, state="readonly", width=18)
        self.combo_horario.grid(row=3, column=1, padx=5, pady=5)

        # 2. Sección Datos Responsable
        frame_resp = ttk.LabelFrame(form_frame, text="2. Datos del Adulto Responsable", padding="10")
        frame_resp.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_resp, text="DNI:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_dni = ttk.Entry(frame_resp)
        self.entry_dni.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_resp, text="Nombre:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(frame_resp)
        self.entry_nombre.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=5)

        ttk.Label(frame_resp, text="Apellido:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_apellido = ttk.Entry(frame_resp)
        self.entry_apellido.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Label(frame_resp, text="Email:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_email = ttk.Entry(frame_resp)
        self.entry_email.grid(row=3, column=1, sticky=tk.EW, padx=5, pady=5)
        
        # *** CAMBIO: Se pide Edad en lugar de Fecha de Nacimiento ***
        ttk.Label(frame_resp, text="Edad:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_edad_resp = ttk.Entry(frame_resp)
        self.entry_edad_resp.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

        self.var_sabe_nadar_resp = tk.BooleanVar()
        self.check_sabe_nadar_resp = ttk.Checkbutton(frame_resp, text="¿Sabe Nadar?", variable=self.var_sabe_nadar_resp)
        self.check_sabe_nadar_resp.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        # 3. Sección Acompañantes
        frame_acomp = ttk.LabelFrame(form_frame, text="3. Acompañantes", padding="10")
        frame_acomp.pack(fill=tk.BOTH, pady=5, expand=True)
        
        # *** CAMBIO: Se pide Edad en lugar de Fecha de Nacimiento ***
        ttk.Label(frame_acomp, text="Ingrese 1 por línea (Formato: Edad,Si/No)", style='Small.TLabel').pack(anchor=tk.W)
        self.text_acompanantes = tk.Text(frame_acomp, height=5, font=('Arial', 10))
        self.text_acompanantes.pack(fill=tk.X, pady=5)
        ttk.Label(frame_acomp, text="Ejemplo: 10,Si\nEjemplo: 6,No", style='Small.TLabel').pack(anchor=tk.W)


        # 4. Sección Pago
        frame_pago = ttk.LabelFrame(form_frame, text="4. Pago", padding="10")
        frame_pago.pack(fill=tk.X, pady=5)

        ttk.Label(frame_pago, text="Medio de Pago:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_medio_pago = ttk.Combobox(frame_pago, state="readonly", values=["Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia"])
        self.combo_medio_pago.grid(row=0, column=1, padx=5, pady=5)
        self.combo_medio_pago.current(0)
        
        # --- Frame Derecho (Recibo) ---
        recibo_frame = ttk.Frame(main_frame)
        recibo_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttk.Label(recibo_frame, text="Recibo / Confirmación", style='Header.TLabel').pack(pady=5)
        
        self.text_recibo = tk.Text(recibo_frame, height=25, font=('Consolas', 10), state="disabled", bg="#f0f0f0")
        self.text_recibo.pack(fill=tk.BOTH, expand=True, pady=5)

        self.btn_confirmar = ttk.Button(recibo_frame, text="CONFIRMAR RESERVA", command=self.on_confirmar_reserva, style='TButton')
        self.btn_confirmar.pack(fill=tk.X, ipady=10, pady=10)

        self.btn_limpiar = ttk.Button(recibo_frame, text="Limpiar Formulario", command=self.limpiar_formulario, style='TButton')
        self.btn_limpiar.pack(fill=tk.X, ipady=5)

    # --- Funciones de Lógica y Eventos ---

    def on_verificar_disponibilidad(self):
        """
        Lee el archivo 'turnos.txt' y filtra los horarios que tienen
        cupo suficiente para la fecha y cantidad de personas indicadas.
        """
        try:
            cantidad = int(self.entry_cantidad.get())
            fecha_consulta = self.entry_fecha.get()
        except ValueError:
            messagebox.showerror("Datos Inválidos", "La cantidad de personas debe ser un número entero.")
            return

        if cantidad <= 0:
            messagebox.showerror("Datos Inválidos", "La cantidad de personas debe ser mayor a 0.")
            return
            
        if not fecha_consulta:
            messagebox.showerror("Datos Inválidos", "La fecha no puede estar vacía.")
            return

        horarios_disponibles = []
        try:
            with open(FILE_TURNOS, 'r') as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    
                    partes = linea.split(',') # [fecha, horario, cupos]
                    
                    if len(partes) != 3:
                        continue # Ignorar líneas corruptas

                    fecha_archivo = partes[0]
                    horario_archivo = partes[1]
                    cupos_archivo = int(partes[2])
                    
                    if fecha_archivo == fecha_consulta and cupos_archivo >= cantidad:
                        horarios_disponibles.append(f"{horario_archivo} ({cupos_archivo} cupos)")
            
            if not horarios_disponibles:
                messagebox.showwarning("Sin Cupo", f"No hay turnos disponibles para {cantidad} personas en la fecha {fecha_consulta}.")
                self.combo_horario['values'] = []
                self.combo_horario.set('')
            else:
                self.combo_horario['values'] = horarios_disponibles
                self.combo_horario.current(0)

        except FileNotFoundError:
            messagebox.showerror("Error Crítico", f"No se encontró el archivo {FILE_TURNOS}. Reinicie la aplicación.")
            self.cargar_datos_iniciales()
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al leer los turnos: {e}")

    def obtener_proximo_id(self):
        """
        Lee el ID de 'proximo_id.txt', lo incrementa y lo guarda.
        Retorna el ID como string (ej: "R1001").
        """
        try:
            with open(FILE_PROXIMO_ID, 'r') as f:
                id_num = int(f.read().strip())
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo leer {FILE_PROXIMO_ID}, reiniciando contador. ({e})")
            id_num = 1001 # Valor default si el archivo está corrupto

        try:
            with open(FILE_PROXIMO_ID, 'w') as f:
                f.write(str(id_num + 1))
        except IOError as e:
            messagebox.showerror("Error Crítico", f"No se pudo actualizar el ID: {e}")
            # Continuamos de todas formas, pero el ID podría repetirse
            
        return f"R{id_num}"

    def on_confirmar_reserva(self):
        """
        Función principal: Valida todos los datos, procesa la reserva,
        actualiza los archivos y genera el recibo.
        """
        
        # --- 1. Obtención y Validación de Datos ---
        try:
            # A. Datos de Consulta
            cantidad = int(self.entry_cantidad.get())
            fecha = self.entry_fecha.get()
            horario_seleccionado = self.combo_horario.get()
            if not horario_seleccionado:
                messagebox.showerror("Error", "Por favor, verifique la disponibilidad y seleccione un horario.")
                return
            horario = horario_seleccionado.split(' ')[0]
            
            # B. Datos Responsable
            dni_resp = self.entry_dni.get()
            nombre_resp = self.entry_nombre.get()
            apellido_resp = self.entry_apellido.get()
            email_resp = self.entry_email.get()
            edad_resp = int(self.entry_edad_resp.get())
            sabe_nadar_resp = "Si" if self.var_sabe_nadar_resp.get() else "No"
            
            if not all([dni_resp, nombre_resp, apellido_resp]):
                messagebox.showerror("Datos Incompletos", "Por favor, complete todos los datos del responsable.")
                return

            if edad_resp < 18:
                messagebox.showerror("Regla de Negocio", "El adulto responsable debe ser mayor de 18 años.")
                return

            # C. Datos Acompañantes
            lista_asistentes = []
            lista_asistentes.append({
                "id": 1,
                "nombre": f"{nombre_resp} {apellido_resp}",
                "edad": edad_resp,
                "sabe_nadar": sabe_nadar_resp
            })
            
            texto_acompanantes = self.text_acompanantes.get("1.0", "end-1c").strip()
            if texto_acompanantes:
                lineas = texto_acompanantes.split('\n')
                for i, linea in enumerate(lineas):
                    linea = linea.strip()
                    if not linea:
                        continue
                        
                    partes = linea.split(',')
                    if len(partes) != 2:
                        messagebox.showerror("Error Acompañantes", f"Error en la línea {i+1} de acompañantes. Use el formato: Edad,Si/No")
                        return
                    
                    edad_acomp = int(partes[0].strip())
                    sabe_nadar_acomp = partes[1].strip().capitalize()
                    
                    if edad_acomp < 5:
                        messagebox.showerror("Regla de Negocio", f"Error: El acompañante {i+1} es menor de 5 años. La edad mínima es 5.")
                        return

                    lista_asistentes.append({
                        "id": i + 2,
                        "nombre": f"Acompañante {i+2}",
                        "edad": edad_acomp,
                        "sabe_nadar": sabe_nadar_acomp
                    })

            # D. Validación Final de Cantidad
            if len(lista_asistentes) != cantidad:
                messagebox.showerror("Error de Cantidad", 
                                     f"Declaró {cantidad} personas pero ingresó datos para {len(lista_asistentes)}.\n"
                                     f"Asegúrese que la cantidad coincida con el responsable más los acompañantes.")
                return

            # E. Datos de Pago
            medio_pago = self.combo_medio_pago.get()
            total_pagar = cantidad * COSTO_ENTRADA
            id_reserva = self.obtener_proximo_id() # Usamos el contador

        except ValueError as e:
            messagebox.showerror("Error de Datos", f"Dato inválido: La EDAD y CANTIDAD deben ser números enteros. Revise los campos.")
            return
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))
            return

        # --- 2. Procesamiento de Archivos (Persistencia) ---
        try:
            # A. Actualizar turnos.txt (Lectura y re-escritura)
            lineas_turnos_actualizadas = []
            with open(FILE_TURNOS, 'r') as f:
                for linea in f:
                    linea_limpia = linea.strip()
                    if not linea_limpia:
                        continue
                    partes = linea_limpia.split(',')
                    if partes[0] == fecha and partes[1] == horario:
                        cupos_actuales = int(partes[2])
                        nuevos_cupos = cupos_actuales - cantidad
                        lineas_turnos_actualizadas.append(f"{fecha},{horario},{nuevos_cupos}\n")
                    else:
                        lineas_turnos_actualizadas.append(linea)
            
            with open(FILE_TURNOS, 'w') as f:
                f.writelines(lineas_turnos_actualizadas)

            # B. Escribir reserva.txt (Append)
            detalle_str = "|".join([f"({p['edad']};{p['sabe_nadar']})" for p in lista_asistentes])
            linea_reserva = f"{id_reserva},{fecha},{horario},{dni_resp},{nombre_resp} {apellido_resp},{cantidad},{total_pagar},{medio_pago},{detalle_str}\n"
            
            with open(FILE_RESERVAS, 'a') as f:
                f.write(linea_reserva)

        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudo guardar la reserva: {e}")
            return

        # --- 3. Generar Recibo (Salida) ---
        recibo_texto = "¡Reserva Confirmada Exitosamente!\n"
        recibo_texto += "=" * 40 + "\n"
        recibo_texto += f"Reserva N°: {id_reserva}\n"
        recibo_texto += f"Responsable: {nombre_resp} {apellido_resp} (DNI: {dni_resp})\n"
        recibo_texto += "-" * 40 + "\n"
        recibo_texto += f"Turno: {fecha} a las {horario} hs.\n"
        recibo_texto += f"Cantidad: {cantidad} personas\n"
        recibo_texto += f"Medio de Pago: {medio_pago}\n"
        recibo_texto += f"TOTAL ABONADO: $ {total_pagar:,.2f}\n"
        recibo_texto += "=" * 40 + "\n"
        recibo_texto += "ENTRADAS GENERADAS:\n"
        
        for p in lista_asistentes:
            tipo_entrada = "VERDE (Adulto)" if p['edad'] >= 18 else "AMARILLA (Menor)"
            recibo_texto += f"  - Asistente {p['id']} (Edad: {p['edad']}) -> Entrada {tipo_entrada}\n"
        
        self.text_recibo.config(state="normal", bg="#e0ffe0")
        self.text_recibo.delete("1.0", tk.END)
        self.text_recibo.insert(tk.END, recibo_texto)
        self.text_recibo.config(state="disabled")

        self.btn_confirmar.config(state="disabled")
        messagebox.showinfo("Éxito", f"Reserva {id_reserva} guardada correctamente.")


    def limpiar_formulario(self):
        """Limpia todos los campos para una nueva venta."""
        self.entry_cantidad.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, "2025-11-15")
        self.combo_horario['values'] = []
        self.combo_horario.set('')
        
        self.entry_dni.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_edad_resp.delete(0, tk.END)
        self.var_sabe_nadar_resp.set(False)
        
        self.text_acompanantes.delete("1.0", tk.END)
        self.combo_medio_pago.current(0)
        
        self.text_recibo.config(state="normal", bg="#f0f0f0")
        self.text_recibo.delete("1.0", tk.END)
        self.text_recibo.config(state="disabled")
        
        self.btn_confirmar.config(state="normal")


if __name__ == "__main__":
    app = AppLagosPark()
    app.mainloop()
