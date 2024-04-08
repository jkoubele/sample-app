curl -X GET http://127.0.0.1:5000/
curl -X POST -F "example_1.fastq=@./example_1.fastq" http://127.0.0.1:5000/compute_gc_content