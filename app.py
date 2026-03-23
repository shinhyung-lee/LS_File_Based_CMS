from flask import Flask, render_template, send_from_directory, abort, redirect, flash, session, url_for, request

import os
from markdown import markdown

from pathlib import Path 

app = Flask(__name__)
app.secret_key = 'very secret'
file_dir = Path(__file__).parent / "cms" / "content"

@app.route("/")
def index():
    filenames = [f.name for f in file_dir.iterdir() if f.is_file()]
    return render_template('home.html', filenames = filenames)

@app.route("/<filename>")
def serve_file(filename):
    filenames = [f.name for f in file_dir.iterdir() if f.is_file()]
    if filename not in filenames:
        flash(f"{filename} does not exist") 
        return redirect(url_for("index"))
        
    if filename.endswith('.txt'):
        return send_from_directory(file_dir, filename)
    else:
        filepath = os.path.join('cms', 'content', filename)
        with open(filepath, 'r') as f:
            content = markdown(f.read())
        print(type(content))
        return content


@app.route("/<filename>/edit")
def edit_file(filename):
    filenames = [f.name for f in file_dir.iterdir() if f.is_file()]
    if filename not in filenames:
        flash(f"{filename} does not exist") 
        return redirect(url_for("index"))
        
    filepath = os.path.join('cms', 'content', filename)
    with open(filepath, 'r') as file:
            content = file.read()
    
    return render_template('edit_file.html', filename=filename, content=content)

@app.route("/<filename>/edit", methods=["POST"])
def edit_file_content(filename):
    content = request.form['file_content']
    
    filepath = os.path.join('cms', 'content', filename)
    with open(filepath, 'w') as file:
        file.write(content)

    flash(f"{filename} has been updated")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5003)