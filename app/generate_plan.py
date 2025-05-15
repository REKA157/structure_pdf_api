import ezdxf
import os

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace(".pdf", ".dxf")
    doc = ezdxf.new()
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 5000) / 10  # échelle réduite
        H = dimensions.get("hauteur", 500) / 10
        B = dimensions.get("largeur", 300) / 10
        nb_etr = int(L // 20)

        # --- VUE EN COUPE TRANSVERSALE ---
        origin_x, origin_y = 0, 0
        msp.add_lwpolyline([(origin_x, origin_y),
                            (origin_x + B, origin_y),
                            (origin_x + B, origin_y + H),
                            (origin_x, origin_y + H)],
                           close=True)

        # Cadre (étriers - simplifiés ici)
        msp.add_lwpolyline([(origin_x + 1, origin_y + 1),
                            (origin_x + B - 1, origin_y + 1),
                            (origin_x + B - 1, origin_y + H - 1),
                            (origin_x + 1, origin_y + H - 1)],
                           close=True)

        # Aciers de traction (4 cercles)
        msp.add_circle((origin_x + 5, origin_y + 5), 1)
        msp.add_circle((origin_x + B - 5, origin_y + 5), 1)
        msp.add_circle((origin_x + 5, origin_y + H - 5), 1)
        msp.add_circle((origin_x + B - 5, origin_y + H - 5), 1)

        # Texte explicatif
        msp.add_text("Coupe A-A", dxfattribs={"insert": (origin_x, origin_y + H + 5)})
        msp.add_text("Cadre", dxfattribs={"insert": (origin_x + B + 2, origin_y + H/2)})
        msp.add_text("Aciers de traction", dxfattribs={"insert": (origin_x + B + 2, origin_y)})

        # --- VUE EN LONGUEUR ---
        base_x = 100
        base_y = 0
        msp.add_lwpolyline([(base_x, base_y),
                            (base_x + L, base_y),
                            (base_x + L, base_y + H),
                            (base_x, base_y + H)],
                           close=True)

        # Appuis simples (hachures)
        msp.add_line((base_x, base_y), (base_x, base_y - 5))
        msp.add_line((base_x + L, base_y), (base_x + L, base_y - 5))
        msp.add_text("Appui", dxfattribs={"insert": (base_x - 5, base_y - 8)})
        msp.add_text("Appui", dxfattribs={"insert": (base_x + L - 5, base_y - 8)})

        # Aciers longitudinaux
        msp.add_line((base_x + 5, base_y + 5), (base_x + L - 5, base_y + 5))   # bas
        msp.add_line((base_x + 5, base_y + H - 5), (base_x + L - 5, base_y + H - 5))  # haut

        # Étriers (répétés)
        for i in range(nb_etr):
            x = base_x + 5 + i * ((L - 10) / nb_etr)
            msp.add_lwpolyline([(x, base_y + 2),
                                (x + 1, base_y + 2),
                                (x + 1, base_y + H - 2),
                                (x, base_y + H - 2)],
                               close=True)

        # Titre
        msp.add_text("Ferraillage d’une poutre sur appuis simples",
                     dxfattribs={"insert": (base_x, base_y + H + 10)})

    doc.saveas(dxf_path)
