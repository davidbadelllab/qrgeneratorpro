import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os
from PIL import Image, ImageTk
import qrcode
from fpdf import FPDF
from pathlib import Path

class ModernQRApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("QR Code Generator Pro")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # Variables de estado
        self.current_step = 0
        self.input_file = tk.StringVar()
        self.logo_file = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.pdf_name = tk.StringVar(value="output.pdf")
        self.logo_size = tk.IntVar(value=30)
        
        # Configurar el tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Crear layout principal
        self.setup_layout()
        self.create_sidebar()
        self.create_main_frames()
        
        # Mostrar el primer frame
        self.show_frame(0)
        
    def setup_layout(self):
        # Grid layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
    def create_sidebar(self):
        # Frame de la barra lateral
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        # Logo y título
        self.logo_label = ctk.CTkLabel(self.sidebar, text="QR Generator", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Botones de navegación
        self.nav_buttons = []
        steps = [
            ("📁 Input File", "Seleccionar archivo TXT"),
            ("🖼️ Logo Setup", "Configurar logo"),
            ("💾 Output Config", "Configurar salida"),
            ("✨ Generate", "Generar códigos QR")
        ]
        
        for i, (text, tooltip) in enumerate(steps):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=lambda x=i: self.show_frame(x),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                height=40
            )
            btn.grid(row=i+1, column=0, padx=20, pady=10)
            self.nav_buttons.append(btn)
            
        # Selector de tema
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode
        )
        self.appearance_mode_menu.grid(row=8, column=0, padx=20, pady=20, sticky="s")
        
    def create_main_frames(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Frames para cada paso
        self.frames = []
        
        # Frame 1: Selección de archivo
        input_frame = ctk.CTkFrame(self.main_frame)
        self.create_input_frame(input_frame)
        self.frames.append(input_frame)
        
        # Frame 2: Configuración de logo
        logo_frame = ctk.CTkFrame(self.main_frame)
        self.create_logo_frame(logo_frame)
        self.frames.append(logo_frame)
        
        # Frame 3: Configuración de salida
        output_frame = ctk.CTkFrame(self.main_frame)
        self.create_output_frame(output_frame)
        self.frames.append(output_frame)
        
        # Frame 4: Generación
        generate_frame = ctk.CTkFrame(self.main_frame)
        self.create_generate_frame(generate_frame)
        self.frames.append(generate_frame)
        
    def create_input_frame(self, parent):
        # Título
        title = ctk.CTkLabel(parent, text="Seleccionar Archivo TXT", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Frame para selección de archivo
        file_frame = ctk.CTkFrame(parent)
        file_frame.pack(fill="x", padx=30, pady=10)
        
        input_entry = ctk.CTkEntry(
            file_frame,
            placeholder_text="Seleccione archivo TXT...",
            textvariable=self.input_file,
            width=400
        )
        input_entry.pack(side="left", padx=(20, 10), pady=20, fill="x", expand=True)
        
        browse_button = ctk.CTkButton(
            file_frame,
            text="Buscar",
            command=self.browse_input_file
        )
        browse_button.pack(side="right", padx=20, pady=20)
        
        # Información
        info_text = """
        📋 Formato requerido:
        El archivo TXT debe contener entradas en el siguiente formato:

        Nombre: Título del QR
        Link: https://tu-url-aqui.com

        Asegúrese de que cada entrada siga exactamente este formato.
        """
        info_label = ctk.CTkLabel(parent, text=info_text, justify="left")
        info_label.pack(pady=20)
        
    def create_logo_frame(self, parent):
        # Título
        title = ctk.CTkLabel(parent, text="Configuración del Logo", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Frame para selección de logo
        logo_frame = ctk.CTkFrame(parent)
        logo_frame.pack(fill="x", padx=30, pady=10)
        
        logo_entry = ctk.CTkEntry(
            logo_frame,
            placeholder_text="Seleccione archivo de logo...",
            textvariable=self.logo_file,
            width=400
        )
        logo_entry.pack(side="left", padx=(20, 10), pady=20, fill="x", expand=True)
        
        browse_button = ctk.CTkButton(
            logo_frame,
            text="Buscar",
            command=self.browse_logo_file
        )
        browse_button.pack(side="right", padx=20, pady=20)
        
        # Control de tamaño del logo
        size_frame = ctk.CTkFrame(parent)
        size_frame.pack(fill="x", padx=30, pady=10)
        
        size_label = ctk.CTkLabel(size_frame, text="Tamaño del logo (%)")
        size_label.pack(pady=5)
        
        size_slider = ctk.CTkSlider(
            size_frame,
            from_=10,
            to=50,
            variable=self.logo_size,
            number_of_steps=40
        )
        size_slider.pack(pady=5, fill="x", padx=20)
        
        # Preview frame (placeholder)
        preview_frame = ctk.CTkFrame(parent, height=200)
        preview_frame.pack(fill="x", padx=30, pady=20)
        
        preview_label = ctk.CTkLabel(preview_frame, text="Vista previa del logo")
        preview_label.pack(pady=10)
        
    def create_output_frame(self, parent):
        # Título
        title = ctk.CTkLabel(parent, text="Configuración de Salida", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Frame para nombre del PDF
        name_frame = ctk.CTkFrame(parent)
        name_frame.pack(fill="x", padx=30, pady=10)
        
        name_label = ctk.CTkLabel(name_frame, text="Nombre del archivo PDF:")
        name_label.pack(pady=5)
        
        name_entry = ctk.CTkEntry(
            name_frame,
            textvariable=self.pdf_name,
            placeholder_text="output.pdf"
        )
        name_entry.pack(pady=5, fill="x", padx=20)
        
        # Frame para directorio de salida
        output_frame = ctk.CTkFrame(parent)
        output_frame.pack(fill="x", padx=30, pady=10)
        
        output_entry = ctk.CTkEntry(
            output_frame,
            placeholder_text="Seleccione directorio de salida...",
            textvariable=self.output_dir,
            width=400
        )
        output_entry.pack(side="left", padx=(20, 10), pady=20, fill="x", expand=True)
        
        browse_button = ctk.CTkButton(
            output_frame,
            text="Buscar",
            command=self.browse_output_dir
        )
        browse_button.pack(side="right", padx=20, pady=20)
        
    def create_generate_frame(self, parent):
        # Título
        title = ctk.CTkLabel(parent, text="Generar Códigos QR", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        # Resumen de configuración
        summary_frame = ctk.CTkFrame(parent)
        summary_frame.pack(fill="x", padx=30, pady=10)
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="Resumen de Configuración",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        summary_title.pack(pady=10)
        
        self.summary_text = ctk.CTkTextbox(summary_frame, height=150)
        self.summary_text.pack(padx=20, pady=10, fill="x")
        
        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(parent)
        self.progress_bar.pack(fill="x", padx=30, pady=20)
        self.progress_bar.set(0)
        
        # Botón de generación
        generate_button = ctk.CTkButton(
            parent,
            text="Generar Códigos QR",
            command=self.generate_qr_codes,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        generate_button.pack(pady=20)
        
    def show_frame(self, frame_index):
        # Actualizar botones de navegación
        for i, button in enumerate(self.nav_buttons):
            if i == frame_index:
                button.configure(fg_color=("gray75", "gray25"))
            else:
                button.configure(fg_color="transparent")
        
        # Ocultar todos los frames
        for frame in self.frames:
            frame.grid_forget()
        
        # Mostrar el frame seleccionado
        self.frames[frame_index].grid(row=0, column=0, sticky="nsew")
        self.current_step = frame_index
        
        # Actualizar resumen si estamos en el último paso
        if frame_index == 3:
            self.update_summary()
    
    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo TXT",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if filename:
            self.input_file.set(filename)
    
    def browse_logo_file(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar logo",
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if filename:
            self.logo_file.set(filename)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Seleccionar directorio de salida")
        if directory:
            self.output_dir.set(directory)
    
    def update_summary(self):
        summary = f"""
📁 Archivo TXT: {self.input_file.get() or 'No seleccionado'}

🖼️ Logo: {self.logo_file.get() or 'No seleccionado'}
📏 Tamaño del logo: {self.logo_size.get()}%

💾 Directorio de salida: {self.output_dir.get() or 'No seleccionado'}
📄 Nombre del PDF: {self.pdf_name.get()}
        """
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert("1.0", summary)
    
    def generate_qr_codes(self):
        # Validar entradas
        if not self.input_file.get():
            messagebox.showerror("Error", "Por favor seleccione un archivo TXT")
            return
        if not self.output_dir.get():
            messagebox.showerror("Error", "Por favor seleccione un directorio de salida")
            return
        if not self.pdf_name.get():
            messagebox.showerror("Error", "Por favor ingrese un nombre para el PDF")
            return

        try:
            # Leer archivo TXT
            with open(self.input_file.get(), 'r', encoding='utf-8') as f:
                content = f.read()

            # Procesar contenido
            lines = [line.strip() for line in content.splitlines() if line.strip()]
            data = []
            current_name = None

            for line in lines:
                if line.startswith("Nombre:"):
                    current_name = line[7:].strip()
                elif line.startswith("Link:") and current_name:
                    link = line[5:].strip()
                    if current_name and link:
                        data.append((current_name, link))
                        current_name = None

            if not data:
                messagebox.showerror("Error", "No se encontraron pares válidos de Nombre/Link en el archivo")
                return

            # Crear PDF
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)

            # Configurar progreso
            total_steps = len(data)
            self.progress_bar.set(0)

            # Primera página con logo si existe
            pdf.add_page()
            if self.logo_file.get():
                try:
                    # Procesar logo
                    with Image.open(self.logo_file.get()) as img:
                        if img.mode in ('RGBA', 'LA'):
                            background = Image.new('RGB', img.size, (255, 255, 255))
                            background.paste(img, mask=img.split()[-1])
                            img = background
                        elif img.mode != 'RGB':
                            img = img.convert('RGB')
                        
                        # Guardar temporalmente
                        temp_logo = "temp_logo.png"
                        img.save(temp_logo)
                        
                        # Añadir al PDF
                        page_width = pdf.w
                        logo_width = page_width * (self.logo_size.get() / 100)
                        x_centered = (page_width - logo_width) / 2
                        pdf.image(temp_logo, x=x_centered, y=10, w=logo_width)
                        
                        # Añadir espacio después del logo (reducido)
                        pdf.ln(logo_width + 10)  # Reducido de 20 a 10 unidades
                        
                        # Limpiar
                        os.remove(temp_logo)
                except Exception as e:
                    messagebox.showwarning("Advertencia", 
                        "No se pudo incluir el logo, pero se continuará con la generación del PDF")

            # Generar QRs
            for i, (name, url) in enumerate(data):
                if i % 2 == 0 and i != 0:
                    pdf.add_page()

                # Calcular posición Y
                if i % 2 == 0:
                    current_y = pdf.get_y()
                else:
                    current_y = pdf.get_y() + 10

                # Añadir nombre y link
                pdf.set_font('Arial', 'B', 11)
                pdf.set_xy(10, current_y)
                pdf.cell(0, 8, f"Nombre: {name}", 0, 1, 'C')
                
                pdf.set_font('Arial', '', 10)
                pdf.set_xy(10, current_y + 8)
                pdf.cell(0, 8, f"Link: {url}", 0, 1, 'C')

                # Generar QR
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_H,
                    box_size=12,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)

                qr_img = qr.make_image(fill_color="black", back_color="white")
                temp_qr = f"temp_qr_{i}.png"
                qr_img.save(temp_qr)

                # Añadir QR al PDF
                pdf.set_xy(10, current_y + 16)
                pdf.cell(0, 8, "QR:", 0, 1, 'C')

                qr_width = 70
                x_centered = (page_width - qr_width) / 2
                pdf.image(temp_qr, x=x_centered, y=current_y + 24, w=qr_width)

                # Limpiar y actualizar progreso
                os.remove(temp_qr)
                self.progress_bar.set((i + 1) / total_steps)
                self.update()

                pdf.set_y(current_y + 95)

            # Guardar PDF
            pdf_path = os.path.join(self.output_dir.get(), self.pdf_name.get())
            if not pdf_path.lower().endswith('.pdf'):
                pdf_path += '.pdf'

            pdf.output(pdf_path)
            self.progress_bar.set(1)
            messagebox.showinfo("Éxito", 
                f"PDF generado exitosamente\nArchivo: {os.path.basename(pdf_path)}\n"
                f"Se procesaron {len(data)} códigos QR")

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el PDF: {str(e)}")
            self.progress_bar.set(0)

if __name__ == "__main__":
    app = ModernQRApp()
    app.mainloop()
