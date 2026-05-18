from pathlib import Path
from zipfile import ZipFile

root = Path(__file__).resolve().parent
output_dir = root / "output"
zip_path = root / "output_qgis_files.zip"

with ZipFile(zip_path, "w") as archive:
    for path in output_dir.glob("*"):
        archive.write(path, arcname=path.name)

print(f"ZIP criado em: {zip_path}")
