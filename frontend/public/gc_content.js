function uploadFile() {
      const fileInput = document.getElementById('formFile');
      const file = fileInput.files[0];

      if (!file) {
        alert('Please select a file.');
        return;
      }

      const xhr = new XMLHttpRequest();
      const formData = new FormData();
      formData.append('file', file);

      var hostIPAddress = window.location.hostname
      console.log(hostIPAddress)
      xhr.open('POST', 'http://'+hostIPAddress+':5000/compute_gc_content', true);
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status >= 200 && xhr.status < 300) {
            var ret = JSON.parse(xhr.responseText);

            updateHistogram(ret)
          } else {
            alert('Error uploading file.');
          }
        }
      };
      xhr.send(formData);
    }


function updateHistogram(histogram_data){
    console.log(histogram_data)
    x=[]
    for(i=0; i<histogram_data['bins'].length-1; i++){
        x.push((histogram_data['bins'][i] + histogram_data['bins'][i+1])/2)
    }
    var data = [
      {
        x: x,
        y: histogram_data['counts'],
        type: 'bar'
      }
    ];
    var layout = {
      title: 'GC Content Histogram',
      xaxis: {title: 'GC content fraction'},
      yaxis: {title: 'Num. Reads'}
    };

    Plotly.newPlot('histogram', data, layout);
}

