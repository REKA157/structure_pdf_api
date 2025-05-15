import ezdxf
import os

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace(".pdf", ".dxf")
    doc = ezdxf.new()
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 5000)  # mm
        H = dimensions.get("hauteur", 500)
        B = dimensions.get("largeur", 300)
        nb_etr = max(3, int(L // 500))  # étriers tous les 500 mm

        # Centrage
        cx, cy = 0, 0
        x0 = cx - B // 2
        y0 = cy - H // 2

        # Coupe transversale
        msp.add_lwpolyline([(x0, y0), (x0 + B, y0), (x0 + B, y0 + H), (x0, y0 + H)], close=True)

        # Étrier intérieur
        msp.add_lwpolyline([(x0 + 10, y0 + 10), (x0 + B - 10, y0 + 10),
                            (x0 + B - 10, y0 + H - 10), (x0 + 10, y0 + H - 10)], close=True)

        # Aciers coin
        r = 5
        msp.add_circle((x0 + 10, y0 + 10), r)
        msp.add_circle((x0 + B - 10, y0 + 10), r)
        msp.add_circle((x0 + 10, y0 + H - 10), r)
        msp.add_circle((x0 + B - 10, y0 + H - 10), r)

        # Coupe longitudinale
        dx = 600
        ly = y0
        msp.add_lwpolyline([(dx, ly), (dx + L, ly), (dx + L, ly + H), (dx, ly + H)], close=True)

        # Appuis
        msp.add_line((dx, ly), (dx, ly - 20))
        msp.add_line((dx + L, ly), (dx + L, ly - 20))

        # Aciers longitudinaux
        msp.add_line((dx + 10, ly + 10), (dx + L - 10, ly + 10))
        msp.add_line((dx + 10, ly + H - 10), (dx + L - 10, ly + H - 10))

        # Étriers
        for i in range(nb_etr):
            x = dx + 10 + i * ((L - 20) / nb_etr)
            msp.add_lwpolyline([(x, ly + 5), (x + 5, ly + 5),
                                (x + 5, ly + H - 5), (x, ly + H - 5)], close=True)

        # Titre
        msp.add_text("Ferraillage d’une poutre avec appuis simples",
                     dxfattribs={"insert": (dx, ly + H + 40)})

    doc.saveas(dxf_path)
