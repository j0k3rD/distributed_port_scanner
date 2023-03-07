## Para conectarse a la aplicación de Django desde una PC remota, se deben seguir los siguientes pasos:

1. Obtener la dirección IP de la máquina principal en la que se está ejecutando la aplicación de Django. En la terminal de Ubuntu, se puede usar el comando **`ip a`** para obtener la dirección IP de la interfaz de red que se está utilizando.

2. Asegurarse de que el firewall de la máquina principal permita el tráfico entrante en el puerto que se está utilizando para la aplicación de Django. Por defecto, Django utiliza el puerto 8000, pero esto puede ser diferente en la configuración. Para permitir el tráfico entrante en el puerto 8000, se puede utilizar el siguiente comando en la terminal de Ubuntu:

``` sudo ufw allow 8000/tcp ```

3. Desde la máquina remota, abrir un navegador web e introducir la dirección IP de la máquina principal seguida del puerto utilizado por la aplicación de Django. Por ejemplo, si la dirección IP de la máquina principal es 192.168.1.100 y la aplicación de Django está utilizando el puerto 8000, se puede acceder a la aplicación desde la máquina remota en la siguiente URL:

``` http://192.168.1.100:8000/area3/ ```

Es importante tener en cuenta que la dirección IP de la máquina principal puede cambiar si se utiliza DHCP en la red. En este caso, se puede utilizar un servicio de DNS dinámico para asignar un nombre de dominio a la dirección IP de la máquina principal y poder acceder a la aplicación de Django utilizando el nombre de dominio en lugar de la dirección IP.

---

## Para conectar un proceso Celery en una PC remota a un proceso Celery principal, necesitarás configurar ambos procesos para trabajar juntos. Hay varios pasos que debes seguir para lograr esto:

1. En el proceso principal, debes configurar el broker de mensajes (por ejemplo, Redis) para permitir conexiones entrantes desde la PC remota. Si estás utilizando Redis, asegúrate de configurar el archivo **`redis.conf`** para permitir conexiones externas. Puedes hacer esto configurando la directiva **`bind`** a la dirección IP de la máquina principal.

2. Una vez que hayas configurado el broker de mensajes, debes asegurarte de que la PC remota pueda conectarse a él. Si la PC remota está en una red diferente, es posible que debas configurar el enrutador para permitir el tráfico en el puerto que utiliza el broker de mensajes.

3. En la PC remota, debes configurar el proceso Celery para conectarse al broker de mensajes en la PC principal. Puedes hacer esto mediante la configuración del archivo **`celeryconfig.py`** para utilizar la dirección IP de la máquina principal como el host del broker de mensajes.

4. Después de configurar el proceso Celery en la PC remota, deberás iniciarlo mediante el comando **`celery worker`**. Asegúrate de que esté configurado para conectarse al broker de mensajes en la máquina principal.

Con estos pasos, deberías poder conectar un proceso Celery en una PC remota a un proceso Celery principal. Ten en cuenta que esto puede requerir ajustes adicionales dependiendo de tu configuración específica.

---

## Autoscale

1. En el caso de que quieras agregar la funcionalidad de *`--autoscale`* a Celery necesitas agregar el argumento antes de iniciarlo:
  ``` celery -A distributed_scanner worker --loglevel=INFO --autoscale=2,16```
  IMPORTANTE: el primer numero indica la cantidad minima de workers con los que se ejecutaran las task y el segundo la cantidad maxima de workers que Celery podra levantar para poder realizar las task. Dependiendo la carga, Celery decidira si agrega o quita workers a su funcionamiento.
