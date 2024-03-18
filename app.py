from flask import Flask, render_template, request
import sqlite3 
import datetime
'''Jeremiah Daniels jbd22a
    due 2/21/2024
    The program in this file is the individual work of Jeremiah Daniels
'''
app=Flask(__name__)

@app.route("/") #home page
def home():
    return render_template('index.html')

@app.route("/addReview") #add review page
def new_review():
    return render_template("addReview.html")

@app.route("/getReviews") #add getreview page
def get_review():
    return render_template("getReviews.html")

@app.route("/getYear")
def get_Year():
    return render_template("getYear.html")

@app.route("/addrec",methods = ['Post', 'Get'])
def addrec():
    if request.method == 'POST':
        try: #error handle, test excepted error
            un = request.form['uname'] #gather data
            ttl = request.form['title']
            dirr = request.form['direc']
            yr = request.form['year']
            gen = request.form['genre']
            rv = request.form['rev']
            rt = request.form['rate']
            mvID=ttl[0:5]
            mvID2=(mvID + yr)   #create MovieID
            tm=datetime.datetime.now()
            #print("from form:",un, ttl,dirr, yr, gen, rv, rt, mvID2, tm)

            con=sqlite3.connect("movieData.db")
            curr=con.cursor()
            #print("from form:2",un, ttl,dirr, yr, gen, rv, rt, mvID2, tm)
            curr.execute("INSERT INTO Reviews VALUES (?,?,?,?,?)",(un,mvID2,tm,rt,rv))
            con.commit()
            curr.execute("insert into Movies (MovieID, Title, Director, Genre, Year) values(?,?,?,?,?)",(mvID2,ttl,dirr,gen,yr))
            con.commit()
            msg = "Record successfully added"
            curr.execute("select * from Movies, Reviews")                
            print(curr.fetchall())
        except: 
            con.rollback()
            msg="error in operation"

        finally:
            con.close() 
            return render_template("index.html",msg = msg)
            #con.close()

@app.route("/genReviews",methods = ['Post', 'Get'])
def genReviews():   #reviews for genre
    if request.method == 'POST':
        rvGen=request.form['genre']

        con=sqlite3.connect("movieData.db")
        con.row_factory=sqlite3.Row

        cur=con.cursor()
        cur.execute("select Movies.Title, Movies.Director, Reviews.Rating, Reviews.Review from Movies inner join Reviews on Movies.MovieID = Reviews.MovieID where Genre =(?)",(rvGen,))
              
        rows=cur.fetchall()
        con.close()
        return render_template("listByGenre.html",rvGen=rvGen, rows=rows)
        
@app.route("/top_Year",methods = ['Post', 'Get'])
def top_Year(): #up to 5 based off year
    if request.method == 'POST':
        yr2 = request.form['year']

        con=sqlite3.connect("movieData.db")
        con.row_factory=sqlite3.Row

        cur=con.cursor()
       
        cur.execute("select Movies.Title, Movies.Genre, Reviews.Rating from Movies inner join Reviews on Movies.MovieID = Reviews.MovieID where Year =(?) order by Rating desc Limit 5", (yr2,))
        rows=cur.fetchall()
        return render_template("bestInYear.html",yr2=yr2, rows=rows)
        
if __name__ == "__main__":
    app.run(debug = True)