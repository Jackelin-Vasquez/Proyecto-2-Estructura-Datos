"""Autenticación de usuarios basada en hashes PBKDF2-HMAC-SHA256.

Las credenciales se guardan en `usuarios.json` (fuera del control de versiones),
nunca en el código fuente. Para crear o actualizar un usuario:

    python -m Datos.auth crear-usuario admin
"""
import getpass
import hashlib
import hmac
import json
import os
import secrets
import sys

ITERACIONES = 240_000
LONGITUD_SAL = 16
ARCHIVO_USUARIOS = os.environ.get(
    "ARBOLES_ARCHIVO_USUARIOS",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "usuarios.json"),
)


def _derivar(contrasena, sal, iteraciones):
    return hashlib.pbkdf2_hmac("sha256", contrasena.encode("utf-8"), sal, iteraciones)


def crear_registro(contrasena, iteraciones=ITERACIONES):
    sal = secrets.token_bytes(LONGITUD_SAL)
    return {
        "algoritmo": "pbkdf2_sha256",
        "iteraciones": iteraciones,
        "sal": sal.hex(),
        "hash": _derivar(contrasena, sal, iteraciones).hex(),
    }


def cargar_usuarios(ruta=ARCHIVO_USUARIOS):
    if not os.path.exists(ruta):
        return {}
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_usuario(usuario, contrasena, ruta=ARCHIVO_USUARIOS):
    usuarios = cargar_usuarios(ruta)
    usuarios[usuario] = crear_registro(contrasena)
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, ensure_ascii=False, indent=4)
    os.chmod(ruta, 0o600)


def verificar(usuario, contrasena, ruta=ARCHIVO_USUARIOS):
    """Devuelve True solo si el usuario existe y la contraseña coincide."""
    registro = cargar_usuarios(ruta).get(usuario)
    sal_falsa = secrets.token_bytes(LONGITUD_SAL)
    if registro is None:
        # Se deriva igual para no filtrar por tiempo si el usuario existe o no.
        _derivar(contrasena, sal_falsa, ITERACIONES)
        return False

    esperado = bytes.fromhex(registro["hash"])
    calculado = _derivar(
        contrasena,
        bytes.fromhex(registro["sal"]),
        int(registro.get("iteraciones", ITERACIONES)),
    )
    return hmac.compare_digest(esperado, calculado)


def _main(argv):
    if len(argv) != 3 or argv[1] != "crear-usuario":
        print("Uso: python -m Datos.auth crear-usuario <usuario>")
        return 1

    usuario = argv[2]
    contrasena = getpass.getpass("Contraseña: ")
    if len(contrasena) < 8:
        print("La contraseña debe tener al menos 8 caracteres.")
        return 1
    if contrasena != getpass.getpass("Repita la contraseña: "):
        print("Las contraseñas no coinciden.")
        return 1

    guardar_usuario(usuario, contrasena)
    print(f"Usuario '{usuario}' guardado en {ARCHIVO_USUARIOS}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
