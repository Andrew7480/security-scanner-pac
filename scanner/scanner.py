import os
import json

# Cargar políticas
def load_policies():
    with open("policies.json", "r") as f:
        return json.load(f)

# Leer archivos
def get_files(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

# Analizar archivos
def scan_file(file_path, policies):
    findings = []

    # Validar extensión prohibida
    for ext in policies["forbidden_extensions"]:
        if file_path.endswith(ext):
            findings.append({
                "file": file_path,
                "risk": "CRITICAL",
                "message": f"Archivo prohibido ({ext})"
            })

    # Validar tamaño
    size = os.path.getsize(file_path)
    if size > policies["max_file_size"]:
        findings.append({
            "file": file_path,
            "risk": "MEDIUM",
            "message": "Archivo supera tamaño permitido"
        })


    # Leer contenido
    try:
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()

            # Detectar palabras sensibles
            for word in policies["forbidden_words"]:
                if word in content:
                    findings.append({
                        "file": file_path,
                        "risk": "HIGH",
                        "message": f"Palabra sensible detectada: {word}"
                    })

            # Detectar funciones peligrosas (SAST básico)
            for func in policies.get("dangerous_functions", []):
                if func in content:
                    findings.append({
                        "file": file_path,
                        "risk": "HIGH",
                        "message": f"Uso de función peligrosa: {func}"
                    })

    except:
        pass

    return findings

# Ejecutar escaneo
def run_scan(directory):
    policies = load_policies()
    files = get_files(directory)

    all_findings = []

    for file in files:
        results = scan_file(file, policies)
        all_findings.extend(results)

    return all_findings

# Main
if __name__ == "__main__":
    path = input("Ruta a escanear: ")
    findings = run_scan(path)

    # Colores ANSI
    COLORS = {
        "CRITICAL": "\033[91m",  # Rojo fuerte
        "HIGH": "\033[31m",      # Rojo estándar
        "MEDIUM": "\033[93m",    # Amarillo
        "LOW": "\033[94m",       # Azul
        "END": "\033[0m"
    }

    ICONS = {
        "CRITICAL": "🛑",
        "HIGH": "⚠️",
        "MEDIUM": "🔶",
        "LOW": "🔹"
    }

    if not findings:
        print("\033[92m✅ No se encontraron problemas\033[0m")
    else:
        print("\n🚨 \033[1mResultados del escaneo:\033[0m\n")        
        for f in findings:
            risk = f["risk"].upper()
            color = COLORS.get(risk, "")
            icon = ICONS.get(risk, "")
            print(f"{icon} {color}[{risk}]{COLORS['END']} {f['file']} -> {f['message']}")
