import ezdxf
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import matplotlib as draw_mpl

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace('.pdf', '.dxf')
    doc = ezdxf.new()
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 5000) / 10
        H = dimensions.get("hauteur", 500) / 10

        # Dessin du contour
        msp.add_lwpolyline([(0, 0), (L, 0), (L, H), (0, H), (0, 0)], close=True)

        # Textes avec position correcte
        msp.add_text("Vue en plan / Top view", dxfattribs={"insert": (L/4, -10)})
        msp.add_text(f"{ferraillage.get('ha', 'HA12')} - {ferraillage.get('nb_barres', 4)} barres",
                     dxfattribs={"insert": (10, H + 10)})
        msp.add_text("Coupe A-A / Section", dxfattribs={"insert": (0, H + 30)})

    doc.saveas(dxf_path)
    # Conversion DXF vers image PNG
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    draw_mpl.draw_layout(doc.modelspace(), ax)
    plt.axis("off")

    png_path = output_path.replace(".pdf", ".png")
    plt.savefig(png_path, dpi=300)
    plt.close(fig)

    # Génération du PDF résumé
    c = canvas.Canvas(output_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, f"Plan de ferraillage – {structure.upper()}")
    c.setFont("Helvetica", 11)

    y = 760
    for label, value in dimensions.items():
        c.drawString(50, y, f"{label.capitalize()} : {value} mm")
        y -= 18

    y -= 10
    for label, value in ferraillage.items():
        c.drawString(50, y, f"{label} : {value}")
        y -= 18

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 40, "Document généré automatiquement – Do not scale / Ne pas modifier")
    c.drawImage(png_path, x=300, y=500, width=200, preserveAspectRatio=True, mask='auto')
    c.save()
