from flask import Flask,render_template,request
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO


math_app = Flask(__name__)

#ホーム画面
@math_app.route("/")
def home():
    return render_template("home.html") #home.htmlを返す


#Plot画面
@math_app.route("/plot", methods=['GET', "POST"])
def plot():
    if request.method == 'GET':
        print("Route /plot accessed")
        return render_template("plot_index.html")
    
    
    if request.method == 'POST':
        d = request.files["file_data"]
        su = request.form.get("calum")
        ku = request.form.get("retu_s")
        uu = request.form.get("retu_e")

        s = int(su)
        k = int(ku)
        u = int(uu)


        data_set = np.loadtxt(
            d,
            dtype = "float",
            delimiter = ",",
            skiprows=s-1,
            usecols=[k-1,u-1]
        )

        for i in data_set:
            plt.scatter(i[0],i[1])
        #plt.plot(data_set[:, 0],data_set[:, 1])
        io = BytesIO()
        plt.savefig(io, format='png')
        io.seek(0)
        plt.close()

        data = base64.b64encode(io.getbuffer()).decode("ascii")

        return render_template(
            'index.html',
            data = data
        )


# #平均計算画面
# @math_app.route("/Mean")

