# ============================================================
# CONCILIADOR DE COTIZACIONES  |  main_qt.py  v6.0
    # ============================================================
from __future__ import annotations

import datetime
import os
import sys

import pandas as pd
from PyQt6.QtCore import (
    QByteArray, QSize, Qt, QThread, pyqtSignal,
)
from PyQt6.QtGui import (
    QColor, QFont, QIcon, QPalette, QPixmap,
)
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDialog,
    QDialogButtonBox, QFileDialog, QFormLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QMainWindow, QMessageBox, QProgressBar,
    QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QSplitter, QStackedWidget, QStatusBar, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget,
)

import engine

# ─────────────────────────────────────────────────────────────
# PALETA DE COLORES
# ─────────────────────────────────────────────────────────────
ACCENT      = "#6E152E"
ACCENT_LITE = "#b84a6b"
BG_DARK     = "#111217"
BG_PANEL    = "#1d1519"
BG_SIDEBAR  = "#2a0f1a"
TEXT_MAIN   = "#f2edf0"
TEXT_MUTED  = "#d8a8b7"
BORDER      = "#5b2637"
INPUT_BG    = "#2b2026"
GREEN       = "#28a745"
RED_WARN    = "#c0392b"

QSS = f"""
QMainWindow, QWidget {{
    background-color: {BG_DARK};
    color: {TEXT_MAIN};
    font-family: "Segoe UI", Arial, sans-serif;
    font-size: 13px;
}}
QSplitter::handle {{
    background-color: {BORDER};
    width: 2px; height: 2px;
}}
/* ── Dock lateral ── */
#sidebar {{
    background-color: {BG_SIDEBAR};
    border-right: 1px solid {BORDER};
}}
/* ── Paneles interiores ── */
QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 6px;
    margin-top: 8px;
    padding-top: 8px;
    color: {TEXT_MAIN};
    font-weight: bold;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    color: {TEXT_MUTED};
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
/* ── Inputs ── */
QLineEdit, QSpinBox, QComboBox, QTextEdit {{
    background-color: {INPUT_BG};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 4px 8px;
}}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {ACCENT_LITE};
}}
QComboBox QAbstractItemView {{
    background-color: {BG_PANEL};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    selection-background-color: {ACCENT};
}}
/* ── Botones ── */
QPushButton {{
    background-color: {INPUT_BG};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: 500;
}}
QPushButton:hover  {{ background-color: {BORDER}; }}
QPushButton:pressed {{ background-color: {ACCENT}; color: #fff; }}
QPushButton#btn_primary {{
    background-color: {ACCENT};
    color: #ffffff;
    font-weight: bold;
    border: none;
    padding: 8px 18px;
}}
QPushButton#btn_primary:hover  {{ background-color: {ACCENT_LITE}; }}
QPushButton#btn_primary:pressed {{ background-color: {ACCENT}; }}
QPushButton#btn_primary:disabled {{
    background-color: #4a2030;
    color: #8a5060;
}}
/* ── Tabla ── */
QTableWidget {{
    background-color: {BG_PANEL};
    color: {TEXT_MAIN};
    gridline-color: {BORDER};
    border: 1px solid {BORDER};
    selection-background-color: {ACCENT};
}}
QTableWidget::item:selected {{ background-color: {ACCENT}; color: #fff; }}
QHeaderView::section {{
    background-color: {BG_SIDEBAR};
    color: {TEXT_MUTED};
    border: 1px solid {BORDER};
    padding: 4px 6px;
    font-size: 11px;
    font-weight: bold;
    text-transform: uppercase;
}}
/* ── Barra de progreso ── */
QProgressBar {{
    background-color: {INPUT_BG};
    border: 1px solid {BORDER};
    border-radius: 4px;
    color: {TEXT_MAIN};
    text-align: center;
    height: 20px;
}}
QProgressBar::chunk {{ background-color: {ACCENT}; border-radius: 3px; }}
/* ── Scroll ── */
QScrollBar:vertical {{
    background: {BG_PANEL}; width: 10px; border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER}; border-radius: 4px; min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {BG_PANEL}; height: 10px; border-radius: 4px;
}}
QScrollBar::handle:horizontal {{
    background: {BORDER}; border-radius: 4px; min-width: 20px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
/* ── Labels de título ── */
QLabel#section_title {{
    background-color: {ACCENT};
    color: #ffffff;
    font-weight: bold;
    padding: 6px 12px;
    border-radius: 4px 4px 0 0;
}}
QLabel#kpi_value {{
    font-size: 18px;
    font-weight: bold;
    color: {ACCENT_LITE};
}}
QLabel#kpi_label {{
    font-size: 11px;
    color: {TEXT_MUTED};
}}
/* ── Checkbox ── */
QCheckBox {{ color: {TEXT_MAIN}; spacing: 6px; }}
QCheckBox::indicator {{
    width: 16px; height: 16px;
    border: 1px solid {BORDER};
    border-radius: 3px;
    background-color: {INPUT_BG};
}}
QCheckBox::indicator:checked {{
    background-color: {ACCENT};
    border-color: {ACCENT};
}}
/* ── Menú ── */
QMenuBar {{
    background-color: {BG_SIDEBAR};
    color: {TEXT_MAIN};
    border-bottom: 1px solid {BORDER};
}}
QMenuBar::item:selected {{ background-color: {ACCENT}; }}
QMenu {{
    background-color: {BG_PANEL};
    color: {TEXT_MAIN};
    border: 1px solid {BORDER};
}}
QMenu::item:selected {{ background-color: {ACCENT}; }}
/* ── Status bar ── */
QStatusBar {{ background-color: {BG_SIDEBAR}; color: {TEXT_MUTED}; font-size: 11px; }}
"""


# ─────────────────────────────────────────────────────────────
# WORKERS (hilos de fondo)
# ─────────────────────────────────────────────────────────────
class RenderWorker(QThread):
    """Renderiza una página del PDF en segundo plano."""
    finished = pyqtSignal(int, QPixmap)   # (page_idx, pixmap)
    failed   = pyqtSignal(int)            # (page_idx)

    def __init__(self, pdf_bytes: bytes, idx: int, scale: float = 1.5):
        super().__init__()
        self._bytes = pdf_bytes
        self._idx   = idx
        self._scale = scale

    def run(self):
        png = engine.render_page(self._bytes, self._idx, self._scale)
        if png:
            pm = QPixmap()
            pm.loadFromData(QByteArray(png))
            self.finished.emit(self._idx, pm)
        else:
            self.failed.emit(self._idx)


class ExtractWorker(QThread):
    """Ejecuta la extracción de montos en segundo plano."""
    progress = pyqtSignal(int, int, str)   # (current, total, label)
    row_done = pyqtSignal(int, dict)       # (section_idx, result_dict)
    warning  = pyqtSignal(str)
    finished = pyqtSignal(list)            # lista completa de dicts

    def __init__(self, pdf_files: list, sec_cfgs: list, bx_token: str):
        super().__init__()
        self._files  = pdf_files
        self._cfgs   = sec_cfgs
        self._token  = bx_token

    def run(self):
        results = []
        n = len(self._cfgs)
        for i, cfg in enumerate(self._cfgs):
            self.progress.emit(i + 1, n, cfg["label"])
            pdf_idx = cfg.get("pdf_idx", 0)
            if pdf_idx < len(self._files):
                pdf_bytes = self._files[pdf_idx]["bytes"]
            else:
                pdf_bytes = self._files[0]["bytes"] if self._files else b""
            try:
                row = engine.extract(
                    pdf_bytes,
                    cfg["label"],
                    cfg["p0"],
                    cfg["p1"],
                    cfg["det_iva"],
                    cfg.get("calc_sub", True),
                    tipo=cfg.get("tipo", "Cotización Proveedor"),
                    moneda=cfg.get("moneda", "MXN"),
                    bx_token=self._token,
                    on_warning=lambda m: self.warning.emit(m),
                )
            except Exception as exc:
                row = {
                    **{k: None for k in engine._COLS},
                    "Tipo":   cfg.get("tipo", "Cotización Proveedor"),
                    "Rubro":  cfg["label"],
                    "QT":     "Sí",
                    "T. Cambio": cfg.get("moneda", "MXN"),
                    "Cantidad":  1,
                    "Fecha":  datetime.date.today().isoformat(),
                    "Observaciones": f"Error: {str(exc)[:120]}",
                }
                self.warning.emit(f"Sección {i+1} «{cfg['label']}»: {exc}")
            results.append(row)
            self.row_done.emit(i, row)
        self.finished.emit(results)


# ─────────────────────────────────────────────────────────────
# WIDGET DE SECCIÓN (barra lateral)
# ─────────────────────────────────────────────────────────────
class SectionWidget(QGroupBox):
    changed = pyqtSignal()

    def __init__(self, idx: int, pdf_names: list[str], max_pages: list[int], parent=None):
        super().__init__(f"Sección {idx + 1}", parent)
        self._idx = idx
        self._pdf_names = pdf_names
        self._max_pages = max_pages
        self._build()

    def _build(self):
        layout = QFormLayout(self)
        layout.setSpacing(6)

        self.le_label = QLineEdit(f"Sección {self._idx + 1}")
        self.le_label.setPlaceholderText("Rubro / Concepto")
        layout.addRow("Rubro:", self.le_label)

        self.cb_tipo = QComboBox()
        self.cb_tipo.addItems(["Cotización Proveedor", "Presupuesto Global"])
        layout.addRow("Tipo:", self.cb_tipo)

        self.cb_pdf = QComboBox()
        if self._pdf_names:
            self.cb_pdf.addItems(self._pdf_names)
        else:
            self.cb_pdf.addItem("(sin PDF)")
        self.cb_pdf.setVisible(len(self._pdf_names) > 1)
        layout.addRow("PDF:", self.cb_pdf)

        h_pages = QHBoxLayout()
        self.sb_p0 = QSpinBox(); self.sb_p0.setMinimum(1)
        self.sb_p1 = QSpinBox(); self.sb_p1.setMinimum(1)
        self._update_max_pages()
        h_pages.addWidget(QLabel("De:")); h_pages.addWidget(self.sb_p0)
        h_pages.addWidget(QLabel("A:"));  h_pages.addWidget(self.sb_p1)
        layout.addRow("Págs.:", h_pages)

        self.cb_moneda = QComboBox()
        self.cb_moneda.addItems(["MXN", "USD", "EUR", "CAD"])
        layout.addRow("Moneda:", self.cb_moneda)

        self.chk_iva = QCheckBox("Detectar IVA")
        self.chk_iva.setChecked(True)
        self.chk_sub = QCheckBox("Calcular subtotal si falta")
        self.chk_sub.setChecked(True)
        layout.addRow("", self.chk_iva)
        layout.addRow("", self.chk_sub)

        # Propagar cambios
        for w in (self.le_label, self.cb_tipo, self.cb_pdf,
                  self.cb_moneda):
            if hasattr(w, "textChanged"):
                w.textChanged.connect(self.changed)
            elif hasattr(w, "currentIndexChanged"):
                w.currentIndexChanged.connect(self.changed)
        for w in (self.sb_p0, self.sb_p1):
            w.valueChanged.connect(self.changed)
        self.chk_iva.toggled.connect(self.changed)
        self.chk_sub.toggled.connect(self.changed)
        self.cb_pdf.currentIndexChanged.connect(self._on_pdf_changed)

    def _update_max_pages(self):
        pdf_idx = self.cb_pdf.currentIndex() if self._pdf_names else 0
        mp = self._max_pages[pdf_idx] if pdf_idx < len(self._max_pages) else 1
        self.sb_p0.setMaximum(mp)
        self.sb_p1.setMaximum(mp)

    def _on_pdf_changed(self):
        self._update_max_pages()
        self.changed.emit()

    def get_config(self) -> dict:
        return {
            "label":    self.le_label.text() or f"Sección {self._idx + 1}",
            "tipo":     self.cb_tipo.currentText(),
            "pdf_idx":  self.cb_pdf.currentIndex(),
            "p0":       self.sb_p0.value(),
            "p1":       self.sb_p1.value(),
            "moneda":   self.cb_moneda.currentText(),
            "det_iva":  self.chk_iva.isChecked(),
            "calc_sub": self.chk_sub.isChecked(),
        }

    def update_pdf_names(self, pdf_names: list[str], max_pages: list[int]):
        self._pdf_names = pdf_names
        self._max_pages = max_pages
        cur = self.cb_pdf.currentIndex()
        self.cb_pdf.blockSignals(True)
        self.cb_pdf.clear()
        self.cb_pdf.addItems(pdf_names if pdf_names else ["(sin PDF)"])
        if cur < self.cb_pdf.count():
            self.cb_pdf.setCurrentIndex(cur)
        self.cb_pdf.blockSignals(False)
        self.cb_pdf.setVisible(len(pdf_names) > 1)
        self._update_max_pages()


# ─────────────────────────────────────────────────────────────
# PANEL LATERAL DE CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────
class ConfigPanel(QWidget):
    extract_requested = pyqtSignal(list, str)  # (sec_configs, bx_token)
    pdf_loaded        = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(280)
        self._pdf_files: list[dict]  = []
        self._sec_widgets: list[SectionWidget] = []
        self._build()

    def _build(self):
        # ── Panel exterior: solo contiene el scroll area del menú ──
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        self._panel_scroll = QScrollArea()
        self._panel_scroll.setWidgetResizable(True)
        self._panel_scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        # No scroll horizontal: el panel tiene ancho fijo
        self._panel_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._panel_scroll.setStyleSheet(
            f"background:{BG_SIDEBAR}; border:none;"
        )

        _content = QWidget()
        _content.setStyleSheet(f"background:{BG_SIDEBAR};")
        main = QVBoxLayout(_content)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(12)

        # ── PDFs ─────────────────────────────────────────────────────
        grp_pdf = QGroupBox("Documentos PDF")
        vl = QVBoxLayout(grp_pdf)
        self.btn_add_pdf = QPushButton("📂  Agregar PDF(s)")
        self.btn_add_pdf.clicked.connect(self._open_pdfs)
        vl.addWidget(self.btn_add_pdf)

        self.lbl_pdf_info = QLabel("Sin archivos cargados")
        self.lbl_pdf_info.setWordWrap(True)
        self.lbl_pdf_info.setStyleSheet(f"color:{TEXT_MUTED}; font-size:11px;")
        vl.addWidget(self.lbl_pdf_info)

        # Lista compacta de archivos (máx 3 filas visibles, scrolleable)
        self.lst_pdf_files = QListWidget()
        self.lst_pdf_files.setMaximumHeight(72)
        self.lst_pdf_files.setStyleSheet(f"""
            QListWidget {{
                background:{INPUT_BG};
                border:1px solid {BORDER};
                color:{TEXT_MUTED};
                font-size:11px;
                border-radius:4px;
            }}
            QListWidget::item {{ padding:2px 6px; }}
            QListWidget::item:selected {{ background:{ACCENT}; color:#fff; }}
        """)
        self.lst_pdf_files.setVisible(False)
        vl.addWidget(self.lst_pdf_files)

        self.btn_clear_pdf = QPushButton("🗑  Limpiar PDFs")
        self.btn_clear_pdf.clicked.connect(self._clear_pdfs)
        self.btn_clear_pdf.setEnabled(False)
        vl.addWidget(self.btn_clear_pdf)
        main.addWidget(grp_pdf)

        # ── Proyecto ──────────────────────────────────────────
        grp_proy = QGroupBox("Proyecto")
        fl = QFormLayout(grp_proy)
        self.le_proyecto = QLineEdit()
        self.le_proyecto.setPlaceholderText("Nombre del proyecto…")
        fl.addRow("Nombre:", self.le_proyecto)
        main.addWidget(grp_proy)

        # ── Banxico ───────────────────────────────────────────
        grp_bx = QGroupBox("Banxico – Tipo de Cambio")
        fl2 = QFormLayout(grp_bx)
        self.le_token = QLineEdit()
        self.le_token.setPlaceholderText("Pega tu token aquí…")
        self.le_token.setEchoMode(QLineEdit.EchoMode.Password)
        fl2.addRow("Token:", self.le_token)
        self.lbl_token_status = QLabel("")
        self.lbl_token_status.setStyleSheet(f"color:{TEXT_MUTED}; font-size:11px;")
        fl2.addRow("", self.lbl_token_status)
        self.le_token.textChanged.connect(
            lambda t: self.lbl_token_status.setText("🔑 Token activo" if t else "")
        )
        main.addWidget(grp_bx)

        # ── Secciones ─────────────────────────────────────────
        grp_sec = QGroupBox("Secciones (Cotizaciones)")
        vl_sec = QVBoxLayout(grp_sec)

        h_spin = QHBoxLayout()
        h_spin.addWidget(QLabel("Núm. de secciones:"))
        self.sb_nsec = QSpinBox()
        self.sb_nsec.setRange(1, 50)
        self.sb_nsec.setValue(1)
        self.sb_nsec.setMinimumWidth(64)   # ancho mínimo para ser clickeable
        self.sb_nsec.valueChanged.connect(self._rebuild_sections)
        h_spin.addWidget(self.sb_nsec)
        h_spin.addStretch()
        vl_sec.addLayout(h_spin)

        # Sin scroll anidado — el panel completo ya scrollea verticalmente
        self._sec_container = QWidget()
        self._sec_layout    = QVBoxLayout(self._sec_container)
        self._sec_layout.setContentsMargins(0, 0, 0, 0)
        self._sec_layout.setSpacing(8)
        self._sec_layout.addStretch()
        vl_sec.addWidget(self._sec_container)
        main.addWidget(grp_sec)

        # ── Botón Extraer ───────────────────────────────────────
        self.btn_extract = QPushButton("🔍  Extraer Montos")
        self.btn_extract.setObjectName("btn_primary")
        self.btn_extract.setEnabled(False)
        self.btn_extract.clicked.connect(self._on_extract)
        main.addWidget(self.btn_extract)
        main.addStretch()

        self._panel_scroll.setWidget(_content)
        outer.addWidget(self._panel_scroll)

        # Construir sección inicial
        self._rebuild_sections(1)

    def _pdf_names(self)  -> list[str]:  return [f["name"] for f in self._pdf_files]
    def _max_pages(self) -> list[int]:   return [f["pages"] for f in self._pdf_files]

    def _rebuild_sections(self, n: int):
        current_n = len(self._sec_widgets)
        if n == current_n:
            return
        
        names = self._pdf_names()
        pages = self._max_pages()
        
        if n > current_n:
            # Solo agregar los nuevos al final
            for i in range(current_n, n):
                sw = SectionWidget(i, names, pages)
                self._sec_layout.insertWidget(i, sw)
                self._sec_widgets.append(sw)
        else:
            # Eliminar solo los que sobran del final
            for i in range(current_n - 1, n - 1, -1):
                w = self._sec_widgets.pop()
                self._sec_layout.removeWidget(w)
                w.deleteLater()

    def _open_pdfs(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Seleccionar PDF(s)", "", "PDF (*.pdf)"
        )
        if not paths:
            return
        import fitz as _fitz
        new_files = []
        for p in paths:
            with open(p, "rb") as fh:
                raw = fh.read()
            h = engine._md5(raw)
            with _fitz.open(stream=raw, filetype="pdf") as doc:
                n = len(doc)
            new_files.append({
                "name":  os.path.basename(p),
                "bytes": raw,
                "hash":  h,
                "pages": n,
            })
        self._pdf_files = new_files
        self._refresh_pdf_ui()
        self.pdf_loaded.emit()

    def _clear_pdfs(self):
        self._pdf_files = []
        self._refresh_pdf_ui()
        self.pdf_loaded.emit()

    def _refresh_pdf_ui(self):
        n = len(self._pdf_files)
        if n == 0:
            self.lbl_pdf_info.setText("Sin archivos cargados")
            self.lst_pdf_files.clear()
            self.lst_pdf_files.setVisible(False)
            self.btn_clear_pdf.setEnabled(False)
            self.btn_extract.setEnabled(False)
        else:
            total = sum(f["pages"] for f in self._pdf_files)
            self.lbl_pdf_info.setText(
                f"✅ {n} archivo{'s' if n > 1 else ''} · {total} págs."
            )
            self.lst_pdf_files.clear()
            for f in self._pdf_files:
                self.lst_pdf_files.addItem(f"• {f['name']}")
            self.lst_pdf_files.setVisible(True)
            self.btn_clear_pdf.setEnabled(True)
            self.btn_extract.setEnabled(True)
        # Actualizar secciones
        names = self._pdf_names()
        pages = self._max_pages()
        for sw in self._sec_widgets:
            sw.update_pdf_names(names, pages)

    def _on_extract(self):
        cfgs = [sw.get_config() for sw in self._sec_widgets]
        self.extract_requested.emit(cfgs, self.le_token.text().strip())

    def get_pdf_files(self) -> list[dict]:
        return self._pdf_files

    def get_proyecto(self) -> str:
        return self.le_proyecto.text().strip()


# ─────────────────────────────────────────────────────────────
# VISOR DE PDF
# ─────────────────────────────────────────────────────────────
class PDFViewer(QWidget):
    page_changed = pyqtSignal(int)   # nueva página (0-based)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pdf_bytes:  bytes      = b""
        self._total_pages: int       = 0
        self._current_page: int      = 0
        self._page_cache: dict[int, QPixmap] = {}
        self._render_worker: RenderWorker | None = None
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Título
        title = QLabel("🔍 Visor de Documento")
        title.setObjectName("section_title")
        layout.addWidget(title)

        # Barra de navegación
        nav = QHBoxLayout()
        self.btn_prev = QPushButton("◀")
        self.btn_prev.setFixedWidth(40)
        self.btn_prev.clicked.connect(lambda: self._go_to(self._current_page - 1))

        self.lbl_page = QLabel("Página 0 / 0")
        self.lbl_page.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sb_jump = QSpinBox()
        self.sb_jump.setMinimum(1)
        self.sb_jump.setFixedWidth(70)
        self.sb_jump.valueChanged.connect(self._on_jump)

        self.btn_next = QPushButton("▶")
        self.btn_next.setFixedWidth(40)
        self.btn_next.clicked.connect(lambda: self._go_to(self._current_page + 1))

        nav.addWidget(self.btn_prev)
        nav.addWidget(self.lbl_page, stretch=1)
        nav.addWidget(self.sb_jump)
        nav.addWidget(self.btn_next)
        layout.addLayout(nav)

        # Indicador de sección
        self.lbl_section = QLabel("")
        self.lbl_section.setStyleSheet(
            f"background:{ACCENT};color:#fff;padding:3px 10px;"
            f"border-radius:4px;font-size:11px;"
        )
        self.lbl_section.setVisible(False)
        layout.addWidget(self.lbl_section)

        # Área de imagen
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_image = QLabel("Carga un PDF para comenzar")
        self.lbl_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_image.setStyleSheet(f"color:{TEXT_MUTED};")
        self.lbl_image.setMinimumSize(400, 300)
        scroll.setWidget(self.lbl_image)
        layout.addWidget(scroll, stretch=1)

        self._scroll = scroll
        self._nav_blocked = False

    def load_pdf(self, pdf_bytes: bytes, total_pages: int):
        self._pdf_bytes   = pdf_bytes
        self._total_pages = total_pages
        self._current_page = 0
        self._page_cache.clear()
        self.sb_jump.setMaximum(max(total_pages, 1))
        self._update_nav()
        self._request_render(0)

    def clear(self):
        self._pdf_bytes   = b""
        self._total_pages = 0
        self._current_page = 0
        self._page_cache.clear()
        self.lbl_image.setPixmap(QPixmap())
        self.lbl_image.setText("Carga un PDF para comenzar")
        self._update_nav()

    def _go_to(self, target: int):
        if self._total_pages == 0:
            return
        target = max(0, min(self._total_pages - 1, target))
        if target == self._current_page:
            return
        self._current_page = target
        self._nav_blocked = True
        self.sb_jump.setValue(target + 1)
        self._nav_blocked = False
        self._update_nav()
        if target in self._page_cache:
            self._show_pixmap(self._page_cache[target])
        else:
            self.lbl_image.setText("Cargando…")
            self._request_render(target)
        self.page_changed.emit(target)

    def _on_jump(self, val: int):
        if self._nav_blocked:
            return
        self._go_to(val - 1)

    def _update_nav(self):
        tp = self._total_pages
        cp = self._current_page
        self.btn_prev.setEnabled(tp > 0 and cp > 0)
        self.btn_next.setEnabled(tp > 0 and cp < tp - 1)
        self.lbl_page.setText(
            f"Página {cp + 1} / {tp}" if tp > 0 else "Página 0 / 0"
        )

    def _request_render(self, idx: int):
        """Lanza un hilo de render para el índice dado."""
        if not self._pdf_bytes:
            return
        # Si ya hay un worker corriendo para otra página, se le deja terminar;
        # el resultado se cachea aunque ya no sea la página visible.
        worker = RenderWorker(self._pdf_bytes, idx, scale=1.5)
        worker.finished.connect(self._on_rendered)
        worker.failed.connect(lambda i: self.lbl_image.setText(f"Error al renderizar pág. {i + 1}"))
        # Guardar referencia para evitar GC prematuro
        if self._render_worker is not None:
            # No matamos el worker anterior, sólo actualizamos la referencia
            self._render_worker.finished.disconnect()
            self._render_worker.failed.disconnect()
        self._render_worker = worker
        worker.start()

    def _on_rendered(self, idx: int, pm: QPixmap):
        """Callback cuando el worker terminó. Guarda en caché y muestra si es la página actual."""
        self._page_cache[idx] = pm
        if idx == self._current_page:
            self._show_pixmap(pm)

    def _show_pixmap(self, pm: QPixmap):
        avail_w = self._scroll.viewport().width() - 10
        scaled = pm.scaledToWidth(avail_w, Qt.TransformationMode.SmoothTransformation)
        self.lbl_image.setPixmap(scaled)
        self.lbl_image.resize(scaled.size())

    def set_section_label(self, text: str):
        if text:
            self.lbl_section.setText(text)
            self.lbl_section.setVisible(True)
        else:
            self.lbl_section.setVisible(False)

    def current_page(self) -> int:
        return self._current_page


# ─────────────────────────────────────────────────────────────
# PANEL DE DATOS (tabla + KPIs)
# ─────────────────────────────────────────────────────────────
DROPDOWN_COLS = {
    "Tipo":    ["Cotización Proveedor", "Presupuesto Global"],
    "QT":      ["Sí", "No"],
    "(+ IVA)": ["Sí", "Incluido", "Exento", "N/M"],
}
READONLY_COLS  = {"Diferencia final"}
MONEY_COLS     = {"Precio Unitario", "Subtotal (Sin IVA)", "IVA 16%",
                  "Total con IVA", "Diferencia final", "Monto en Anexo Escrito"}
NUMERIC_COLS   = {"Cantidad"} | MONEY_COLS

COL_WIDTHS = {
    "Tipo": 160, "Fecha": 90, "Rubro": 200, "QT": 50,
    "T. Cambio": 80, "(+ IVA)": 75, "Cantidad": 65,
    "Precio Unitario": 110, "Subtotal (Sin IVA)": 120, "IVA 16%": 90,
    "Total con IVA": 110, "Diferencia final": 110,
    "Monto en Anexo Escrito": 140, "Observaciones": 200,
}


class DataPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._df: pd.DataFrame | None = None
        self._updating = False
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        # Título
        title = QLabel("✏️ Editor de Datos")
        title.setObjectName("section_title")
        layout.addWidget(title)

        # KPIs
        kpi_row = QHBoxLayout()
        kpi_row.setSpacing(8)
        self._kpi_prov  = self._make_kpi("Total Proveedores")
        self._kpi_anx   = self._make_kpi("Monto Anexo Manual")
        self._kpi_dif   = self._make_kpi("Diferencia")
        kpi_row.addWidget(self._kpi_prov[0])
        kpi_row.addWidget(self._kpi_anx[0])
        kpi_row.addWidget(self._kpi_dif[0])
        layout.addLayout(kpi_row)

        # Advertencias
        self.lbl_warnings = QLabel("")
        self.lbl_warnings.setWordWrap(True)
        self.lbl_warnings.setStyleSheet(
            f"color:{ACCENT_LITE};background:{BG_PANEL};"
            f"border:1px solid {BORDER};border-radius:4px;padding:4px;"
        )
        self.lbl_warnings.setVisible(False)
        layout.addWidget(self.lbl_warnings)

        # Tabla
        self.table = QTableWidget(0, len(engine._COLS))
        self.table.setHorizontalHeaderLabels(engine._COLS)
        self.table.horizontalHeader().setSectionsMovable(False)
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(False)
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked |
            QTableWidget.EditTrigger.AnyKeyPressed
        )
        self.table.itemChanged.connect(self._on_item_changed)

        for ci, col in enumerate(engine._COLS):
            w = COL_WIDTHS.get(col, 100)
            self.table.setColumnWidth(ci, w)
        self.table.horizontalHeader().setSectionResizeMode(
            engine._COLS.index("Observaciones"),
            QHeaderView.ResizeMode.Stretch,
        )
        layout.addWidget(self.table, stretch=1)

        # Botones de descarga
        btn_row = QHBoxLayout()
        self.btn_export = QPushButton("⬇️  Descargar Excel")
        self.btn_export.setObjectName("btn_primary")
        self.btn_export.setEnabled(False)
        self.btn_export.clicked.connect(self._export_excel)

        self.btn_template = QPushButton("📄  Plantilla vacía")
        self.btn_template.setEnabled(False)
        self.btn_template.clicked.connect(self._export_template)

        btn_row.addWidget(self.btn_export)
        btn_row.addWidget(self.btn_template)
        layout.addLayout(btn_row)

        # Placeholder
        self.lbl_placeholder = QLabel(
            "Configura las secciones y presiona 🔍 Extraer Montos"
        )
        self.lbl_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_placeholder.setStyleSheet(f"color:{TEXT_MUTED};")
        layout.addWidget(self.lbl_placeholder)

    def _make_kpi(self, label: str):
        box = QWidget()
        box.setStyleSheet(
            f"background:{BG_PANEL};border:1px solid {BORDER};"
            f"border-radius:8px;"
        )
        vl = QVBoxLayout(box)
        vl.setContentsMargins(10, 8, 10, 8)
        val_lbl = QLabel("$ 0.00")
        val_lbl.setObjectName("kpi_value")
        val_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl = QLabel(label)
        lbl.setObjectName("kpi_label")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vl.addWidget(val_lbl)
        vl.addWidget(lbl)
        return box, val_lbl, lbl

    def load_data(self, df: pd.DataFrame, proyecto: str = ""):
        self._df = df.copy()
        self._proyecto = proyecto
        self._updating = True
        self._populate_table(df)
        self._updating = False
        self._refresh_kpis()
        self.btn_export.setEnabled(True)
        self.btn_template.setEnabled(True)
        self.lbl_placeholder.setVisible(False)
        self.table.setVisible(True)
        self._check_warnings()

    def _populate_table(self, df: pd.DataFrame):
        self.table.setRowCount(0)
        self.table.setRowCount(len(df))
        for r, (_, row) in enumerate(df.iterrows()):
            self.table.setRowHeight(r, 26)
            for ci, col in enumerate(engine._COLS):
                val = row.get(col, "")
                if col in DROPDOWN_COLS:
                    cb = QComboBox()
                    cb.addItems(DROPDOWN_COLS[col])
                    s = str(val) if val is not None and str(val) != "nan" else DROPDOWN_COLS[col][0]
                    idx_cb = cb.findText(s)
                    cb.setCurrentIndex(max(idx_cb, 0))
                    cb.currentIndexChanged.connect(
                        lambda _, r=r, ci=ci, cb=cb: self._on_combo_changed(r, ci, cb)
                    )
                    self.table.setCellWidget(r, ci, cb)
                else:
                    if val is None or (isinstance(val, float) and pd.isna(val)):
                        display = ""
                    elif col in MONEY_COLS and val != "":
                        try:
                            display = f"${float(val):,.2f}"
                        except (ValueError, TypeError):
                            display = str(val)
                    else:
                        display = str(val)
                    item = QTableWidgetItem(display)
                    if col in READONLY_COLS:
                        item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                        item.setForeground(QColor(TEXT_MUTED))
                    self.table.setItem(r, ci, item)

    def _on_combo_changed(self, r: int, ci: int, cb: QComboBox):
        if self._updating or self._df is None:
            return
        col = engine._COLS[ci]
        self._df.at[r, col] = cb.currentText()
        self._recalc_and_refresh_row(r)

    def _on_item_changed(self, item: QTableWidgetItem):
        if self._updating or self._df is None:
            return
        r   = item.row()
        ci  = item.column()
        col = engine._COLS[ci]
        if col in READONLY_COLS or col in DROPDOWN_COLS:
            return
        txt = item.text().replace("$", "").replace(",", "").strip()
        if col in NUMERIC_COLS:
            try:
                self._df.at[r, col] = float(txt) if txt else None
            except ValueError:
                self._df.at[r, col] = None
        else:
            self._df.at[r, col] = txt
        self._recalc_and_refresh_row(r)

    def _recalc_and_refresh_row(self, r: int):
        # En lugar de usar recalc_derived, hacemos cálculo ligero hacia adelante.
        qty = self._df.at[r, "Cantidad"]
        qty = float(qty) if pd.notna(qty) else 1.0
        pu = self._df.at[r, "Precio Unitario"]
        has_iva = str(self._df.at[r, "(+ IVA)"]).strip().lower() in ["sí", "si"]
        
        if pd.notna(pu):
            sub = qty * float(pu)
            self._df.at[r, "Subtotal (Sin IVA)"] = sub
            if has_iva:
                self._df.at[r, "IVA 16%"] = sub * 0.16
                self._df.at[r, "Total con IVA"] = sub * 1.16
            else:
                self._df.at[r, "IVA 16%"] = 0.0
                self._df.at[r, "Total con IVA"] = sub

        tot = self._df.at[r, "Total con IVA"]
        anx = self._df.at[r, "Monto en Anexo Escrito"]
        if pd.notna(tot) and pd.notna(anx):
            self._df.at[r, "Diferencia final"] = float(tot) - float(anx)
        else:
            self._df.at[r, "Diferencia final"] = None

        self._updating = True
        row = self._df.iloc[r]
        for ci, col in enumerate(engine._COLS):
            if col in DROPDOWN_COLS:
                continue
            if col in READONLY_COLS or col in MONEY_COLS:
                val = row.get(col)
                if val is None or (isinstance(val, float) and pd.isna(val)):
                    display = ""
                elif col in MONEY_COLS:
                    try:
                        display = f"${float(val):,.2f}"
                    except (ValueError, TypeError):
                        display = str(val)
                else:
                    display = str(val)
                item = self.table.item(r, ci)
                if item:
                    item.setText(display)
        self._updating = False
        self._refresh_kpis()

    def _refresh_kpis(self):
        if self._df is None:
            return
        df_prov   = self._df[self._df["Tipo"] == "Cotización Proveedor"]
        df_presup = self._df[self._df["Tipo"] == "Presupuesto Global"]
        ts = pd.to_numeric(df_prov["Total con IVA"], errors="coerce").sum()
        if not df_presup.empty:
            rs = pd.to_numeric(df_presup["Total con IVA"], errors="coerce").sum()
            self._kpi_anx[2].setText("Ppto. Global Extraído")
        else:
            rs = pd.to_numeric(self._df["Monto en Anexo Escrito"], errors="coerce").sum()
            self._kpi_anx[2].setText("Monto Anexo Manual")
        dif = ts - rs
        self._kpi_prov[1].setText(f"${ts:,.2f}")
        self._kpi_anx[1].setText(f"${rs:,.2f}")
        self._kpi_dif[1].setText(f"${dif:,.2f}")
        color = RED_WARN if abs(dif) > 0.01 else GREEN
        self._kpi_dif[1].setStyleSheet(
            f"font-size:18px; font-weight:bold; color:{color};"
        )

    def _check_warnings(self):
        if self._df is None:
            self.lbl_warnings.setVisible(False)
            return
        warn_rows = self._df[
            self._df["Observaciones"].astype(str).str.contains("⚠|OCR|inferido", na=False)
        ]
        if not warn_rows.empty:
            lines = [
                f"• {r['Rubro']}: {r['Observaciones']}"
                for _, r in warn_rows.iterrows()
            ]
            self.lbl_warnings.setText(f"⚠ {len(warn_rows)} aviso(s):\n" + "\n".join(lines))
            self.lbl_warnings.setVisible(True)
        else:
            self.lbl_warnings.setVisible(False)

    def add_warning(self, msg: str):
        cur = self.lbl_warnings.text()
        self.lbl_warnings.setText((cur + "\n" if cur else "") + f"⚠ {msg}")
        self.lbl_warnings.setVisible(True)

    def _export_excel(self):
        if self._df is None:
            return
        proyecto = getattr(self, "_proyecto", "")
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        name = (proyecto or "Cotizaciones").replace(" ", "_")
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Excel",
            f"Conciliacion_{name}_{ts}.xlsx",
            "Excel (*.xlsx)"
        )
        if not path:
            return
        try:
            data = engine.to_excel(self._df, nombre=proyecto)
            with open(path, "wb") as fh:
                fh.write(data)
            QMessageBox.information(self, "Exportado", f"Archivo guardado en:\n{path}")
        except Exception as exc:
            QMessageBox.critical(self, "Error", f"No se pudo guardar:\n{exc}")

    def _export_template(self):
        if self._df is None:
            return
        proyecto = getattr(self, "_proyecto", "")
        name = (proyecto or "Cotizaciones").replace(" ", "_")
        path, _ = QFileDialog.getSaveFileName(
            self, "Guardar Plantilla Vacía",
            f"Plantilla_{name}.xlsx",
            "Excel (*.xlsx)"
        )
        if not path:
            return
        try:
            # Enviamos flag blank=True para que to_excel mantenga todo excepto numéricos
            data = engine.to_excel(self._df, nombre=proyecto, blank=True)
            with open(path, "wb") as fh:
                fh.write(data)
            QMessageBox.information(self, "Éxito", f"Plantilla guardada en:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al generar la plantilla:\n{e}")


# ─────────────────────────────────────────────────────────────
# VENTANA PRINCIPAL
# ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conciliador de Cotizaciones v6.0")
        self.resize(1400, 860)
        self._extract_worker: ExtractWorker | None = None
        self._pdf_combined_bytes: bytes = b""
        self._pdf_files: list[dict]     = []
        self._sec_cfgs:  list[dict]     = []
        self._build()

    def _build(self):
        # ── Barra de menú ─────────────────────────────────────
        menu = self.menuBar()
        file_m = menu.addMenu("Archivo")
        file_m.addAction("Acerca de…", self._show_about)
        file_m.addSeparator()
        file_m.addAction("Salir", self.close)

        # ── Barra de estado ───────────────────────────────────
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage("Listo · Conciliador v6.0")

        # ── Barra de progreso (oculta por defecto) ────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(18)
        self.status.addPermanentWidget(self.progress_bar, 1)

        # ── Layout principal ─────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        h_main = QHBoxLayout(central)
        h_main.setContentsMargins(0, 0, 0, 0)
        h_main.setSpacing(0)

        # Panel de config (sidebar fijo a la izquierda)
        self.config_panel = ConfigPanel()
        self.config_panel.extract_requested.connect(self._start_extract)
        self.config_panel.pdf_loaded.connect(self._on_pdf_loaded)
        h_main.addWidget(self.config_panel)

        # Splitter central
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(4)

        self.pdf_viewer = PDFViewer()
        self.pdf_viewer.page_changed.connect(self._on_page_changed)
        splitter.addWidget(self.pdf_viewer)

        self.data_panel = DataPanel()
        splitter.addWidget(self.data_panel)

        splitter.setSizes([500, 700])
        h_main.addWidget(splitter, stretch=1)

    # ── Carga de PDF ──────────────────────────────────────────
    def _on_pdf_loaded(self):
        files = self.config_panel.get_pdf_files()
        self._pdf_files = files
        if not files:
            self.pdf_viewer.clear()
            return
        combined_bytes, _, total_pages, _ = engine.build_combined_pdf(files)
        self._pdf_combined_bytes = combined_bytes
        self.pdf_viewer.load_pdf(combined_bytes, total_pages)
        self.status.showMessage(
            f"PDF cargado · {len(files)} archivo(s) · {total_pages} páginas"
        )

    def _on_page_changed(self, page_idx: int):
        # Mostrar indicador de sección
        for cfg in self._sec_cfgs:
            pdf_idx = cfg.get("pdf_idx", 0)
            offset = sum(
                f["pages"] for f in self._pdf_files[:pdf_idx]
            )
            g_p0 = offset + cfg["p0"] - 1
            g_p1 = offset + cfg["p1"] - 1
            if g_p0 <= page_idx <= g_p1:
                self.pdf_viewer.set_section_label(
                    f"{'🌐' if cfg.get('tipo') == 'Presupuesto Global' else '📑'} "
                    f"{cfg['label']} · {cfg.get('moneda', 'MXN')}"
                )
                return
        self.pdf_viewer.set_section_label("")

    # ── Extracción ────────────────────────────────────────────
    def _start_extract(self, cfgs: list, bx_token: str):
        if not self._pdf_files:
            QMessageBox.warning(self, "Sin PDF", "Carga al menos un PDF antes de extraer.")
            return
        self._sec_cfgs = cfgs
        self.config_panel.btn_extract.setEnabled(False)
        self.progress_bar.setMaximum(len(cfgs))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status.showMessage("Extrayendo montos…")

        self._extract_worker = ExtractWorker(
            self._pdf_files, cfgs, bx_token
        )
        self._extract_worker.progress.connect(self._on_extract_progress)
        self._extract_worker.warning.connect(self.data_panel.add_warning)
        self._extract_worker.finished.connect(self._on_extract_finished)
        self._extract_worker.start()

    def _on_extract_progress(self, current: int, total: int, label: str):
        self.progress_bar.setValue(current)
        self.status.showMessage(f"Extrayendo {current}/{total}: {label}…")

    def _on_extract_finished(self, results: list):
        self.progress_bar.setVisible(False)
        self.config_panel.btn_extract.setEnabled(True)
        df = pd.DataFrame(results).reindex(columns=engine._COLS)
        df = engine.recalc_derived(df)
        self.data_panel.load_data(df, self.config_panel.get_proyecto())
        self.status.showMessage(
            f"Extracción completa · {len(results)} sección(es) procesada(s)"
        )

    # ── Acerca de ─────────────────────────────────────────────
    def _show_about(self):
        QMessageBox.about(
            self,
            "Acerca del Conciliador",
            "<b>Conciliador de Cotizaciones v6.0</b><br>"
            "Motor de extracción PDF nativo con PyQt6.<br><br>"
            "5 estrategias de extracción + OCR + Banxico API.<br>"
            "Sin dependencias de servidor web."
        )


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────
def main():
    # Habilitar soporte para pantallas HiDPI
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("Conciliador de Cotizaciones")
    app.setOrganizationName("Conciliador")
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
