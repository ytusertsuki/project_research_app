from flask import Flask,render_template,request
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from app.function.mean_calc import calc_mean ,calc_mode,calc_stdev,calc_var

math_app = Flask(__name__)

#ホーム画面
@math_app.route("/")
def home():
    return render_template("home.html") #home.htmlを返す


#Plot画面
@math_app.route("/plot", methods=['GET', "POST"])
def plot():
    if request.method == 'GET':
        return render_template("plot_index.html")
    
    
    if request.method == 'POST':
        d = request.files["file_data"]
        su = request.form.get("calum")
        ku = request.form.get("retu_s")
        uu = request.form.get("retu_e")

        if d and su and ku and uu:
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
                'plot_index.html',
                data = data
            )
        
        else:
            erro = ("※入力項目に空きがあります")
            return render_template(
                'plot_index.html',
                erro=erro
            )


#平均計算画面
@math_app.route("/mean", methods=['GET', "POST"])
def mean():
    if request.method == 'GET':
        return render_template("mean_index.html")

    if request.method == 'POST':
        #初期値
        results = {
            "mean": None,
            "mode": None,
            "var": None,
            "stdev": None
        }
        #入力された数字を受け取る
        values = request.form['number']
        try:
            #入力されたフォームを_で要素に分ける
            values_list = [int(value) for value in values.split()]
            #チェックされたボックスのvalueを得る
            selected_metrics = request.form.getlist('check')
            print(selected_metrics)
            if 'mean' in selected_metrics:
                results["mean"] = calc_mean(values_list)
            else:
                results["mean"] = ""

            if 'mode' in selected_metrics:    
                results["mode"] = calc_mode(values_list)
            else:
                results["mode"] = ""
            
            if 'var' in selected_metrics:    
                results["var"] = calc_var(values_list)
            else:
                results["var"] = ""

            if 'stdev' in selected_metrics:    
                results["stdev"] = calc_stdev(values_list)
            else:
                results["stdev"] = ""
            print(results)
            return render_template("mean_index.html",A=results["mean"],B=results["mode"],C=results["var"],D=results["stdev"],valueErrorMessage="")

        except ValueError as e:
            print(f"ValueErrorが発生しました: {e}")
            valueErrorMessage = '※数字を入力してください'
            return render_template("mean_index.html", valueErrorMessage= valueErrorMessage)

#お問い合わせ画面
@math_app.route("/contact", methods=['GET'])
def contact():
    if request.method == 'GET':
        return render_template("contact.html")


    