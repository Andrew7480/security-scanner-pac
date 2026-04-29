# security-scanner-pac

## Descripción

**security-scanner-pac** es una herramienta para escanear proyectos en busca de archivos y contenidos potencialmente inseguros, basada en políticas configurables y fácilmente extensible.

## Justificación y Marco Teórico

La exposición accidental de contraseñas, claves privadas y otra información sensible dentro del código fuente representa una de las vulnerabilidades más comunes en el desarrollo de software. Este proyecto surge para demostrar cómo la seguridad puede integrarse directamente en el proceso de desarrollo mediante enfoques automatizados, aplicando el paradigma de "Policy as Code" (PaC) y el principio de "Shift Left" en DevSecOps.

Puedes consultar el documento completo con toda la teoría y justificación aquí:

1. [Justificación y Marco Teórico del Proyecto](https://pruebacorreoescuelaingeduco-my.sharepoint.com/:w:/g/personal/andres_cardozo-m_mail_escuelaing_edu_co/IQD3YREPCx0MQ6D38vMMeQDsAVGpAF3P8Z0GIh48NKdF4DU?e=9IhLpY)

### Resumen de la teoría

- **Security as Code (SaC):** Define y ejecuta controles de seguridad mediante código, permitiendo automatización, trazabilidad y consistencia.
- **Policy as Code (PaC):** Expresa políticas de seguridad como reglas programables evaluadas automáticamente.
- **Automatización de controles:** Permite validar seguridad en pipelines CI/CD y detectar secretos antes de producción.
- **Shift Left:** Lleva la seguridad a etapas tempranas del desarrollo, reduciendo costos y riesgos.
- **DevSecOps:** Integra la seguridad como parte continua y compartida en el ciclo de desarrollo.

El escáner implementa políticas como:
- Bloqueo de palabras sensibles (ej: password, SECRET_KEY)
- Bloqueo de archivos de configuración sensibles (.env)
- Restricción de tamaño de archivos

La arquitectura es modular y fácilmente integrable en pipelines CI/CD, permitiendo extender reglas sin modificar el código base.


## ¿Qué hace?

- Busca extensiones de archivo prohibidas (ej: `.env`)
- Detecta palabras sensibles en el contenido de los archivos (ej: `password`, `SECRET_KEY`)
- Verifica que los archivos no excedan un tamaño máximo definido
- Reporta los hallazgos con nivel de riesgo (CRITICAL, HIGH, MEDIUM)

## Estructura del proyecto

- `scanner/scanner.py`: Script principal del escáner.
- `policies.json`: Políticas de seguridad (palabras, extensiones y tamaño máximo).
- `test_project/`: Carpeta de ejemplo para pruebas.
- `docs/images/firstTest.png`: Imagen de ejemplo de la ejecución.

## Uso

1. Asegúrate de tener Python instalado.
2. Ejecuta el escáner desde la raíz del proyecto:

	```
	python scanner/scanner.py
	```

3. Ingresa la ruta del directorio a escanear, por ejemplo:

	```
	test_project/
	```

## Historial de versiones

### Versión 4 — Reporte automático en JSON

**¿Qué se agregó?**

- Al finalizar cada escaneo, se genera automáticamente un archivo `report.json` con todos los hallazgos en formato estructurado.
- Se muestra un mensaje en consola indicando la generación del reporte.
- Permite guardar evidencia, compartir resultados y facilitar la integración con otras herramientas.

**¿Por qué estos cambios?**

- Generar reportes automáticos es una práctica estándar en la industria, útil para auditorías, CI/CD y trazabilidad.
- Facilita la revisión y el análisis posterior de los resultados.

**Ejemplo de archivos generados:**

![Mensaje](docs/images/GuardaReport.png)
![Archivo generado](docs/images/exampleReport.png)

**Mensaje en consola:**

```
📁 Reporte generado: report.json
```

![](docs/images/GuardaReport.png)
![](docs/images/exampleReport.png)





### Versión 3 — SCA: Detección de dependencias vulnerables

**¿Qué se agregó?**

- Análisis de dependencias (SCA, Software Composition Analysis):
	- Detecta automáticamente dependencias vulnerables en archivos `requirements.txt`.
	- Utiliza una base de datos simulada (`vuln_db.json`) para identificar versiones inseguras.
- Reporta dependencias vulnerables como hallazgos CRITICAL en el escaneo.

**¿Por qué estos cambios?**

- El análisis SCA permite identificar riesgos en librerías de terceros, una de las fuentes más frecuentes de vulnerabilidades en proyectos modernos.
- Facilita la detección temprana de componentes inseguros antes de que lleguen a producción.

**Ejemplo de archivos:**

`test_project/3version`
```txt
flask==1.0
requests==2.25.0
```

`vuln_db.json`
```json
{
	"flask": ["1.0"],
	"requests": ["2.25.0"]
}
```

**Ejemplo de resultado:**
![Ejecución de ejemplo](docs/images/thirdTest.png)





### Versión 2 — SAST básico y visual mejorado

**¿Qué se agregó?**

- Detección de funciones peligrosas en código fuente (SAST básico): eval(), exec(), etc.
- Nueva política: `dangerous_functions` en policies.json
- Salida visual profesional: colores y emojis según nivel de riesgo
- Leyenda visual explicando los colores y niveles

**¿Por qué estos cambios?**

- El análisis SAST (Static Application Security Testing) permite detectar patrones de código inseguros, no solo secretos expuestos.
- Mejorar la experiencia del usuario y la interpretación de resultados con una salida visual clara y profesional.

**Ejemplo de política extendida:**

```json
{
	"forbidden_words": ["password", "SECRET_KEY"],
	"forbidden_extensions": [".env"],
	"max_file_size": 5000,
	"dangerous_functions": ["eval(", "exec("]
}
```

**Ejemplo de resultado:**

![Ejecución de ejemplo](docs/images/secondTest.png)

---

### Versión 1 — Detección básica de secretos

**¿Qué hace?**

- Busca extensiones de archivo prohibidas (ej: `.env`)
- Detecta palabras sensibles en el contenido de los archivos (ej: `password`, `SECRET_KEY`)
- Verifica que los archivos no excedan un tamaño máximo definido
- Reporta los hallazgos con nivel de riesgo (CRITICAL, HIGH, MEDIUM)

**¿Por qué?**

La exposición accidental de contraseñas, claves privadas y otra información sensible dentro del código fuente es una de las vulnerabilidades más comunes. Esta versión demuestra cómo la seguridad puede integrarse en el desarrollo mediante reglas automatizadas y configurables (Policy as Code).

**Ejemplo de políticas (`policies.json`):**

```json
{
	"forbidden_words": ["password", "SECRET_KEY"],
	"forbidden_extensions": [".env"],
	"max_file_size": 5000
}
```

**Ejemplo de resultado:**

![Ejecución de ejemplo](docs/images/firstTest.png)

---