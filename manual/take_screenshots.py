"""
take_screenshots.py
Genera capturas del Conciliador v6.0 usando QWidget.grab().
Guarda las imágenes en: manual/images/
"""
import sys
import os
import datetime
import pandas as pd

# ── Rutas ────────────────────────────────────────────────────
BASE   = r"C:\Users\gus_j\.gemini\antigravity\scratch\conciliador_qt"
OUT    = r"C:\Users\gus_j\.gemini\antigravity\brain\cb1e1079-0145-4e5b-be93-7fada5f459a6\manual\images"
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, BASE)

# ── Qt ───────────────────────────────────────────────────────
sys.argv = ["screenshot_tool"]
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QTimer, QEventLoop
from PyQt6.QtGui import QPixmap

app = QApplication(sys.argv)
app.setStyle("Fusion")

import engine
import main_qt

app.setStyleSheet(main_qt.QSS)

# ── Helper ───────────────────────────────────────────────────
def process():
    """Fuerza varios ciclos del event loop para garantizar el render."""
    for _ in range(5):
        app.processEvents()

def grab(widget, filename, w=1400, h=860):
    widget.resize(w, h)
    widget.show()
    process()
    px = widget.grab()
    path = os.path.join(OUT, filename)
    px.save(path, "PNG")
    print(f"  [OK] {filename}  ({px.width()}×{px.height()})")

# ── Datos de muestra (EFIDEPORTE 2026) ───────────────────────
SAMPLE_ROWS = [
    {
        "Tipo": "Cotización Proveedor",
        "Fecha": "2026-01-15",
        "Rubro": "Caballerizas",
        "QT": "Sí", "T. Cambio": "MXN", "(+ IVA)": "Incluido",
        "Cantidad": 1,
        "Precio Unitario": 3051724.14,
        "Subtotal (Sin IVA)": 3051724.14,
        "IVA 16%": 488275.86,
        "Total con IVA": 3540000.00,
        "Diferencia final": 0.00,
        "Monto en Anexo Escrito": 3540000.00,
        "Observaciones": "IVA Incluido | IVA descompuesto del total",
    },
    {
        "Tipo": "Cotización Proveedor",
        "Fecha": "2026-02-10",
        "Rubro": "Carpas y estructura",
        "QT": "Sí", "T. Cambio": "MXN", "(+ IVA)": "Sí",
        "Cantidad": 1,
        "Precio Unitario": 1000000.00,
        "Subtotal (Sin IVA)": 1000000.00,
        "IVA 16%": 160000.00,
        "Total con IVA": 1160000.00,
        "Diferencia final": 0.00,
        "Monto en Anexo Escrito": 1160000.00,
        "Observaciones": "IVA desglosado",
    },
    {
        "Tipo": "Cotización Proveedor",
        "Fecha": "2026-01-20",
        "Rubro": "Equipamiento FEM",
        "QT": "Sí", "T. Cambio": "MXN", "(+ IVA)": "Incluido",
        "Cantidad": 5,
        "Precio Unitario": 463000.00,
        "Subtotal (Sin IVA)": 1995689.66,
        "IVA 16%": 319310.34,
        "Total con IVA": 2315000.00,
        "Diferencia final": 0.00,
        "Monto en Anexo Escrito": 2315000.00,
        "Observaciones": "IVA Incluido | IVA descompuesto del total",
    },
    {
        "Tipo": "Cotización Proveedor",
        "Fecha": "2026-03-05",
        "Rubro": "Servicio Yolístico",
        "QT": "Sí", "T. Cambio": "MXN", "(+ IVA)": "Incluido",
        "Cantidad": 1,
        "Precio Unitario": 517241.38,
        "Subtotal (Sin IVA)": 517241.38,
        "IVA 16%": 82758.62,
        "Total con IVA": 600000.00,
        "Diferencia final": 0.00,
        "Monto en Anexo Escrito": 600000.00,
        "Observaciones": "IVA Incluido | IVA descompuesto del total",
    },
    {
        "Tipo": "Cotización Proveedor",
        "Fecha": "2026-02-20",
        "Rubro": "ARQ Ecuestre",
        "QT": "Sí", "T. Cambio": "MXN", "(+ IVA)": "Incluido",
        "Cantidad": 1,
        "Precio Unitario": 2500000.00,
        "Subtotal (Sin IVA)": 2500000.00,
        "IVA 16%": 400000.00,
        "Total con IVA": 2900000.00,
        "Diferencia final": 0.00,
        "Monto en Anexo Escrito": 2900000.00,
        "Observaciones": "IVA Incluido | Total (línea adyacente)",
    },
    {
        "Tipo": "Presupuesto Global",
        "Fecha": "2026-01-10",
        "Rubro": "Programa Nacional Ecuestres",
        "QT": "Sí", "T. Cambio": "MXN", "(+ IVA)": "Sí",
        "Cantidad": 1,
        "Precio Unitario": 15344827.59,
        "Subtotal (Sin IVA)": 15344827.59,
        "IVA 16%": 2455172.41,
        "Total con IVA": 17800000.00,
        "Diferencia final": 0.00,
        "Monto en Anexo Escrito": 17800000.00,
        "Observaciones": "IVA desglosado",
    },
]

PDF_FILES = [
    {"name": "COT_Caballerizas_2026.pdf",       "pages": 3, "bytes": b"", "hash": "a"},
    {"name": "COT_Carpas_Estructura_2026.pdf",   "pages": 2, "bytes": b"", "hash": "b"},
    {"name": "COT_Equipamiento_FEM_2026.pdf",    "pages": 5, "bytes": b"", "hash": "c"},
    {"name": "COT_Servicio_Yolistico_2026.pdf",  "pages": 4, "bytes": b"", "hash": "d"},
    {"name": "COT_ARQ_Ecuestre_2026.pdf",        "pages": 3, "bytes": b"", "hash": "e"},
    {"name": "Ppto_ProgramaNacional_2026.pdf",   "pages": 8, "bytes": b"", "hash": "f"},
]

# ── Ventana principal ─────────────────────────────────────────
print("\nGenerando capturas de pantalla…")
window = main_qt.MainWindow()

# ────────────────────────────────────────────────────────────
# CAPTURA 1: Estado inicial (sin datos)
# ────────────────────────────────────────────────────────────
grab(window, "01_estado_inicial.png", 1400, 860)

# ────────────────────────────────────────────────────────────
# CAPTURA 2: Sidebar con PDFs cargados y secciones configuradas
# ────────────────────────────────────────────────────────────
cp = window.config_panel
cp._pdf_files = PDF_FILES
cp._refresh_pdf_ui()
cp.le_proyecto.setText("EFIDEPORTE 2026")
cp.sb_nsec.setValue(6)
process()
# Configurar secciones manualmente
names = [f["name"] for f in PDF_FILES]
for i, sw in enumerate(cp._sec_widgets):
    sw._pdf_names = names
    sw._max_pages = [f["pages"] for f in PDF_FILES]
    labels = ["Caballerizas", "Carpas y Estructura", "Equipamiento FEM",
              "Servicio Yolístico", "ARQ Ecuestre", "Ppto. Nacional"]
    monedas = ["MXN", "MXN", "MXN", "MXN", "MXN", "MXN"]
    sw.le_label.setText(labels[i] if i < len(labels) else f"Sección {i+1}")
    sw.cb_moneda.setCurrentText(monedas[i])
    sw.cb_pdf.clear()
    sw.cb_pdf.addItems(names)
    sw.cb_pdf.setCurrentIndex(i)
    sw.cb_pdf.setVisible(True)
    sw.sb_p0.setValue(1)
    sw.sb_p1.setValue(PDF_FILES[i]["pages"])
process()

grab(window, "02_sidebar_configurado.png", 1400, 860)

# Captura solo del sidebar
px = cp.grab()
px.save(os.path.join(OUT, "02b_sidebar_zoom.png"), "PNG")
print(f"  [OK] 02b_sidebar_zoom.png  ({px.width()}×{px.height()})")

# ────────────────────────────────────────────────────────────
# CAPTURA 3: Tabla con resultados extraídos
# ────────────────────────────────────────────────────────────
df = pd.DataFrame(SAMPLE_ROWS).reindex(columns=engine._COLS)
df = engine.recalc_derived(df)
window.data_panel.load_data(df, "EFIDEPORTE 2026")
process()

grab(window, "03_tabla_resultados.png", 1400, 860)

# Captura solo del data panel
px = window.data_panel.grab()
px.save(os.path.join(OUT, "03b_datos_zoom.png"), "PNG")
print(f"  [OK] 03b_datos_zoom.png  ({px.width()}×{px.height()})")

# ────────────────────────────────────────────────────────────
# CAPTURA 4: KPIs en primer plano
# ────────────────────────────────────────────────────────────
px = window.data_panel._kpi_prov[0].parent().grab() if hasattr(window.data_panel._kpi_prov[0], 'parent') else window.data_panel.grab()
# Grab the data panel at reduced height to focus on KPIs
dp = window.data_panel
dp_small = main_qt.DataPanel()
dp_small.load_data(df, "EFIDEPORTE 2026")
dp_small.resize(900, 300)
dp_small.show()
process()
px = dp_small.grab()
px.save(os.path.join(OUT, "04_kpis.png"), "PNG")
print(f"  [OK] 04_kpis.png  ({px.width()}×{px.height()})")

# ────────────────────────────────────────────────────────────
# CAPTURA 5: Sidebar seccion individual
# ────────────────────────────────────────────────────────────
if cp._sec_widgets:
    sw0 = cp._sec_widgets[0]
    px = sw0.grab()
    px.save(os.path.join(OUT, "05_seccion_widget.png"), "PNG")
    print(f"  [OK] 05_seccion_widget.png  ({px.width()}×{px.height()})")

print(f"\nListo. Imágenes en: {OUT}")
