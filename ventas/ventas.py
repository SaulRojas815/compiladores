
from kivy.app import App  # Importamos la clase App del módulo kivy.app
from kivy.uix.boxlayout import BoxLayout # Importamos la clase BoxLayout del módulo kivy.uix.boxlayout
from kivy.uix.recycleview import RecycleView  # Importamos la clase RecycleView del módulo kivy.uix.recycleview
from kivy.uix.recycleview.views import RecycleDataViewBehavior # Importamos la clase RecycleDataViewBehavior del módulo kivy.uix.recycleview.views
from kivy.properties import BooleanProperty # Importamos la clase BooleanProperty del módulo kivy.properties
from kivy.uix.recycleboxlayout import RecycleBoxLayout # Importamos la clase RecycleBoxLayout del módulo kivy.uix.recycleboxlayout
from kivy.uix.behaviors import FocusBehavior # Importamos la clase FocusBehavior del módulo kivy.uix.behaviors
from kivy.uix.recycleview.layout import LayoutSelectionBehavior  # Importamos la clase LayoutSelectionBehavior del módulo kivy.uix.recycleview.layout
from kivy.uix.popup import Popup # Importamos la clase Popup del módulo kivy.uix.popup
from kivy.clock import Clock # Importamos la clase Clock del módulo kivy.clock
from kivy.lang import Builder # Importamos la clase Builder del módulo kivy.lang

Builder.load_file('ventas/ventas.kv') 

from datetime import datetime, timedelta # Importamos las clases datetime y timedelta del módulo datetime
from sqlqueries import QueriesSQLite # Importamos la clase QueriesSQLite del módulo sqlqueries

inventario=[
	{'codigo': '111', 'nombre': 'leche 1L', 'precio': 20.0, 'cantidad': 20},
	{'codigo': '222', 'nombre': 'cereal 500g', 'precio': 50.5, 'cantidad': 15}, 
	{'codigo': '333', 'nombre': 'yogurt 1L', 'precio': 25.0, 'cantidad': 10},
	{'codigo': '444', 'nombre': 'helado 2L', 'precio': 80.0, 'cantidad': 20},
	{'codigo': '555', 'nombre': 'alimento para perro 20kg', 'precio': 750.0, 'cantidad': 5},
	{'codigo': '666', 'nombre': 'shampoo', 'precio': 100.0, 'cantidad': 25},
	{'codigo': '777', 'nombre': 'papel higiénico 4 rollos', 'precio': 35.5, 'cantidad': 30},
	{'codigo': '888', 'nombre': 'jabón para trastes', 'precio': 65.0, 'cantidad': 5},
	{'codigo': '999', 'nombre': 'refresco 600ml', 'precio': 15.0, 'cantidad': 10}
]

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout): #hereda de las clases FocusBehavior, es un comportamiento que permite 
													#a un widget recibir el foco y manejar eventos relacionados con el foco.
    ''' // '''
    touch_deselect_last = BooleanProperty(True)
    # La propiedad booleana touch_deselect_last determina si el último elemento seleccionado se deselecciona al tocarlo


class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):#Hereda de las clases RecycleDataViewBehavior y BoxLayout.
  
    index = None # Almacena el índice del elemento en la vista del RecycleView.
    selected = BooleanProperty(False) #Indica si el elemento está seleccionado o no.
    selectable = BooleanProperty(True) #Determina si el elemento es seleccionable o no.

    def refresh_view_attrs(self, rv, index, data): #cuando haya cambios
    	self.index = index  # Almacena el índice del elemento en la vista del RecycleView.
    	self.ids['_hashtag'].text = str(1+index) # Actualiza el texto del widget identificado como '_hashtag'.
    	self.ids['_articulo'].text = data['nombre'].capitalize()# Actualiza el texto del widget identificado como '_articulo'.
    	self.ids['_cantidad'].text = str(data['cantidad_carrito']) #actualiza ...
    	self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))#actualiza ...dos decimales
    	self.ids['_precio'].text = str("{:.2f}".format(data['precio_total']))
    	return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data) #Se llama al método refresh_view_attrs de la clase base para completar la actualización de los atributos de la vista.

    def on_touch_down(self, touch):
        '''  '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):# Verifica si se ha seleccionado y se imprime.
            return True
        if self.collide_point(*touch.pos) and self.selectable: # Comprueba si el punto de contacto está dentro del widget y si el elemento es seleccionable.
            return self.parent.select_with_touch(self.index, touch)#accede al atributo data, # Llama al método select_with_touch del padre para seleccionar el elemento con el índice y el toque proporcionados.

    def apply_selection(self, rv, index, is_selected): #se responde a la selección de elementos en la vista. 
        ''' // '''
        self.selected = is_selected # Actualiza el estado de selección del elemento.
        if is_selected: # Verifica si el elemento está seleccionado.
        	rv.data[index]['seleccionado']=True # Actualiza el atributo 'seleccionado' del elemento en el índice del RecycleView.
        else:
        	rv.data[index]['seleccionado']=False

class SelectableBoxLayoutPopup(RecycleDataViewBehavior, BoxLayout): #En esta clase SelectableBoxLayoutPopup, se agrega soporte de selección a un widget BoxLayout.
    ''' // '''
    index = None # Almacena el índice del elemento en la vista del RecycleView.
    selected = BooleanProperty(False)  # Indica si el elemento está seleccionado o no.
    selectable = BooleanProperty(True)  # Determina si el elemento es seleccionable o no.

    def refresh_view_attrs(self, rv, index, data): #se actualizan los atributos de la vista con los datos 
    	self.index = index # Almacena el índice del elemento en la vista del RecycleView.
    	self.ids['_codigo'].text = data['codigo'] # Actualiza el texto del widget identificado como '_codigo'.
    	self.ids['_articulo'].text = data['nombre'].capitalize() # _articulo
    	self.ids['_cantidad'].text = str(data['cantidad']) #_cantidad
    	self.ids['_precio'].text = str("{:.2f}".format(data['precio'])) #_precio
    	return super(SelectableBoxLayoutPopup, self).refresh_view_attrs(
            rv, index, data) #Se llama al método refresh_view_attrs de la clase base para completar la actualización de los atributos de la vista.

    def on_touch_down(self, touch): #se agrega la funcionalidad de selección al tocar el widget.
        ''' // '''
        if super(SelectableBoxLayoutPopup, self).on_touch_down(touch): # Verifica si se ha seleccionado y se imprime.
            return True
        if self.collide_point(*touch.pos) and self.selectable: # Comprueba si el punto de contacto está dentro del widget y si el elemento es seleccionable.
            return self.parent.select_with_touch(self.index, touch) # Llama al método select_with_touch del padre para seleccionar el elemento con el índice y el toque proporcionados.

    def apply_selection(self, rv, index, is_selected):
        ''' // '''
        self.selected = is_selected # Actualiza el estado de selección del elemento.
        if is_selected: # Verifica si el elemento está seleccionado.
        	rv.data[index]['seleccionado']=True  # Actualiza el atributo 'seleccionado' del elemento en el índice del RecycleView.
        else:
        	rv.data[index]['seleccionado']=False


class RV(RecycleView): #se hereda de la clase RecycleView y se añade un constructor (__init__) para inicializar algunos atributos. 
    def __init__(self, **kwargs): #Es una lista que almacena los elementos que se mostrarán en la vista. Cada vez que se agregue un elemento, este aparecerá en esta lista.
        super(RV, self).__init__(**kwargs)
        self.data = [] # Cada vez que agreguemos un elemento, aparecerá en esta lista.
        self.modificar_producto=None  # Variable para realizar modificaciones en un producto.

    def agregar_articulo(self, articulo):#funcion para que no se amontone lo mismo y solo muestre una vez
    	articulo['seleccionado']=False #Se establece la propiedad 'seleccionado' del artículo en False, ya que se está agregando un nuevo artículo y no está seleccionado inicialmente.
    	indice=-1 #Se inicializa la variable indice en -1, que se utilizará para rastrear si el artículo ya existe en la lista.
    	if self.data:
    		for i in range(len(self.data)):
    			if articulo['codigo']==self.data[i]['codigo']:#si llega a encontrar que el articulo ya esta el indice se convierte en i
    				indice=i
    		if indice >=0: # Si el artículo ya existe en la lista, se modifica la cantidad y el precio total del artículo existente. 
    			self.data[indice]['cantidad_carrito']+=1 
    			self.data[indice]['precio_total']=self.data[indice]['precio']*self.data[indice]['cantidad_carrito']
    			self.refresh_from_data()
    		else:
	    		self.data.append(articulo)# Si el artículo no existe en la lista, se agrega como un nuevo elemento.
    	else:
    		self.data.append(articulo) # Si no hay elementos en la lista, se agrega el artículo como el primer elemento.

    def eliminar_articulo(self): #Esta función maneja la lógica de eliminar un artículo de la vista del RecycleView y devuelve su precio total.
    	indice=self.articulo_seleccionado()# Obtiene el índice del artículo seleccionado.
    	precio=0
    	if indice>=0:
    		self._layout_manager.deselect_node(self._layout_manager._last_selected_node)#para que no este seleccionado luego de eliminar
    		precio=self.data[indice]['precio_total']#regresa el precio toal
    		self.data.pop(indice) #elimina lo que esta en el indice
    		self.refresh_from_data() #refresca
    	return precio

    def modificar_articulo(self): #modifica
    	indice=self.articulo_seleccionado() # Obtiene el índice del artículo seleccionado.
    	if indice>=0:
    		popup=CambiarCantidadPopup(self.data[indice], self.actualizar_articulo) # Crea una instancia del Popup para modificar la cantidad del artículo.
    		popup.open() # Abre el Popup.

    def actualizar_articulo(self, valor):
    	indice=self.articulo_seleccionado()
    	if indice>=0:
    		if valor==0: # Si el valor es 0, se elimina el artículo de la lista y se desmarca el último nodo seleccionado.
    			self.data.pop(indice)
    			self._layout_manager.deselect_node(self._layout_manager._last_selected_node)#al eliminar se deseleccion
    		else:
    		# Si el valor no es 0, se actualiza la cantidad y el precio total del artículo.
    			self.data[indice]['cantidad_carrito']=valor #se le asigna el nuevo valor
    			self.data[indice]['precio_total']=self.data[indice]['precio']*valor #se le asigna el nuevo valor total
    		self.refresh_from_data()  # Actualiza la vista del RecycleView.
    		nuevo_total=0
    		for data in self.data:
    			nuevo_total+=data['precio_total']
    		self.modificar_producto(False, nuevo_total) # Actualiza el producto modificado en la interfaz de usuario.

    def articulo_seleccionado(self): #Esta función permite determinar el índice del artículo seleccionado en el RecycleView.
    	indice=-1  # Inicializa el índice del artículo seleccionado en -1.
    	for i in range(len(self.data)):
    		if self.data[i]['seleccionado']: # Si la llave 'seleccionado' del artículo es verdadera, se guarda el índice del artículo seleccionado.
    			indice=i
    			break
    	return indice


class ProductoPorNombrePopup(Popup): #se hereda de la clase Popup y se añade un constructor (__init__) para inicializar algunos atributos.
	def __init__(self, input_nombre, agregar_producto_callback, **kwargs):#llamamos agregar producto de ven w
		super(ProductoPorNombrePopup, self).__init__(**kwargs)
		self.input_nombre=input_nombre  # Almacena el nombre del producto ingresado en la entrada de texto.
		self.agregar_producto=agregar_producto_callback # Almacena el callback para agregar un producto desde la ventana de ventas.

	def mostrar_articulos(self): #Esta función consulta el inventario de productos, busca los artículos cuyos nombres coinciden con self.input_nombre y los agrega a la vista del RecycleView.
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")  # Crea una conexión a la base de datos.
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos") # Ejecuta una consulta SQL para obtener el inventario de productos.
		self.open() # Abre la ventana emergente.
		for nombre in inventario_sql:
		# Itera sobre los nombres de los productos obtenidos del inventario.
        # Si el nombre coincide con self.input_nombre (ignorando mayúsculas y minúsculas):
			if nombre[1].lower().find(self.input_nombre)>=0: #find busca ej leche mos arroja el nro del indice de donde esta leche, si lo encuentra manda un mayor 1 y i no un menor 1
				producto={'codigo': nombre[0], 'nombre': nombre[1], 'precio': nombre[2], 'cantidad': nombre[3]} # Código del producto.
				self.ids.rvs.agregar_articulo(producto) # Agrega el artículo a la vista del RecycleView.

	def seleccionar_articulo(self): #Esta función maneja la acción de seleccionar un artículo en el Popup, obteniendo sus datos y llamando a una función (self.agregar_producto) para agregar el artículo a la lógica de la ventana de ventas. Luego, cierra el Popup.
		indice=self.ids.rvs.articulo_seleccionado() # Obtiene el índice del artículo seleccionado en el RecycleView del Popup.
		if indice>=0: 
			_articulo=self.ids.rvs.data[indice] # Obtiene el artículo seleccionado en el RecycleView del Popup.
			articulo={}
			articulo['codigo']=_articulo['codigo'] # Código del artículo.
			articulo['nombre']=_articulo['nombre']
			articulo['precio']=_articulo['precio']
			articulo['cantidad_carrito']=1  # Cantidad del artículo en el carrito (inicialmente 1).
			articulo['cantidad_inventario']=_articulo['cantidad'] # Cantidad del artículo en el inventario.
			articulo['precio_total']=_articulo['precio']  #Precio total del artículo (inicialmente el mismo que el precio individual).
			if callable(self.agregar_producto):#llamamos el def agreagr producto
				self.agregar_producto(articulo)
			self.dismiss() # Cierra el Popup

class CambiarCantidadPopup(Popup):#se hereda de la clase Popup y se añade un constructor (__init__) para inicializar algunos atributos.
	def __init__(self, data, actualizar_articulo_callback, **kwargs): #Estos atributos permiten almacenar y mostrar los datos del artículo a modificar en el Popup.
		super(CambiarCantidadPopup, self).__init__(**kwargs)
		self.data=data # Almacena los datos del artículo a modificar.
		self.actualizar_articulo=actualizar_articulo_callback  # Almacena el callback para actualizar el artículo.
		self.ids.info_nueva_cant_1.text = "Producto: " + self.data['nombre'].capitalize() # Actualiza el texto de información del producto en el Popup.
		self.ids.info_nueva_cant_2.text = "Cantidad: "+str(self.data['cantidad_carrito']) # Actualiza el texto de información de la cantidad en el Popup.
	def validar_input(self, texto_input):#validar el texto
		try:
			nueva_cantidad=int(texto_input) # Intenta convertir el texto de entrada en un entero.
			self.ids.notificacion_no_valido.text='' # Borra cualquier notificación de cantidad no válida en la interfaz.
			self.actualizar_articulo(nueva_cantidad) # Llama al callback actualizar_articulo y pasa la nueva cantidad como argumento.
			self.dismiss()
		except:
			self.ids.notificacion_no_valido.text='Cantidad no valida' #cuando se ingresa un valor invalido


class PagarPopup(Popup): #se hereda de la clase Popup y se añade un constructor (__init__) para inicializar algunos atributos
	def __init__(self, total, pagado_callback, **kwargs): #Estos atributos permiten almacenar el monto total a pagar, gestionar el evento de pago y controlar el cierre del Popup al presionar el botón de pagar.
		super(PagarPopup, self).__init__(**kwargs)
		self.total=total # Almacena el monto total a pagar.
		self.pagado=pagado_callback # Almacena el callback para manejar el evento de pago.
		self.ids.total.text= "{:.2f}".format(self.total) # Actualiza el texto del total en la interfaz.
		self.ids.boton_pagar.bind(on_release=self.dismiss) #bind, se presiona y se cierra, Asocia el evento de "on_release" del botón de pagar con el método "dismiss()" para cerrar el Popup.

	def mostrar_cambio(self):
		recibido= self.ids.recibido.text # Obtiene el monto recibido del input de recibido.
		try: #verificar que es un numero y no letra
			cambio=float(recibido)-float(self.total) # Calcula el cambio restando el total recibido del total a pagar.
			if cambio>=0:
				self.ids.cambio.text="{:.2f}".format(cambio) # Muestra el cambio en la interfaz formateado con dos decimales.
				self.ids.boton_pagar.disabled=False # Habilita el botón de pagar.
			else: 
				self.ids.cambio.text="Pago menor a cantidad a pagar"
		except:
			self.ids.cambio.text="Pago no valido"

class NuevaCompraPopup(Popup):
	def __init__(self, nueva_compra_callback, **kwargs): #Estos atributos permiten almacenar el callback para manejar el evento de nueva compra y controlar el cierre del Popup al presionar el botón aceptar
		super(NuevaCompraPopup, self).__init__(**kwargs)
		self.nueva_compra=nueva_compra_callback # Almacena el callback para manejar el evento de nueva compra.
		self.ids.aceptar.bind(on_release=self.dismiss) # Asocia el evento de "on_release" del botón aceptar con el método "dismiss()" para cerrar el Popup.


class VentasWindow(BoxLayout):
	usuario=None # Almacena información del usuario (se asume que se establece en otro lugar del código).
	def __init__(self, actualizar_productos_callback, **kwargs):
		super().__init__(**kwargs)
		self.total=0.0  # Almacena el total de la venta (inicializado en 0.0).
		self.ids.rvs.modificar_producto=self.modificar_producto # Asigna el método "modificar_producto" al atributo "modificar_producto" del RecycleView (self.ids.rvs)
		self.actualizar_productos=actualizar_productos_callback # Almacena el callback para actualizar los productos.

		self.ahora=datetime.now() # Obtiene la fecha y hora actual.
		self.ids.fecha.text=self.ahora.strftime("%d/%m/%y")#fecha
		Clock.schedule_interval(self.actualizar_hora, 1)#actualizacion de hora


	def agregar_producto_codigo(self, codigo): #se agrega un producto a la venta según el código proporcionado.  
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")  # Crea una conexión a la base de datos.
		inventario_sql=QueriesSQLite.execute_read_query(connection, "SELECT * from productos")  # Obtiene los datos del inventario de la base de datos.
		for producto in inventario_sql:
			if codigo==producto[0]:  # Compara el código proporcionado con el código de cada producto en el inventario.
				articulo={}
				articulo['codigo']=producto[0] # Código del producto.
				articulo['nombre']=producto[1]
				articulo['precio']=producto[2]
				articulo['cantidad_carrito']=1 # Cantidad del producto en el carrito (inicialmente 1).
				articulo['cantidad_inventario']=producto[3] # Cantidad del producto en el inventario.
				articulo['precio_total']=producto[2] # Precio total del producto (inicialmente el mismo que el precio individual).
				self.agregar_producto(articulo) # Llama al método agregar_producto y pasa el diccionario articulo como argumento.
				self.ids.buscar_codigo.text='' # Limpia el texto del input de búsqueda de código.
				break

	def agregar_producto_nombre(self, nombre): # se agrega un producto a la venta según el nombre proporcionado.
		self.ids.buscar_nombre.text=''  # Limpia el texto del input de búsqueda de nombre.
		popup=ProductoPorNombrePopup(nombre, self.agregar_producto) # Crea una instancia de ProductoPorNombrePopup pasando el nombre y el callback agregar_producto.
		popup.mostrar_articulos() # Muestra los productos encontrados en el popup.

	def agregar_producto(self, articulo):# se agrega un producto a la venta y se actualiza el subtotal
		self.total+=articulo['precio'] # Actualiza el total sumando el precio del artículo al total existente.
		self.ids.sub_total.text= '$ '+"{:.2f}".format(self.total) # Actualiza la etiqueta del subtotal en la interfaz mostrando el total formateado con dos decimales.
		self.ids.rvs.agregar_articulo(articulo) # Agrega el artículo a la data del RecycleView.

	def eliminar_producto(self): #se elimina un producto de la venta y se actualiza el subtotal
		menos_precio=self.ids.rvs.eliminar_articulo() # Obtiene el precio del producto que se va a eliminar del RecycleView.
		self.total-=menos_precio # Resta el precio del producto eliminado al total existente.
		self.ids.sub_total.text='$ '+"{:.2f}".format(self.total) # Actualiza la etiqueta del subtotal en la interfaz mostrando el total formateado con dos decimales.

	def modificar_producto(self, cambio=True, nuevo_total=None): # se modifica un producto en la venta y se actualiza el subtotal. 
		if cambio:	
			self.ids.rvs.modificar_articulo() # Llama al método modificar_articulo del RecycleView para realizar cambios en el producto seleccionado.
		else:
			self.total=nuevo_total # Actualiza el total de la venta con el nuevo total proporcionado.
			self.ids.sub_total.text='$ '+"{:.2f}".format(self.total) # Actualiza la etiqueta del subtotal en la interfaz mostrando el nuevo total formateado con dos decimales.

	def actualizar_hora(self, *args): #funcion de actualizacion de hora
		self.ahora=self.ahora+timedelta(seconds=1) # Incrementa la hora actual en un segundo utilizando timedelta.
		self.ids.hora.text=self.ahora.strftime("%H:%M:%S") # Actualiza la etiqueta de la hora en la interfaz mostrando la hora formateada como "hora:minuto:segundo".		

	def pagar(self): #funcion para pagar
		if self.ids.rvs.data:
			popup=PagarPopup(self.total, self.pagado) # Crea una instancia de PagarPopup pasando el total de la venta y el callback pagado.
			popup.open()# Abre el popup de pago.
		else:
			self.ids.notificacion_falla.text='No hay nada que pagar' #id mptofcaoon falla de pagar, # Muestra un mensaje de notificación en caso de que no haya productos en la venta.

	def pagado(self): #e maneja la acción después de realizar el pago. 
		self.ids.notificacion_exito.text='Compra realizada con exito'  # Muestra un mensaje de notificación indicando que la compra se realizó con éxito.
		self.ids.notificacion_falla.text='' # Borra cualquier mensaje de notificación de fallo.
		self.ids.total.text="{:.2f}".format(self.total) # Actualiza la etiqueta de total en la interfaz mostrando el total formateado con dos decimales
		self.ids.buscar_codigo.disabled=True # Deshabilita el input de búsqueda por código.
		self.ids.buscar_nombre.disabled=True # Deshabilita el input de búsqueda por nombre.
		self.ids.pagar.disabled=True # Deshabilita el botón de pagar.

		connection = QueriesSQLite.create_connection("pdvDB.sqlite")  
		actualizar=""" UPDATE productos SET cantidad=? WHERE codigo=? """ #Consulta SQL para actualizar la cantidad del producto.
		actualizar_admin=[] # Lista de diccionarios para almacenar los datos de actualización de productos en la interfaz de administración.

		venta = """ INSERT INTO ventas (total, fecha, username) VALUES (?, ?, ?) """  # Consulta SQL para insertar la venta en la base de datos.
		venta_tuple = (self.total, self.ahora, self.usuario['username']) # Tupla con los datos de la venta a insertar.
		venta_id = QueriesSQLite.execute_query(connection, venta, venta_tuple) # Inserta la venta en la base de datos y obtiene el ID de la última fila insertada.
		ventas_detalle = """ INSERT INTO ventas_detalle(id_venta, precio, producto, cantidad) VALUES (?, ?, ?, ?) """ # Consulta SQL para insertar los detalles de la venta en la base de datos.

		for producto in self.ids.rvs.data:
			nueva_cantidad=0
			if producto['cantidad_inventario']-producto['cantidad_carrito']>0:
				nueva_cantidad=producto['cantidad_inventario']-producto['cantidad_carrito']
			producto_tuple=(nueva_cantidad, producto['codigo']) # Tupla con los datos para actualizar la cantidad del producto en la base de datos.
			ventas_detalle_tuple= (venta_id, producto['precio'], producto['codigo'], producto['cantidad_carrito'])  # Tupla con los datos para insertar los detalles de la venta en la base de datos.
			actualizar_admin.append({'codigo': producto['codigo'], 'cantidad': nueva_cantidad}) # Agrega los datos de actualización de productos a la lista actualizar_admin.

			QueriesSQLite.execute_query(connection, ventas_detalle, ventas_detalle_tuple) # Inserta los detalles de la venta en la base de datos.
			QueriesSQLite.execute_query(connection, actualizar, producto_tuple) # Actualiza la cantidad del producto en la base de datos.
		self.actualizar_productos(actualizar_admin) # Llama al método actualizar_productos pasando la lista actualizar_admin para actualizar los productos en la interfaz de administración.



	def nueva_compra(self, desde_popup=False): # se inicia una nueva compra.
		if desde_popup:
			self.ids.rvs.data=[]
			self.total=0.0
			self.ids.sub_total.text= '0.00'
			self.ids.total.text= '0.00'
			self.ids.notificacion_exito.text=''
			self.ids.notificacion_falla.text=''
			self.ids.buscar_codigo.disabled=False
			self.ids.buscar_nombre.disabled=False
			self.ids.pagar.disabled=False
			self.ids.rvs.refresh_from_data()
		elif len(self.ids.rvs.data): #si el carrito tiene algo que haga la nueva compra
			popup=NuevaCompraPopup(self.nueva_compra)  # Crea una instancia de NuevaCompraPopup pasando la función nueva_compra como callback.
			popup.open() # Abre el popup de nueva compra.

	def admin(self): #Esta función permite navegar a la pantalla de administración desde la pantalla de ventas.
		self.parent.parent.current='scrn_admin'
		# connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		# select_products = "SELECT * from productos"
		# productos = QueriesSQLite.execute_read_query(connection, select_products)
		# for producto in productos:
		# 	print(producto)


	def signout(self):
		if self.ids.rvs.data:
			self.ids.notificacion_falla.text='Compra abierta'  # Muestra un mensaje de notificación si hay productos en la venta actual.
		else:
			self.parent.parent.current='scrn_signin' # Cambia a la pantalla de inicio de sesión.

	def poner_usuario(self, usuario): 
		self.ids.bienvenido_label.text='Bienvenido '+usuario['nombre'] # Muestra un mensaje de bienvenida con el nombre del usuario.
		self.usuario=usuario # Almacena el usuario en el atributo `usuario` del objeto actual (VentasWindow).
		if usuario['tipo']=='trabajador':
			self.ids.admin_boton.disabled=True # Deshabilita el botón de administración si el usuario es de tipo "trabajador".
			self.ids.admin_boton.text=''  # Borra el texto del botón de administración.
			self.ids.admin_boton.opacity=0 # Establece la opacidad del botón de administración a 0 (invisible).
		else:
			self.ids.admin_boton.disabled=False # Habilita el botón de administración si el usuario no es de tipo "trabajador".
			self.ids.admin_boton.text='Admin' # Establece el texto del botón de administración como "Admin".
			self.ids.admin_boton.opacity=1 # Establece la opacidad del botón de administración a 1 (visible).


class VentasApp(App): #Es una subclase de App que representa la aplicación de ventas. Define el comportamiento de la aplicación y proporciona el método build() que se ejecuta al iniciar la aplicación.
	def build(self): #Es el método de la clase VentasApp que se encarga de construir y devolver la ventana principal de la aplicación, en este caso, la instancia de VentasWindow
		return VentasWindow()


if __name__=='__main__': #Verifica si el archivo actual es el punto de entrada principal del programa.
	VentasApp().run() #Crea una instancia de VentasApp y ejecuta el método run() para iniciar la aplicación.