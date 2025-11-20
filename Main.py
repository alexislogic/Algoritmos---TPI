#TPI algoritmos.
import datetime
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Constantes Globales
PrecioEntrada = 12000 #Precio de cada entrada del parque.
ESTADOS = ["Pendiente", "Abonado", "Cancelado"] #Tipos de estados posibles para la reserva. ESTO FALTA RESOLVER.
HORARIOS_PARQUE = ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
METODOS_DE_PAGO = ["Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia"]

# --- Archivos
FILE_TURNOS = "turnos.txt" #Archivo para almacenar los turnos disponibles.
FILE_RESERVAS = "reservas.txt" #Almacena las reservas confirmadas.
FILE_PROXIMO_ID = "proximo_id.txt" # Archivo para el contador de reservas
FILE_CONSTANCIA = "constancia.txt" #Archivo con las constancias de pago.
FILE_TARIFA = "tarifas.txt" #Acumula las diferentes transacciones efectuadas por la venta de entradas.

# --- Estructura de Archivos---
#   Funcionamiento:
    # 1. turnos.txt /LISTO
    #    - Propósito: Almacena los cupos disponibles por cada turno.
    #    - Formato: CSV (Valores Separados por Coma)
    #    - Estructura: fecha,horario,cupos_disponibles
    #    - Ejemplo:
    #      2025-11-15,11:00,80
    #      2025-11-15,12:00,100
    #
    # 2. reservas.txt /LISTO
    #    - Propósito: Log de todas las reservas confirmadas.
    #    - Formato: CSV (Valores Separados por Coma)
    #    - Estructura: id_reserva,dni_resp,nombre_resp,apellido_resp,detalle_str,fecha,horario,cantidad,total_pagar,FechaSolicitud,HoraSolicitud,ESTADOS            
    #    - 'detalle_asistentes' es un string separado por '|'
    #    - Ejemplo:
    #      R1001,2025-11-15,11:00,30123456,Alexis Peralta,2,24000,Tarjeta de Crédito,(18;Si)|(10;No)
    #
    # 3. proximo_id.txt /LISTO
    #    - Propósito: Almacena el próximo número de ID de reserva.
    #    - Formato: Texto plano (un solo número)
    #    - Ejemplo:
    #      1001
   
   #Alcances Gestionar (Se crean durante el programa): /LISTO
    # Solicitud de turno (Nro Solicitud, DatosResponsable, DatosAcompañantes, FechaTurno, HoraTurno, Cantidad de personas, Importe, FechaSolicitud, HoraSolicitud,  Estado)
        #Se almacenara en una variable, para luego guardarse en el archivo reservas.
    # Constancia de pago (Nro Solicitud, Importe, Medio de pago, FechaPago, HoraPago)
#
   #Alcances Administrar (Ya deben estar cargados): /LISTO
    # Metodo de pago (Nro MedioDePago, Descripción)
    # Tarifas (Nro Operación, Descripción, Costo)

class AppLagosPark(tk.Tk): 
    
    def __init__(self): #DEFINIDOR DE BLOQUES.
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

    def cargar_datos_iniciales(self): #Carga los datos de los archivos.
        """
        Verifica si los archivos de datos existen. Si no, los crea.
        Usa try/except FileNotFoundError.
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
            self.crear_archivo_vacio(FILE_PROXIMO_ID, "0") # Empezar contador en 0

    def crear_archivo_vacio(self, nombre_archivo, contenido_inicial=""): #Crea y setea el valor predeterminado de un archivo.
        """Crea un archivo vacío o con contenido inicial."""
        try:
            with open(nombre_archivo, 'w') as f:
                f.write(contenido_inicial)
        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudo crear {nombre_archivo}: {e}")

    def crear_archivo_turnos_default(self): #Crea el archivo, los valores se registran segun las reservas.
        try:
            with open(FILE_TURNOS, 'w') as f:
               pass #No hace nada.
        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudo crear {FILE_TURNOS}: {e}")

    #def crear_archivo_turnos_default_OLD(self): #Crea y setea el valor predeterminado del archivo turnos (De ejemplo).
    #    """
    #    Crea un archivo 'turnos.txt' con cupos fijos para fechas.
    #    Entra aqui si es la primera vez que se crea el archivo.
    #    """
    #    lineas_turnos = [
    #        # Datos para el dia actual:
    #        "2025-11-15,11:00,100",
    #        "2025-11-15,12:00,100",
    #        "2025-11-15,13:00,100",
    #        "2025-11-15,14:00,100",
    #        "2025-11-15,15:00,100",
    #       "2025-11-15,16:00,100",
    #       "2025-11-15,17:00,100",
    #        "2025-11-15,18:00,100",
    #        "2025-11-15,19:00,100",
    #        # Datos para siguiente dia:
    #       "2025-11-16,11:00,100",
    #       "2025-11-16,12:00,100",
    #       "2025-11-16,13:00,100",
    #        "2025-11-16,14:00,100",
    #        "2025-11-16,15:00,100",
    #       "2025-11-16,16:00,100",
    #       "2025-11-16,17:00,100",
    #       "2025-11-16,18:00,100",
    #        "2025-11-16,19:00,100"
    #    ]
    #    try:
    #        with open(FILE_TURNOS, 'w') as f:
    #           for linea in lineas_turnos:
    #               f.write(linea + "\n")
    #    except IOError as e:
    #        messagebox.showerror("Error de Archivo", f"No se pudo crear {FILE_TURNOS}: {e}")

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

        ttk.Label(frame_consulta, text="Fecha (AAAA-MM-DD):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5) #VERIFICAR: CAMBIAR A FECHA LATAM.
        self.entry_fecha = ttk.Entry(frame_consulta, width=15)
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5)
        self.entry_fecha.insert(0, "2025-12-15") # Fecha de ejemplo

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
        
        # *** CAMBIO: Se pide Edad en lugar de Fecha de Nacimiento *** VERIFICAR: MODIFICAR PARA QUE SE GUARDE LA FECHA DE NACIMIENTO.
        ttk.Label(frame_resp, text="Edad:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_edad_resp = ttk.Entry(frame_resp)
        self.entry_edad_resp.grid(row=4, column=1, sticky=tk.EW, padx=5, pady=5)

        self.var_sabe_nadar_resp = tk.BooleanVar()
        self.check_sabe_nadar_resp = ttk.Checkbutton(frame_resp, text="¿Sabe Nadar?", variable=self.var_sabe_nadar_resp)
        self.check_sabe_nadar_resp.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        # 3. Sección Acompañantes
        frame_acomp = ttk.LabelFrame(form_frame, text="3. Acompañantes", padding="10")
        frame_acomp.pack(fill=tk.BOTH, pady=5, expand=True)
        
        # *** CAMBIO: Se pide Edad en lugar de Fecha de Nacimiento *** VERIFICAR: MODIFICAR PARA QUE SE GUARDE LA FECHA DE NACIMIENTO.
        ttk.Label(frame_acomp, text="Ingrese 1 por línea (Formato: Edad,Si/No)", style='Small.TLabel').pack(anchor=tk.W)
        self.text_acompanantes = tk.Text(frame_acomp, height=5, font=('Arial', 10))
        self.text_acompanantes.pack(fill=tk.X, pady=5)
        ttk.Label(frame_acomp, text="Ejemplo: 10,Si\nEjemplo: 6,No", style='Small.TLabel').pack(anchor=tk.W)


        # 4. Sección Pago VERIFICAR Y MODIFICAR LAS "VALUES" PARA UTILIZAR DIRECTAMENTE UNA VARIABLE/ARCHIVO QUE LAS CONTENGA.
        frame_pago = ttk.LabelFrame(form_frame, text="4. Pago", padding="10")
        frame_pago.pack(fill=tk.X, pady=5)

        ttk.Label(frame_pago, text="Medio de Pago:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_medio_pago = ttk.Combobox(frame_pago, state="readonly", values=METODOS_DE_PAGO)
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
    # A medida que interactua con la interfaz, se ejecutan las funciones logicas.

    def on_verificar_disponibilidad(self):
        """
        Lee el archivo 'turnos.txt' y filtra los horarios que tienen
        cupo suficiente para la fecha y cantidad de personas indicadas.
        """

        # Comprueba que los datos sean correctos:
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

        horarioActual = time.localtime()
        fecha_actual = time.strftime("%d/%m/%Y", horarioActual)
        if fecha_consulta < fecha_actual: #Comprueba que la fecha sea valida. 
            messagebox.showerror("Datos Inválidos", "La fecha debe ser mayor o igual a hoy.")
            return

        #Define las variables a utilizar.
        horarios_Ocupados = [] #Crea una variable para almacenar los horarios que estan ocupados en esa fecha.
        horarios_Disponibles = [] #Crea una variable para almacenar los horarios que estan disponibles en esa fecha.
        flag = False #Bandera para indicar cuando un horario no este disponible.
        #Busca los horarios NO disponibles.
        try:
            with open(FILE_TURNOS, 'r') as f:
                for linea in f: #Obtiene el archivo por los campos.
                    linea = linea.strip()
                    if not linea:
                        continue
                    
                    partes = linea.split(',') # Lo almacena en una lista: [fecha, horario, cupos]
                    
                    if len(partes) != 3:
                        continue # Ignorar líneas corruptas

                    fecha_archivo = partes[0]
                    horario_archivo = partes[1]
                    cupos_archivo = int(partes[2])
                    
                    if fecha_archivo == fecha_consulta and cupos_archivo < cantidad: #Si coincide la fecha y no hay lugares disponibles.
                        horarios_Ocupados.append(horario_archivo)
            
            if len(horarios_Ocupados) > len(HORARIOS_PARQUE): #Si todos los turnos fueron ocupados.
                messagebox.showwarning("Sin Cupo", f"No hay turnos disponibles para {cantidad} personas en la fecha {fecha_consulta}.")
                self.combo_horario['values'] = []
                self.combo_horario.set('')
            else: #Obtener turnos disponibles y mostrarlos.
                for i in range(len(HORARIOS_PARQUE)): #Itera todos los horarios.
                    flag = False
                    for j in range(len(horarios_Ocupados)): #Itera los horarios no disponibles.
                        if HORARIOS_PARQUE[i] == horarios_Ocupados[j]:
                            flag = True #Si coincide con un horario no disponible, activa la bandera.
                    if flag == False: #Mientras sea un horario disponible.
                        horarios_Disponibles.append(HORARIOS_PARQUE[i])

                self.combo_horario['values'] = horarios_Disponibles
                self.combo_horario.current(0)

        #Abordar errores:
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
        try: #Obtiene el ultimo ID.
            with open(FILE_PROXIMO_ID, 'r') as f:
                id_num = int(f.read().strip())
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo leer {FILE_PROXIMO_ID}, reiniciando contador. ({e})")
            id_num = 0 # Valor default si el archivo está corrupto

        try: #Añade el ID que le sigue.
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
            if not horario_seleccionado: #Verificacion que exista.
                messagebox.showerror("Error", "Por favor, verifique la disponibilidad y seleccione un horario.")
                return
            horario = horario_seleccionado
            
            print(f"El horario seleccionado actual es: {horario}")

            # B. Datos Responsable
            dni_resp = self.entry_dni.get()
            nombre_resp = self.entry_nombre.get()
            apellido_resp = self.entry_apellido.get()
            email_resp = self.entry_email.get()
            edad_resp = int(self.entry_edad_resp.get()) #VERIFICAR: CAMBIAR POR FECHA DE NACIMIENTO.
            sabe_nadar_resp = "Si" if self.var_sabe_nadar_resp.get() else "No"
            
            if not all([dni_resp, nombre_resp, apellido_resp]): #Comprueba que los datos se ingresen.
                messagebox.showerror("Datos Incompletos", "Por favor, complete todos los datos del responsable.")
                return

            if edad_resp < 18: #Comprueba que sea mayor de edad. #VERIFICAR: MODIFICAR POR FECHA DE NACIMIENTO.
                messagebox.showerror("Regla de Negocio", "El adulto responsable debe ser mayor de 18 años.")
                return

            # C. Datos Acompañantes VERIFICAR FUNCIONAMIENTO, HACERLO MAS SIMPLE.
            lista_asistentes = []
            lista_asistentes.append({
                "id": 1,
                "nombre": f"{nombre_resp} {apellido_resp}",
                "edad": edad_resp,
                "sabe_nadar": sabe_nadar_resp
            })
            
            texto_acompanantes = self.text_acompanantes.get("1.0", "end-1c").strip()
            if texto_acompanantes: #MATI NECESITO QUE MODIFIQUES EL CUADRO DE TEXTO PARA SIMPLIFICAR LA OBTENCION DE DATOS.
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
            total_pagar = cantidad * PrecioEntrada
            id_reserva = self.obtener_proximo_id() # Usamos el contador

        #Abarca datos de funcionamiento:
        except ValueError as e:
            messagebox.showerror("Error de Datos", f"Dato inválido: La EDAD y CANTIDAD deben ser números enteros. Revise los campos.")
            return
        except Exception as e:
            messagebox.showerror("Error Inesperado", str(e))
            return

        # --- 2. Procesamiento de Archivos (Persistencia) ---
        try:
            # A. Actualizar turnos.txt (Lectura y re-escritura)

            #Definicion de variables.
            lineas_turnos_actualizadas = []
            flag = False #Bandera en caso de que deba crear un nuevo turno.

            with open(FILE_TURNOS, 'r') as f: #Abre el archivo de turnos.
                for linea in f:
                    linea_limpia = linea.strip() #Obtiene el registro.
                    if not linea_limpia:
                        continue

                    partes = linea_limpia.split(',') #Convierte el registro en una lista.
                    if partes[0] == fecha and partes[1] == horario: #Si coincide el horario y fecha (Ya existia un turno creado)
                        cupos_actuales = int(partes[2])
                        nuevos_cupos = cupos_actuales - cantidad
                        lineas_turnos_actualizadas.append(f"{fecha},{horario},{nuevos_cupos}\n")
                        flag = True #Activa bandera para no crear otro turno.
                    else:
                        lineas_turnos_actualizadas.append(linea)
            
            print(f"El horario seleccionado es: {horario} en reservas")

            if flag == False: #Crea un nuevo turno.
                lineas_turnos_actualizadas.append(f"{fecha},{horario},{100 - cantidad}\n") #100 es la cantidad de cupos que ofrece el parque.

            with open(FILE_TURNOS, 'w') as f:
                f.writelines(lineas_turnos_actualizadas)

            # B. Escribir reserva.txt (Append)
            #Obtener horario de la transaccion.
            hora_local = time.localtime()
            FechaSolicitud = time.strftime("%d/%m/%Y", hora_local) #OBTENER FECHA ACTUAL
            HoraSolicitud = time.strftime("%H:%M:%S", hora_local) #OBTENER HORA ACTUAL
            detalle_str = "|".join([f"({p['edad']};{p['sabe_nadar']})" for p in lista_asistentes]) #VERIFICAR: ESTOY HAY QUE CAMBIARLO NI BIEN ESTE HECHA LA INTERFAZ.
            
            linea_reserva = f"{id_reserva},{dni_resp},{nombre_resp} {apellido_resp},{detalle_str},{fecha},{horario},{cantidad},{total_pagar},{FechaSolicitud},{HoraSolicitud},{ESTADOS[0]}\n"
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
