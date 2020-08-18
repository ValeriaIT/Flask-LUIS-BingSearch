from flask import Flask, render_template
from flask import request, flash
import json
import requests
#from IPython.display import HTML
from credentials import credentialsSearchCar

from luis import luisservice
from QnA import callQnAservice
from flask_mail import Mail, Message
import os
from flask import Markup

app = Flask(__name__)
app.secret_key = '_5#y2L"F4Q8z\n\xec]/'
subscriptionKey, customConfigId = credentialsSearchCar() 


#tosend mail
app.config.update(
        DEBUG=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_SSL=True,
        MAIL_USE_TLS=False,
        MAIL_USERNAME = 'xxxxxxxxxxxxxxxx@gmail.com',
        MAIL_PASSWORD = 'xxxxxxxxxxxxxxx'
        )
mail = Mail(app)

def send_simple_mail(nameFile):      
    try:
        msg = Message(subject="Document: "+ nameFile,
        sender="xxxxxxxxxxxxxxxxxxxxx@gmail.com",
        recipients=["xxxxxxxxxxxxxxxxxx@gmail.com"])
        msg.body = "please find attached the Turners document: "+ nameFile
        working_dir=os.getcwd()
        namepath=working_dir+"/TurnersDoc/"+nameFile
        with open(namepath,'rb') as fh:
            msg.attach(namepath,"application/pdf",fh.read())
            #print('open file')
        mail.send(msg)
        print('mail with attached file ',nameFile)
        #print('mail with attached file')

    except Exception as e:
        print('error arise in send mail', str(e))


 
@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/websearch.html', methods=['POST','GET'])
#@app.route('/websearch')
def websearch():
    error = None
    if request.method == "POST":
        searchTerm=request.form.get('searchTerm')
        if searchTerm == "":
            error = 'Invalid input'
            flash('-Please write the topic-', category='searchTermErr')
        if error != None:
            return render_template('websearch.html')

        #searchTerm = "artificial"
        url = 'https://api.cognitive.microsoft.com/bingcustomsearch/v7.0/search?' + 'q=' + searchTerm + '&' + 'customconfig=' + customConfigId
        r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': subscriptionKey})
        response=r
        print('response type',type(response))
        responseDict=response.json()
        print('responseDict type',type(responseDict))
        print('responseDict ',responseDict)

        #show the result
        if 'webPages' in responseDict:
            for item in response.json()['webPages']['value']:
                if 'openGraphImage' in item:
                    flash(item['openGraphImage']['contentUrl'],"openGraphImage")             
                    print('openGraphImage',item['openGraphImage']['contentUrl'])   
                    print('')
                if 'displayUrl' in item:
                    if item['displayUrl'][0:8]!='https://':
                        item['displayUrl']='https://'+ item['displayUrl']
                    flash(item['displayUrl'],"displayUrl")
                    print('displayUrl',item['displayUrl'])
                    print('')
                if 'snippet' in item:
                    flash(item['snippet'],"snippet")            
                    print('snippet',item['snippet']) 
                flash('') 
        else:  
            error = 'Invalid input'
            flash('-no news available for this topic-', category='searchTermErr')
            return render_template('websearch.html')
        flash('the API return')
        flash(type(r.text))
        return render_template('websearch.html')
    else:
        return render_template('websearch.html')

@app.route('/internalsearch.html', methods=['POST','GET'])
def internalsearch():
    error = None
    if request.method == "POST":        
        searchInfo=request.form.get('searchInfo')
        if searchInfo == "":
            error = 'Invalid input'
            flash('-Please write the Turners information you are looking for-', category='searchInfoErr')
        if error != None:
            return render_template('internalsearch.html')      
        searchInfoJSON_reply=luisservice(searchInfo,'QnA')  
        intent=searchInfoJSON_reply['prediction']['topIntent']
        internalSearch=callQnAservice(intent)
        print('reply',internalSearch)
        print('type reply', type(internalSearch))
        internalSearchJSON=json.dumps(json.loads(internalSearch))
        print('type internalSearchJSON...',type(internalSearchJSON))
        internalSearchDict=json.loads(internalSearchJSON)
        print('type internalSearchDict...',type(internalSearchDict))
        print('internalSearchDict...',internalSearchDict)        
        print('reply...',internalSearchDict['answers'][0]['answer'])
        message = Markup(internalSearchDict['answers'][0]['answer'])
        flash(message,category='searchTurnersInfo')
        return render_template('internalsearch.html')

    else:
        return render_template('internalsearch.html')



@app.route('/internaldocument.html', methods=['POST','GET'])
def internaldocument():
    error = None
    if request.method == "POST":
        
        internalDoc=request.form.get('internalDoc')
        if internalDoc == "":
            error = 'Invalid input'
            flash('-Please write the name of the Turners document you looking for-', category='internalDocErr') 
        if error != None:
            return render_template('internaldocument.html')

        internalDocumentJSON_reply=luisservice(internalDoc,'document')
        reply=internalDocumentJSON_reply['prediction']['topIntent']
        if reply=="None":
            error = 'Invalid input'
            flash('-Please, try to insert another keyword-', category='internalDocErr') 
            if error != None:
                return render_template('internaldocument.html')  
        else:          
            nameFile=internalDocumentJSON_reply['prediction']['topIntent']+".pdf"
            flash(nameFile,'internalDoc')
            print('.............IN THE APPP...........')
            print('internalDocumentJSON_reply',internalDocumentJSON_reply)
            print('type of internalDocumentJSON_reply',type(internalDocumentJSON_reply)   )    
            if (request.form.get('sendMail')=='Email'):
                send_simple_mail(nameFile) 
            return render_template('internaldocument.html')    
    else:
        return render_template('internaldocument.html')

if __name__ == '__main__':
 app.run(debug=True)