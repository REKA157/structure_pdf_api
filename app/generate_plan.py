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

        # === VUE LONGITUDINALE ===
        msp.add_lwpolyline([(dx, dy), (dx + L, dy), (dx + L, dy + H), (dx, dy + H)], close=True)

        # Appuis + texte
        msp.add_line((dx, dy), (dx, dy - 20))
        msp.add_line((dx + L, dy), (dx + L, dy - 20))
        msp.add_text("Appui 20 cm", dxfattribs={"insert": (dx - 50, dy - 40), "height": text_height})
        msp.add_text("Appui 20 cm", dxfattribs={"insert": (dx + L - 50, dy - 40), "height": text_height})

        # Trait sous poutre "< >" + texte L
        msp.add_line((dx, dy - 70), (dx + L, dy - 70))
        msp.add_text("<", dxfattribs={"insert": (dx - 10, dy - 75), "height": text_height})
        msp.add_text(">", dxfattribs={"insert": (dx + L, dy - 75), "height": text_height})
        msp.add_text(f"{L} mm", dxfattribs={"insert": (dx + L / 2 - 40, dy - 75), "height": text_height})

        # Aciers longitudinaux + flèche verticale
        msp.add_line((dx + 20, dy + 20), (dx + L - 20, dy + 20))
        msp.add_line((dx + 20, dy + H - 20), (dx + L - 20, dy + H - 20))
        msp.add_line((dx + L / 2, dy + H), (dx + L / 2, dy + H + 50))
        msp.add_text(f"{nb_barres} {ha_type}", dxfattribs={"insert": (dx + L / 2 + 10, dy + H + 50), "height": text_height * 1.2})

        # Étriers
        nb_etr = int(L / 200)
        spacing = L / nb_etr
        for i in range(nb_etr):
            x = dx + i * spacing
            msp.add_lwpolyline([(x, dy + 5), (x + 2, dy + 5), (x + 2, dy + H - 5), (x, dy + H - 5)], close=True)

        # Flèche étriers + flèche verticale descendante
        fx = dx + 300
        fy = dy + H / 2
        msp.add_line((fx, fy), (fx + 100, fy))
        msp.add_text(f"{etrs}", dxfattribs={"insert": (fx + 110, fy + 10), "height": text_height})
        msp.add_line((fx + 150, fy), (fx + 150, fy - 50))
        msp.add_text(f"{etrs}", dxfattribs={"insert": (fx + 155, fy - 60), "height": text_height * 1.2})

        # Repère 1
        rx1 = dx + 800
        msp.add_line((rx1, dy + H), (rx1, dy + H + 50))
        msp.add_circle((rx1, dy + H + 70), 10)
        msp.add_text("1", dxfattribs={"insert": (rx1 - 5, dy + H + 62), "height": text_height * 1.2})

        # Repère 2
        rx2 = dx + 1200
        msp.add_line((rx2, dy + H / 2), (rx2 + 80, dy + H / 2))
        msp.add_circle((rx2 + 100, dy + H / 2), 10)
        msp.add_text("2", dxfattribs={"insert": (rx2 + 95, dy + H / 2 - 5), "height": text_height * 1.2})

        # === VUE EN COUPE TRANSVERSALE ===
        cx = dx
        cy = dy + H + 300
        cover = 25
        msp.add_lwpolyline([(cx, cy), (cx + B, cy), (cx + B, cy + H), (cx, cy + H)], close=True)

        # Cadre unique
        msp.add_lwpolyline([(cx + cover, cy + cover), (cx + B - cover, cy + cover),
                            (cx + B - cover, cy + H - cover), (cx + cover, cy + H - cover)], close=True)
        msp.add_text("Cadre HA6", dxfattribs={"insert": (cx + B + 40, cy + H + 30), "height": text_height * 1.2})

        # Flèche diagonale + texte acier longitudinal
        start = (cx + cover, cy + cover + 5)
        end = (cx + cover - 30, cy + cover - 30)
        msp.add_line(start, end)
        msp.add_text(f"{nb_barres} {ha_type}", dxfattribs={"insert": (end[0] - 30, end[1]), "height": text_height})

        # Cotation largeur B
        msp.add_line((cx, cy + H + 40), (cx + B, cy + H + 40))
        msp.add_text("<", dxfattribs={"insert": (cx - 10, cy + H + 40), "height": 20})
        msp.add_text(">", dxfattribs={"insert": (cx + B + 10, cy + H + 40), "height": 20})
        msp.add_text(f"{B} mm", dxfattribs={"insert": (cx + B / 2 - 20, cy + H + 60), "height": 20})

        # Cotation hauteur H
        msp.add_line((cx - 40, cy), (cx - 40, cy + H))
        msp.add_text("^", dxfattribs={"insert": (cx - 45, cy + H + 5), "height": 20})
        msp.add_text("v", dxfattribs={"insert": (cx - 45, cy - 20), "height": 20})
        msp.add_text(f"{H} mm", dxfattribs={"insert": (cx - 80, cy + H / 2), "height": 20})

        # Titre
        msp.add_text("Section I-I", dxfattribs={"insert": (cx, cy - 50), "height": text_height * 1.15})

        # Légende
        lx = dx + L + 400
        ly = dy + H + 100
        msp.add_text("LÉGENDE : ", dxfattribs={"insert": (lx, ly), "height": 25})
        msp.add_text(f"Longitudinal : {nb_barres} {ha_type}", dxfattribs={"insert": (lx, ly - 40), "height": 20})
        msp.add_text(f"Etriers : {etrs}", dxfattribs={"insert": (lx, ly - 70), "height": 20})

    doc.saveas(dxf_path)
