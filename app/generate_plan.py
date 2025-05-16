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
        nb_barres = ferraillage.get("nb_barres", 2)
        etrs = ferraillage.get("etrs", "8@20")

        dx, dy = 100, 200
        text_height = 25

        # === VUE LONGITUDINALE ===
        msp.add_lwpolyline([(dx, dy), (dx + L, dy), (dx + L, dy + H), (dx, dy + H)], close=True)

        # Appuis + texte
        msp.add_line((dx, dy), (dx, dy - 20))
        msp.add_line((dx + L, dy), (dx + L, dy - 20))
        msp.add_text("Appui 20 cm", dxfattribs={"insert": (dx - 50, dy - 40), "height": text_height})
        msp.add_text("Appui 20 cm", dxfattribs={"insert": (dx + L - 50, dy - 40), "height": text_height})

        # Aciers longitudinaux
        msp.add_line((dx + 20, dy + 20), (dx + L - 20, dy + 20))  # bas
        msp.add_line((dx + 20, dy + H - 20), (dx + L - 20, dy + H - 20))  # haut

        msp.add_line((dx + L / 2, dy + H), (dx + L / 2, dy + H + 50))
        msp.add_text(f"{nb_barres} {ha_type}", dxfattribs={"insert": (dx + L / 2 + 10, dy + H + 50), "height": text_height})

        # Étriers espacés
        nb_etr = int(L / 200)
        spacing = L / nb_etr
        for i in range(nb_etr):
            x = dx + i * spacing
            msp.add_lwpolyline([(x, dy + 5), (x + 2, dy + 5), (x + 2, dy + H - 5), (x, dy + H - 5)], close=True)

        # Flèche horizontale + texte étriers
        fx = dx + 300
        fy = dy + H / 2
        msp.add_line((fx, fy), (fx + 100, fy))
        msp.add_text(f"{etrs}", dxfattribs={"insert": (fx + 110, fy + 10), "height": text_height})

        # Repère (1)
        rx1 = dx + 800
        msp.add_line((rx1, dy + H), (rx1, dy + H + 50))
        msp.add_circle((rx1, dy + H + 70), 10)
        msp.add_text("1", dxfattribs={"insert": (rx1 - 5, dy + H + 62), "height": 15})

        # Repère (2)
        rx2 = dx + 1200
        msp.add_line((rx2, dy + H / 2), (rx2 + 80, dy + H / 2))
        msp.add_circle((rx2 + 100, dy + H / 2), 10)
        msp.add_text("2", dxfattribs={"insert": (rx2 + 95, dy + H / 2 - 5), "height": 15})

        # === VUE EN COUPE TRANSVERSALE ===
        cx = dx
        cy = dy + H + 300
        cover = 25
        msp.add_lwpolyline([(cx, cy), (cx + B, cy), (cx + B, cy + H), (cx, cy + H)], close=True)

        # Aciers d’angle avec annotation
        r = 5
        msp.add_circle((cx + cover, cy + cover), r)
        msp.add_line((cx + cover, cy + cover), (cx + cover - 30, cy + cover - 30))
        msp.add_text(f"{nb_barres} {ha_type}", dxfattribs={"insert": (cx + cover - 70, cy + cover - 30), "height": 20})

        msp.add_circle((cx + B - cover, cy + cover), r)
        msp.add_circle((cx + cover, cy + H - cover), r)
        msp.add_circle((cx + B - cover, cy + H - cover), r)

        msp.add_line((cx + B - 20, cy + H - 20), (cx + B + 30, cy + H + 30))
        msp.add_text("Cadres HA6", dxfattribs={"insert": (cx + B + 40, cy + H + 30), "height": 20})

        msp.add_text("Section I-I", dxfattribs={"insert": (cx, cy - 50), "height": 20})

        # Tableau annotations
        lx = dx + L + 400
        ly = dy + H + 100
        msp.add_text("LÉGENDE : ", dxfattribs={"insert": (lx, ly), "height": 25})
        msp.add_text(f"Longitudinal : {nb_barres} {ha_type}", dxfattribs={"insert": (lx, ly - 40), "height": 20})
        msp.add_text(f"Etriers : {etrs}", dxfattribs={"insert": (lx, ly - 70), "height": 20})

    doc.saveas(dxf_path)
