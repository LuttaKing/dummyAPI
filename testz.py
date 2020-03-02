# server.py
import subprocess
from flask import Flask,request
app = Flask(__name__)

@app.route('/',methods=["POST","GET"])
def hello_world():
        spider_name = "quotes"
        if request.method=="POST":

            username = request.form.get('username')
            password=request.form.get('password')
            try:
                if len(username) < 14 or len(password) < 8:
                    return "username or password is invalid"
            except :
                
                return "<h1>credential type error  </h1>" + username + " " + password
            
    
            returned_output=subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", f"user={username}", "-a", f"pasw={password}", "-s", "LOG_ENABLED=False"])
            try:
                
                print(type(returned_output.decode('utf-8')))
                return returned_output.decode('utf-8').strip()
            except subprocess.CalledProcessError as cpe:
            
                print(type(cpe.output))
                return cpe.output.strip()
           
        return "<h1>Nothing to see here,(post server,username,password)</h1>"
    

if __name__ == '__main__':
    app.run(debug=True)
