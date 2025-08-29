from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import re
from werkzeug.utils import secure_filename
from ClasePrincipal import ClasePrincipal
from datosapp import ContadorCalorias

# Configuración
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "cambia_esto_por_algo_mas_seguro"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    url = request.form.get('image_url', '').strip()
    file = request.files.get('image_file')

    if not url and (not file or file.filename == ''):
        flash('Selecciona una imagen o introduce una URL.', 'error')
        return redirect(url_for('index'))

    image_path = None

    # Guardar archivo si lo suben
    if file and file.filename != '':
        if not allowed_file(file.filename):
            flash('Tipo de archivo no permitido.', 'error')
            return redirect(url_for('index'))
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)
    else:
        image_path = url  # Si se pasa URL

    try:
        principal = ClasePrincipal(image_path)
        principal.obtener_texto_imagen()
        principal.obtener_resultado_final()

        texto = principal.resultado_final
        resultado = principal.calorias

        # Extraer número después de </think>
        resultado_str = str(resultado)
        match = re.search(r"</think>\s*(\d+)", resultado_str)
        calorias = match.group(1) if match else "No encontrado"

        total_calorias = ContadorCalorias.obtener_total_calorias_consumidas()

        return render_template(
            "index.html",
            texto_generado=texto,
            respuesta_modelo=resultado,
            calorias_detectadas=calorias,
            total_calorias=total_calorias,
            image_filename=os.path.basename(image_path) if image_path and image_path.startswith("uploads") else None,
            image_url=image_path if image_path and not image_path.startswith("uploads") else None,
        )
    except Exception as e:
        import traceback
        flash(f"Error al procesar la imagen: {e}\n{traceback.format_exc()}", "error")
        return redirect(url_for("index"))


# Servir imágenes subidas
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
