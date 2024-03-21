## PrintOnDemand
Se trata de una aplicación web desarrollada usando el framework de Flask con el apoyo de Bootstrap para las vistas.
Consta de una tienda en linea en la cual es posible realizar pedidos de modelos 3D. Cada modelo tiene asignados distintos materiales de impresión, los cuales afectan al precio final.

Cuenta con la opción de usar un usuario, de los cuales hay dos tipos, cliente y administrador.

Los usuarios cliente tienen la posibilidad de:
- Realizar pedidos de modelos del catalogo
- Subir un modelo personalizado y realizar un pedido

Los usuarios administrador tienen la capacidad de:
- Acceder a la administración de Modelos, materiales, materiales asignados a modelos y usuarios.
- Acceso al CRUD de todos los registros mencionados anteriormente.

Los usuarios que no ingresen con una cuenta pueden:
- Realizar pedidos anónimos únicamente con los modelos del catalogo.
- Buscar pedidos realizados en base al Id del pedido

### Guia de instalación
Se debe tener instalado `Python 8` para ejecutar el servidor. MySQL Server instalado y configurado.
- Dentro de un CMD, ingresar la siguiente secuencia de comandos dentro de la carpeta del proyecto.
```
    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    deactivate
    mysql -u root -p
    [contraseña]
    source src\PrintOnDemandDatabase.sql
    exit
    env\Scripts\activate
    python src\app.py
```
Esto es en caso de ser primera instalación.
A partir de aqui, el servidor puede iniciarse al activar el entorno virtual y ejecutar `app.py`.
