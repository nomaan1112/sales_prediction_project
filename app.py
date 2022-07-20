from tkinter import E
from sales.logger import logging
from sales.exception import SalesException
from flask import Flask
import sys,os

app= Flask(__name__)

@app.route("/", methods =['GET','POST'])

def index():
    try:
        pass
    except Exception as e:
        raise SalesException (e,sys) from e 


if __name__ == "__main__":
    app.run(debug=True)    