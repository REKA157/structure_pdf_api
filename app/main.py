from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from app.generate_plan import generate_structural_plan
import uuid
import os
import glob

app = FastAPI()

@app.post("/generate-pdf")
async def generate_pdf(request: Request):
    data = await request.json()
    structure = data.get("structure", "poutre")
    dimensions = data.get("dimensions", {})
    ferraillage = data.get("ferraillage", {})

    file_id = uuid.uuid4().hex
    pdf_path = f"app/output/plan_{structure}_{file_id}.pdf"
    dxf_path = pdf_path.replace(".pdf", ".dxf")

    generate_structural_plan(structure, dimensions, ferraillage, pdf_path)

    # Lien simulé du dxf
    dxf_filename = os.path.basename(dxf_path)
    dxf_download_url = f"/download-dxf/{dxf_filename}"

    return {
        "message": "PDF généré avec succès",
        "pdf": f"/generate-pdf (téléchargement automatique)",
        "dxf_download_link": dxf_download_url
    }

@app.get("/download-dxf/{filename}")
async def download_dxf_file(filename: str):
    filepath = os.path.join("app/output", filename)
    if not os.path.exists(filepath):
        return {"error": "Fichier introuvable"}
    return FileResponse(filepath, media_type="application/dxf", filename=filename)
