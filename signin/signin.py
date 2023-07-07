from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from sqlqueries import QueriesSQLite

Builder.load_file('signin/signin.kv') # Carga el archivo de diseño .kv que define la interfaz de usuario

class SigninWindow(BoxLayout):
	def __init__(self, poner_usuario_callback, **kwargs):
		super().__init__(*kwargs)
		self.poner_usuario=poner_usuario_callback
        # La clase SigninWindow hereda de BoxLayout y se utiliza para crear una ventana de inicio de sesión en la interfaz de usuario

        # El constructor recibe un argumento poner_usuario_callback, que es una función o método proporcionado desde otro contexto
        # Esta función se utilizará más adelante para manejar el evento de poner el nombre de usuario

        # Se llama al constructor de la clase base (BoxLayout) para asegurar que las inicializaciones se realicen correctamente

        # Se asigna el valor del argumento poner_usuario_callback al atributo poner_usuario de la instancia actual
        # Esto permite que el callback se utilice posteriormente dentro de la clase para manejar el evento

	def verificar_usuario(self, username, password):
		 # Se establece una conexión a la base de datos utilizando la función create_connection del módulo QueriesSQLite
		connection = QueriesSQLite.create_connection("pdvDB.sqlite")
		 # Se ejecuta una consulta SELECT para obtener todos los usuarios de la base de datos
		users=QueriesSQLite.execute_read_query(connection, "SELECT * from usuarios")
		if users:
			if username=='' or password=='':
			# Si el nombre de usuario o la contraseña están vacíos, se muestra un mensaje de error 
				self.ids.signin_notificacion.text='Falta nombre de usuario y/o contraseña'
			else:
				usuario={}
				for user in users: 
					if user[0]==username:
					# Se encontró un usuario coincidente con el nombre de usuario proporcionado
                    # Se guarda la información del usuario en un diccionario
						usuario['nombre']=user[1]
						usuario['username']=user[0]
						usuario['password']=user[2]
						usuario['tipo']=user[3]
						break
				if usuario: # Si se encontró un usuario coincidente, se verifica la contraseña
					if usuario['password']==password:
						self.ids.username.text=''
						self.ids.password.text=''
						self.ids.signin_notificacion.text=''
						# Si la contraseña es correcta, se realiza lo siguiente:
	                    # Se limpian los campos de entrada de nombre de usuario y contraseña
	                    # Se borra el texto de notificación
	                    # Se determina la ventana a mostrar según el tipo de usuario
	                    # Se llama al callback poner_usuario con el diccionario de usuario como argumento
						if usuario['tipo']=='trabajador':
							self.parent.parent.current='scrn_ventas'
						else:
							self.parent.parent.current='scrn_admin'
						self.poner_usuario(usuario)
					else:
						# Si la contraseña es incorrecta, se muestra un mensaje de error
						self.ids.signin_notificacion.text='Usuario o contraseña incorrecta'
				else:
					 # Si no se encontró un usuario coincidente, se muestra un mensaje de error
					self.ids.signin_notificacion.text='Usuario o contraseña incorrecta'
		else:
			# Si no hay usuarios en la base de datos, se crea un primer usuario con nombre de usuario 'usuario', contraseña '123' y tipo 'admin'
		    usuario_tuple=('usuario', 'Usuario Inicio', '123', 'admin')
		    crear_usuario = "INSERT INTO usuarios (username, nombre, password, tipo) VALUES (?,?,?,?);"
		    QueriesSQLite.execute_query(connection, crear_usuario, usuario_tuple)
		    self.ids.signin_notificacion.text='Se creo primer usuario. usuario 123'



class SigninApp(App):
	def build(self):
		return SigninWindow()
	 # El método build() es requerido por la clase base App y se utiliza para construir y retornar la interfaz de usuario de la aplicación
     # En este caso, se retorna una instancia de la clase SigninWindow, que representa la ventana de inicio de sesión


if __name__=="__main__":
	# Este bloque se ejecuta si el script se ejecuta directamente (no se importa como módulo)
    # Crea una instancia de la clase SigninApp y ejecuta la aplicación llamando al método run()
	SigninApp().run()