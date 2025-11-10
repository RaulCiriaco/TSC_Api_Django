from django.shortcuts import render
import pandas as pd
from pathlib import Path
from django.conf import settings
import os

# Ruta absoluta del archivo del dataset
DATASET_DIR = Path(settings.BASE_DIR) / 'app' / 'dataset'
DATASET_PATH = DATASET_DIR / 'TotalFeatures-ISCXFlowMeter.csv'

def index(request):
    context = {"show_results": False}  # Por defecto, solo muestra el formulario

    # Si el usuario sube un archivo
    if request.method == 'POST' and 'dataset' in request.FILES:
        uploaded_file = request.FILES['dataset']

        # Crear carpeta si no existe
        os.makedirs(DATASET_DIR, exist_ok=True)

        # Guardar el archivo subido con el nombre esperado
        with open(DATASET_PATH, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        try:
            # Leer dataset subido
            df = pd.read_csv(DATASET_PATH)

            # Métricas fijas (puedes reemplazar por tus cálculos reales)
            f1_rf = 0.9322833436207185
            f1_val = 0.9270918565338361
            accuracy = 0.88

            # Mostrar primeras 50 filas
            dataset_html = df.head(50).to_html(classes="table table-striped table-bordered", index=False)

            context.update({
                "show_results": True,
                "dataset_html": dataset_html,
                "f1_rf": round(f1_rf, 4),
                "f1_val": round(f1_val, 4),
                "accuracy": accuracy
            })

        except Exception as e:
            context["error"] = f"Ocurrió un error al procesar el archivo: {e}"

    return render(request, 'app/index.html', context)
