import ezdxf
import os

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace(".pdf", ".dxf")
    doc = ezdxf.new()
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 5000) / 10
        H = dimensions.get("hauteur", 500) / 10
        B = dimensions.get("largeur", 300) / 10
        nb_etr = int(L // 20)

        # === VUE EN COUPE TRANSVERSALE ===
        origin_x, origin_y = 0, 0
        msp.add_lwpolyline([(origin_x, origin_y),
                            (origin_x + B, origin_y),
                            (origin_x + B, origin_y + H),
                            (origin_x, origin_y + H)],
                           close=True)

        # Étrier
        cadre_offset = 1
        msp.add_lwpolyline([(origin_x + cadre_offset, origin_y + cadre_offset),
                            (origin_x + B - cadre_offset, origin_y + cadre_offset),
                            (origin_x + B - cadre_offset, origin_y + H - cadre_offset),
                            (origin_x + cadre_offset, origin_y + H - cadre_offset)],
                           close=True)

        # Aciers dans les coins
        msp.add_circle((origin_x + 5, origin_y + 5), 1)
        msp.add_circle((origin_x + B - 5, origin_y + 5), 1)
        msp.add_circle((origin_x + 5, origin_y + H - 5), 1)
        msp.add_circle((origin_x + B - 5, origin_y + H - 5), 1)

        msp.add_text("Coupe A-A", dxfattribs={"insert": (origin_x, origin_y + H + 5)})

        # === VUE EN COUPE LONGITUDINALE ===
        base_x = 100
        base_y = 0
        msp.add_lwpolyline([(base_x, base_y),
                            (base_x + L, base_y),
                            (base_x + L, base_y + H),
                            (base_x, base_y + H)],
                           close=True)

        # Appuis
        msp.add_line((base_x, base_y), (base_x, base_y - 5))
        msp.add_line((base_x + L, base_y), (base_x + L, base_y - 5))

        # Aciers longitudinaux
        msp.add_line((base_x + 5, base_y + 5), (base_x + L - 5, base_y + 5))
        msp.add_line((base_x + 5, base_y + H - 5), (base_x + L - 5, base_y + H - 5))

        # Étriers
        for i in range(nb_etr):
            x = base_x + 5 + i * ((L - 10) / nb_etr)
            msp.add_lwpolyline([(x, base_y + 2),
                                (x + 1, base_y + 2),
                                (x + 1, base_y + H - 2),
                                (x, base_y + H - 2)],
                               close=True)

        # Cotes
        msp.add_text(f"L = {int(L * 10)} mm", dxfattribs={"insert": (base_x + L / 3, base_y - 10)})
        msp.add_text(f"H = {int(H * 10)} mm", dxfattribs={"insert": (base_x - 20, base_y + H / 2)})

        # Titre
        msp.add_text("Ferraillage d’une poutre sur appuis simples",
                     dxfattribs={"insert": (base_x, base_y + H + 10)})

    doc.saveas(dxf_path)
