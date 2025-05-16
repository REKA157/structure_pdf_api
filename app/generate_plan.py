import ezdxf
import os

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace(".pdf", ".dxf")
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 5000)
        H = dimensions.get("hauteur", 250)
        B = dimensions.get("largeur", 400)
        ha_type = ferraillage.get("ha", "HA12")
        nb_barres = ferraillage.get("nb_barres", 4)
        etrs = ferraillage.get("etrs", "8@20")

        dx, dy = 100, 200
        text_height = 25

        # === VUE EN COUPE ===
        cx = dx
        cy = dy + H + 300
        cover = 25
        msp.add_lwpolyline([(cx, cy), (cx + B, cy), (cx + B, cy + H), (cx, cy + H)], close=True)

        # Cadre d'étrier unique (rectangle intérieur)
        msp.add_lwpolyline([(cx + cover, cy + cover), (cx + B - cover, cy + cover),
                            (cx + B - cover, cy + H - cover), (cx + cover, cy + H - cover)], close=True)

        # Annotation "Cadre HA6"
        msp.add_text("Cadre HA6", dxfattribs={"insert": (cx + B + 20, cy + H - 10), "height": text_height})

        # Annotation flèche acier longitudinal (trait + texte décalé)
        start = (cx + B - cover, cy + cover + 5)
        end = (cx + B + 40, cy + cover - 30)
        msp.add_line(start, end)
        msp.add_text(f"{nb_barres} {ha_type}", dxfattribs={"insert": (end[0] + 10, end[1]), "height": text_height})

        # === COTATIONS RECTANGLE ===

        # Largeur (horizontal, haut)
        cxm = cx + B / 2 - 30
        msp.add_line((cx, cy + H + 40), (cx + B, cy + H + 40))
        msp.add_text("<------------------->", dxfattribs={"insert": (cxm, cy + H + 50), "height": 20})
        msp.add_text(f"{B} mm", dxfattribs={"insert": (cx + B / 2 - 10, cy + H + 70), "height": 20})

        # Hauteur (vertical, gauche)
        cym = cy + H / 2 - 10
        msp.add_line((cx - 40, cy), (cx - 40, cy + H))
        msp.add_text("^", dxfattribs={"insert": (cx - 45, cy + H + 5), "height": 20})
        msp.add_text("v", dxfattribs={"insert": (cx - 45, cy - 20), "height": 20})
        msp.add_text(f"{H} mm", dxfattribs={"insert": (cx - 70, cym), "height": 20})

        # Titre section
        msp.add_text("Section I-I", dxfattribs={"insert": (cx, cy - 50), "height": 20})

    doc.saveas(dxf_path)
