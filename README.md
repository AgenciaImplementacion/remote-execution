# remote-execution

Ejecutar software remotamente con python3

## ejecución

CMD:

```batch
set FLASK_APP=main.py
set FLASK_DEBUG=1
flask run --host=0.0.0.0
```

Powershell:

```powershell
$env:FLASK_APP = "main.py"
$env:FLASK_DEBUG = "1"
flask run --host=0.0.0.0
```

## referencias

- https://github.com/juusechec/reportes-python/blob/master/webservice.py
