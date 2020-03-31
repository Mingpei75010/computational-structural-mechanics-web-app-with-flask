# flask and webapp modules
from flask import Flask,request,render_template,url_for,redirect,session,flash
import os
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField, FloatField
from wtforms.validators import EqualTo,DataRequired
# result visualisation
import matplotlib
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from pylab import *
# other objectives in this project
import numpy as np
from finalcal import finalcal
from Digitalize import SetRods, SetForces, SetNodes, SetBasicData
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')


class InputBasicData(FlaskForm):
    n = IntegerField(label='Number of nodes',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input number of nodes.'})
    m = IntegerField(label='Number of rods',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input number of rods'})
    nc = IntegerField(label='Number of immovable nodes',validators=[DataRequired()],
                      render_kw={'placeholder':'Please input number of immovable nodes'})
    nLoad = IntegerField(label='Number of loads',validators=[DataRequired()],
                      render_kw={'placeholder':'Please input number of loads'})
    submit = SubmitField(label='Submit')

class InputNodes(FlaskForm):
    x = FloatField(label='x position',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the horizontal position.'})
    y = FloatField(label='y position',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the vertical position.'})
    submit = SubmitField(label='Submit')

class ArrayofXandY(FlaskForm):
    x = StringField(label='x position of each nodes',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the horizontal position of each nodes.'})
    y = StringField(label='y position of each nodes',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the vertical position of each nodes.'})
    submit = SubmitField(label='Submit x and y')

class ArrayofLandR(FlaskForm):
    ihl = StringField(label='The left node',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the number of the left node.'})
    ihr = StringField(label='The right node',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the number of the right node.'})
    submit = SubmitField(label='Submit ihl and ihr')

class ArrayofLoad(FlaskForm):
    loadnum = StringField(label='Node number of the force',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input node number of the force.'})
    force = StringField(label='The load sizes',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the force.'})
    theta = StringField(label='The load directions',validators=[DataRequired()],
                     render_kw={'placeholder':'Please input the angle.'})
    submit = SubmitField(label='Submit force info')



@app.route("/",methods=['POST','GET'])
def login():
    return render_template('home.html')

# Set basic information, nodes, rods, and loads, to the program.
@app.route("/setbasic",methods=['POST','GET'])
def basic():
    form = InputBasicData()
    if request.method == "POST":
        # get information from the table
        if form.validate_on_submit():
            n = form.n.data
            m = form.m.data
            nc = form.nc.data
            nLoad = form.nLoad.data
            nn = 2 * (n - nc)
            return redirect(url_for('setnode',n=n, m=m, nc=nc, nLoad=nLoad))
        else:
            message = form.errors
            # every typo in 'form' will be catch by 'errors'
            flash(message)
    return render_template('SetBasic.html',form=form)

# Set nodes information
# we use url to transfer parameters between web pages
@app.route("/setnode?n=<int:n>m=<int:m>nc=<int:nc>nLoad=<int:nLoad>",methods=['POST','GET'])
def setnode(n,m,nc,nLoad):
    form = ArrayofXandY()
    basicdata = [n, m, nc, nLoad]
    if request.method == "POST":
        if form.validate_on_submit():
            x = form.x.data
            y = form.y.data
            # transfer parameters, both old and new, to the next page.
            return redirect(url_for('setrod',n=n, m=m, nc=nc, nLoad=nLoad, x=x, y=y))
        else:
            message = form.errors
            flash(message)
    return render_template('SetNodesPosition.html', basicdata=basicdata, form=form)


# Set rods information (the left and right nodes of each rod).
@app.route("/setrod?n=<int:n>m=<int:m>nc=<int:nc>nLoad=<int:nLoad>x=<x>y=<y>",methods=['POST','GET'])
def setrod(n,m,nc,nLoad,x,y):
    form = ArrayofLandR()
    basicdata = [n, m, nc, nLoad]
    # Plot nodes location on canvas, which has been set before.
    plt.clf()
    x1 = x.split()
    y1 = y.split()
    for i in range(n):
        x1[i] = float(x1[i])
        y1[i] = float(y1[i])
    plt.rcParams['figure.dpi'] = 100  # Resolution
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['figure.figsize'] = (8.0, 8.0)  # set figure_size
    for i in range(n):
        if(i<nc):
            plt.plot(x1[i], y1[i], "k^")
            plt.annotate(i, (x1[i], y1[i]), weight='bold',color='red')
        else:
            plt.plot(x1[i], y1[i], "ro")
            plt.annotate(i, (x1[i], y1[i]), weight='bold', color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    # save figure as a binary file
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    # convert picture format into html
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    if request.method == "POST":
        if form.validate_on_submit():
            ihl = form.ihl.data
            ihr = form.ihr.data
            str = 'not yet'
            # return str
            return redirect(url_for('setload',n=n, m=m, nc=nc, nLoad=nLoad, x=x, y=y, ihl=ihl, ihr=ihr))
        else:
            message = form.errors
            flash(message)
    return render_template('SetRod.html', basicdata=basicdata, form=form, x=x, y=y, img=imd)

# Set loads information (both direction and magnitude data required)
@app.route("/setrod?n=<int:n>m=<int:m>nc=<int:nc>nLoad=<int:nLoad>x=<x>y=<y>ihl=<ihl>ihr=<ihr>",methods=['POST','GET'])
def setload(n,m,nc,nLoad,x,y,ihl,ihr):
    form = ArrayofLoad()
    basicdata = [n, m, nc, nLoad]
    plt.clf()
    x1 = x.split()
    y1 = y.split()
    ihl1 = ihl.split()
    ihr1 = ihr.split()
    for i in range(m):
        ihl1[i] = int(ihl1[i])
        ihr1[i] = int(ihr1[i])
    for i in range(n):
        x1[i] = float(x1[i])
        y1[i] = float(y1[i])
    plt.rcParams['figure.dpi'] = 100  # Resolution
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['figure.figsize'] = (8.0, 8.0)  # set figure_size
    for i in range(n):
        if(i<nc):
            plt.plot(x1[i], y1[i], "k^")
            plt.annotate(i, (x1[i], y1[i]), weight='bold', color='red')
        else:
            plt.plot(x1[i], y1[i], "ro")
            plt.annotate(i, (x1[i], y1[i]), weight='bold', color='red')
    for i in range(0, m):
        plt.plot([x1[ihl1[i]], x1[ihr1[i]]], [y1[ihl1[i]], y1[ihr1[i]]],"k")
        lala=(x1[ihl1[i]]+x1[ihr1[i]])/2
        kaka=(y1[ihl1[i]]+y1[ihr1[i]])/2
        plt.annotate((i+1), (lala, kaka), weight='roman', color='blue')
    plt.xlabel('x')
    plt.ylabel('y')
    # save figure as a binary file
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    # convert picture format into html
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    if request.method == "POST":
        if form.validate_on_submit():
            loadnum = form.loadnum.data
            force = form.force.data
            theta = form.theta.data
            str = 'not yet'
            # return str
            return redirect(url_for('everythingdone',n=n, m=m, nc=nc, nLoad=nLoad,
                                    x=x, y=y, ihl=ihl, ihr=ihr, loadnum=loadnum,
                                    force=force, theta=theta))
        else:
            message = form.errors
            flash(message)
    return render_template('SetLoads.html', basicdata=basicdata, form=form,
                           x=x, y=y, ihl=ihl, ihr=ihr, imh=imd)

# display computation result
@app.route("/result?n=<int:n>m=<int:m>nc=<int:nc>nLoad=<int:nLoad>x=<x>y=<y>ihl=<ihl>ihr=<ihr>loadnum=<loadnum>force=<force>theta=<theta>",
           methods=['POST','GET'])
def everythingdone(n,m,nc,nLoad,x,y,ihl,ihr,loadnum,force,theta):
    basicdata = [n, m, nc, nLoad]

    # calling function 'finalcal'
    U, S=finalcal(basicdata,x,y,ihl,ihr,loadnum,force,theta)

    # display results
    plt.clf()
    x1 = x.split()
    y1 = y.split()
    ihl1 = ihl.split()
    ihr1 = ihr.split()
    theta1 = theta.split()
    force1 = force.split()
    loadnum1 = loadnum.split()
    for i in range(m):
        ihl1[i] = int(ihl1[i])
        ihr1[i] = int(ihr1[i])
    for i in range(n):
        x1[i] = float(x1[i])
        y1[i] = float(y1[i])
    for i in range(nLoad):
        theta1[i] = float(theta1[i])
        force1[i] = float(force1[i])
        loadnum1[i] = int(loadnum1[i])
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 100
    plt.rcParams['figure.figsize'] = (8.0, 8.0)
    for i in range(n):
        if(i<nc):
            plt.plot(x1[i], y1[i], "k^")
            plt.annotate(i, (x1[i], y1[i]), weight='bold', color='red')
        else:
            plt.plot(x1[i], y1[i], "ro")
            plt.annotate(i, (x1[i], y1[i]), weight='bold', color='red')
    for i in range(0, m):
        lala = (x1[ihl1[i]]+x1[ihr1[i]])/2
        kaka = (y1[ihl1[i]]+y1[ihr1[i]])/2
        plt.annotate((i + 1), (lala, kaka), weight='roman', color='blue')
    for i in range(0, nLoad):
        u = np.cos(theta1[i])
        v = np.sin(theta1[i])
        pipi=x1[loadnum1[i]]+u*0.1
        qiqi=y1[loadnum1[i]]+v*0.15
        plt.quiver(x1[loadnum1[i]], y1[loadnum1[i]], u, v,color='r', width=0.005, scale=10)
        plt.text(pipi, qiqi, force1[i], size=10, alpha=0.9)
    S1=S
    S = np.array(abs(S))
    HAHA = np.argsort(S)
    for i in range(0,m):
        j=1.2*i+1
        plt.plot([x1[ihl1[HAHA[i]]], x1[ihr1[HAHA[i]]]], [y1[ihl1[HAHA[i]]], y1[ihr1[HAHA[i]]]],linewidth=j, color = 'k')

    plt.xlabel('x')
    plt.ylabel('y')
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    imb = base64.b64encode(plot_data)
    ims = imb.decode()
    imd = "data:image/png;base64," + ims
    
    return render_template('result.html', basicdata=basicdata,
                           x=x, y=y, ihl=ihl, ihr=ihr, loadnum=loadnum, force=force, theta=theta, U=U, S=S1, imo=imd)


if __name__ == '__main__':
    app.run(debug=True)