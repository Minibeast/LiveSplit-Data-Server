from flask import Flask, request, abort, render_template, make_response
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)


data_storage = {} # I hate doing this.


def get_from_storage(identifier : str) -> list:
    if identifier in data_storage and len(data_storage[identifier]) != 0:
        return data_storage[identifier][-1]
    else:
        return []


@app.route("/", methods=["POST"])
def routing():
    form_data = dict(request.form)

    data = form_data['data'].split(",")

    identifier = form_data['identifier']

    if form_data['action'] == "undo":
        if get_from_storage(identifier) != []:            
            data_storage[identifier].pop()
    elif form_data['action'] == "split":
        if get_from_storage(identifier) == []:
            data_storage[identifier] = [data]
        else:
            data_storage[identifier].append(data)
    elif form_data['action'] == "skip":
        if get_from_storage(identifier) != []:
            temp_copy = get_from_storage(identifier)
            temp_copy[1] = data[0]
            temp_copy[3] = ""
            data_storage[identifier].append(temp_copy)


    user = {"identifier": identifier, "data": get_from_storage(identifier)}
    turbo.push(turbo.replace(render_template('split.html', user=user), identifier))
    
    resp = make_response()
    resp.status_code = 200
    return resp


@app.route("/get")
def get_all_splits():
    temp = []
    for x in data_storage:
        temp.append({"identifier": x, "data": get_from_storage(x)})

    return render_template('base.html', users=temp)


@app.route("/get/<user>")
def get_splits(user=None):
    if user is None:
        abort(404)

    return render_template('base.html', users=[{"identifier": user, "data": get_from_storage(user)}])
