from flask import render_template, flash, redirect, url_for, request, jsonify
from app import app,celery
from app.forms import LoginForm
from selenium import webdriver
from app import downloadedCourses,session,lastEdit
from app.backend import net,downloader
from app.backend import regex 
from celery import Celery
from tasks import download_task
import json
import project
import pickle






@app.route('/login', methods=['GET', 'POST'])
def login():
    global session



    form = LoginForm()
    if form.validate_on_submit():
        network=net.Net()

        try:
            network.checkConnection()
        except Exception:
            flash('You are not connected to the RWTH network')
            return redirect('/login')

        loginSuccesful=network.login(form.username.data,form.password.data)        

    
        if(loginSuccesful):
            #flash('Login succesful for user {}'.format(form.username.data))
            session=network
            print(session)
            return redirect('/select')
        else:
            flash('Login failed')

    return render_template('login.html',  title='Sign In', form=form)


@app.route('/')
@app.route('/index')
@app.route('/list')
def list():


    global downloadedCourses
    project.loadFiles()
    print(downloadedCourses[0].name)
    d=map(lambda c:c.__dict__,downloadedCourses)
    return render_template('list.html',courses=d)


@app.route('/edit/<int:course_id>')
def show_edit(course_id):
    global downloadedCourses
    print(json.dumps(downloadedCourses[course_id].rootNode.recordTable))

    col_labels=["ABS","LN","PLABS","PLTOR","TOR"]



    n=downloadedCourses[course_id].rootNode

   # for i in range(0,10):
    #    x=n.childNodes[i]
     #   for cn in x.childNodes:
      #      cn.childNodes=[]
    return render_template('edit.html',name=n.name,table=n.recordTable,lab=col_labels,node=n)



@app.route('/tree')
def show_tree():

	return render_template('tree.html')





@app.route('/download/<int:node_id>')
def start_download(node_id):
    global session
    print("downloading node "+str(node_id))
    #if(session!=None):
    pickle.dump(session, open("session.p","wb"))
    task = download_task.s().delay(node_id)
    return redirect('/')
    #else:
     #   flash('Please log in')
      #  return redirect('/login')




@app.route('/select')
def show_select():
    return render_template('select.html')



@app.route('/save/<int:course_id>',methods=['POST'])
def save_edit(course_id):
    global lastEdit
    print(request.json)
    j=request.json
    lastEdit=j
    print(j[0]['name'])
    return "ok"



@app.route('/search')
def search():
    term=request.args.get('term',0,type=str)
    global session


    #commented out to test functionality offline, dont forget to reenable
    """try:            
        session.checkConnection()
    except Exception:
        print("not connected")
        flash("Please log in")
        return jsonify("error")"""


    #res=session.getSearchResult(term)


    res=open("search/"+term+".txt",'r').read()
    """pages=regex.getSearchNumberOfPages(res)
    for x in range (2,pages+1):
        res+=session.getSearchResult(term,x)"""
    x=res.split('coTableGR1')
    nodes=[]
    names=[]
    for section in x:
        nodes.append(regex.getSearchKnoten(section))
        names.append(regex.getSearchNames(section))	
    titles=regex.getSearchTitles(res)
    ind=0
    data={}
    data['list']=[]

    for j in range(len(nodes)):
        if(len(nodes[j])>0):
            item={}
            item['title']=titles[ind]
            item['courses']=[]
            for i in range(len(nodes[j])):
                course={}
                course['name']=names[j][i]
                course['id']=nodes[j][i]
                item['courses'].append(course)
            data['list'].append(item)
            ind=ind+1
	#print(json.dumps(data))

    return jsonify(data)



@app.route('/changes')
def show_changes():
    global lastEdit
    print(lastEdit)
    return render_template('changes.html',c=lastEdit)
