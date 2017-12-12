# remote-execution

Ejecutar software remotamente con python3

## inicio

CMD y powershell:

```batch
python main.py
```

## uso

Ingresa al navegador con:
http://mi.ip:5000/
O en terminal:

```bash
curl -X POST -F 'username=admin' -F 'password=secret' http://localhost:5000/execute
```

## referencias

- https://github.com/juusechec/reportes-python/blob/master/webservice.py
