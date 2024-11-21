from openpyxl import Workbook
import numpy as np

aminoacidos_esenciales = ['histidina', 'isoleucina', 'leucina', 'lisina', 'metionina', 'fenilalanina', 'treonina', 'triptofano', 'valina']

def crear_tabla_calculos(nombres, fraccion_proteina, digestibilidad_proteina, contenido_aminoacidos, requerimientos):
    wb = Workbook()

    ws = wb.active

    ws.cell(row=2, column=2, value='INGRED.')

    ws.cell(row=2, column=3, value='FRAC. PROT.')

    ws.cell(row=2, column=4, value='DIGEST. PROT.')

    ws.cell(row=1, column=5, value='CONT. AMINOACIDOS. [mg por gr de proteína]')

    ws.cell(row=9, column=5, value='REQUERI. AMINOACIDOS')

    for nc,aa_nombre in enumerate(aminoacidos_esenciales, start=5):
        ws.cell(row=2, column=nc, value=aa_nombre)

    for nf,id in enumerate(nombres.keys(), start=3):

        ws.cell(row=nf, column=2, value=nombres[id])

        ws.cell(row=nf, column=3, value=fraccion_proteina[id])

        ws.cell(row=nf, column=4, value=digestibilidad_proteina[id])

        for nc,aa in enumerate(contenido_aminoacidos[id], start=5):

            ws.cell(row=nf, column=nc, value=aa)

            ws.cell(row=10, column=nc, value=requerimientos[0][nc-5])


    print('requerimientos')
    print(requerimientos)
    return wb
