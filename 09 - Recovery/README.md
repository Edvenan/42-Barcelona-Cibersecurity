# RECOVERY
Teniendo en cuenta un entorno Windows 10, obtener la siguiente informacion, teniendo en cuenta que queremos acotar la consulta en un rango de tiempo:

1) Fechas de cambio de ramas de registro (CurrentVersionRun)
2) Archivos recientes
3) Programas instalados
4) Programas abiertos
5) Historial de navegación
6) Dispositivos conectados
7) Eventos de log

Para obtener la siguiente información en un entorno Windows 10 y acotar la consulta en un rango de tiempo, se pueden utilizar diferentes fuentes y herramientas del sistema. A continuación, te indico dónde puedes encontrar cada una de ellas:

## Fechas de cambio de ramas de registro (CurrentVersionRun):
Puedes consultar las fechas de cambio de ramas de registro en el Registro de Windows. La ruta específica puede variar según la rama que estés buscando. Por ejemplo, si estás buscando la rama "CurrentVersionRun", puedes verificarla en la siguiente ubicación del registro:

**HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run**

Se puede utilizar la librería **winreg** para acceder y leer las claves y valores del registro de Windows.

## Archivos recientes:
Puedes obtener los archivos recientes accediendo al Explorador de archivos y navegando hasta la sección "Archivos recientes" en el panel izquierdo. Aquí encontrarás una lista de los archivos más recientes abiertos o accedidos por el usuario.

Se puede utilizar la librería **winshell** para obtener la lista de archivos recientes en Windows.

## Programas instalados:
Para obtener la lista de programas instalados, puedes acceder al Panel de control y abrir la sección "Programas" o "Programas y características". Aquí encontrarás una lista de los programas instalados en el sistema.

Se puede utilizar la librería **pywin32** para acceder y consultar la información de programas instalados en Windows.

## Programas abiertos:
Puedes verificar los programas actualmente abiertos utilizando el Administrador de tareas de Windows. Para abrirlo, puedes presionar las teclas Ctrl + Shift + Esc juntas. En la pestaña "Procesos" del Administrador de tareas, encontrarás una lista de los programas en ejecución.

Se puede utilizar la librería **psutil** para obtener la lista de procesos en ejecución y filtrar los programas abiertos.

## Historial de navegación:
El historial de navegación se encuentra en el navegador web que estés utilizando. Si usas Google Chrome, por ejemplo, puedes acceder a tu historial presionando Ctrl + H en el navegador. Otros navegadores como Firefox o Microsoft Edge también tienen opciones para ver el historial de navegación.

Para acceder al historial de navegación de diferentes navegadores web, Se puede utilizar las librerías específicas de cada uno, como **sqlite3** para Google Chrome o **python-firefox-history** para Firefox.


## Dispositivos conectados:
Para ver los dispositivos actualmente conectados a tu computadora, puedes abrir el Administrador de dispositivos de Windows. Puedes acceder a él buscando "Administrador de dispositivos" en el menú Inicio o utilizando la combinación de teclas Win + X y seleccionando "Administrador de dispositivos". Aquí encontrarás una lista de los dispositivos conectados, como unidades de almacenamiento, impresoras, dispositivos de red, etc.

Se puede utilizar la librería **pywin32** para acceder al Administrador de dispositivos de Windows y obtener información sobre los dispositivos conectados.

## Eventos de log:
Puedes consultar los eventos de log utilizando la herramienta "Visor de eventos" de Windows. Puedes acceder a ella buscando "Visor de eventos" en el menú Inicio o utilizando la combinación de teclas Win + X y seleccionando "Visor de eventos". Aquí encontrarás diferentes categorías de eventos, como eventos del sistema, eventos de seguridad, eventos de aplicaciones, etc.

Se puede utilizar la librería **pywin32** para acceder al Visor de eventos de Windows y consultar los eventos de registro.


Es importante tener en cuenta que la ubicación exacta y la forma de acceder a esta información pueden variar ligeramente dependiendo de la versión específica de Windows que estés utilizando.

Recuerda que algunos de estos procesos pueden requerir permisos de administrador en Windows. Asegúrate de ejecutar tu script con privilegios elevados si es necesario.

Ten en cuenta que cada uno de estos aspectos puede requerir un enfoque y métodos específicos para obtener la información deseada. Es recomendable consultar la documentación de cada librería y explorar ejemplos de código para obtener más detalles sobre cómo utilizarlas en tu script.