import requests

url = "https://github.com/opencv/opencv_3rdparty/raw/master/dnn_models/res10_300x300_ssd_iter_140000.caffemodel"
output_path = "facial_detector/res10_300x300_ssd_iter_140000.caffemodel"

response = requests.get(url, stream=True)

if response.status_code == 200:
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print("Download complete!")
else:
    print("Failed to download file. Status code:", response.status_code)
