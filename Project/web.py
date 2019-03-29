from bottle import route, run, template, response, request
from Datafile import Datafile
from json import dumps


@route('/')
def index():
    return template('home.html')


@route('/register')
def register():
    return template('register.html')


@route('/register', method='POST')
def do_register():
    name = request.forms.get('name')
    uid_tmp = request.forms.get('uid')
    # Save data to file: dataRFID.json
    uid = [int(n) for n in uid_tmp.split(',')]
    fileObj.updateUsername(name, uid)
    fileObj.saveContentToFile()
    return "Register success! You can check in path /users"


@route('/users')
def getListUsers():
    fileObj.setContentFromFile()
    dataRFID = fileObj.getContent()
    response.content_type = 'application/json'
    return dumps(dataRFID)


@route('/forecast')
def forecast():
    fileObjSensor.setContentFromFile()
    dataSensor = fileObjSensor.getContent()
    response.content_type = 'application/json'
    return dumps(dataSensor)


if __name__ == "__main__":
    filename = 'dataRFID.json'
    fileObj = Datafile(filename, "")

    filename_sensor = "dataSensor.json"
    fileObjSensor = Datafile(filename_sensor, "")

    run(host='0.0.0.0', port=8080, reloader=True)
