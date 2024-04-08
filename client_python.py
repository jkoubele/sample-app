import requests
from pathlib import Path
import matplotlib.pyplot as plt

if __name__ == "__main__":
    file_path = Path('example_1.fastq')
    with open(file_path) as file:
        response = requests.post('http://127.0.0.1:5000/compute_gc_content', files={file_path.name: file})
        response_content = response.json()
        print(f"{response_content=}")
    with open('response.json', 'w') as output_file:
        output_file.write(str(response.text))
    # Plot the histogram:
    x = [(response_content['bins'][i] + response_content['bins'][i - 1]) / 2 for i in
         range(1, len(response_content['bins']))]
    plt.bar(x, response_content['counts'], width=0.1)
    plt.xlabel('Fraction of GC content')
    plt.ylabel('Reads')
    plt.title('Histogram of GC content among reads')
    plt.show()
