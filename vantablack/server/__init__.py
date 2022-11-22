from typing import Optional
from flask import Flask, Response, render_template, request, redirect
import fs.zipfs
from simfile.dir import SimfileDirectory

from vantablack.rule import RuleViolation

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000

DIRS_TO_IGNORE = ["__MACOSX"]


def _process_simfile_directory(simfile_dir: SimfileDirectory) -> Response:
    return ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_file():
    if "songfolder" not in request.files:
        return redirect(request.url)

    file = request.files["songfolder"]

    if file.filename == "":
        return redirect(request.url)

    with fs.zipfs.ZipFS(file.stream) as zip_fs:
        zip_components = [
            item for item in zip_fs.listdir("/") if item not in DIRS_TO_IGNORE
        ]
        match zip_components:
            case [simfile_dir_path]:
                directory = SimfileDirectory(simfile_dir_path, filesystem=zip_fs)
                return _process_simfile_directory(directory)
            case []:
                return "invalid! empty ZIP"
            case _:
                # TODO: Have special output for this.
                return "invalid! your ZIP file should contain exactly one top-level folder."
