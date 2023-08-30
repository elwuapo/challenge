## Descarga del repositorio
Descarga la solución del challenge que se encuentra en [`https://github.com/elwuapo/challenge.git`](https://github.com/elwuapo/challenge) y trabaja con la rama `main`

## Solución en local
Crea una un directorio virutal en la carpeta del proyecto con el siguiente comando:

=== "Windows"
    ```cmd
    python -m venv .env
    ```

=== "Mac & Linux"
    ```cmd
    python3 -m venv .env
    ```

Activa el entorno virtual

=== "Windows"
    ```cmd
    .env/Scripts/activate
    ```

=== "Mac & Linux"
    ```cmd
    source .env/bin/activate
    ```

Ahora vamos a instalar las librerias necesarias para que se ejecute el proyecto

```
pip install -r ./ms1/requirements.txt
pip install -r ./ms2/requirements.txt
```

Recuerda tener creada tu instancia de base de datos local con postgres usando los siguientes parametros user: `nrivera` password: `password` db: `REPORTS` host: `localhost` port: `5432`

Vamos aplicar las migraciones con el orm de django para generar las tablas desde ms1.

```cmd
cd ms1/
python manage.py makemigrations
python manage.py migrate
```

Recuerda definir las variables de entorno en tu terminal

=== "Windows (PowerShell)"
    ```
    $Env:NAME = "REPORTS"
    $Env:USER = "nrivera"
    $Env:PASSWORD = "password"
    $Env:HOST = "localhost"
    $Env:PORT = "5432"
    $Env:MS1 = "http://127.0.0.1:7000/"
    ```
=== "Mac & Linux"
    ``` 
    export NAME = "REPORTS"
    export USER = "nrviera"
    export PASSWORD = "password"
    export HOST = "localhost"
    export PORT = "5432"
    export MS1 = "http://127.0.0.1:7000/"
    ```

Ahora vamos a levantar ms1,

```cmd
cd ms1/
python manage.py runserver 7000
```

Para levantar ms2

```cmd
cd ms2/
sanic server
```

cuando quieras salir derl entorno virtual solo escribe en la consola

```cmd
deactivate
```

## Deploy con docker

Vamos a detener y eliminar los contenedores, redes y volumenes relacionados al docker-compose.yml

=== "Mac"
    ```cmd
    docker-compose down -v
    ```

=== "Windows & Linux"
    ```cmd
    docker compose down -v
    ```

Ahora vamos a construir los contenedores y forzamos a construirlo desde 0

=== "Mac"
    ```cmd 
    docker-compose build --no-cache
    ```
=== "Windows & Linux"
    ```cmd
    docker compose build --no-cache
    ```

Ahora levantamos los contenedores en modo demonizado

=== "Mac"
    ```
    docker-compose up -d
    ```
=== "Windows & Linux"
    ```cmd
    docker compose up -d
    ```

Aplicamos las migraciones a la base de datos

=== "Mac"
    ```
    docker-compose run ms1 python manage.py makemigrations
    docker-compose run ms1 python manage.py migrate
    ```
=== "Windows & Linux"
    ```
    docker compose run ms1 python manage.py makemigrations
    docker compose run ms1 python manage.py migrate
    ```

## Endpoints
puedes ver los endpoint desarrollados [`aqui`](https://scm-latam.postman.co/workspace/My-Workspace~4125f99b-16dd-4d80-8345-94f9271ff31f/documentation/22918131-90aa1e7c-55cc-4520-8326-1faa168a8c1f) (solo visible para cuentas scmlatam)

## Ejecución de un reporte.
Vamos a crear un reporte

Asegurate de tener activado el enviroment `challenge` en postman

Ejecuta el endpoint `Create persons`, este enpoint se encargará de crear la mockdata de 10 personas en la base de datos, si quieres otra cantidad de elementos puedes cambiar el valor de amount en el body de la petición.

Luego ejecuta el endpoint `Create punches`, este endpoint creará las marcas de entrada y salida de los últimos 7 días para cada persona.

Para crear un reporte ejecuta el endpoint `Create report`, este endpoint empezará a crear el reporte para la persona con person_id 8, si deseas cambiar a la persona cambia el valor de person_id en el body, puedes visualizar los datos de las personas con el endpoint `Get persons`.

Para saber el estado de la ejecución del reporte puedes ejecutar el endpoint `Checking report status` y enviarle el por query_params el id del reporte.

Finalmente para visualizar el archivo del reporte puedes ejecutar el endpoint `Get report file`, la url del endpoint tiene la siguiente estructura `{{domain}}/static/reports/{{filename}}`, el filename te llegará en el response de `Create report`.

## Orden de pasos

- Create persons
- Create punches
- Get persons
- Create report
- Checking report status
- Get report file