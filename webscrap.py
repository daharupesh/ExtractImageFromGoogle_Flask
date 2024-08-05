from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as UReq
import os

app = Flask(__name__)

@app.route("/")
def show_page():
    return render_template("index.html")


@app.route("/extract", methods=["POST"])
def extract_img():
    save_dir = "images/"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    query = request.form.get("query")  # Corrected the way to get the form data
    response = requests.get(f"https://www.google.com/search?sca_esv=40a5306b60f26a7a&sxsrf=ADLYWIKOcUUaJ4fNwBgOGh-l9WqnHEZ0DA:1722847976157&q={query}&udm=2&fbs=AEQNm0AMrUEM0u25RSHSP2GXBv1FqRTJXslv5T9cWPShXuZK-unDRtidhDD6MO07O664cf3rzCkRGzT6TOmIkWN6z59BEI_sG_WvMHTpzIDOeN0PG5PbQE-fUxh_CRmIjIVTMPZLqRLt8LEJmd-JeyXMTy_SsVO4Ripm82z6vpZhP9tO4TJ_Xc2C9SbcBfqKU5SUBcd-NfHrlEA0NtWnPbhLSCHG8iDz0g&sa=X&sqi=2&ved=2ahUKEwiAufvsvN2HAxU9wTgGHSTQNWsQtKgLegQIDhAB&biw=1536&bih=730&dpr=1.25#vhid=xF-XssFToaUyGM&vssid=mosaic")
    soup = BeautifulSoup(response.content, "html.parser")
    image_tag = soup.find_all("img")
    del image_tag[0]
    for i in image_tag:
        image_url = i["src"]
        image_data = requests.get(image_url).content
        with open(os.path.join(save_dir, f"{query}_{image_tag.index(i)}.jpg"), "wb") as f:
            f.write(image_data)

    return "Images extracted successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000)
