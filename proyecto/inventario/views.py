from django.views.generic import ListView, DetailView
from .models import inventario_objetos
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.template.loader import render_to_string
from .forms import objetoForm
from django.db.models import Q
from django.utils.dateparse import parse_date

# Exportación
import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from docx import Document
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Create your views here.

class agregar_objeto(ListView):
    model = inventario_objetos
    template_name = 'agregar_objeto.html'
    context_object_name = 'inventario'

class detalles_objeto(ListView):
    model = inventario_objetos
    template_name = 'detalles_objeto.html'
    context_object_name = 'inventario'

class exportar(ListView):
    model = inventario_objetos
    template_name = 'exportar.html'
    context_object_name = 'inventario'

class inventarioListView(ListView):
    model = inventario_objetos
    template_name = 'inventario.html'
    context_object_name = 'inventario'

class inventarioDetailView(DetailView):
    model = inventario_objetos
    template_name = 'vista_objeto.html'
    context_object_name = 'inventario'


# Funciones
def inventario_inicio(request):
    objeto = inventario_objetos.objects.all()
    template = loader.get_template('inicio.html')
    context = {
            'inventario': objeto
        }
    return HttpResponse(template.render(context, request))

def agregar_objeto(request):
    if request.method == 'POST':
        form = objetoForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = objetoForm()
    return render(request, 'agregar_objeto.html', {'form': form})

def detalles_objeto(request, pk):
    objeto = inventario_objetos.objects.get(pk=pk)
    return render(request, 'detalles_objeto.html', {'objeto': objeto})

def editar_objeto(request, pk):
    objeto = inventario_objetos.objects.get(pk=pk)
    
    if request.method == 'POST':
        objeto.codigo_pddh = request.POST.get('codigo_pddh')
        objeto.descripcion = request.POST.get('descripcion')
        objeto.marca = request.POST.get('marca')
        objeto.modelo = request.POST.get('modelo')
        objeto.serie = request.POST.get('serie')
        nueva_fecha = parse_date(request.POST.get('fecha_adquisicion', ''))
        if nueva_fecha:
            objeto.fecha_adquisición = nueva_fecha
        objeto.valor_unitario = request.POST.get('valor_unitario')
        objeto.save()

    return render(request, 'detalles_objeto.html', {'objeto': objeto})

def buscar_objetos(request):
    query = request.GET.get('q','')
    if query:
        resultados = inventario_objetos.objects.filter(
            Q(codigo_pddh__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(marca__icontains=query) |
            Q(modelo__icontains=query) |
            Q(serie__icontains=query)
        )
    else:
        resultados = inventario_objetos.objects.all()
    
    return render(request, 'inventario.html', {'object_list': resultados})

def borrar_objetos(pk):
    objeto = inventario_objetos.objects.get(pk=pk)
    objeto.delete()
    return redirect('inventario')


# EXPORTAR A FORMATOS
def exportar_tabla_pdf(request):
    # 1. Configurar la respuesta HTTP para descarga de PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Inventario_PDDH.pdf"'

    # 2. Configurar documento en formato Horizontal (Landscape) para que quepan las 7 columnas
    doc = SimpleDocTemplate(
        response, 
        pagesize=landscape(letter),
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )
    story = []
    
    # Estilos de texto
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    titulo_style = ParagraphStyle(
        'TituloReporte',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1, # Centrado
        spaceAfter=20
    )
    
    # Estilos para el texto de las celdas (permite que los textos largos hagan salto de línea)
    cell_text_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=11
    )
    
    cell_header_style = ParagraphStyle(
        'CellHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.whitesmoke
    )

    # Agregar título al PDF
    story.append(Paragraph("INVENTARIO DE OBJETOS - PDDH SAN MIGUEL", titulo_style))
    story.append(Spacer(1, 10))
    
    # 3. Obtener los registros de SQLite
    registros = inventario_objetos.objects.all()
    
    # Definir los encabezados envueltos en Paragraph para que no se corten
    tabla_datos = [[
        Paragraph("<b>Código PDDH</b>", cell_header_style),
        Paragraph("<b>Descripción</b>", cell_header_style),
        Paragraph("<b>Marca</b>", cell_header_style),
        Paragraph("<b>Modelo</b>", cell_header_style),
        Paragraph("<b>Serie</b>", cell_header_style),
        Paragraph("<b>Fecha Adq.</b>", cell_header_style),
        Paragraph("<b>Valor Unit.</b>", cell_header_style)
    ]]
    
    # 4. Rellenar las filas con los datos del modelo
    for item in registros:
        tabla_datos.append([
            Paragraph(str(item.codigo_pddh), cell_text_style),
            Paragraph(str(item.descripcion), cell_text_style),
            Paragraph(str(item.marca), cell_text_style),
            Paragraph(str(item.modelo), cell_text_style),
            Paragraph(str(item.serie), cell_text_style),
            Paragraph(str(item.fecha_adquisición.strftime('%d/%m/%Y') if item.fecha_adquisición else ''), cell_text_style),
            Paragraph(f"${item.valor_unitario}", cell_text_style)
        ])
    
    # 5. Definir el ancho proporcional para cada una de las 7 columnas (Total disponible ~732 puntos)
    # Ajustamos más espacio para la descripción y el código
    col_widths = [100, 182, 80, 80, 80, 75, 65]
    
    # Crear la tabla y aplicar estilos visuales profesionales
    tabla = Table(tabla_datos, colWidths=col_widths, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#343a40')), # Fondo oscuro para encabezado
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')), # Bordes grises finos
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]) # Filas alternas
    ]))
    
    story.append(tabla)
    
    # Construir el PDF
    doc.build(story)
    return response

def exportar_a_word(request):
    registros = inventario_objetos.objects.all()

    doc = Document()
    doc.add_heading('Inventario de Objetos de la PDDH San Miguel', level=1)
    doc.add_paragraph('A continuación se presentan los registros almacenados en la base de datos:')

    # CAMBIA ESTO DE 3 A 7
    columnas = 7 
    tabla = doc.add_table(rows=1, cols=columnas)
    tabla.style = 'Light Shading Accent 1'
    
    hdr_cells = tabla.rows[0].cells
    hdr_cells[0].text = 'Código PDDH'
    hdr_cells[1].text = 'Descripción'
    hdr_cells[2].text = 'Marca'
    hdr_cells[3].text = 'Modelo'
    hdr_cells[4].text = 'Serie'
    hdr_cells[5].text = 'Fecha de Adquisición'
    hdr_cells[6].text = 'Valor Unitario'

    # 4. Rellenar la tabla con los registros de la base de datos
    for item in registros:
        row_cells = tabla.add_row().cells
        row_cells[0].text = str(item.codigo_pddh)
        row_cells[1].text = str(item.descripcion)
        row_cells[2].text = str(item.marca)
        row_cells[3].text = str(item.modelo)
        row_cells[4].text = str(item.serie)
        row_cells[5].text = str(item.fecha_adquisición)
        row_cells[6].text = str(item.valor_unitario)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="reporte_tablas.docx"'

    doc.save(response)
    return response

def exportar_excel(request):
    # 1. Crear libro de trabajo de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos"

    # 2. Diseñar primero el gran encabezado superior (Filas 1 a 4)
    ws.merge_cells('A1:G4')
    ws['A1'] = "INVENTARIO DE PDDH SAN MIGUEL"
    ws['A1'].font = Font(name='Arial', size=16, bold=True)
    ws['A1'].alignment = Alignment(horizontal='center', vertical='center')

    # 3. Escribir los encabezados de la tabla en la Fila 6 (dejamos la 5 en blanco de espacio)
    encabezados = ['Código PDDH', 'Descripción', 'Marca', 'Modelo', 'Serie', 'Fecha de Adquisición', 'Valor Unitario']
    
    # Asignamos los encabezados directamente a la fila 6
    for col_num, header_title in enumerate(encabezados, start=1):
        cell = ws.cell(row=6, column=col_num)
        cell.value = header_title
        cell.font = Font(bold=True) # Texto de la tabla en negrita

    # 4. Escribir los objetos desde el ORM de Django a partir de la Fila 7
    row_num = 7
    for obj in inventario_objetos.objects.all():
        row_data = [
            obj.codigo_pddh, 
            obj.descripcion, 
            obj.marca, 
            obj.modelo, 
            obj.serie, 
            str(obj.fecha_adquisición), 
            str(obj.valor_unitario)
        ]
        for col_num, value in enumerate(row_data, start=1):
            ws.cell(row=row_num, column=col_num, value=value)
        row_num += 1

    # 5. Ajustar el ancho de las columnas automáticamente según el contenido
    for col in ws.columns:
        # Obtenemos el número de la columna usando la primera celda del grupo
        col_idx = col[0].column  
        col_letter = get_column_letter(col_idx) # <-- Solución al error
        
        # Evitamos que tome en cuenta el título largo de A1 para el cálculo del ancho
        if col_letter == 'A':
            ws.column_dimensions[col_letter].width = 20
        else:
            # Calculamos la longitud máxima ignorando celdas vacías o combinadas problemáticas
            max_len = max(len(str(cell.value or '')) for cell in col if cell.value is not None)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    # 6. Configurar la respuesta de descarga
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=INVENTARIO_PDDH.xlsx'
    wb.save(response)
    return response