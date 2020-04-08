# computational-structural-mechanics-web-app-with-flask
Web application for analysing plain truss structure displacement and internal force using matrix displacement method, built on top of Flask.

Flask is a lightweight WSGI web application framework. It began as a simple wrapper around Werkzeug and Jinja and has become one of the most popular Python web application frameworks.




## Object-oriented programming

The truss structure is digitalized using object-oriented programming method. 

Two classes are defined here: Node and Rod.

### Class 'Node'

Class Node has 5 properties: x, y, num, loadX, loadY, defining the position, number, and the current load on this node.

Besides some 'get value' and 'set value' functions, there is a function named AddLoad, and the form is ``AddLoad(self, Force:float, theta:float)``. This function is used to add a force (no torque in this web application) on this node by changing its properties, loadX and loadY.


### Class 'Rod'

Class Rod has 5 properties: num, leftNode, rightNode, youngsModulus, and crossSection. Like nodes, each rod also has a unique number that will be stored in variable 'num'. Two Node-class variables, leftNode and rightNode, can tell the rod's position. youngsModulus and crossSection are physical properties of this rod that will be used to calculate the displacement of this structure, and a default value will be set as this object was created.

Besides 'get value' and 'set value' functions, there are some other functions: CalLength, CalCos, CalSin, Calrd, CalStif, etc. 

``def Calrd(self)``: 'rd' is the abbreviation of rigid, that is

$$
rigid = \frac{EA}{l}.
$$

where E is the variable youngsModulus, A is cross section area, and l is the length of this rod.


``def CalStif(self)``:  Stif is the Stiffness matrix of this rod, which can be calculated as follows:

$$
[K] = [T][k][T]^T
$$

$$
[ T ] = \left[ \begin{array} { l } \cos \alpha \\ \sin \alpha \end{array} \right].
$$

where $k$ is rigid above.


## Multipage design

This is a multi-page web application, which uses view functions, Inherit Class 'FlaskForm', and HTML rendering to build the whole application run from page to page.

### View function

Viwe function has the same sturcture as follows:

```
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
    return render_template('SetBasic.html',form=form)
```
where 'setbasic' is the URL of the current page, and the function 'basic' is the view function (as you can see, there is no input variable in this view function). 'SetBasic.html' is the HTML file that this view function targeted, and the 'form' next to it is the parameter that this page requires to finish its rendering process.


### Inheriting class 'FlaskForm'

We inherit class 'FlaskForm' like this:
```
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
```

after a user submit this form successsfully, the n, m, nc, nLoad will be the number of nodes, rods, fixed nodes, and loads respectively, which will be transferred to next page for computation.




### HTML rendering and parameter transferring

Just like I said in the subsection View function, ``render_template('SetBasic.html',form=form)`` will render the current page, which uses `` {{...}} `` to pass parameters from program to html page. Meanwhile, `` {%...%}`` can control the direction of rendering. Just like the following code.

```
{% for message in get_flashed_messages() %} 
    {{ message }} 
{% endfor %}
```


