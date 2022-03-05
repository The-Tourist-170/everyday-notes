from website import create_app

app = create_app()

if __name__ == '__main__': # __name == '__main__' says if this file ran then only the cmd under if will run or the website will run. Importing this file will not also run the website or statement under if.
    app.run(debug=True) #Will run our flask app and start the web server | debig=True means if any changes made to code it will auto rerun the web server
     