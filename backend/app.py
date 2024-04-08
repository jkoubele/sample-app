from pathlib import Path

import numpy as np
from Bio import SeqIO, SeqUtils
from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

tmp_folder = Path(__file__).parent / 'tmp'
tmp_folder.mkdir(parents=True, exist_ok=True)


def compute_gc_content_from_fastq(fastq_path: Path) -> dict[str, list]:
    cg_contents = [SeqUtils.gc_fraction(record) for record in SeqIO.parse(fastq_path, "fastq")]
    histogram = np.histogram(cg_contents, range=(0, 1.0))
    return {'counts': histogram[0].tolist(), 'bins': histogram[1].tolist()}


@app.route('/')
def index():
    return 'This app computes GC content histogram from .fastq file (submit on /compute_gc_content) endpoint.'


@app.route('/compute_gc_content', methods=['POST'])
def compute_gc_content():
    if len(request.files) != 1:
        return "Please provide exactly one .fastq file."
    for file_name, file_storage in request.files.items():
        tmp_file_path = tmp_folder / file_name
        file_storage.save(tmp_file_path)
    gc_content_histogram = compute_gc_content_from_fastq(tmp_file_path)
    tmp_file_path.unlink()
    return make_response(jsonify(gc_content_histogram), 200)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
