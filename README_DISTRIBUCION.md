# Guía de Distribución y Uso del Security Scanner

Este documento explica cómo replicar e integrar el escáner de seguridad en cualquier proyecto Python, siguiendo buenas prácticas de la industria.

---

## 1. Crear archivo de políticas

Crea un archivo `policies.json` en la raíz del proyecto con las reglas de seguridad. Ejemplo:

```json
{
  "forbidden_words": ["password", "SECRET_KEY"],
  "forbidden_extensions": [".env"],
  "max_file_size": 5000,
  "dangerous_functions": ["eval(", "exec("]
}
```

---

## 2. Agregar el código del escáner

Copia el archivo `scanner/scanner.py` en tu proyecto. Ejemplo de estructura:

```
scanner/
  scanner.py
policies.json
```

Puedes adaptar el código según tus necesidades. El escáner soporta:
- Detección de secretos y credenciales hardcodeadas
- Detección de funciones peligrosas
- SCA (dependencias vulnerables)
- Reporte JSON y SARIF
- Reducción de falsos positivos (regex)


---

## 3. Configurar el workflow de CI/CD (opcional pero recomendado)

Crea el archivo `.github/workflows/security-scan.yml` con el siguiente contenido:

```yaml
name: Security Scan

on:
  push:
  pull_request:

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - name: Clonar repositorio
        uses: actions/checkout@v3
      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Ejecutar Scanner
        run: |
          python scanner/scanner.py ./directorio_a_escanear
      - name: Subir resultados SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: report.sarif
      - name: Validar resultados
        run: |
          if grep -q "CRITICAL" report.json; then
            echo "❌ Vulnerabilidades críticas encontradas"
            exit 1
          else
            echo "✅ Sin vulnerabilidades críticas"
          fi
```

Ajusta `./directorio_a_escanear` según tu estructura.

---

## 4. (Opcional) Configurar pre-commit hook para máxima protección

Crea el archivo `.git/hooks/pre-commit` con:

```bash
#!/bin/bash
python scanner/scanner.py ./directorio_a_escanear
if grep -q "CRITICAL" report.json; then
    echo "❌ Commit bloqueado por vulnerabilidades críticas"
    exit 1
fi
echo "✅ Commit permitido"
```

Dale permisos de ejecución (en Linux/Mac):

```bash
chmod +x .git/hooks/pre-commit
```

---

## 5. (Opcional) Personaliza tus políticas

Edita `policies.json` para agregar/quitar palabras, extensiones, tamaño máximo, o funciones peligrosas según las necesidades de tu proyecto.

---

## 6. ¡Listo!

- El escáner funciona tanto en modo manual como automático (CI/CD y pre-commit).
- Los reportes se generan en JSON y SARIF para máxima compatibilidad.
- Puedes integrar y distribuir este flujo en cualquier proyecto Python.

---

¿Dudas o mejoras? ¡Adapta el flujo a tu equipo y comparte buenas prácticas!
