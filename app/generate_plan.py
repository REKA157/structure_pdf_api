import ezdxf
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import matplotlib.pyplot as plt
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend

def generate_structural_plan(structure, dimensions, ferraillage, output_path):
    dxf_path = output_path.replace('.pdf', '.dxf')
    png_path = output_path.replace(".pdf", ".png")

    doc = ezdxf.new()
    msp = doc.modelspace()

    if structure == "poutre":
        L = dimensions.get("longueur", 5000) / 10
        H = dimensions.get("hauteur", 500) / 10

        # Dessin du contour
        msp.add_lwpolyline([(0, 0), (L, 0), (L, H), (0, H), (0, 0)], close=True)

        # Textes positionnés
        msp.add_text("Vue en plan / Top view", dxfattribs={"insert": (L / 4, -10)})
        msp.add_text(f"{ferraillage.get('ha', 'HA12')} - {ferraillage.get('nb_barres', 4)} barres",
                     dxfattribs={"insert": (10, H + 10)})
        msp.add_text("Coupe A-A / Section", dxfattribs={"insert": (0, H + 30)})

    doc.saveas(dxf_path)

    # ✅ Générer PNG depuis DXF
    try:
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ctx = RenderContext(doc)
        backend = MatplotlibBackend(ax)
        Frontend(ctx, backend).draw_layout(msp, finalize=True)
        plt.axis("off")
        plt.savefig(png_path, dpi=300)
        plt.close(fig)
    except Exception as e:
        print("Erreur lors du rendu PNG :", e)

    # ✅ Générer le PDF avec image et texte
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

    # ✅ Tente d'insérer l'image PNG si présente
    c.setFont("Helvetica-Oblique", 8)
    if os.path.exists(png_path):
        c.drawImage(os.path.abspath(png_path), x=300, y=500, width=200, preserveAspectRatio=True, mask='auto')
    else:
        c.drawString(300, 500, "⚠️ Image du plan non trouvée")

    c.drawString(50, 40, "Document généré automatiquement – Do not scale / Ne pas modifier")
    c.save()
