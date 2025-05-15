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

        dx = 0
        dy = 0
        h_appui = 20
        text_height = 50

        # Poutre principale (vue longitudinale)
        msp.add_lwpolyline([(dx, dy),
                            (dx + L, dy),
                            (dx + L, dy + H),
                            (dx, dy + H)],
                           close=True)

        # Appuis
        msp.add_line((dx, dy), (dx, dy - h_appui))
        msp.add_line((dx + L, dy), (dx + L, dy - h_appui))
        msp.add_text("Appui", dxfattribs={"insert": (dx - 80, dy - h_appui - 20), "height": text_height})
        msp.add_text("Appui", dxfattribs={"insert": (dx + L - 80, dy - h_appui - 20), "height": text_height})

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
        msp.add_line((fl_x, dy + H + 100), (fl_x, dy + H))
        msp.add_text("P/2", dxfattribs={"insert": (fl_x - 40, dy + H + 120), "height": text_height})

        fl2_x = dx + 3 * L / 4
        msp.add_line((fl2_x, dy + H + 100), (fl2_x, dy + H))
        msp.add_text("P/2", dxfattribs={"insert": (fl2_x - 40, dy + H + 120), "height": text_height})

        # Cotes texte
        msp.add_text("3000", dxfattribs={"insert": (dx + 100, dy - 100), "height": text_height})
        msp.add_text("700", dxfattribs={"insert": (dx + 3100, dy - 100), "height": text_height})
        msp.add_text("L = 3400 mm", dxfattribs={"insert": (dx + L / 3, dy - 160), "height": text_height})

        # Titre
        msp.add_text("Ferraillage d’une poutre avec appuis simples",
                     dxfattribs={"insert": (dx, dy + H + 180), "height": text_height})
        msp.add_text("Schéma indicatif - cotations en mm",
                     dxfattribs={"insert": (dx, dy + H + 140), "height": text_height // 2})

        # Vue en coupe
        offset_x = dx + L + 200
        offset_y = dy
        msp.add_lwpolyline([(offset_x, offset_y),
                            (offset_x + B, offset_y),
                            (offset_x + B, offset_y + H),
                            (offset_x, offset_y + H)],
                           close=True)

        r = 5
        margin = 15
        msp.add_circle((offset_x + margin, offset_y + margin), r)
        msp.add_circle((offset_x + B - margin, offset_y + margin), r)
        msp.add_circle((offset_x + margin, offset_y + H - margin), r)
        msp.add_circle((offset_x + B - margin, offset_y + H - margin), r)

        # Cotations coupe
        msp.add_text("Ø10mm", dxfattribs={"insert": (offset_x + B + 20, offset_y + H - 30), "height": text_height // 2})
        msp.add_text("Ø8mm", dxfattribs={"insert": (offset_x + B + 20, offset_y + H / 2), "height": text_height // 2})
        msp.add_text("20mm", dxfattribs={"insert": (offset_x + B + 20, offset_y + 30), "height": text_height // 2})
        msp.add_text("250", dxfattribs={"insert": (offset_x + 20, offset_y - 40), "height": text_height // 2})
        msp.add_text("500", dxfattribs={"insert": (offset_x + B + 20, offset_y + H / 2 - 40), "height": text_height // 2})

    doc.saveas(dxf_path)
