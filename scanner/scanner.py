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

            for word in policies["forbidden_words"]:
                if word in content:
                    findings.append({
                        "file": file_path,
                        "risk": "HIGH",
                        "message": f"Palabra sensible detectada: {word}"
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

    if not findings:
        print("✅ No se encontraron problemas")
    else:
        print("\n🚨 Resultados:")
        for f in findings:
            print(f"[{f['risk']}] {f['file']} -> {f['message']}")
