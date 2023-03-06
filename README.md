# Final Computacion II
## Profesor: Diego Cordoba -- Alumno: Aaron Moya

<h1 align="center"> 
  Distributed Ports Scanner
</h1>
<h3>

*Detalles del Proyecto:*

</h3>

<p>Quiero armar una app cliente-servidor que genere escaneos de puertos abiertos en una ip o un rango de ips determinado, el cual pueda probar la seguridad de los sistemas involucrados, generar un reporte del mismo y brindar algunas ayudas para solucionar el problema dependiendo el tipo de puerto que se encuentra critico. La idea tambien es que se puedan conectar mas colas Celery con mas workers y asi mejorar el procesamiento de las tasks.
Esto se realizaria con ayuda de: 

  - Celery y Redis para generar las tareas asincronicas y encolarlas para su posterior procesamiento. 
  - Django como framework de ayuda para la creacion de la estructura de la aplicacion.
  - Otras herramientas como Nmap, Nessus para generar otros tipos de escaneos. (NESSUS A IMPLEMENTAR A FUTURO..)

<h3>

*Grafico de la Arquitectura*

</h3>

<p align="center">
   <img height="500" src="https://user-images.githubusercontent.com/83615514/220962856-9a6286e1-5206-4dc9-9ab6-f5183a79b48a.png">
</p>

<h3>

*Funcionamiento:*

</h3>

<h4>

*Entidades:*

</h4>

<p>Esta compuesta por: 
  
  - Servidor: este sera el cerebro. Se encarga de:
    - Levantar el Celery: usaremos este sistema distribuido para ejecutar todas las tareas usando los workers que se le configuren.
    - Crear la lista de Redis: aca se van a enlistar todas las tareas que realicen los workers.
    - Crear y levantar una base de datos: dentro de esta base de datos se almacenaran principalmente los registros de tablas que se hayan recolectado en los escaneos. Asi cuando se necesiten generar los reportes de la base de datos o de una ip en particular, se recoge la informacion de la misma.
    - Realizara la conexion con cada uno de los clientes. Una vez se conecta un nuevo cliente, se crea una conexion a traves de Websocket, el cual sera el que se comunique y reciba ordenes del cliente durante toda su sesion. Ademas se podra crear Canales por los cuales grupos dentro de la red pueden trabajar por separado enviando sus peticiones al servidor.
  
  - Cliente: los clientes se conectaran al server a traves de un navegador web.
  - Celery: este creará los diferentes workers que se usaran para realizar las tareas de los ataques.
  - Redis: enlistar las tareas en memoria.
  - Django: ayuda con la creacion de la estructura de la app.
</p>
