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
    output_path = f"app/output/plan_{structure}_{file_id}.pdf"

    generate_structural_plan(structure, dimensions, ferraillage, output_path)
    return FileResponse(output_path, media_type="application/pdf", filename=os.path.basename(output_path))

@app.get("/download-dxf")
async def download_last_dxf():
    try:
        files = sorted(glob.glob("app/output/*.dxf"), key=os.path.getmtime, reverse=True)
        if not files:
            return {"error": "Aucun fichier DXF trouvé."}
        latest_dxf = files[0]
        return FileResponse(latest_dxf, media_type="application/dxf", filename=os.path.basename(latest_dxf))
    except Exception as e:
        return {"error": str(e)}
