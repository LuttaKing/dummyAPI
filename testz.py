# server.py
import subprocess
from flask import Flask,request,jsonify,json
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
                
                    response = app.response_class(
                            response=json.dumps(returned_output.decode('utf-8').strip()),
                            status=200,
                            mimetype='application/json'
                                )
                    return response
                        # if len(returned_output.decode('utf-8').strip()) > 1:
                #     return jsonify(returned_output.decode('utf-8').strip())

                # else:
                #     return "<h1>Invalid credentials</h1>"
            except subprocess.CalledProcessError as cpe:

                    response = app.response_class(
                                    response=json.dumps(cpe.output.strip()),
                                    status=200,
                                    mimetype='application/json'
                                        )
                    return response

                # if len(cpe.output.strip()) > 1:
                #     return jsonify(cpe.output.strip())

                # else:
                #     return "<h1>Invalid credentials CPE2</h1>"
              
                # #  cpe.output.strip()
           
        return "<h1>Nothing to see here,(post server,username,password)</h1>"
    

if __name__ == '__main__':
    app.run(debug=True)
