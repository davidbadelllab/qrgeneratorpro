from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # Crear una imagen cuadrada
    size = (256, 256)
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Dibujar un círculo como fondo
    margin = 10
    draw.ellipse([margin, margin, size[0]-margin, size[1]-margin], 
                 fill='#2B60DE')  # Azul
    
    # Dibujar un QR estilizado
    qr_size = 120
    qr_pos = ((size[0] - qr_size) // 2, (size[1] - qr_size) // 2)
    
    # Dibujar un QR simplificado (cuadrados blancos)
    square_size = qr_size // 4
    for i in range(3):
        for j in range(3):
            if (i == 0 and j == 0) or (i == 0 and j == 2) or (i == 2 and j == 0):
                # Dibujar los cuadrados de posición del QR
                draw.rectangle([
                    qr_pos[0] + i * square_size,
                    qr_pos[1] + j * square_size,
                    qr_pos[0] + (i + 1) * square_size,
                    qr_pos[1] + (j + 1) * square_size
                ], fill='white')
    
    # Guardar como ICO
    image.save('icon.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_icon() 