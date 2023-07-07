
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.dropdown import DropDown 
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder

from sqlqueries import QueriesSQLite # Importar el módulo que contiene las consultas SQL
from datetime import datetime, timedelta # Importar los módulos para trabajar con fechas
#import csv
from pathlib import Path # Importar el módulo para trabajar con rutas de archivos y directorios
import os # Importar el módulo para trabajar con el sistema operativo

from kivy.utils import get_color_from_hex
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Importar los módulos necesarios para la interfaz gráfica y el generador de reportes
# Los módulos de Kivy se importan para construir la interfaz de usuario
# Los módulos de reportlab se importan para generar el reporte en PDF


Builder.load_file('admin/admin.kv') # Carga el archivo de descripción de la interfaz gráfica en formato .kv

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):#La clase "SelectableRecycleBoxLayout" es una subclase de "FocusBehavior", "LayoutSelectionBehavior" y "RecycleBoxLayout".
    touch_deselect_last = BooleanProperty(True) 
# Define un diseño de caja para un RecycleView con capacidades de selección de elementos.
# El atributo "touch_deselect_last" es una propiedad booleana personalizada que determina si se debe deseleccionar el último elemento tocado.

class SelectableProductoLabel(RecycleDataViewBehavior, BoxLayout): # La clase "SelectableProductoLabel" es una subclase de "RecycleDataViewBehavior" y "BoxLayout".
# Define un widget de etiqueta que se puede seleccionar en un RecycleView.
	index = None # El atributo "index" se utiliza para almacenar el índice del elemento en el RecycleView.
	selected = BooleanProperty(False) # El atributo "selected" indica si el elemento está seleccionado o no.
	selectable = BooleanProperty(True)  # El atributo "selectable" indica si el elemento se puede seleccionar o no.

	def refresh_view_attrs(self, rv, index, data):# Este método se utiliza para actualizar los atributos de vista del widget cuando se recicla en el RecycleView.
    # Se llama automáticamente por el RecycleView al mostrar el widget en una nueva posición.
		self.index = index  # Almacena el índice del elemento en el atributo "index" del widget actual.
		self.ids['_hashtag'].text = str(1+index) # Actualiza el texto del widget con el número de índice.
		self.ids['_codigo'].text = data['codigo'] # Actualiza el texto del widget con el valor de 'codigo' del diccionario 'data'.
		self.ids['_articulo'].text = data['nombre'].capitalize() # Actualiza el texto del widget con el valor capitalizado de 'nombre' del diccionario 'data'.
		self.ids['_cantidad'].text = str(data['cantidad']) # Actualiza el texto del widget con el valor de 'cantidad' del diccionario 'data'.
		self.ids['_precio'].text = str("{:.2f}".format(data['precio'])) # Actualiza el texto del widget con el valor formateado de 'precio' del diccionario 'data'.
		return super(SelectableProductoLabel, self).refresh_view_attrs(
            rv, index, data)  # Llama al método "refresh_view_attrs" de la superclase para asegurarse de que los atributos de vista se actualicen correctamente.

	def on_touch_down(self, touch): # Llama al método "on_touch_down" de la superclase para manejar el evento de toque.
		if super(SelectableProductoLabel, self).on_touch_down(touch):
			return True
	# Si la superclase devuelve True, significa que se ha realizado alguna acción y se debe retornar True.
		if self.collide_point(*touch.pos) and self.selectable: # Verifica si el punto de colisión del toque está dentro del widget actual y si el widget es seleccionable.
			return self.parent.select_with_touch(self.index, touch) # Llama al método "select_with_touch" del padre (RecycleView) para manejar la selección del widget con el toque.

	def apply_selection(self, rv, index, is_selected):# Actualiza el estado de selección del widget según el valor de "is_selected".
		self.selected = is_selected
    # El atributo "selected" indica si el widget está seleccionado o no.
		if is_selected:
			rv.data[index]['seleccionado']=True # Si el widget está seleccionado, actualiza el valor de "seleccionado" en el diccionario correspondiente al índice "index" en los datos del RecycleView.
		else:
			rv.data[index]['seleccionado']=False # Si el widget no está seleccionado, actualiza el valor de "seleccionado" en el diccionario correspondiente al índice "index" en los datos del RecycleView.

class SelectableUsuarioLabel(RecycleDataViewBehavior, BoxLayout): # La clase "SelectableUsuarioLabel" es una subclase de "RecycleDataViewBehavior" y "BoxLayout".
	index = None  # El atributo "index" se utiliza para almacenar el índice del elemento en el RecycleView.
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index# Almacena el índice del elemento en el atributo "index" del widget actual.
		self.ids['_hashtag'].text = str(1+index) # Actualiza el texto del widget con el número de índice.
		self.ids['_nombre'].text = data['nombre'].title()
		self.ids['_username'].text = data['username']
		self.ids['_tipo'].text = str(data['tipo'])
		return super(SelectableUsuarioLabel, self).refresh_view_attrs(
            rv, index, data) # Llama al método "refresh_view_attrs" de la superclase para asegurarse de que los atributos de vista se actualicen correctamente.

	def on_touch_down(self, touch):# Llama al método "on_touch_down" de la superclase para manejar el evento de toque.
		if super(SelectableUsuarioLabel, self).on_touch_down(touch):
			return True
    	# Si la superclase devuelve True, significa que se ha realizado alguna acción y se debe retornar True.
		if self.collide_point(*touch.pos) and self.selectable:  # Verifica si el punto de colisión del toque está dentro del widget actual y si el widget es seleccionable.
			return self.parent.select_with_touch(self.index, touch) # Llama al método "select_with_touch" del padre (RecycleView) para manejar la selección del widget con el toque.

	def apply_selection(self, rv, index, is_selected):# Actualiza el estado de selección del widget según el valor de "is_selected".
		self.selected = is_selected
    	# El atributo "selected" indica si el widget está seleccionado o no.
		if is_selected:
			rv.data[index]['seleccionado']=True  # Si el widget está seleccionado, actualiza el valor de "seleccionado" en el diccionario correspondiente al índice "index" en los datos del RecycleView.
		else:
			rv.data[index]['seleccionado']=False


class ItemVentaLabel(RecycleDataViewBehavior, BoxLayout):# La clase "ItemVentaLabel" es una subclase de "RecycleDataViewBehavior" y "BoxLayout".
	index = None
	# Define un widget de etiqueta para un elemento de venta en un RecycleView.
    # El atributo "index" se utiliza para almacenar el índice del elemento en el RecycleView.

	def refresh_view_attrs(self, rv, index, data):
		self.index = index # Almacena el índice del elemento en el atributo "index" del widget actual.
		self.ids['_hashtag'].text = str(1+index) # Actualiza el texto del widget con el número de índice.
		self.ids['_codigo'].text = data['codigo'] # Actualiza el texto del widget con el valor de 'codigo' del diccionario 'data'.
		self.ids['_articulo'].text = data['producto'].capitalize()
		self.ids['_cantidad'].text = str(data['cantidad'])
		self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))+" /artículo"
		self.ids['_total'].text= str("{:.2f}".format(data['total']))
		return super(ItemVentaLabel, self).refresh_view_attrs(
            rv, index, data)# Llama al método "refresh_view_attrs" de la superclase para asegurarse de que los atributos de vista se actualicen correctamente.


class SelectableVentaLabel(RecycleDataViewBehavior, BoxLayout): # La clase "SelectableVentaLabel" es una subclase de "RecycleDataViewBehavior" y "BoxLayout".
	# Define un widget de etiqueta de venta que se puede seleccionar en un RecycleView.
	index = None
	selected = BooleanProperty(False)
	selectable = BooleanProperty(True)

	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.ids['_hashtag'].text = str(1+index)
		self.ids['_username'].text = data['username']
		self.ids['_cantidad'].text = str(data['productos'])
		self.ids['_total'].text = '$ '+str("{:.2f}".format(data['total']))
		self.ids['_time'].text = str(data['fecha'].strftime("%H:%M:%S"))
		self.ids['_date'].text = str(data['fecha'].strftime("%d/%m/%Y"))
		return super(SelectableVentaLabel, self).refresh_view_attrs(
            rv, index, data)

	def on_touch_down(self, touch):# Llama al método "on_touch_down" de la superclase para manejar el evento de toque.
		if super(SelectableVentaLabel, self).on_touch_down(touch):
			return True
		if self.collide_point(*touch.pos) and self.selectable:
			return self.parent.select_with_touch(self.index, touch)

	def apply_selection(self, rv, index, is_selected):# Actualiza el estado de selección del widget según el valor de "is_selected".
		self.selected = is_selected
		if is_selected:
			rv.data[index]['seleccionado']=True
		else:
			rv.data[index]['seleccionado']=False


class AdminRV(RecycleView): # La clase "AdminRV" es una subclase de "RecycleView".
 # Define un RecycleView personalizado para la administración.
    def __init__(self, **kwargs):# El método "__init__" se ejecuta al crear una instancia de la clase y se utiliza para inicializar el objeto.
        super(AdminRV, self).__init__(**kwargs)   # Llama al método "__init__" de la superclase para asegurarse de que la inicialización de la superclase se realice correctamente. 
        self.data=[]# Inicializa el atributo "data" como una lista vacía para almacenar los datos del RecycleView.

    def agregar_datos(self,datos):
        for dato in datos:
            dato['seleccionado']=False# Agrega la clave 'seleccionado' al diccionario 'dato' y la establece como False.
            self.data.append(dato) # Agrega el diccionario 'dato' a la lista 'data' del RecycleView.
        self.refresh_from_data() # Actualiza la vista del RecycleView para reflejar los nuevos datos agregados.

    def dato_seleccionado(self): #nos trae el indice
        indice=-1    # Establece el valor inicial del índice como -1.
        for i in range(len(self.data)):
            if self.data[i]['seleccionado']:# Verifica si el elemento en el índice 'i' tiene la clave 'seleccionado' establecida como True.
                indice=i# Asigna el valor del índice 'i' a la variable 'indice'.
            # Esto captura el índice del primer elemento seleccionado encontrado en los datos.
                break # Sale del bucle una vez que se encuentra un elemento seleccionado.
        return indice # Devuelve el índice del elemento seleccionado, o -1 si no se encuentra ninguno.

class ProductoPopup(Popup): # La clase "ProductoPopup" es una subclase de "Popup".
        # Define un popup personalizado para la selección de productos
	def __init__(self, agregar_callback, **kwargs):
		super(ProductoPopup, self).__init__(**kwargs)
		self.agregar_callback=agregar_callback# Asigna el argumento "agregar_callback" al atributo "agregar_callback" del objeto.
		# Esto permite pasar una función de callback para agregar un producto seleccionado desde el popup.

	def abrir(self, agregar, producto=None):
		if agregar:
			self.ids.producto_info_1.text='Agregar producto nuevo'
			self.ids.producto_codigo.disabled=False
			 # Si se va a agregar un producto nuevo, se actualiza el texto del widget "producto_info_1"
        	# y se habilita la edición del widget "producto_codigo".
		else:
			self.ids.producto_info_1.text='Modificar producto'
			self.ids.producto_codigo.text=producto['codigo']
			self.ids.producto_codigo.disabled=True
			self.ids.producto_nombre.text=producto['nombre']
			self.ids.producto_cantidad.text=str(producto['cantidad'])
			self.ids.producto_precio.text=str(producto['precio'])
			# Si se va a modificar un producto existente, se actualiza el texto del widget "producto_info_1"
	        # y se establecen los valores de los widgets "producto_codigo", "producto_nombre", "producto_cantidad" y "producto_precio"
	        # con los valores correspondientes del diccionario "producto" proporcionado.
		self.open()
		   # Abre el popup para mostrarlo en la interfaz.

	def verificar(self, producto_codigo, producto_nombre, producto_cantidad, producto_precio):
		alert1='Falta: '  # Variable para almacenar los campos faltantes en la validación
		alert2='' # Variable para almacenar los errores de validación adicionales
		validado={} # Diccionario para almacenar los datos validados
		if not producto_codigo:
			alert1+='Codigo. ' # Si el campo "producto_codigo" está vacío, se agrega "Código" a la variable "alert1"
			validado['codigo']=False # Se establece el valor de "validado['codigo']" como False para indicar que no está validado
		else:
			try:
				numeric=int(producto_codigo) # Se intenta convertir "producto_codigo" a entero para validar que sea un número
				validado['codigo']=producto_codigo # Si se puede convertir a entero, se considera válido y se almacena en "validado['codigo']"
			except:
				alert2+='Código no válido. ' # Si la conversión a entero falla, se agrega "Código no válido" a la variable "alert2"
				validado['codigo']=False # Se establece el valor de "validado['codigo']" como False para indicar que no está validado

		if not producto_nombre:
			alert1+='Nombre. ' # Si el campo "producto_nombre" está vacío, se agrega "Nombre" a la variable "alert1"
			validado['nombre']=False # Se establece el valor de "validado['nombre']" como False para indicar que no está validado
		else:
			validado['nombre']=producto_nombre.lower() # Si el campo "producto_nombre" tiene un valor, se convierte a minúsculas y se almacena en "validado['nombre']"

		if not producto_precio:
			alert1+='Precio. ' # Si el campo "producto_precio" está vacío, se agrega "Precio" a la variable "alert1"
			validado['precio']=False # Se establece el valor de "validado['precio']" como False para indicar que no está validado
		else:
			try:
				numeric=float(producto_precio)  # Se intenta convertir "producto_precio" a float para validar que sea un número
				validado['precio']=producto_precio  # Si se puede convertir a float, se considera válido y se almacena en "validado['precio']"
			except:
				alert2+='Precio no válido. ' # Si la conversión a float falla, se agrega "Precio no válido" a la variable "alert2"
				validado['precio']=False # Se establece el valor de "validado['precio']" como False para indicar que no está validado
			
		if not producto_cantidad:
			alert1+='Cantidad. ' # Si el campo "producto_cantidad" está vacío, se agrega "Cantidad" a la variable "alert1"
			validado['cantidad']=False # Se establece el valor de "validado['cantidad']" como False para indicar que no está validado
		else:
			try:
				numeric=int(producto_cantidad) # Se intenta convertir "producto_cantidad" a entero para validar que sea un número
				validado['cantidad']=producto_cantidad # Si se puede convertir a entero, se considera válido y se almacena en "validado['cantidad']"
			except:
				alert2+='Cantidad no válida. ' # Si la conversión a entero falla, se agrega "Cantidad no válida" a la variable "alert2"
				validado['cantidad']=False # Se establece el valor de "validado['cantidad']" como False para indicar que no está validado

		valores=list(validado.values()) # Se obtienen los valores de "validado" como una lista

		if False in valores:
			self.ids.no_valid_notif.text=alert1+alert2 # Si hay algún valor False en la lista "valores", se muestra el mensaje de campos faltantes y errores de validación
		else:
			self.ids.no_valid_notif.text='Validado' # Si todos los campos están validados, se muestra el mensaje de validación exitosa
			validado['cantidad']=int(validado['cantidad']) # Se convierte "validado['cantidad']" a entero
			validado['precio']=float(validado['precio']) # Se convierte "validado['precio']" a float
			self.agregar_callback(True, validado) # Se llama a la función de callback "agregar_callback" pasando los datos validados como argumento
			self.dismiss() # Se cierra el popup


class VistaProductos(Screen):# La clase "VistaProductos" es una subclase de "Screen".
        # Define una pantalla para mostrar la vista de productos.
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_productos, 1)
		# Se programa una llamada a la función "cargar_productos" después de 1 segundo utilizando el reloj de Kivy.
        # Esto se hace para cargar los productos una vez que la pantalla esté completamente cargada y visible.

	def cargar_productos(self, *args):
		_productos=[] # Lista para almacenar los productos
		connection=QueriesSQLite.create_connection("pdvDB.sqlite") # Crea una conexión a la base de datos "pdvDB.sqlite" utilizando la función "create_connection" de "QueriesSQLite"
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos") # Ejecuta una consulta SELECT a la tabla "productos" de la base de datos utilizando la función "execute_read_query" de "QueriesSQLite"
    # El resultado se guarda en la variable "inventario_sql"
		if inventario_sql: # Verifica si se obtuvo algún resultado de la consulta 
			for producto in inventario_sql: # Itera sobre cada producto obtenido de la consulta
				_productos.append({'codigo': producto[0], 'nombre': producto[1], 'precio': producto[2], 'cantidad': producto[3]}) # Agrega un diccionario con los datos del producto a la lista "_productos"
            # Los datos del producto se obtienen de las columnas de la tabla

		self.ids.rv_productos.agregar_datos(_productos)# Llama al método "agregar_datos" del widget "rv_productos" (posiblemente un RecycleView) para agregar los datos de los productos.

	def agregar_producto(self, agregar=False, validado=None):
		if agregar:
			producto_tuple=tuple(validado.values()) # Convierte los valores del diccionario "validado" en una tupla utilizando la función "values" del diccionario
			connection=QueriesSQLite.create_connection("pdvDB.sqlite")
			crear_producto="""
			INSERT INTO
				productos (codigo, nombre, precio, cantidad)
			VALUES
				(?, ?, ?, ?);
			"""
			QueriesSQLite.execute_query(connection, crear_producto, producto_tuple)# Ejecuta la consulta SQL utilizando la función "execute_query" de "QueriesSQLite"
        # Se pasa la conexión, la sentencia SQL y los valores del producto como argumentos
			self.ids.rv_productos.data.append(validado)# Agrega el diccionario "validado" a la lista de datos del widget "rv_productos" (posiblemente un RecycleView)
			self.ids.rv_productos.refresh_from_data() # Actualiza la vista del widget "rv_productos" para reflejar los nuevos datos agregados
		else:
			popup=ProductoPopup(self.agregar_producto)# Crea una instancia de la clase "ProductoPopup" pasando la función "agregar_producto" como argumento para el callback
			popup.abrir(True)# Abre el popup para agregar un nuevo producto

	def modificar_producto(self, modificar=False, validado=None):
		indice=self.ids.rv_productos.dato_seleccionado() # Obtiene el índice del producto seleccionado llamando al método "dato_seleccionado" del widget "rv_productos" (posiblemente un RecycleView)
		if modificar:
			producto_tuple=(validado['nombre'], validado['precio'], validado['cantidad'], validado['codigo'])# Crea una tupla con los valores del producto validado
			connection=QueriesSQLite.create_connection("pdvDB.sqlite")
			actualizar="""
			UPDATE
				productos
			SET
				nombre=?, precio=?, cantidad=?
			WHERE
				codigo=?
			"""
			QueriesSQLite.execute_query(connection, actualizar, producto_tuple)# Ejecuta la consulta SQL utilizando la función "execute_query" de "QueriesSQLite"
        # Se pasa la conexión, la sentencia SQL y los valores del producto como argumentos
			self.ids.rv_productos.data[indice]['nombre']=validado['nombre']
			self.ids.rv_productos.data[indice]['cantidad']=validado['cantidad']
			self.ids.rv_productos.data[indice]['precio']=validado['precio'] # Actualiza los valores del producto en la lista de datos del widget "rv_productos" (posiblemente un RecycleView)
			self.ids.rv_productos.refresh_from_data()# Actualiza la vista del widget "rv_productos" para reflejar los cambios realizados
		else:
			if indice>=0:
				producto=self.ids.rv_productos.data[indice] # Obtiene el producto seleccionado de la lista de datos del widget "rv_productos"
				popup=ProductoPopup(self.modificar_producto)# Crea una instancia de la clase "ProductoPopup" pasando la función "modificar_producto" como argumento para el callback
				popup.abrir(False, producto)# Abre el popup para modificar el producto seleccionado

	def eliminar_producto(self):
		indice=self.ids.rv_productos.dato_seleccionado() # Obtiene el índice del producto seleccionado llamando al método "dato_seleccionado" del widget "rv_productos" (posiblemente un RecycleView)
		if indice>=0:
			producto_tuple=(self.ids.rv_productos.data[indice]['codigo'],)# Crea una tupla con el código del producto a eliminar
			connection=QueriesSQLite.create_connection("pdvDB.sqlite")
			borrar= """DELETE from productos WHERE codigo =? """
			QueriesSQLite.execute_query(connection, borrar, producto_tuple) #Ejecuta la consulta SQL utilizando la función "execute_query" de "QueriesSQLite"
        	# Se pasa la conexión, la sentencia SQL y los valores del producto como argumentos
			self.ids.rv_productos.data.pop(indice)# Elimina el producto de la lista de datos del widget "rv_productos" (posiblemente un RecycleView)
			self.ids.rv_productos.refresh_from_data()# Actualiza la vista del widget "rv_productos" para reflejar los cambios realizados

	def actualizar_productos(self, producto_actualizado):
		for producto_nuevo in producto_actualizado:
			for producto_viejo in self.ids.rv_productos.data:
				if producto_nuevo['codigo']==producto_viejo['codigo']:
					producto_viejo['cantidad']=producto_nuevo['cantidad']
					# Actualiza la cantidad del producto viejo con la cantidad del producto nuevo

					break# Sale del bucle interno una vez que se encuentra el producto correspondiente
		self.ids.rv_productos.refresh_from_data()# Actualiza la vista del widget "rv_productos" para reflejar los cambios realizados en las cantidades de los productos


class UsuarioPopup(Popup):# La clase "UsuarioPopup" es una subclase de "Popup".
        # Define un popup personalizado para la gestión de usuarios.
	def __init__(self, _agregar_callback, **kwargs):
		super(UsuarioPopup, self).__init__(**kwargs)
		self.agregar_usuario=_agregar_callback
		# Asigna el argumento "_agregar_callback" al atributo "agregar_usuario" del objeto.
        # Esto permite pasar una función de callback para agregar un nuevo usuario desde el popup.

	def abrir(self, agregar, usuario=None):
		if agregar:
			self.ids.usuario_info_1.text='Agregar Usuario nuevo'
			self.ids.usuario_username.disabled=False
			# Si se va a agregar un usuario nuevo, se actualiza el texto del widget "usuario_info_1"
        	# y se habilita la edición del widget "usuario_username".
		else:
			self.ids.usuario_info_1.text='Modificar Usuario'
			self.ids.usuario_username.text=usuario['username']
			self.ids.usuario_username.disabled=True
			self.ids.usuario_nombre.text=usuario['nombre']
			self.ids.usuario_password.text=usuario['password']
			# Si se va a modificar un usuario existente, se actualiza el texto del widget "usuario_info_1"
	        # y se establecen los valores de los widgets "usuario_username", "usuario_nombre" y "usuario_password"
	        # con los valores correspondientes del diccionario "usuario" proporcionado.

			if usuario['tipo']=='admin':
				self.ids.admin_tipo.state='down'
			else:
				self.ids.trabajador_tipo.state='down'
			# Se establece el estado del widget "admin_tipo" o "trabajador_tipo" según el tipo de usuario en el diccionario "usuario".
		self.open()# Abre el popup para mostrarlo en la interfaz.

	def verificar(self, usuario_username, usuario_nombre, usuario_password, admin_tipo, trabajador_tipo):
		alert1 = 'Falta: ' # Variable para almacenar los campos faltantes en la validación
		validado = {} # Diccionario para almacenar los datos validados
		if not usuario_username:
			alert1+='Username. ' # Si el campo "usuario_username" está vacío, se agrega "Username" a la variable "alert1"
			validado['username']=False
		else:
			validado['username']=usuario_username # Si el campo "usuario_username" tiene un valor, se almacena en "validado['username']"

		if not usuario_nombre:
			alert1+='Nombre.  '# Si el campo "usuario_nombre" está vacío, se agrega "Nombre" a la variable "alert1"
			validado['nombre']=False
		else:
			validado['nombre']=usuario_nombre.lower() # Si el campo "usuario_nombre" tiene un valor, se convierte a minúsculas y se almacena en "validado['nombre']"

		if not usuario_password:
			alert1+='Password. ' # Si el campo "usuario_password" está vacío, se agrega "Password" a la variable "alert1"
			validado['password']=False
		else:
			validado['password']=usuario_password # Si el campo "usuario_password" tiene un valor, se almacena en "validado['password']"

		if admin_tipo=='normal' and trabajador_tipo=='normal':
			alert1+='Tipo. ' # Si no se selecciona ningún tipo de usuario, se agrega "Tipo" a la variable "alert1"
			validado['tipo']=False
		else:
			if admin_tipo=='down':
				validado['tipo']='admin'# Si se selecciona el tipo "admin", se asigna 'admin' a "validado['tipo']"
			else:
				validado['tipo']='trabajador'

		valores = list(validado.values()) # Se obtienen los valores de "validado" como una lista

		if False in valores:
			self.ids.no_valid_notif.text=alert1  # Si hay algún valor False en la lista "valores", se muestra el mensaje de campos faltantes en "no_valid_notif"
		else:
			self.ids.no_valid_notif.text='' # Si todos los campos están validados, se borra el mensaje de "no_valid_notif"
			self.agregar_usuario(True,validado)# Llama a la función de callback "agregar_usuario" pasando los datos validados como argumento
        	# El primer argumento "True" indica que se está agregando un nuevo usuario
			self.dismiss()# Cierra el popup


class VistaUsuarios(Screen): # La clase "VistaUsuarios" es una subclase de "Screen".
    # Define una pantalla para mostrar la vista de usuarios.
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Clock.schedule_once(self.cargar_usuarios, 1)
		# Se programa una llamada a la función "cargar_usuarios" después de 1 segundo utilizando el reloj de Kivy.
        # Esto se hace para cargar los usuarios una vez que la pantalla esté completamente cargada y visible.

	def cargar_usuarios(self, *args):
		_usuarios=[] # Lista para almacenar los usuarios
		connection=QueriesSQLite.create_connection("pdvDB.sqlite") 
		usuarios_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
		# Ejecuta una consulta SELECT a la tabla "usuarios" de la base de datos utilizando la función "execute_read_query" de "QueriesSQLite"
    	# El resultado se guarda en la variable "usuarios_sql"
		if usuarios_sql: # Verifica si se obtuvo algún resultado de la consulta
			for usuario in usuarios_sql:
				_usuarios.append({'nombre': usuario[1], 'username': usuario[0], 'password': usuario[2], 'tipo': usuario[3]})
				# Agrega un diccionario con los datos del usuario a la lista "_usuarios"
            	# Los datos del usuario se obtienen de las columnas de la tabla
		self.ids.rv_usuarios.agregar_datos(_usuarios) # Llama al método "agregar_datos" del widget "rv_usuarios" (posiblemente un RecycleView) para agregar los datos de los usuarios.

	def agregar_usuario(self, agregar=False, validado=None):
		if agregar:
			usuario_tuple=tuple(validado.values()) # Convierte los valores del diccionario "validado" en una tupla utilizando la función "values" del diccionario
			connection=QueriesSQLite.create_connection("pdvDB.sqlite")
			crear_usuario = """
			INSERT INTO
				usuarios (username, nombre, password, tipo)
			VALUES
				(?,?,?,?);
			"""
			QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)
			# Ejecuta la consulta SQL utilizando la función "execute_query" de "QueriesSQLite"
        # Se pasa la conexión, la sentencia SQL y los valores del usuario como argumentos
			self.ids.rv_usuarios.data.append(validado)# Agrega el diccionario "validado" a la lista de datos del widget "rv_usuarios" (posiblemente un RecycleView)
			self.ids.rv_usuarios.refresh_from_data()# Actualiza la vista del widget "rv_usuarios" para reflejar los nuevos datos agregados
		else:
			popup=UsuarioPopup(self.agregar_usuario)# Crea una instancia de la clase "UsuarioPopup" pasando la función "agregar_usuario" como argumento para el callback
			popup.abrir(True)

	def modificar_usuario(self, modificar=False, validado=None):
		indice = self.ids.rv_usuarios.dato_seleccionado() # Obtiene el índice del usuario seleccionado llamando al método "dato_seleccionado" del widget "rv_usuarios" (posiblemente un RecycleView)
		if modificar:
			usuario_tuple=(validado['nombre'],validado['password'],validado['tipo'],validado['username'])# Crea una tupla con los valores del usuario validad
			connection=QueriesSQLite.create_connection("pdvDB.sqlite")
			actualizar = """
			UPDATE
			  usuarios
			SET
			  nombre=?, password=?, tipo = ?
			WHERE
			  username = ?
			"""
			QueriesSQLite.execute_query(connection, actualizar, usuario_tuple)
			self.ids.rv_usuarios.data[indice]['nombre']=validado['nombre']
			self.ids.rv_usuarios.data[indice]['tipo']=validado['tipo']
			self.ids.rv_usuarios.data[indice]['password']=validado['password']
			self.ids.rv_usuarios.refresh_from_data()
		else:
			if indice>=0:
				usuario = self.ids.rv_usuarios.data[indice]
				popup = UsuarioPopup(self.modificar_usuario)
				popup.abrir(False,usuario)
		

	def eliminar_usuario(self):
		indice = self.ids.rv_usuarios.dato_seleccionado() # Obtiene el índice del usuario seleccionado llamando al método "dato_seleccionado" del widget "rv_usuarios" (posiblemente un RecycleView)
		if indice>=0:
			usuario_tuple=(self.ids.rv_usuarios.data[indice]['username'],)# Crea una tupla con el nombre de usuario del usuario a eliminar
			connection=QueriesSQLite.create_connection("pdvDB.sqlite")
			borrar = """DELETE from usuarios where username = ?"""
			QueriesSQLite.execute_query(connection, borrar, usuario_tuple)
			self.ids.rv_usuarios.data.pop(indice)# Elimina el usuario de la lista de datos del widget "rv_usuarios" (posiblemente un RecycleView)
			self.ids.rv_usuarios.refresh_from_data()



class InfoVentaPopup(Popup):
	connection=QueriesSQLite.create_connection("pdvDB.sqlite") #conexion
	select_item_query=" SELECT nombre FROM productos WHERE codigo = ?  " #el codigo sql
	def __init__(self, venta, **kwargs):
		super(InfoVentaPopup, self).__init__(**kwargs)	
		self.venta=[{"codigo": producto[3], "producto": QueriesSQLite.execute_read_query(self.connection, self.select_item_query, (producto[3],))[0][0], "cantidad": producto[4], "precio": producto[2], "total": producto[4]*producto[2]} for producto in venta]
		 # Crea una lista de diccionarios para almacenar los datos de la venta.
    # Cada diccionario representa un producto de la venta e incluye el código del producto, el nombre del producto obtenido de la base de datos,
    # la cantidad, el precio unitario y el total (cantidad * precio) del producto.
    # Se utiliza una comprensión de lista para iterar sobre cada producto en la lista "venta" y crear el diccionario correspondiente.

	def mostrar(self): #mostrar la info
		self.open() #abrimos
		total_items=0
		total_dinero=0.0
		# Variables para almacenar el total de items y el total de dinero de la venta
		for articulo in self.venta:
			total_items+=articulo['cantidad']
			total_dinero+=articulo['total']
			# Itera sobre cada artículo de la venta y actualiza los totales sumando la cantidad y el total del artículo
		self.ids.total_items.text=str(total_items) # Actualiza el texto del widget "total_items" con el total de items de la venta
		self.ids.total_dinero.text="G "+str("{:.2f}".format(total_dinero))# Actualiza el texto del widget "total_dinero" con el total de dinero de la venta formateado con dos decimales y precedido de "G"
		self.ids.info_rv.agregar_datos(self.venta)  # Llama al método "agregar_datos" del widget "info_rv" (posiblemente un RecycleView) para agregar los datos de la venta y mostrarlos en la interfaz

# nueva clase creada y tabien en kv
class VistaVentas(Screen):
	productos_actuales=[]# Lista para almacenar los productos actuales
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# La clase "VistaVentas" es una subclase de "Screen".
        # Define una pantalla para mostrar la vista de ventas.


	def mas_info(self):
		indice=self.ids.ventas_rv.dato_seleccionado()  # Obtiene el índice de la venta seleccionada llamando al método "dato_seleccionado" del widget "ventas_rv" (posiblemente un RecycleView)
		if indice>=0: # Verifica si se seleccionó una venta (índice válido)
			venta=self.productos_actuales[indice] # Obtiene la venta correspondiente al índice de la lista "productos_actuales"
			p=InfoVentaPopup(venta) # Crea una instancia de la clase "InfoVentaPopup" pasando la venta como argumento
			p.mostrar() # Llama al método "mostrar" de la instancia "p" para mostrar la información de la venta en un popup


	#def build(self):
		#layout = BoxLayout(orientation='vertical')
			#label = Label(text='¡Hola, mundo!')
		   # button = Button(text='Generar PDF', on_press=self.pdf)
		  #  layout.add_widget(label)
		 #   layout.add_widget(button)
		#return layout



	def pdf(self):
	    connection = QueriesSQLite.create_connection("pdvDB.sqlite")
	    select_item_query = "SELECT nombre FROM productos WHERE codigo=?"

	    if self.ids.ventas_rv.data: # Verifica si hay datos en el widget "ventas_rv" (posiblemente un RecycleView)
	        path = Path(__file__).absolute().parent   #Obtiene la ruta del archivo actual y se asigna a la variable "path"
	        pdf_path = path / "ventas_pdf"
	        pdf_path.mkdir(exist_ok=True)
	        # Crea un directorio "ventas_pdf" dentro del directorio actual (donde se encuentra el archivo) utilizando la ruta "path"
   			 # Si el directorio ya existe, se omite la creación ("exist_ok=True")
	        pdf_file = pdf_path / f"{self.ids.date_id.text}.pdf"
	        # Crea una ruta al archivo PDF utilizando el directorio "pdf_path" y el texto del widget "date_id" como nombre de archivo
    		# El texto del widget "date_id" se utiliza como parte del nombre del archivo PDF

	        productos_pdf = []# Lista para almacenar los productos en el formato adecuado para generar el PDF
	        total = 0 # Variable para almacenar el total de la venta

	        for venta in self.productos_actuales:  # Itera sobre cada venta en la lista "productos_actuales"
	            for item in venta: # Itera sobre cada artículo (item) en la venta
	                item_found = next((producto for producto in productos_pdf if producto["codigo"] == item[3]), None)
	                # Busca si el artículo ya está en la lista "productos_pdf" utilizando su código como criterio de búsqueda
        			# Si encuentra el artículo, asigna el diccionario correspondiente a "item_found"; si no lo encuentra, asigna None
	                total += item[2] * item[4] # Calcula el total sumando el precio unitario (item[2]) multiplicado por la cantidad (item[4])

	                if item_found: # Si el artículo ya está en la lista "productos_pdf"
	                    item_found["cantidad"] += item[4] # Aumenta la cantidad del artículo en "item_found"
	                    item_found["precio_total"] = item_found["precio"] * item_found["cantidad"] # Calcula el nuevo precio total del artículo multiplicando el precio unitario por la cantidad
	                else: # Si el artículo no está en la lista "productos_pdf"
	                    nombre = QueriesSQLite.execute_read_query(connection, select_item_query, (item[3],))[0][0] # Obtiene el nombre del artículo utilizando una consulta SQL a la base de datos
	                    productos_pdf.append({
	                        "nombre": nombre,
	                        "codigo": item[3],
	                        "cantidad": item[4],
	                        "precio": item[2],
	                        "precio_total": item[2] * item[4],
	                    }) # Agrega un diccionario con los datos del artículo a la lista "productos_pdf"

	        # crea el documento pdf
	        doc = SimpleDocTemplate(str(pdf_file), pagesize=letter)
	        elements = []

	        # el estilo 
	        styles = getSampleStyleSheet()

	        # agrega la tabla con productos
	        data = [[
	            "Nombre",
	            "Código",
	            "Cantidad",
	            "Precio",
	            "Precio Total",
	        ]]

	        for producto in productos_pdf:
	            data.append([
	                producto["nombre"],
	                producto["codigo"],
	                producto["cantidad"],
	                producto["precio"],
	                producto["precio_total"],
	            ])

	        table = Table(data)
	        table.setStyle(TableStyle([
	            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
	            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
	            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
	            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
	            ("FONTSIZE", (0, 0), (-1, 0), 12),
	            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
	            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
	            ("GRID", (0, 0), (-1, -1), 1, colors.black)
	        ]))

	        elements.append(table)

	        # agrega el total
	        total_text = f"Total: {total}"
	        total_paragraph = Paragraph(total_text, styles["BodyText"])
	        elements.append(total_paragraph)

	        # genera el pdf
	        doc.build(elements)

	        self.ids.notificacion.text = "PDF creado y guardado"
	    else:
	        self.ids.notificacion.text = "No hay datos que guardar"





	def cargar_venta(self, choice='Default'):
		connection = QueriesSQLite.create_connection("pdvDB.sqlite") #conexion
		valid_input=True #
		final_sum=0
		f_inicio=datetime.strptime('01/01/00', '%d/%m/%y')
		f_fin=datetime.strptime('31/12/2099', '%d/%m/%Y')

		_ventas=[] # Lista para almacenar las ventas
		_total_productos=[]# Lista para almacenar los productos de las ventas

		select_ventas_query = " SELECT * FROM ventas WHERE fecha BETWEEN ? AND ? " #traer las tablas que creamos a traves de fecha
		selec_productos_query = " SELECT * FROM ventas_detalle WHERE id_venta=? " #traer de otra tabla en forma especifica
		# Consultas SQL para obtener las ventas y los productos de las ventas

		self.ids.ventas_rv.data=[] # Borra los datos actuales del widget "ventas_rv" (posiblemente un RecycleView)
		if choice=='Default': #lo de hoy
			f_inicio=datetime.today().date()
			f_fin=f_inicio+timedelta(days=1) #time delta ayuda a sumar fechas
			self.ids.date_id.text=str(f_inicio.strftime("%d-%m-%y")) #pone la feha en date_id
		elif choice=='Date':
			date=self.ids.single_date.text #le sacamos el texto del input
			try:
				f_elegida=datetime.strptime(date,'%d/%m/%y')
			except:
				valid_input=False
			if valid_input: #si si es valida
				f_inicio=f_elegida #el inicio sera el elegido
				f_fin=f_elegida+timedelta(days=1)
				self.ids.date_id.text=f_elegida.strftime('%d-%m-%y') #mostramos en el label que nos dice que vemos
		else:
			if self.ids.initial_date.text:
				initial_date=self.ids.initial_date.text #le asignamos el valor
				try:
					f_inicio=datetime.strptime(initial_date, '%d/%m/%y') #
				except:
					valid_input=False
			if self.ids.last_date.text:
				last_date=self.ids.last_date.text
				try:
					f_fin=datetime.strptime(last_date, '%d/%m/%y')
				except:
					valid_input=False
			if valid_input:
				self.ids.date_id.text=f_inicio.strftime("%d-%m-%y")+" - "+f_fin.strftime("%d-%m-%y") #muestra de tal fecha a tal fecha

		if valid_input:
			inicio_fin=(f_inicio, f_fin)# Tupla que contiene las fechas de inicio y fin
			ventas_sql=QueriesSQLite.execute_read_query(connection, select_ventas_query, inicio_fin) #pasamos a la bd lq nos pide
			if ventas_sql:
				for venta in ventas_sql:
					final_sum+=venta[1] # Suma el total de cada venta a la variable "final_sum"
					ventas_detalle_sql=QueriesSQLite.execute_read_query(connection, selec_productos_query, (venta[0],)) #trae por id
					_total_productos.append(ventas_detalle_sql) #le agrega los productos que estan en el query, lista de listas
					count=0
					for producto in ventas_detalle_sql:
						count+=producto[4] #el cuatro es lacantidad o sea sumamos y para saber la el total
					_ventas.append({"username": venta[3], "productos": count, "total": venta[1], "fecha": datetime.strptime(venta[2], '%Y-%m-%d %H:%M:%S.%f')}) #le pasamos la informacion que quiere
				self.ids.ventas_rv.agregar_datos(_ventas)#mandamos los datos al rv
				self.productos_actuales=_total_productos
		self.ids.final_sum.text='$ '+str("{:.2f}".format(final_sum)) # Muestra el valor total de las ventas en el widget "final_sum"
		self.ids.initial_date.text=''
		self.ids.last_date.text=''
		self.ids.single_date.text=''
		self.ids.notificacion.text='Datos de Ventas'
		# Reinicia los valores de los widgets utilizados para la selección de fechas y muestra una notificación



class CustomDropDown(DropDown):
	def __init__(self, cambiar_callback, **kwargs):
		self._succ_cb = cambiar_callback # Almacena la función "cambiar_callback" en la variable "_succ_cb" para ser utilizada posteriormente
		super(CustomDropDown, self).__init__(**kwargs)# La clase "CustomDropDown" es una subclase de "DropDown".
        # Define un drop-down personalizado para cambiar de vista.

	def vista(self, vista):# Método para cambiar de vista
		if callable(self._succ_cb):# Verifica si "_succ_cb" es una función llamable
			self._succ_cb(True, vista)# Llama a la función "_succ_cb" pasando True y la vista seleccionada como argumentos


class AdminWindow(BoxLayout):
	# La clase "AdminWindow" es una subclase de "BoxLayout".
    # Define la ventana principal de la aplicación.
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.vista_actual='Productos' # Variable para almacenar la vista actual, inicializada como 'Productos'
		self.vista_manager=self.ids.vista_manager# Obtiene la referencia al widget "vista_manager" a través de su ID
		self.dropdown = CustomDropDown(self.cambiar_vista)# Crea una instancia de la clase "CustomDropDown" pasando la función "cambiar_vista" como argumento				
		self.ids.cambiar_vista.bind(on_release=self.dropdown.open)	# Vincula el evento "on_release" del widget "cambiar_vista" a la función "open" del drop-down
		
		
	def cambiar_vista(self, cambio=False, vista=None): #cambiar la vista
		if cambio:
			self.vista_actual=vista
			self.vista_manager.current=self.vista_actual
			self.dropdown.dismiss()

	def signout(self): #salir
		self.parent.parent.current='scrn_signin'

	def venta(self): #cambiar a ventas
		self.parent.parent.current='scrn_ventas'

	def actualizar_productos(self, productos): #actualiza el producto
		self.ids.vista_productos.actualizar_productos(productos)



class AdminApp(App):# La clase "AdminApp" es una subclase de "App".
	def build(self):
		return AdminWindow()
    # Define la aplicación principal.

if __name__=="__main__":
    AdminApp().run() 
    # Si el script se ejecuta directamente (no se importa como módulo),
    # crea una instancia de la clase "AdminApp" y ejecuta el método "run" para iniciar la aplicación.