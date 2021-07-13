from flask import Blueprint, render_template, Response, redirect, url_for, request,jsonify
from flask import current_app as app
import datetime
from threading import Thread

api = Blueprint('api',__name__)

def getDateTime():
    import datetime
    dateTime = '{0:%Y-%m-%d}'.format(datetime.datetime.now())
    onlyTime = '{0:%H-%M-%S}'.format(datetime.datetime.now())
    return "{}_{}".format(dateTime, onlyTime)


@api.route('/api/server_stats')
def ServerStats():
    status = app.sc.status
    prog   = app.sc.dd_prog_msg

    data = {
        "status": status,
        "prog"  : prog
    }
    return jsonify(data)


@api.route('/api/update_conf', methods=["GET", "POST"])
def updateConf():
    try:
        data = request.get_json()
        app.conf.updateConfig(data['key'], data['value'])
        return jsonify({"state":"success"})
    except Exception as e:
        print(e)
        return jsonify({"state":"error"})

@api.route('/api/make_img', methods=['POST'])
def makeImage():
    try:
        data = request.get_json()
        img_name = data["img_name"]
        if(img_name == "empty"):
            img_name = getDateTime() + ".img"
        else:
            img_name = img_name.replace(" ", "_")
            img_name = img_name + ".img"

        conf = app.conf.loadConfigFromFile()
        # print(img_name)
        Thread(target=app.sc.ImageProcessor, args=(conf['input'],img_name, conf['zip'], conf['reset'])).start()
        return jsonify({"state":"success"})
    except Exception as e:
        print(e)
        return jsonify({"state":"error"})