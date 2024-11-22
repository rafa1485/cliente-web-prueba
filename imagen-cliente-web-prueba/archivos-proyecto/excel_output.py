from openpyxl import Workbook
import numpy as np

aminoacidos_esenciales = ['histidina', 'isoleucina', 'leucina', 'lisina', 'metionina', 'fenilalanina', 'treonina', 'triptofano', 'valina']

def crear_tabla_calculos(nombres, fraccion_proteina, digestibilidad_proteina, contenido_aminoacidos, requerimientos, porcentajes_mezcla, aminoacidos_mezcla, puntaje_aminoacidos, digestibilidad, PDCAAS):
    wb = Workbook()

    ws = wb.active


    # TABLA 1 - Ingredientes
    ws.cell(row=2, column=2, value='INGRED.')

    ws.cell(row=2, column=3, value='FRAC. PROT.')

    ws.cell(row=2, column=4, value='DIGEST. PROT.')

    ws.cell(row=1, column=5, value='CONTENIDO DE AMINOACIDOS. [mg por gr de proteína]')

    for nc,aa_nombre in enumerate(aminoacidos_esenciales, start=5):
        ws.cell(row=2, column=nc, value=aa_nombre)


    for nf,id in enumerate(nombres.keys(), start=3):

        ws.cell(row=nf, column=2, value=nombres[id])

        ws.cell(row=nf, column=3, value=fraccion_proteina[id])

        ws.cell(row=nf, column=4, value=digestibilidad_proteina[id])

        for nc,aa in enumerate(contenido_aminoacidos[id], start=5):

            ws.cell(row=nf, column=nc, value=aa)


    # TABLA 2 - Requerimientos
    ws.cell(row=5+len(nombres), column=5, value='REQUERIMIENTOS DE  [mg por gr proteína]')
    
    for nc,aa_nombre in enumerate(aminoacidos_esenciales, start=5):
        ws.cell(row=6+len(nombres), column=nc, value=aa_nombre)

        ws.cell(row=7+len(nombres), column=nc, value=requerimientos[0][nc-5])

    # TABLA 3 - Porcentajes mezcla ingredientes
    ws.cell(row=2, column=7+len(aminoacidos_esenciales), value='FRACCION MEZCLA [%]')

    for nf,p in enumerate(porcentajes_mezcla,3):
        ws.cell(row=nf, column=7+len(aminoacidos_esenciales), value=p[0]*100)

    # TABLA 4 - Aminoácidos mezcla
    ws.cell(row=10+len(nombres), column=5, value='AMINOACIDOS EN MEZCLA  [mg por gr de mezcla]')
    
    for nc,aa_nombre in enumerate(aminoacidos_esenciales, start=5):
        ws.cell(row=11+len(nombres), column=nc, value=aa_nombre)
        ws.cell(row=12+len(nombres), column=nc, value=aminoacidos_mezcla[0][nc-5]  )

    # TABLA 5 - AAS 
    ws.cell(row=15+len(nombres), column=5, value='PUNTAJE DE AMINOACIDOS (AAS)')
    for nc,aa_nombre in enumerate(aminoacidos_esenciales, start=5):
        ws.cell(row=16+len(nombres), column=nc, value=aa_nombre)
        ws.cell(row=17+len(nombres), column=nc, value=puntaje_aminoacidos[0][nc-5] )

    # RESULTADO FINAL - DIGESTIBILIDAD Y PDCAAS
    ws.cell(row=20+len(nombres), column=5, value='DIGESTIBILIDAD')
    ws.cell(row=21+len(nombres), column=5, value=digestibilidad)

    ws.cell(row=23+len(nombres), column=5, value='PDCAAS')
    ws.cell(row=24+len(nombres), column=5, value=PDCAAS)

    return wb
