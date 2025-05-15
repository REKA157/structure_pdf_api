import ezdxf
import os

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace(".pdf", ".dxf")
    doc = ezdxf.new(setup=True)
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 3400)
        H = dimensions.get("hauteur", 500)
        B = dimensions.get("largeur", 250)

        dx = 0
        dy = 0
        h_appui = 20
        text_height = 40

        # Poutre principale
        msp.add_lwpolyline([(dx, dy), (dx + L, dy), (dx + L, dy + H), (dx, dy + H)], close=True)

        # Appuis
        msp.add_line((dx, dy), (dx, dy - h_appui))
        msp.add_line((dx + L, dy), (dx + L, dy - h_appui))

        # Zones d'étriers
        zone1_start = dx
        zone1_end = dx + 1400
        for i in range(14):
            x = zone1_start + i * 100
            msp.add_lwpolyline([(x, dy + 5), (x + 5, dy + 5), (x + 5, dy + H - 5), (x, dy + H - 5)], close=True)

        zone2_start = zone1_end
        zone2_end = zone2_start + 600
        for i in range(4):
            x = zone2_start + i * 150
            msp.add_lwpolyline([(x, dy + 5), (x + 5, dy + 5), (x + 5, dy + H - 5), (x, dy + H - 5)], close=True)

        zone3_start = zone2_end
        for i in range(14):
            x = zone3_start + i * 100
            msp.add_lwpolyline([(x, dy + 5), (x + 5, dy + 5), (x + 5, dy + H - 5), (x, dy + H - 5)], close=True)

        # Aciers longitudinaux
        msp.add_line((dx + 10, dy + 10), (dx + L - 10, dy + 10))
        msp.add_line((dx + 10, dy + H - 10), (dx + L - 10, dy + H - 10))

        # Repères
        msp.add_circle((zone1_start + 700, dy + H + 50), 20)
        msp.add_text("1", dxfattribs={"insert": (zone1_start + 693, dy + H + 40), "height": 25})
        msp.add_circle((zone2_start + 300, dy + H + 50), 20)
        msp.add_text("2", dxfattribs={"insert": (zone2_start + 293, dy + H + 40), "height": 25})
        msp.add_circle((zone3_start + 700, dy + H + 50), 20)
        msp.add_text("3", dxfattribs={"insert": (zone3_start + 693, dy + H + 40), "height": 25})

        # Légende
        legend_x = dx + L + 400
        legend_y = dy + H + 100
        msp.add_text("LÉGENDE : ", dxfattribs={"insert": (legend_x, legend_y), "height": 25})
        msp.add_text("(1) : 2HA6  l = 3.470  e = 0.080", dxfattribs={"insert": (legend_x, legend_y - 40), "height": 20})
        msp.add_text("(2) : 33DX6 l = 0.900  e = 0.150", dxfattribs={"insert": (legend_x, legend_y - 70), "height": 20})
        msp.add_text("(3) : 2HA6  l = 3.470  e = 0.080", dxfattribs={"insert": (legend_x, legend_y - 100), "height": 20})

        # Cotations texte manuelles
        msp.add_text("14 × 0.10", dxfattribs={"insert": (zone1_start + 500, dy - 60), "height": text_height})
        msp.add_text("4 × 0.15", dxfattribs={"insert": (zone2_start + 250, dy - 60), "height": text_height})
        msp.add_text("14 × 0.10", dxfattribs={"insert": (zone3_start + 500, dy - 60), "height": text_height})

        # Ajout de vraies cotations linéaires
        doc.dimstyles.new("MyDimStyle", dxfattribs={"dimtxsty": "Standard", "dimscale": 1})

        msp.add_linear_dim(base=(dx, dy - 150),
                           p1=(zone1_start, dy),
                           p2=(zone1_end, dy),
                           override={"dimstyle": "MyDimStyle"}).render()
        msp.add_linear_dim(base=(dx, dy - 180),
                           p1=(zone2_start, dy),
                           p2=(zone2_end, dy),
                           override={"dimstyle": "MyDimStyle"}).render()
        msp.add_linear_dim(base=(dx, dy - 210),
                           p1=(zone3_start, dy),
                           p2=(zone3_start + 1400, dy),
                           override={"dimstyle": "MyDimStyle"}).render()

        # Titre
        msp.add_text("Ferraillage d’une poutre avec cotations réelles", dxfattribs={"insert": (dx, dy + H + 150), "height": 30})

        # Vue en coupe
        cx = dx + L + 200
        cy = dy
        msp.add_lwpolyline([(cx, cy), (cx + B, cy), (cx + B, cy + H), (cx, cy + H)], close=True)

        r = 5
        margin = 15
        msp.add_circle((cx + margin, cy + margin), r)
        msp.add_circle((cx + B - margin, cy + margin), r)
        msp.add_circle((cx + margin, cy + H - margin), r)
        msp.add_circle((cx + B - margin, cy + H - margin), r)

        msp.add_text("Coupe transversale", dxfattribs={"insert": (cx, cy + H + 50), "height": 25})

    doc.saveas(dxf_path)
