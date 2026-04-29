from scanner.scanner import run_scan
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: secscan <ruta>")
        sys.exit(1)

    path = sys.argv[1]
    findings = run_scan(path)

    if not findings:
        print("✅ Sin problemas")
    else:
        for f in findings:
            print(f"[{f['risk']}] {f['file']} -> {f['message']}")

if __name__ == "__main__":
    main()
