from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml


def add_line_numbering_to_docx(doc):
    # * aplicar numeración de líneas a todas las secciones del documento
    for section in doc.sections:
        # * crear un nuevo objeto OxmlElement para cada sección
        lineNumbering = parse_xml(r'<w:lnNumType %s w:countBy="1" w:restart="continuous"/>' % nsdecls('w'))
        sectPr = section._sectPr
        sectPr.append(lineNumbering)
        
def remove_line_numbering_from_docx(doc):
    # * aplicar numeración de líneas a todas las secciones del documento
    for section in doc.sections:
        if section._sectPr.xpath("w:lnNumType"):
            section._sectPr.remove(section._sectPr.xpath("w:lnNumType")[0])
            
def eliminar_pie_pagina(doc):
    for section in doc.sections:
        footer = section._sectPr
        for child in list(footer):
            if child.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}footerReference':
                footer.remove(child)