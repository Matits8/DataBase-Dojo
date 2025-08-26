from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from openpyxl import Workbook

def exportar_a_pdf(alumnos, ruta_salida):
    c = canvas.Canvas(ruta_salida, pagesize=A4)
    ancho, alto = A4
    x = 50
    y = alto - 50

    c.setFont("Helvetica-Bold", 14)
    c.drawString(x, y, "Listado de Alumnos")
    y -= 30

    c.setFont("Helvetica", 12)
    for alumno in alumnos:
        linea = f"{alumno['Nombre']} {alumno['Apellido']} - DNI: {alumno['DNI']}"
        c.drawString(x, y, linea)
        y -= 20
        if y < 50:
            c.showPage()
            y = alto - 50

    c.save()

def exportar_a_excel(alumnos, ruta_salida):
    wb = Workbook()
    ws = wb.active
    ws.title = "Alumnos"

    # Escribimos encabezado
    encabezado = list(alumnos[0].keys()) if alumnos else []
    ws.append(encabezado)

    # Escribimos cada alumno
    for alumno in alumnos:
        ws.append(list(alumno.values()))

    wb.save(ruta_salida)
