#TPI algoritmos.
import datetime
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# --- Constantes Globales
PrecioEntrada = 12000 #Precio de cada entrada del parque (Inicial).
ESTADOS = ["Pendiente", "Abonado", "Cancelado"] #Tipos de estados posibles para la reserva. ESTO FALTA RESOLVER.
HORARIOS_PARQUE = ['11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
METODOS_DE_PAGO = ["Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia"]

# --- Archivos
FILE_TURNOS = "turnos.txt" #Archivo para almacenar los turnos disponibles.
FILE_RESERVAS = "reservas.txt" #Almacena las reservas confirmadas.
FILE_PROXIMO_ID = "proximo_id.txt" # Archivo para el contador de reservas
FILE_CONSTANCIA = "constancia.txt" #Archivo con las constancias de pago, que contiene los datos de las transacciones.
FILE_TARIFA = "tarifas.txt" #Contiene el valor de la tarifa por cada entrada.
FILE_CANCELACION = "cancelacion.txt" #Contiene las cancelaciones.

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
    #       -
    #
    # 3. proximo_id.txt /LISTO
    #    - Propósito: Almacena el próximo número de ID de reserva.
    #    - Formato: Texto plano (un solo número)
    #    - Ejemplo:
    #      1001
   
   #Alcances Gestionar (Se crean durante el programa): /LISTO
    # Solicitud de turno (Nro Solicitud, DatosResponsable, DatosAcompañantes, FechaTurno, HoraTurno, Cantidad de personas, Importe, FechaSolicitud, HoraSolicitud,  Estado)
        #Se almacenara en varias variables, para luego guardarse en el archivo reservas.
    # Constancia de pago (Nro Solicitud, Importe, Medio de pago, FechaPago, HoraPago)
#
   #Alcances Administrar (Ya deben estar cargados): /LISTO
    # Metodo de pago (Nro MedioDePago, Descripción)
    # Tarifas (Nro Operación, Descripción, Costo)
    # Cancelaciones (Nro Solicitud, ImporteTotal, ImporteDevuelto, FechaCancelación, HoraCancelación, Motivo)

def es_fecha_valida(texto): #Verifica que la fecha sea valida en formato.
        try:
            # Intenta crear la fecha. Si el formato está mal o el día no existe (ej: 30/02), falla.
            datetime.datetime.strptime(texto, '%d/%m/%Y')
            return True
        except ValueError:
            return False

class AppLagosPark(tk.Tk):
    def __init__(self):
        super().__init__()
        #Definimos flexibilidad de ventana.
        self.title("TPI Algoritmos - Venta de Entradas 'Lagos Park'")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width*0.6)}x{int(screen_height*0.6)}") # 80% de la pantalla
        self.resizable(True, True)
        
        # Intento de Maximizar Automáticamentes
        try:
            # Para Windows
            self.state('zoomed')
        except:
            # Para Linux (Si falla el anterior)
            try:
                self.attributes('-zoomed', True)
            except:
                pass # Si falla todo, igual ya seteamos el geometry grande arriba

        # Estilos
        # --- ESTILOS ---
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Definimos el color base para no escribirlo mil veces
        COLOR_FONDO = '#E0F4FF'
        
        # 1. Estilos Generales
        self.style.configure('TLabel', background=COLOR_FONDO, font=('Arial', 10))
        self.style.configure('TFrame', background=COLOR_FONDO)
        self.style.configure('TButton', background='#6EC6FF')
        self.style.map('TButton', background=[('active', '#e7d5ff')])
        
        # 2. IMPORTANTE: Para los recuadros con título (1. Datos del turno, etc)
        self.style.configure('TLabelframe', background=COLOR_FONDO, bordercolor=COLOR_FONDO)
        self.style.configure('TLabelframe.Label', background=COLOR_FONDO, font=('Arial', 10, 'bold'))
        
        # 3. Para el Checkbox "¿Sabe Nadar?"
        self.style.configure('TCheckbutton', background=COLOR_FONDO, font=('Arial', 10))
        
        # 4. Entradas y otros
        self.style.configure('TEntry', font=('Arial', 10))
        self.style.configure('TCombobox', font=('Arial', 10))

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
            # 2. Verificar reservas.txt
            with open(FILE_CANCELACION, 'r') as f:
                pass
        except FileNotFoundError:
            self.crear_archivo_vacio(FILE_CANCELACION)
            
        try:
            # 3. Verificar proximo_id.txt
            with open(FILE_PROXIMO_ID, 'r') as f:
                pass
        except FileNotFoundError:
            self.crear_archivo_vacio(FILE_PROXIMO_ID, "1") # Empezar contador en 1
        
        try:
            # 4. Verificar tarifas.txt
            with open(FILE_TARIFA, 'r') as f:
                pass
        except FileNotFoundError:
            self.crear_archivo_vacio(FILE_TARIFA, str(PrecioEntrada))
        
        try:
            # 5. Verificar constancia.txt
            with open(FILE_CONSTANCIA, 'r') as f:
                pass
        except FileNotFoundError:
            self.crear_archivo_vacio(FILE_CONSTANCIA)

    def crear_archivo_vacio(self, nombre_archivo, contenido_inicial=""): #Crea y setea el valor predeterminado de un archivo.
        """Crea un archivo vacío o con contenido inicial."""
        try:
            with open(nombre_archivo, 'x') as f:
                f.write(contenido_inicial)
        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudo crear {nombre_archivo}: {e}")

    def crear_archivo_turnos_default(self): #Crea el archivo, los valores se registran segun las reservas.
        try:
            with open(FILE_TURNOS, 'x') as f:
               pass #No hace nada.
        except IOError as e:
            messagebox.showerror("Error de Archivo", f"No se pudo crear {FILE_TURNOS}: {e}")

    def crear_widgets(self):
        """Crea todos los componentes de la interfaz gráfica."""
        
        # --- Frame Principal ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Frame Izquierdo (Formulario) ---
        form_frame = ttk.Frame(main_frame, width=550) 
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        form_frame.pack_propagate(False)

        # =================================================================
        # 1. Sección UNIFICADA: Consulta de Turno y Pago
        # =================================================================
        frame_consulta = ttk.LabelFrame(form_frame, text="1. Datos del Turno y Pago", padding="5")
        frame_consulta.pack(fill=tk.X, pady=5)
        
        # Fila 0: Cantidad y Fecha
        ttk.Label(frame_consulta, text="Cant. Personas:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.entry_cantidad = ttk.Entry(frame_consulta, width=5)
        self.entry_cantidad.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)

        ttk.Label(frame_consulta, text="Fecha (DD/MM/AAAA):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.entry_fecha = ttk.Entry(frame_consulta, width=12)
        self.entry_fecha.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.entry_fecha.insert(0, "")

        # Fila 1: Botón Verificar
        self.btn_verificar = ttk.Button(frame_consulta, text="Verificar Disponibilidad", command=self.on_verificar_disponibilidad)
        self.btn_verificar.grid(row=1, column=0, columnspan=4, pady=8, sticky=tk.EW)

        # Fila 2: Horario y Medio de Pago
        ttk.Label(frame_consulta, text="Horario:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.combo_horario = ttk.Combobox(frame_consulta, state="readonly", width=12)
        self.combo_horario.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        ttk.Label(frame_consulta, text="Medio Pago:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.combo_medio_pago = ttk.Combobox(frame_consulta, state="readonly", values=METODOS_DE_PAGO, width=15)
        self.combo_medio_pago.grid(row=2, column=3, padx=5, pady=2, sticky=tk.W)
        self.combo_medio_pago.current(0)


        # =================================================================
        # 2. Sección Datos Responsable: Entre las 2 columnas.
        # =================================================================
        frame_resp = ttk.LabelFrame(form_frame, text="2. Datos del Responsable", padding="5")
        frame_resp.pack(fill=tk.X, pady=5)
        
        # Fila 0: DNI y Nombre
        ttk.Label(frame_resp, text="DNI:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.entry_dni = ttk.Entry(frame_resp, width=15)
        self.entry_dni.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(frame_resp, text="Nombre:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.entry_nombre = ttk.Entry(frame_resp, width=15)
        self.entry_nombre.grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)

        # Fila 1: Apellido y Email
        ttk.Label(frame_resp, text="Apellido:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.entry_apellido = ttk.Entry(frame_resp, width=15)
        self.entry_apellido.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(frame_resp, text="Email:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.entry_email = ttk.Entry(frame_resp, width=15)
        self.entry_email.grid(row=1, column=3, sticky=tk.W, padx=5, pady=2)
        
        # Fila 2: Nacimiento y Checkbox
        ttk.Label(frame_resp, text="F. Nacim.:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.entry_nacimiento = ttk.Entry(frame_resp, width=15)
        self.entry_nacimiento.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)

        self.var_sabe_nadar_resp = tk.BooleanVar()
        self.check_sabe_nadar_resp = ttk.Checkbutton(frame_resp, text="¿Sabe Nadar?", variable=self.var_sabe_nadar_resp)
        self.check_sabe_nadar_resp.grid(row=2, column=2, columnspan=2, sticky=tk.W, padx=5, pady=2)


        # =================================================================
        # 3. Sección Acompañantes
        # =================================================================
        frame_acomp = ttk.LabelFrame(form_frame, text="3. Acompañantes", padding="5")
        frame_acomp.pack(fill=tk.BOTH, pady=5, expand=True)
        
        ttk.Label(frame_acomp, text="1 por línea (F. Nacimiento, Si/No):", style='Small.TLabel').pack(anchor=tk.W)
        self.text_acompanantes = tk.Text(frame_acomp, height=4, font=('Arial', 10)) # Reduje height a 4 para ahorrar espacio
        self.text_acompanantes.pack(fill=tk.X, pady=2)
        ttk.Label(frame_acomp, text="Ej: 12/05/2015, Si", style='Small.TLabel').pack(anchor=tk.W)

        # --- Botón de Acceso a Gestión (Admin) ---
        frame_admin = ttk.Frame(main_frame) # Quitamos padding excesivo
        frame_admin.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        ttk.Separator(frame_admin, orient='horizontal').pack(fill='x', pady=2)
        
        btn_admin = ttk.Button(frame_admin, text="Acceso Encargado/Admin", 
                               command=self.abrir_admin)
        btn_admin.pack(side=tk.LEFT)
        
        # --- Frame Derecho (Recibo) ---
        recibo_frame = ttk.Frame(main_frame)
        recibo_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttk.Label(recibo_frame, text="Recibo / Confirmación", style='Header.TLabel').pack(pady=5)
        
        self.text_recibo = tk.Text(recibo_frame, height=20, font=('Consolas', 9), state="disabled", bg="#f0f0f0") # Achiqué un poco la letra y altura
        self.text_recibo.pack(fill=tk.BOTH, expand=True, pady=5)

        self.btn_confirmar = ttk.Button(recibo_frame, text="CONFIRMAR RESERVA", command=self.on_confirmar_reserva, style='TButton')
        self.btn_confirmar.pack(fill=tk.X, ipady=8, pady=5)

        self.btn_limpiar = ttk.Button(recibo_frame, text="Limpiar Formulario", command=self.limpiar_formulario, style='TButton')
        self.btn_limpiar.pack(fill=tk.X, ipady=4)


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

        if not es_fecha_valida(fecha_consulta):
            messagebox.showerror("Datos Inválidos", "La fecha debe usar el formato ´dd/mm/yyyy´.")
            return

        horarioActual = time.localtime()
        fecha_actual = time.strftime("%d/%m/%Y", horarioActual)
        print(f"Esta es la fecha actual: {fecha_actual}, esta la fecha consulta: {fecha_consulta}")
        fecha_actual_lista = fecha_actual.split("/")
        fecha_consulta_lista = fecha_consulta.split("/")
        for i in range(3): #Comparar fechas.
            if int(fecha_consulta_lista[2-i]) < int(fecha_actual_lista[2-i]): #Verifica si es menor comparando desde el año hasta el dia.
                messagebox.showerror("Datos Inválidos", "La fecha debe ser mayor o igual a hoy.")
                return
            elif int(fecha_consulta_lista[2-i]) > int(fecha_actual_lista[2-i]): #Si es mayor sale automaticamente.
                break
                

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
            
        return f"{id_num}" #Retorna el id correspondiente.

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
            horarioActual = time.localtime()
            fecha_actual = time.strftime("%d/%m/%Y", horarioActual)

            # B. Datos Responsable
            dni_resp = self.entry_dni.get()
            nombre_resp = self.entry_nombre.get()
            apellido_resp = self.entry_apellido.get()
            email_resp = self.entry_email.get()
            edad_resp1 = self.entry_nacimiento.get() #Lo guardamos como edad para verificar que sea mayor a 18 años
            sabe_nadar_resp = "Si" if self.var_sabe_nadar_resp.get() else "No"
            
            if not all([dni_resp, nombre_resp, apellido_resp]): #Comprueba que los datos se ingresen.
                messagebox.showerror("Datos Incompletos", "Por favor, complete todos los datos del responsable.")
                return
            
            if not dni_resp.isdigit():
                messagebox.showerror("Datos invalidos", "Debe ingresar un DNI VALIDO: Solo numeros.")
                return

            if not "@" in email_resp:
                messagebox.showerror("Datos invalidos", "El mail debe ser valido.")
                return

            if not es_fecha_valida(edad_resp1):
                messagebox.showerror("Datos invalidos", "Debe ingresar una fecha valida.")
                return

            fecact= fecha_actual.split("/")
            edad_resp=edad_resp1.split("/")
            for i in range(3):
                edad_resp[i]=int(edad_resp[i])
                fecact[i]=int(fecact[i])
            b=0
            if edad_resp[2]>fecact[2]-18:
                b=1
            elif edad_resp[1]>fecact[1] and edad_resp[2]==fecact[2]-18:
                b=1
            elif edad_resp[0]>fecact[0] and edad_resp[2]==fecact[2]-18 and edad_resp[1]==fecact[1]:
                b=1

            if b==1: #Comprueba que sea mayor de edad. #VERIFICAR: MODIFICAR POR FECHA DE NACIMIENTO.
                messagebox.showerror("Regla de Negocio", "El adulto responsable debe ser mayor de 18 años.")
                return
            fecha_nacimiento = self.entry_nacimiento.get()

            # C. Datos Acompañantes, usamos un formato de diccionarios
            lista_asistentes = []
            lista_asistentes.append({
                "id": 1,
                "nombre": f"{nombre_resp} {apellido_resp}",
                "Fecha_nacimiento": fecha_nacimiento ,
                "sabe_nadar": sabe_nadar_resp
            })
            
            texto_acompanantes = self.text_acompanantes.get("1.0", "end-1c").strip()
            if texto_acompanantes: #Obtenemos los datos de los acompañantes.
                lineas = texto_acompanantes.split('\n')
                for i, linea in enumerate(lineas):
                    linea = linea.strip()
                    if not linea:
                        continue
                        
                    partes = linea.split(',')

                    if len(partes) != 2:
                        messagebox.showerror("Error Acompañantes", f"Error en la línea {i+1} de acompañantes. Use el formato: Fecha de nacimiento,Si/No")
                        return
                    horarioActual = time.localtime()
                    fecha_actual = time.strftime("%d/%m/%Y", horarioActual)
                    edad_acomp = partes[0].split("/")
                    sabe_nadar_acomp = partes[1].strip().capitalize()
                    
                    if not es_fecha_valida(partes[0]): #Verificar bien formato de fecha.
                        messagebox.showerror("Error de formato", "ingrese fecha (DD,MM,AAAA),si/no")
                        return

                    if "no" != sabe_nadar_acomp.lower() and "si" != sabe_nadar_acomp.lower(): #Verificar que ingrese bien los datos.
                        messagebox.showerror("Error de formato", "ingrese si o no: (DD,MM,AAAA),si/no")
                        return

                    fecact= fecha_actual.split("/")
                    for j in range(3):
                        edad_acomp[j]=int(edad_acomp[j])
                        fecact[j]=int(fecact[j])
                    b=0
                    if edad_acomp[2]>fecact[2]-5:
                        b=1
                    elif edad_acomp[1]>fecact[1] and edad_acomp[2]==fecact[2]-5:
                        b=1
                    elif edad_acomp[0]>fecact[0] and edad_acomp[2]==fecact[2]-5 and edad_acomp[1]==fecact[1]:
                        b=1

                    if b==1: #Comprueba que sea mayor de edad.
                        messagebox.showerror("Regla de Negocio", "El niño debe tener al menos 5 años.")
                        return


                    #Crear un diccionario identificando la edad de los acompañantes
                    lista_asistentes.append({
                        "id": i + 2,
                        "nombre": f"Acompañante {i+2}",
                        "Fecha_nacimiento": partes[0],
                        "sabe_nadar": sabe_nadar_acomp
                    }) 

            # D. Validación Final de Cantidad
            if len(lista_asistentes) != cantidad:
                messagebox.showerror("Error de Cantidad", 
                                     f"Declaró {cantidad} personas pero ingresó datos para {len(lista_asistentes)}.\n"
                                     f"Asegúrese que la cantidad coincida con el responsable más los acompañantes.")
                return

            # E. Datos de Pago
            with open(FILE_TARIFA, 'r') as f:
                Precio = int(f.read().strip())
            
            medio_pago = self.combo_medio_pago.get()
            total_pagar = cantidad * Precio
            id_reserva = self.obtener_proximo_id() # Usamos el contador

        #Abarca datos de funcionamiento:
        except ValueError as e:
            messagebox.showerror("Error de Datos", f"Dato inválido: La CANTIDAD debe ser número entero. Revise el campo.")
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
            detalle_str = "|".join([f"({p['Fecha_nacimiento']};{p['sabe_nadar']})" for p in lista_asistentes]) #DETALLE DE LOS ACOMPAÑANTES EN TEXTO.

            linea_reserva = f"{id_reserva},{dni_resp},{nombre_resp} {apellido_resp},{detalle_str},{fecha},{horario},{cantidad},{total_pagar},{FechaSolicitud},{HoraSolicitud},{ESTADOS[1]}\n" #Añadir nuevo registro al archivo FILE_RESERVAS. (Reserva)
            linea_constancia = f"{id_reserva},{total_pagar},{medio_pago},{HoraSolicitud}\n" #Añadir registro nuevo al archivo de FILE_CONSTANCIA. (Pago)

            with open(FILE_RESERVAS, 'a') as f:
                f.write(linea_reserva)
            
            with open(FILE_CONSTANCIA, 'a') as f:
                f.write(linea_constancia)


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

        
        for p in lista_asistentes: # Verificar edad para asignar la entrada
            horarioActual = time.localtime()
            fecha_actual = time.strftime("%d/%m/%Y", horarioActual)
            edad_acomp1 = p['Fecha_nacimiento']
            edad_acomp = edad_acomp1.split("/")

            fecact= fecha_actual.split("/")
            for j in range(3):
                edad_acomp[j]=int(edad_acomp[j])
                fecact[j]=int(fecact[j])
            b=0
            if edad_acomp[2]>fecact[2]-18:
                b=1
            elif edad_acomp[1]>fecact[1] and edad_acomp[2]==fecact[2]-18:
                b=1
            elif edad_acomp[0]>fecact[0] and edad_acomp[2]==fecact[2]-18 and edad_acomp[1]==fecact[1]:
                    b=1
            
            tipo_entrada = "VERDE (Adulto)" if b == 0 else "AMARILLA (Menor)" #Verificamos si es mayor para entregar la entrada correspondiente.
            recibo_texto += f"  - Asistente {p['id']} (Fecha de nacimiento: {p['Fecha_nacimiento']}) -> Entrada {tipo_entrada}\n"
        
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
        self.combo_horario['values'] = []
        self.combo_horario.set('')
        
        self.entry_dni.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_nacimiento.delete(0, tk.END)
        self.var_sabe_nadar_resp.set(False)
        
        self.text_acompanantes.delete("1.0", tk.END)
        self.combo_medio_pago.current(0)
        
        self.text_recibo.config(state="normal", bg="#f0f0f0")
        self.text_recibo.delete("1.0", tk.END)
        self.text_recibo.config(state="disabled")
        
        self.btn_confirmar.config(state="normal")
    
    def abrir_admin(self):
        ventana_admin = AppAdmin(self) #Le pasamos a "self" como referencia.
        ventana_admin.grab_set() # Para no tocar la ventana de ventas si estas en administracion.


class AppAdmin(tk.Toplevel): #Administracion e informes.
    """
    Ventana exclusiva para el Encargado/Administrador.
    Maneja Cancelaciones e Informes.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Lagos Park - Módulo de Gestión (Admin)")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{int(screen_width*0.4)}x{int(screen_height*0.4)}") # 80% de la pantalla
        self.resizable(True, True)
        
        # Creamos un sistema de Pestañas (Tabs) para organizar
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # --- Pestaña 1: Cancelaciones ---
        self.frame_cancelacion = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_cancelacion, text="  Gestionar Cancelaciones  ")
        self.crear_interfaz_cancelaciones()
        
        # --- Pestaña 2: Informes ---
        self.frame_informes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_informes, text="  Informes y Estadísticas  ")
        self.crear_interfaz_informes()

    # ---------------------------------------------------------
    # LÓGICA DE CANCELACIONES
    # ---------------------------------------------------------
    def crear_interfaz_cancelaciones(self):
        panel = ttk.LabelFrame(self.frame_cancelacion, text="Buscar Reserva a Cancelar", padding=20)
        panel.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(panel, text="ID de Reserva (ej: 1001):").pack(side="left", padx=5)
        self.entry_buscar_id = ttk.Entry(panel, width=15)
        self.entry_buscar_id.pack(side="left", padx=5)
        
        ttk.Button(panel, text="<Buscar>", command=self.buscar_reserva).pack(side="left", padx=10)
        
        # Area de detalles
        self.lbl_detalles = tk.Label(self.frame_cancelacion, text="", justify="left", font=("Consolas", 10), bg="#fff3e0", relief="solid")
        self.lbl_detalles.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón de acción (inicialmente deshabilitado)
        self.btn_cancelar = ttk.Button(self.frame_cancelacion, text="X: CANCELAR RESERVA (Reintegro 80%)", state="disabled", command=self.ejecutar_cancelacion)
        self.btn_cancelar.pack(fill="x", padx=20, pady=20, ipady=10)

        # --- APARTADO PARA MOTIVO ---
        frame_motivo = ttk.Frame(self.frame_cancelacion)
        frame_motivo.pack(fill="x", padx=20, pady=5)
        
        ttk.Label(frame_motivo, text="Motivo de Cancelación:", font=('Arial', 10, 'bold')).pack(anchor="w")
        self.entry_motivo = ttk.Entry(frame_motivo)
        self.entry_motivo.pack(fill="x", pady=5)
        # ----------------------------------

    def buscar_reserva(self):
        self.entry_motivo.delete(0, tk.END) #Limpiar motivo.
        id_buscado = self.entry_buscar_id.get().strip() #Obtiene el ID que ingreso.
        self.reserva_encontrada = None # Variable temporal para guardar datos
        
        if not id_buscado.isdigit():
            messagebox.showerror("Datos invalidos", "Ingrese SOLO numeros.")
            return

        if int(id_buscado) < 1:
            messagebox.showerror("Datos invalidos", "El valor minimo es 1.")
            return

        try:
            with open(FILE_RESERVAS, 'r') as f: #BUSQUEDA EFICIENTE DENTRO DEL ARCHIVO POR INDICE.
                lineas = f.readlines()
                if int(id_buscado) > len(lineas):
                    messagebox.showerror("Datos invalidos", "No existe ese numero de registro.")
                    return
                self.reserva_encontrada = lineas[int(id_buscado)-1].strip().split(',') #Busca en la linea especifica usando el indice.
            
            if self.reserva_encontrada:
                # Agrupar datos en un string llamado "info"
                estado = self.reserva_encontrada[10] # El estado es el último campo
                info = f"ID: {self.reserva_encontrada[0]}\n"
                info = info + f"Titular: {self.reserva_encontrada[2]} (DNI: {self.reserva_encontrada[1]})\n"
                info = info + f"Fecha Turno: {self.reserva_encontrada[4]} a las {self.reserva_encontrada[5]}\n"
                info = info + f"Monto Abonado: ${self.reserva_encontrada[7]}\n"
                info = info + f"ESTADO ACTUAL: {estado}"
                
                self.lbl_detalles.config(text=info)
                
                # Solo permitir cancelar si no está cancelada ya
                if "Cancelado" not in estado:
                    self.btn_cancelar.config(state="normal")
                else:
                    self.btn_cancelar.config(state="disabled")
                    messagebox.showinfo("Info", "Esta reserva ya fue cancelada previamente.")
            else: #Casos particulares.
                self.lbl_detalles.config(text="Reserva no encontrada.")
                self.btn_cancelar.config(state="disabled")
                
        except FileNotFoundError:
            messagebox.showerror("Error", "No existe el archivo de reservas.")

    def ejecutar_cancelacion(self):
        if not self.reserva_encontrada:
            return

        # 1. Calcular devolución (Regla de Negocio: 80%)
        total_abonado = float(self.reserva_encontrada[7])
        reintegro = total_abonado * 0.80
        
        confirmacion = messagebox.askyesno("Confirmar Cancelación", 
                                           f"Se devolverá ${reintegro:.2f} al cliente.\n¿Confirmar cancelación?")
        if not confirmacion:
            return

        # 2. Actualizar archivo RESERVAS (Reescribir archivo)
        id_target = self.reserva_encontrada[0]
        fecha_turno = self.reserva_encontrada[4]
        horario_turno = self.reserva_encontrada[5]
        cantidad_personas = int(self.reserva_encontrada[6])
        motivo = self.entry_motivo.get().strip()

        try:
            with open(FILE_RESERVAS, 'r') as f: #Entra en modo lecutra para no borrarlo.
                lineas = f.readlines()
            
            with open(FILE_RESERVAS, 'w') as f: #Busca la reserva correspondiente.
                for linea in lineas:
                    partes = linea.strip().split(',')

                    if partes[0] == id_target: #Cuando encuentre el ID.
                        # Modificamos el estado (último elemento)
                        partes[10] = "Cancelado"
                        nueva_linea = ",".join(partes) + "\n"
                        f.write(nueva_linea) #Añadimos la linea modificada.
                    else: #Sigue escribiendo la nueva version del archivo.
                        f.write(linea)
            
            # 3. Devolver Cupos a TURNOS.TXT
            # Leemos turnos, buscamos fecha/hora y sumamos cupos
            turnos_nuevos = []
            with open(FILE_TURNOS, 'r') as f:
                for linea in f:
                    partes = linea.strip().split(',') #Convertimos el registro en una lista.
                    if partes[0] == fecha_turno and partes[1] == horario_turno: #Comparamos fecha y hora del turno.
                        cupos_actuales = int(partes[2])
                        nuevo_cupo = cupos_actuales + cantidad_personas #Sumamos cupos disponibles luego de la cancelacion.
                        turnos_nuevos.append(f"{fecha_turno},{horario_turno},{nuevo_cupo}\n") #Añadimos la linea modificada.
                    else: #Sigue escribiendo la nueva verison del archivo.
                        turnos_nuevos.append(linea)

            horarioActual = time.strftime("%H:%M:%S", time.localtime()) #Horario actual de la transaccion.
            fecha_actual = time.strftime("%d/%m/%Y", time.localtime()) #Fecha actual de la transaccion.

            linea_cancelacion = []
            linea_cancelacion = (f"{id_target},{total_abonado},{reintegro},{fecha_actual},{horarioActual},{motivo}")

            with open(FILE_TURNOS, 'w') as f:
                f.writelines(turnos_nuevos)

            with open(FILE_CANCELACION, 'a') as f:
                f.writelines(linea_cancelacion)

            messagebox.showinfo("Éxito", "Reserva cancelada, cupos liberados y reintegro calculado.")
            self.lbl_detalles.config(text="--- OPERACIÓN FINALIZADA ---")
            self.btn_cancelar.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al cancelar: {e}")

    # ---------------------------------------------------------
    # LÓGICA DE INFORMES
    # ---------------------------------------------------------
    def crear_interfaz_informes(self):
        panel = ttk.LabelFrame(self.frame_informes, text="Generador de Reportes", padding=10)
        panel.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(panel, text="Tipo de Informe:").pack(side="left", padx=5)
        self.combo_tipo_informe = ttk.Combobox(panel, values=["Recaudación Mensual", "Reservas por Estado"], state="readonly")
        self.combo_tipo_informe.current(0)
        self.combo_tipo_informe.pack(side="left", padx=5)
        
        ttk.Button(panel, text="Generar", command=self.generar_reporte).pack(side="left", padx=10)
        
        # Área de texto para el reporte
        self.txt_reporte = tk.Text(self.frame_informes, font=("Consolas", 9), height=20)
        self.txt_reporte.pack(fill="both", expand=True, padx=10, pady=10)

    def generar_reporte(self):
        tipo = self.combo_tipo_informe.get()
        self.txt_reporte.delete("1.0", tk.END)
        
        texto_reporte = f"--- REPORTE: {tipo.upper()} ---\n"
        texto_reporte += f"Generado el: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
        
        # Definimos las fechas de control antes de abrir el archivo para no recalcular en cada vuelta
        hoy = datetime.datetime.now()
        hace_un_mes = hoy - datetime.timedelta(days=30) #Tomamos en cuenta los 30 dias anteriores.

        recaudacion_total = 0
        conteo_estados = {"Pendiente": 0, "Abonado": 0, "Cancelado": 0}

        try:
            with open(FILE_RESERVAS, 'r') as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea: continue
                    p = linea.split(',')
                    
                    # --- ZONA DE DATOS ---
                    fecha_str = p[8] 
                    
                    try:
                        # Convertimos el texto del archivo a un objeto fecha real
                        fecha_registro = datetime.strptime(fecha_str, "%d/%m/%Y")
                    except ValueError:
                        # Si la fecha está mal escrita o el formato no coincide, saltamos la línea
                        continue

                    # --- ZONA DE FILTRO ---
                    if hace_un_mes <= fecha_registro <= hoy:
                        
                        # Si pasa el filtro, recién ahí procesamos el dinero
                        monto = float(p[7]) # Total a pagar
                        estado = p[10]      # Estado
                        
                        if estado in conteo_estados:
                            conteo_estados[estado] += 1
                        
                        if estado != "Cancelado":
                            recaudacion_total += monto

                if tipo == "Recaudación Mensual (Tomando los 30 dias anteriores)":
                    # Nota: Aquí podrías filtrar por fecha si quisieras hacerlo más complejo
                    texto_reporte += f"Total Recaudado (Neto): ${recaudacion_total:,.2f}\n"
                    texto_reporte += "(Excluye reservas canceladas)\n"
                    
                elif tipo == "Reservas por Estado":
                    for est, cant in conteo_estados.items():
                        texto_reporte += f"{est}: {cant} reservas\n"
                
                self.txt_reporte.insert(tk.END, texto_reporte)  
        except FileNotFoundError:
            self.txt_reporte.insert(tk.END, "No se encontró el archivo de reservas.")

if __name__ == "__main__":
    app = AppLagosPark()
    app.mainloop()
