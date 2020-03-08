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
                
                return "<h1>credential type error  </h1>"
            
    
            returned_output=subprocess.check_output(['scrapy', 'crawl', spider_name, "-a", f"user={username}", "-a", f"pasw={password}", "-s", "LOG_ENABLED=False"])
            try:
                
              
                if len(returned_output.decode('utf-8').strip()) > 1:
                    return returned_output.decode('utf-8').strip()

                else:
                    return "<h1>Invalid credentials</h1>"
            except subprocess.CalledProcessError as cpe:

                if len(cpe.output.strip()) > 1:
                    return cpe.output.strip()

                else:
                    return "<h1>Invalid credentials CPE2</h1>"
              
                #  cpe.output.strip()
           
        return "<h1>Nothing to see here,(post server,username,password)</h1>"
    

if __name__ == '__main__':
    app.run(debug=True)
