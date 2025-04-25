import qrcode
from datetime import datetime
import os

def generate_qr():
    while True:
        # Solicitar URL o texto al usuario
        url = input("\nIngrese la URL o texto para generar el QR (o 'salir' para terminar): ")
        
        if url.lower() == 'salir':
            print("¡Hasta luego!")
            break
            
        if not url.strip():
            print("Por favor, ingrese una URL o texto válido.")
            continue
        
        # Solicitar nombre personalizado para el archivo
        custom_name = input("\nIngrese el nombre para guardar el archivo QR (sin extensión): ")
        
        if not custom_name.strip():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"qr_{timestamp}.png"
            print("Nombre no proporcionado, se usará un nombre automático.")
        else:
            # Limpiar el nombre del archivo de caracteres no permitidos
            custom_name = "".join(c for c in custom_name if c.isalnum() or c in (' ', '-', '_'))
            filename = f"{custom_name}.png"
            
        try:
            # Crear el objeto QR
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            
            # Agregar los datos
            qr.add_data(url)
            qr.make(fit=True)
            
            # Crear la imagen
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Crear directorio para QRs si no existe
            if not os.path.exists('qr_codes'):
                os.makedirs('qr_codes')
            
            # Ruta completa del archivo
            full_path = os.path.join('qr_codes', filename)
            
            # Verificar si el archivo ya existe
            counter = 1
            while os.path.exists(full_path):
                name, ext = os.path.splitext(filename)
                filename = f"{name}_{counter}{ext}"
                full_path = os.path.join('qr_codes', filename)
                counter += 1
            
            # Guardar la imagen
            qr_image.save(full_path)
            print(f"\n✅ Código QR generado exitosamente y guardado como: {full_path}")
            
            # Preguntar si quiere generar otro
            continuar = input("\n¿Desea generar otro código QR? (s/n): ")
            if continuar.lower() != 's':
                print("¡Hasta luego!")
                break
                
        except Exception as e:
            print(f"\n❌ Error al generar el código QR: {str(e)}")
            print("Por favor, intente nuevamente.")

if __name__ == "__main__":
    print("=== Generador de Códigos QR ===")
    print("Escriba 'salir' en cualquier momento para terminar el programa")
    generate_qr()