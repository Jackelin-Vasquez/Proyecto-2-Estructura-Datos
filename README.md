# Proyecto-2-Estructura-Datos

## Usuarios y acceso

Las credenciales no están en el código. Antes del primer inicio de sesión hay que
crear un usuario (se guarda con PBKDF2-HMAC-SHA256 en `Datos/usuarios.json`, archivo
ignorado por git):

```
python -m Datos.auth crear-usuario admin
```

Luego se ejecuta la aplicación con `python Interfaz/ventana_login.py`.