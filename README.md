Mi proyecto es una aplicación de gestión de usuarios y pedidos de una pizzería, implementada en Flask con soporte para autenticación de usuarios usando Flask-login. Básicamente, se encarga de manejar desde el registro de usuarios y autenticación hasta el control de pedidos y consulta de ventas. Te explico cómo funciona:

Autenticación de usuarios:
Uso Flask-login para manejar todo el proceso de inicio de sesión, cierre de sesión y protección de rutas. Los usuarios registrados pueden iniciar sesión con sus credenciales y acceder a las secciones de pedidos y consultas. Esto garantiza que solo personas autorizadas puedan interactuar con el sistema. Para proteger las contraseñas, utilizo  para cifrarlas con un hash seguro. No guardo contraseñas en texto claro para evitar riesgos de seguridad.

Registro de usuarios:
Los nuevos usuarios pueden registrarse mediante un formulario que guarda sus datos en una base de datos SQL utilizando SQLAlchemy. Durante el registro, verifico que no existan duplicados en el nombre de usuario y cifro su contraseña antes de guardarla.

Rutas protegidas:
Las rutas sensibles, como  y , están protegidas con el decorador . Esto significa que solo usuarios autenticados pueden acceder a ellas. Por ejemplo, si alguien sin iniciar sesión intenta entrar a , será redirigido automáticamente al formulario de login.

Pedidos de pizza:
Una vez que un usuario autenticado entra al sistema, puede registrar pedidos. El formulario de pedidos recoge datos del cliente (nombre, dirección, teléfono, fecha del pedido) y detalles del pedido (tamaño de la pizza, ingredientes, cantidad). El subtotal se calcula automáticamente con base en el tamaño y los ingredientes seleccionados.

Consulta de ventas:
Los usuarios pueden consultar las ventas del día, mes o una fecha específica. La información se obtiene desde un archivo de texto () que guarda cada transacción. Esto les permite tener un resumen completo de las ventas realizadas y el número total de pedidos.

Cierre de sesión:
Cuando el usuario termina su sesión, puede salir usando la opción de logout, que limpia las cookies de autenticación y lo redirige al formulario de login.
