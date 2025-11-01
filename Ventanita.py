import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Para el fondo con textura
from Cliente import *
from tkinter import filedialog
from Conexion import *

root = tk.Tk()
root.withdraw()

class FormularioCliente:
    global texBoxId, texBoxNombre, texBoxApellido, combo, groupBox, tree
    texBoxId = texBoxNombre = texBoxApellido = combo = groupBox = tree = None

def formulario():
    global texBoxId, texBoxNombre, texBoxApellido, combo, groupBox, tree

    try:
        base = Tk()
        base.geometry("1200x460")
        base.title("Formulario de Registro - One Piece 🏴‍☠️")

        # ==================== FONDO ====================
        try:
            fondo = Image.open("fondo_map.png")
            fondo = fondo.resize((1200, 460))
            fondo_img = ImageTk.PhotoImage(fondo)
            label_fondo = Label(base, image=fondo_img)
            label_fondo.place(x=0, y=0, relwidth=1, relheight=1)
            label_fondo.lower()
        except Exception as e:
            print("⚠️ No se pudo cargar el fondo, error:", e)
            base.configure(bg="#d2b48c")  # Color pergamino si no hay imagen

        # ==================== GRUPO DE DATOS ====================
        groupBox = LabelFrame(
            base,
            text="Datos del Tripulante ☠️",
            padx=8, pady=8,
            font=("One Piece", 18, "bold"),
            bg="#f5deb3"
        )
        groupBox.grid(row=0, column=0, padx=8, pady=8)

        Label(groupBox, text="ID:", font=("Arial", 12, "bold"), bg="#f5deb3").grid(row=0, column=0, sticky=W, pady=3)
        texBoxId = Entry(groupBox)
        texBoxId.grid(row=0, column=1, pady=3)

        Label(groupBox, text="Nombre:", font=("Arial", 12, "bold"), bg="#f5deb3").grid(row=1, column=0, sticky=W, pady=3)
        texBoxNombre = Entry(groupBox)
        texBoxNombre.grid(row=1, column=1, pady=3)

        Label(groupBox, text="Apellido:", font=("Arial", 12, "bold"), bg="#f5deb3").grid(row=2, column=0, sticky=W, pady=3)
        texBoxApellido = Entry(groupBox)
        texBoxApellido.grid(row=2, column=1, pady=3)

        Label(groupBox, text="Sexo:", font=("Arial", 12, "bold"), bg="#f5deb3").grid(row=3, column=0, sticky=W, pady=3)
        seleccionSexo = tk.StringVar()
        combo = ttk.Combobox(groupBox, values=["Masculino", "Femenino", "Otro"], textvariable=seleccionSexo)
        combo.grid(row=3, column=1, pady=3)
        seleccionSexo.set("Masculino")

        # ==================== BOTONES ====================
        estilo_boton = {
            "font": ("Arial", 10, "bold"),
            "width":15,
            "bg": "#8b4513",
            "fg": "white",
            "relief": "ridge"
        }

        Button(groupBox, text="⚓ Guardar", command=guardarRegistro, **estilo_boton).grid(row=4, column=0, pady=8)
        Button(groupBox, text="🧭 Modificar", command=modificarRegistro, **estilo_boton).grid(row=4, column=1, pady=8)
        Button(groupBox, text="💀 Eliminar", command=eliminarRegistro, **estilo_boton).grid(row=4, column=2, pady=8)
        Button(groupBox, text="Cargar Archivo", command=CargarArchivo, **estilo_boton).grid(row=4, column=3, pady=8)
        Button(groupBox, text="⬇️ Descargar Archivo", command=DescargarArchivo, **estilo_boton).grid(row=5, column=3, pady=8)



        # ==================== TABLA ====================
        groupBox2 = LabelFrame(
            base,
            text="Lista de Tripulantes ⚓",
            padx=5, pady=5,
            font=("One Piece", 14, "bold"),
            bg="#f5deb3"
        )
        groupBox2.grid(row=0, column=1, padx=10, pady=10)

        tree = ttk.Treeview(groupBox2, columns=("Id", "Nombre", "Apellido", "Sexo","Mostrar_Archivo"), show='headings', height=10)
        tree.heading("#1", text="ID")
        tree.heading("#2", text="Nombre")
        tree.heading("#3", text="Apellido")
        tree.heading("#4", text="Sexo")
        tree.heading("#5", text="Mostrar_Archivo")
        tree.column("#1", width=60)
        tree.column("#2", width=120)
        tree.column("#3", width=120)
        tree.column("#4", width=100)
        tree.column("#5", width=100)
        tree.pack(padx=10, pady=5)
        tree.bind("<Double-1>", lambda event: DescargarArchivo())


        mostrarRegistros()

        base.mainloop()

    except ValueError as error:
        print("Error al mostrar la interfaz:", error)


def guardarRegistro():
    """Guarda el registro en la base de datos junto con el archivo cargado."""
    global archivo_cargado, nombre_archivo

    try:
        nombre = texBoxNombre.get()
        apellido = texBoxApellido.get()
        sexo = combo.get()

        # Validaciones
        if nombre == "" or apellido == "":
            messagebox.showwarning("Advertencia", "Debes llenar todos los campos ⚠️")
            return

        if archivo_cargado is None:
            confirmar = messagebox.askyesno(
                "Archivo no cargado",
                "No has cargado ningún archivo. ¿Deseas guardar el registro sin archivo?"
            )
            if not confirmar:
                return

        # Conexión con la base de datos
        cone = CConexion.ConectorBaseDatos()
        cursor = cone.cursor()

        # Si hay archivo, lo guardamos; si no, se inserta NULL
        sql = "INSERT INTO usuario (nombre, apellido, sexo, archivo, Mostrar_Archivo) VALUES (%s, %s, %s, %s, %s)"
        valores = (nombre, apellido, sexo, archivo_cargado, nombre_archivo)


       
        cursor.execute(sql, valores)
        cone.commit()
        cone.close()

        # Limpiar campos y variables
        limpiarCampos()
        archivo_cargado = None
        nombre_archivo = None

        messagebox.showinfo("Éxito", "¡Nuevo tripulante agregado al barco! ☠️")
        mostrarRegistros()

    except Exception as error:
        messagebox.showerror("Error", f"Error al ingresar los datos: {error}")


def modificarRegistro():
    try:
        id_cliente = texBoxId.get()
        nombre = texBoxNombre.get()
        apellido = texBoxApellido.get()
        
        sexo = combo.get()

        cone = CConexion.ConectorBaseDatos()
        if not cone:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        cursor = cone.cursor()
        sql = "UPDATE usuario SET nombre=%s, apellido=%s, sexo=%s WHERE id=%s"
        valores = (nombre, apellido, sexo, id_cliente)
        cursor.execute(sql, valores)
        cone.commit()
        cone.close()

        messagebox.showinfo("Modificado", "¡Registro actualizado exitosamente! 🧭")
        limpiarCampos()
        mostrarRegistros()

    except Exception as error:
        print("Error al modificar el registro:", error)


def eliminarRegistro():
    try:
        id_cliente = texBoxId.get()

        if id_cliente == "":
            messagebox.showwarning("Advertencia", "Debes ingresar un ID para eliminar ⚠️")
            return

        cone = CConexion.ConectorBaseDatos()
        if not cone:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos")
            return

        cursor = cone.cursor()
        sql = "DELETE FROM usuario WHERE id=%s"
        cursor.execute(sql, (id_cliente,))
        cone.commit()
        cone.close()

        messagebox.showinfo("Eliminado", "Tripulante eliminado del barco 💀")
        limpiarCampos()
        mostrarRegistros()
    except Exception as error:
        print("Error al eliminar el registro:", error)


def mostrarRegistros():
    """Muestra los registros de la base de datos (solo nombre_archivo, no el binario)."""
    for item in tree.get_children():
        tree.delete(item)

    cone = CConexion.ConectorBaseDatos()
    if not cone:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return

    cursor = cone.cursor()
    cursor.execute("SELECT id, nombre, apellido, sexo, Mostrar_Archivo FROM usuario")
    filas = cursor.fetchall()

    for fila in filas:
        # Si no tiene archivo, mostrar texto por defecto
        Mostrar_Archivo = fila[4] if fila[4] else "(sin archivo)"
        tree.insert("", END, values=(fila[0], fila[1], fila[2], fila[3], Mostrar_Archivo))

    cone.close()


def limpiarCampos():
    texBoxId.delete(0, END)
    texBoxNombre.delete(0, END)
    texBoxApellido.delete(0, END)
    combo.set("Masculino")

# Variable global para guardar temporalmente el archivo cargado
archivo_cargado = None  # contendrá el contenido binario
nombre_archivo = None   # contendrá el nombre del archivo

def CargarArchivo():
    """Permite seleccionar un archivo CSV o Excel y lo guarda temporalmente en memoria."""
    global archivo_cargado, nombre_archivo

    try:
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo CSV o Excel",
            filetypes=(("Archivos CSV", "*.csv"), ("Archivos Excel", "*.xlsx"))
        )

        if not ruta_archivo:
            messagebox.showinfo("Aviso", "No se seleccionó ningún archivo.")
            return

        # Leer archivo como binario
        with open(ruta_archivo, "rb") as f:
            archivo_cargado = f.read()

        nombre_archivo = ruta_archivo.split("/")[-1]  # Solo el nombre
        messagebox.showinfo("Archivo cargado ✅", f"El archivo '{nombre_archivo}' se cargó correctamente.\n\nAhora puedes guardar el registro.")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al cargar el archivo: {e}")


def DescargarArchivo():
    """Permite descargar el archivo asociado a un registro seleccionado."""
    try:
        # Verificar si hay un elemento seleccionado
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Selecciona un registro en la tabla para descargar su archivo.")
            return

        # Obtener datos de la fila seleccionada
        valores = tree.item(seleccionado, "values")
        id_cliente = valores[0]
        nombre_archivo = valores[4]

        # Verificar si tiene archivo
        if nombre_archivo == "(sin archivo)" or not nombre_archivo:
            messagebox.showinfo("Aviso", "Este registro no tiene ningún archivo guardado.")
            return

        # Conexión a la base de datos
        cone = CConexion.ConectorBaseDatos()
        cursor = cone.cursor()
        cursor.execute("SELECT archivo FROM usuario WHERE id = %s", (id_cliente,))
        archivo = cursor.fetchone()

        if archivo and archivo[0]:
            # Elegir ubicación donde guardar
            ruta_guardar = filedialog.asksaveasfilename(
                title="Guardar archivo como",
                initialfile=nombre_archivo,
                filetypes=[("Todos los archivos", "*.*")]
            )

            if ruta_guardar:
                with open(ruta_guardar, "wb") as f:
                    f.write(archivo[0])
                messagebox.showinfo("Éxito", f"Archivo guardado en: {ruta_guardar}")
        else:
            messagebox.showinfo("Aviso", "No hay archivo almacenado en la base de datos para este usuario.")

        cone.close()

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al descargar el archivo: {e}")

# Ejecutar la ventana
formulario()