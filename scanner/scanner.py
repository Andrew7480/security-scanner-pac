
import os
import json
import sys

# Cargar políticas
def load_policies():
    with open("policies.json", "r") as f:
        return json.load(f)
# SCA: Escaneo de dependencias vulnerables
def scan_dependencies(file_path):
    findings = []

    if file_path.endswith("requirements.txt"):
        with open(file_path, "r") as f:
            deps = f.readlines()

        with open("vuln_db.json", "r") as v:
            vuln_db = json.load(v)

        for dep in deps:
            if "==" in dep:
                name, version = dep.strip().split("==")
                if name in vuln_db and version in vuln_db[name]:
                    findings.append({
                        "file": file_path,
                        "risk": "CRITICAL",
                        "message": f"Dependencia vulnerable: {name} {version}"
                    })

    return findings
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
        import re
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()

            # Detectar credenciales hardcodeadas (regex)
            for word in policies["forbidden_words"]:
                pattern = rf"{word}\s*=\s*['\"].+['\"]"
                if re.search(pattern, content, re.IGNORECASE):
                    findings.append({
                        "file": file_path,
                        "risk": "HIGH",
                        "message": f"Credencial hardcodeada detectada: {word}"
                    })

            # Detectar funciones peligrosas (SAST básico)
            for func in policies.get("dangerous_functions", []):
                if func.lower() in content.lower():
                    findings.append({
                        "file": file_path,
                        "risk": "HIGH",
                        "message": f"Uso de función peligrosa: {func}"
                    })

    except:
        pass

    return findings
# Generar reporte SARIF
def generate_sarif(findings):
    sarif = {
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "Custom Security Scanner",
                        "rules": []
                    }
                },
                "results": []
            }
        ]
    }

    for f in findings:
        sarif["runs"][0]["results"].append({
            "ruleId": f["risk"],
            "message": {"text": f["message"]},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {
                            "uri": f["file"]
                        }
                    }
                }
            ]
        })

    with open("report.sarif", "w") as f:
        json.dump(sarif, f, indent=4)
        
# Ejecutar escaneo
def run_scan(directory):
    policies = load_policies()
    files = get_files(directory)

    all_findings = []

    for file in files:
        results = scan_file(file, policies)
        dep_results = scan_dependencies(file)

        all_findings.extend(results)
        all_findings.extend(dep_results)

    return all_findings

# Main
if __name__ == "__main__":

    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
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


    # Guardar reporte en JSON
    with open("report.json", "w") as f:
        json.dump(findings, f, indent=4)
    print("\n📁 Reporte generado: report.json")

    # Guardar reporte en SARIF
    generate_sarif(findings)
    print("📁 Reporte SARIF generado: report.sarif")
