import ezdxf
import os

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace(".pdf", ".dxf")
    doc = ezdxf.new()
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 3400)
        H = dimensions.get("hauteur", 500)
        B = dimensions.get("largeur", 250)

        # VUE LONGITUDINALE (avec étriers, appuis, flèches, cotations)
        dx = 0
        dy = 0
        h_appui = 20

        # Poutre principale
        msp.add_lwpolyline([(dx, dy),
                            (dx + L, dy),
                            (dx + L, dy + H),
                            (dx, dy + H)],
                           close=True)

        # Appuis
        msp.add_line((dx, dy), (dx, dy - h_appui))
        msp.add_line((dx + L, dy), (dx + L, dy - h_appui))
        msp.add_text("Appui", dxfattribs={"insert": (dx - 40, dy - h_appui - 10), "height": 15})
        msp.add_text("Appui", dxfattribs={"insert": (dx + L - 30, dy - h_appui - 10), "height": 15})

        # Étriers
        nb_etr = 16
        spacing = L / nb_etr
        for i in range(nb_etr):
            x = dx + i * spacing
            msp.add_lwpolyline([(x, dy + 5), (x + 5, dy + 5), (x + 5, dy + H - 5), (x, dy + H - 5)], close=True)

        # Aciers longitudinaux
        msp.add_line((dx + 10, dy + 10), (dx + L - 10, dy + 10))
        msp.add_line((dx + 10, dy + H - 10), (dx + L - 10, dy + H - 10))

        # Flèches de charge
        fl_x = dx + L / 4
        msp.add_line((fl_x, dy + H + 50), (fl_x, dy + H))
        msp.add_text("P/2", dxfattribs={"insert": (fl_x - 10, dy + H + 60), "height": 15})

        fl2_x = dx + 3 * L / 4
        msp.add_line((fl2_x, dy + H + 50), (fl2_x, dy + H))
        msp.add_text("P/2", dxfattribs={"insert": (fl2_x - 10, dy + H + 60), "height": 15})

        # Cotation horizontale
        msp.add_text("3000", dxfattribs={"insert": (dx + 150, dy - 50), "height": 12})
        msp.add_text("700", dxfattribs={"insert": (dx + 3100, dy - 50), "height": 12})
        msp.add_text("3400", dxfattribs={"insert": (dx + 1400, dy - 80), "height": 14})

        # Titre
        msp.add_text("Ferraillage d’une poutre avec appuis simples", dxfattribs={"insert": (dx, dy + H + 100), "height": 20})
        msp.add_text("Schéma indicatif - cotations en mm", dxfattribs={"insert": (dx, dy + H + 80), "height": 10})

        # VUE EN COUPE (à droite)
        offset_x = dx + L + 100
        offset_y = dy
        msp.add_lwpolyline([(offset_x, offset_y),
                            (offset_x + B, offset_y),
                            (offset_x + B, offset_y + H),
                            (offset_x, offset_y + H)],
                           close=True)

        # Aciers de coin
        r = 5
        margin = 15
        msp.add_circle((offset_x + margin, offset_y + margin), r)
        msp.add_circle((offset_x + B - margin, offset_y + margin), r)
        msp.add_circle((offset_x + margin, offset_y + H - margin), r)
        msp.add_circle((offset_x + B - margin, offset_y + H - margin), r)

        # Cotation coupe
        msp.add_text("Ø10mm", dxfattribs={"insert": (offset_x + B + 10, offset_y + H - 20), "height": 10})
        msp.add_text("Ø8mm", dxfattribs={"insert": (offset_x + B + 10, offset_y + H / 2), "height": 10})
        msp.add_text("20mm", dxfattribs={"insert": (offset_x + B + 10, offset_y + 20), "height": 10})
        msp.add_text("250", dxfattribs={"insert": (offset_x + 30, offset_y - 20), "height": 10})
        msp.add_text("500", dxfattribs={"insert": (offset_x + B + 20, offset_y + H / 2), "height": 10})

    doc.saveas(dxf_path)
