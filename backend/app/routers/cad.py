from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import os
import shutil
from datetime import datetime
from pathlib import Path

router = APIRouter(
    prefix="/api/cad",
    tags=["cad"]
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads/cad_files")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_cad_file(file: UploadFile = File(...)):
    """
    Upload and process a CAD file
    Supported formats: DXF, DWG, STEP, IGES, STL, OBJ
    """
    try:
        # Validate file extension
        allowed_extensions = {'.dxf', '.dwg', '.step', '.stp', '.iges', '.igs', '.stl', '.obj'}
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
            )

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / safe_filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process CAD file based on type
        analysis_result = await analyze_cad_file(file_path, file_ext)

        return {
            "success": True,
            "message": "CAD file uploaded and analyzed successfully",
            "filename": safe_filename,
            "file_type": file_ext,
            "file_size": file_path.stat().st_size,
            "upload_path": str(file_path),
            "analysis": analysis_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process CAD file: {str(e)}"
        )


async def analyze_cad_file(file_path: Path, file_ext: str) -> dict:
    """
    Analyze CAD file and extract basic information
    """
    analysis = {
        "file_format": file_ext,
        "status": "processed"
    }

    try:
        if file_ext == '.dxf':
            # Use ezdxf to analyze DXF files
            import ezdxf

            doc = ezdxf.readfile(str(file_path))
            modelspace = doc.modelspace()

            # Count entities
            entity_counts = {}
            for entity in modelspace:
                entity_type = entity.dxftype()
                entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

            # Get layer information
            layers = [layer.dxf.name for layer in doc.layers]

            analysis.update({
                "dxf_version": doc.dxfversion,
                "entity_count": len(list(modelspace)),
                "entity_types": entity_counts,
                "layer_count": len(layers),
                "layers": layers[:10],  # First 10 layers
                "units": doc.header.get('$INSUNITS', 'Not specified')
            })

        elif file_ext in ['.stl']:
            # Use trimesh for STL files
            import trimesh

            mesh = trimesh.load(str(file_path))

            analysis.update({
                "vertices": len(mesh.vertices),
                "faces": len(mesh.faces),
                "is_watertight": mesh.is_watertight,
                "volume": float(mesh.volume) if mesh.is_watertight else None,
                "surface_area": float(mesh.area),
                "bounds": {
                    "min": mesh.bounds[0].tolist(),
                    "max": mesh.bounds[1].tolist()
                }
            })

        else:
            # For other formats, just return basic file info
            analysis.update({
                "note": f"Basic file validation passed for {file_ext} format",
                "advanced_analysis": "Available on request"
            })

    except ImportError as e:
        analysis["warning"] = f"Advanced analysis not available: {str(e)}"
    except Exception as e:
        analysis["error"] = f"Analysis error: {str(e)}"

    return analysis


@router.get("/uploads")
async def list_uploaded_files():
    """
    List all uploaded CAD files
    """
    files = []
    for file_path in UPLOAD_DIR.glob("*"):
        if file_path.is_file():
            files.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "uploaded_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            })

    return {
        "total": len(files),
        "files": sorted(files, key=lambda x: x['uploaded_at'], reverse=True)
    }
