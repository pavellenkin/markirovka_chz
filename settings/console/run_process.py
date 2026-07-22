import os
import subprocess
import shlex


def process(cmd, timeout=30):

    """Выполняет команду с проверкой и обработкой ошибок"""
    try:
        # Разбиваем команду на аргументы
        args = shlex.split(cmd) if isinstance(cmd, str) else cmd

        result = subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return {
            "success": True,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "returncode": e.returncode,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "error": str(e)
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": f"Команда не найдена: {cmd}"
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Таймаут выполнения ({timeout} сек)"
        }
