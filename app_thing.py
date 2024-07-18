from flask import Flask,render_template,url_for,request,flash,redirect
import mysql.connector
import random
import smtplib
import ssl
from email.message import EmailMessage
email=""
username=""
Name=""

prod_ID=""
Product_Info_Dict1={"Prod_ID":"#1111", "Product_Name":"Black Coat"}
Product_Info_Dict2={"Prod_ID":"#2222", "Product_Name":"Grey Coat"}
Product_Info_Dict3={"Prod_ID":"#3333", "Product_Name":"Red Coat"}
Product_Info_Dict4={"Prod_ID":"#4444", "Product_Name":"Grey Coat"}
count=0
p1=1
p2=1
p3=1
p4=1
Dp={}
DictAB={}
Dict={}
Data={}
prod_IDs=[]
prod_abc=[]
countL=[]
countN=[]
app=Flask(__name__)
app.secret_key=b'a secret key'


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/my_profile')
def my_profile():
    return render_template('my_profile.html')
@app.route('/signin', methods=["GET"])
def sign_in_get():
    return render_template('sign_in.html')
@app.route('/signin', methods=["POST"])
def sign_in():
#create variables for username
#share these variables with profile page, which then reads the table and populates the name
#The profile pic must change into his image saved into the database(will cover next class)
    global username
    if (request.method=="POST"):
        username=request.form["nm"]
        password=request.form["ps"]
        mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
        cur=mydb.cursor()
        cur.execute("USE my_company_data")
        cur.execute("SELECT * from clothing_database where user_name=\""+username+"\"")
        results3=cur.fetchall()
        row_count3=cur.rowcount
        print("row count of username=", row_count3)
        mydb.close()
        if(row_count3==0):
            flash("Username doesn't exsist","error")
            return render_template('sign_in.html')
        mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
        cur=mydb.cursor()
        cur.execute("USE my_company_data")
        cur.execute("SELECT * from clothing_database where pass_word=\""+password+"\"")
        results4=cur.fetchall()
        row_count4=cur.rowcount
        print("row count of password=", row_count4)

        mydb.close()
        if(row_count4==0):
            flash("Incorrect Password","error")
            return render_template('sign_in.html')
        elif((row_count3==1) and (row_count4>=1)):
            return redirect("/myprofile",code=302)
        elif((row_count3==0) and (row_count4==0)):
            flash("Both the username and password are incorrect.")
    else:
        return render_template('sign_in.html')
@app.route('/collections')
def collections_func():
    return render_template('collectionspage.html')
@app.route('/categories')
def categories_func():
    return render_template('categoriespage.html')
@app.route('/about')
def about_func():
    return render_template('aboutpage.html')
@app.route('/offer')
def offer_func():
    return render_template('offerpage.html')
@app.route('/base')
def basefunc():
    return render_template('base.html')

@app.route('/signup', methods=["GET"])
def sign_up_get():
    return render_template('sign_up.html')
@app.route('/signup', methods=["POST"])
def sign_up_page():
    if(request.method=="POST"):
        first_name=request.form["fn"]
        last_name=request.form["ln"]
        user_name=request.form["un"]
        email_id=request.form["em"]
        pass_word=request.form["ps1"]
        pass_word2=request.form["ps2"]
        mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
        cur=mydb.cursor()
        cur.execute("USE my_company_data")
        cur.execute("SELECT * from clothing_database where user_name=\""+user_name+"\"")
        results=cur.fetchall()
        print("results:",results)
        row_count=cur.rowcount
        print("username row count:",row_count)
        mydb.close()
        if(row_count==1):
            flash("Username is taken","error")
            return render_template('sign_up.html')
        mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
        cur=mydb.cursor()
        cur.execute("USE my_company_data")
        cur.execute("SELECT * from clothing_database where email_id=\""+email_id+"\"")
        results2=cur.fetchall()
        print("result2:",results2)
        row_count2=cur.rowcount
        mydb.close()
        print("email row count:",row_count2)
        if(row_count2==1):
            flash("Email ID is taken","error")
            return render_template('sign_up.html')
        if(pass_word==pass_word2):
           pass_auth=0
        else:
            pass_auth=1
            flash("Please authenticate password","error")
            return render_template('sign_up.html')
        if((pass_auth==0) and (row_count==0) and (row_count2==0)):
            mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
            cur=mydb.cursor()
            cur.execute("USE my_company_data")
            cur.execute("""INSERT INTO clothing_database(first_name,last_name,user_name,email_id,pass_word) 
            VALUES(%s,%s,%s,%s,%s)""",(first_name,last_name,user_name,email_id,pass_word))
            mydb.commit()
            mydb.close()
            return render_template('sign_in.html')


        
    else:
        return render_template('sign_up.html')
@app.route('/forgot', methods=["GET"])
def get_forgot():
    return render_template('forgot_password.html')
@app.route('/forgot', methods=["POST"])
def forgotfunc():
    if(request.method=="POST"):
        global email
        email=request.form["em3"]
        mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
        cur=mydb.cursor()
        cur.execute("USE my_company_data")
        cur.execute("SELECT * from clothing_database where email_id=\""+email+"\"")
        results3=cur.fetchall()
        row_count3=cur.rowcount
        mydb.close()
        if(row_count3==0):
            flash("Email not found","error")
            return render_template('forgot_password.html')
        elif(row_count3==1):
            v1=random.randint(0,9)
            v2=random.randint(0,9)
            v3=random.randint(0,9)
            v4=random.randint(0,9)
            v5=random.randint(0,9)
            new=str(v1)+str(v2)+str(v3)+str(v4)+str(v5)
            mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
            cur=mydb.cursor()
            cur.execute("USE my_company_data")
            cur.execute("INSERT into passcode(code) VALUES(%s)",(new,))
            mydb.commit()
            mydb.close()
            email_sender='nehaonteru@gmail.com'
            email_password='gohl jtzd efkr yfnp'
            email_receiver=email
            subject="Passcode"
            body="Your 5-digit passcode is: "+new+". Please do not share this with anyone."
            em=EmailMessage()
            em['From']=email_sender                   
            em['To']=email_receiver
            em['Subject']=subject
            em.set_content(body)
            context=ssl.create_default_context()
            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                smtp.login(email_sender,email_password)
                smtp.sendmail(email_sender,email_receiver,em.as_string())
            #return render_template('passcode.html')
            return redirect("/passcode", code=302) 
    else:
        return render_template('forgot_password.html')

@app.route('/passcode', methods=["GET"])
def get_passcode():
    return render_template('passcode.html')
@app.route('/passcode', methods=["POST"])
def passcode_check():
    if(request.method=="POST"):
        pass_code=request.form["pc"]
        mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
        cur=mydb.cursor()
        cur.execute("USE my_company_data")
        cur.execute("SELECT * from passcode where code=\""+pass_code+"\"")
        results4=cur.fetchall()
        row_count4=cur.rowcount
        print("The passcode rowcount is ",row_count4)
        mydb.close()
        if(row_count4==0):
            flash("Incorrect Passcode","error")
            return render_template('passcode.html')
        elif(row_count4==1):
            mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
            cur=mydb.cursor()
            cur.execute("USE my_company_data")
            cur.execute("TRUNCATE table passcode")
            mydb.commit()
            mydb.close()
            return render_template('new_password.html')
            #return redirect("/addnewpassword", code=302)
            
    else:
        return render_template('passcode.html')

@app.route('/addnewpassword', methods=["GET"])
def new_password():
#    return render_template("new_password.html")
    return render_template('new_password_error.html')
@app.route('/addnewpassword', methods=["POST"])
def newpassword():
    if(request.method=="POST"):
        global email
        new_pass=request.form["pw"]
        re_pass=request.form["pw2"]
        if (new_pass==re_pass):
            mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
            cur=mydb.cursor()
            cur.execute("USE my_company_data")
            cur.execute("UPDATE clothing_database set pass_word=\""+new_pass+"\" where email_id=\""+email+"\"")
            mydb.commit()
            mydb.close()
            return redirect('/signin', code=302)
        else:
            flash("Please authenticate password","error")
            return render_template('new_password.html')
    else:
        return render_template('new_password.html')

@app.route('/myprofile', methods=["GET"])
def get_profile_func():
    global username
    #get the first and last name from the database here,, join them, store in variable, variable appears in dictionary
    mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
    cur=mydb.cursor()
    cur.execute("USE my_company_data")
    cur.execute("SELECT first_name from clothing_database where user_name=\""+username+"\"")
    firstname=cur.fetchall()
    mydb.close()

#close the cursor
        #2 -3
        #append(out[2:-3])
    mydb=mysql.connector.connect(host='localhost',user='root',password='f0r+00n')
    cur=mydb.cursor()
    cur.execute("USE my_company_data")
    cur.execute("SELECT last_name from clothing_database where user_name=\""+username+"\"")
    lastname=cur.fetchall()
    mydb.close()


    Name=str(firstname[0][0])+" "+str(lastname[0][0])
    dict={"name":Name,"username":username}
    username=""
    Name=""
    return render_template("my_profile.html",dataToRender=dict)

@app.route('/myprofile', methods=["POST"])
def profile_func():
    return render_template("my_profile.html")

@app.route('/mycart', methods=["GET"])
def my_cart_func_get():
    global Data
    return render_template("my_cart.html",ID=prod_ID)

@app.route('/mycart', methods=["POST"])
def cart_func():
    global count
    global Dp
    global p1
    global p2
    global p3
    global p4
    global DictAB
    global Dict
    global prod_IDs
    global prod_abc
    global countL
    global countN
    global Data
    Dict=Dp
    if((Dict["Prod_ID"]=="#1111")and(p1==1)):
        count=count+1
        countL.append(count)
        countN.append("count1)")
        prod_IDs.append("#1111")
        DictAB["count1"]=count
        if(count==1):
            DictAB["Proda"]="#1111"
            prod_abc.append("Proda")
        if(count==2):
            DictAB["Prodb"]="#1111"
            prod_abc.append("Prodb")
        if(count==3):
            DictAB["Prodc"]="#1111"
            prod_abc.append("Prodc")
        if(count==4):
            DictAB["Prodd"]="#1111"
            prod_abc.append("Prodd")
        print("Count1=",count)
        p1=0
    if((Dict["Prod_ID"]=="#2222")and(p2==1)):
        count=count+1
        countL.append(count)
        countN.append("count2)")
        prod_IDs.append("#2222")
        DictAB["count2"]=count
        if(count==1):
            DictAB["Proda"]="#2222"
            prod_abc.append("Proda")
        if(count==2):
            DictAB["Prodb"]="#2222"
            prod_abc.append("Prodb")
        if(count==3):
            DictAB["Prodc"]="#2222"
            prod_abc.append("Prodc")
        if(count==4):
            DictAB["Prodd"]="#2222"
            prod_abc.append("Prodd")
        print("Count2=",count)
        p2=0

    if((Dict["Prod_ID"]=='#3333')and(p3==1)):
        count=count+1
        countL.append(count)
        countN.append("count3)")
        DictAB["count3"]=count
        prod_IDs.append("#3333")
        if(count==1):
            DictAB["Proda"]="#3333"
            prod_abc.append("Proda")
        if(count==2):
            DictAB["Prodb"]="#3333"
            prod_abc.append("Prodb")
        if(count==3):
            DictAB["Prodc"]="#3333"
            prod_abc.append("Prodc")
        if(count==4):
            DictAB["Prodd"]="#3333"
            prod_abc.append("Prodd")
        print("Count3=",count)
        p3=0

    if((Dict["Prod_ID"]=='#4444')and(p4==1)):
        count=count+1
        countL.append(count)
        countN.append("count4)")
        DictAB["count4"]=count
        prod_IDs.append("#4444")
        if(count==1):
            DictAB["Proda"]="#4444"
            prod_abc.append("Proda")
        if(count==2):
            DictAB["Prodb"]="#4444"
            prod_abc.append("Prodb")
        if(count==3):
            DictAB["Prodc"]="#4444"
            prod_abc.append("Prodc")
        if(count==4):
            DictAB["Prodd"]="#4444"
            prod_abc.append("Prodd")
        print("Count3=",count)
        p4=0

    if request.method == "POST":
        return render_template('my_cart.html', Data = DictAB)
    

@app.route('/edit_profile', methods=["GET"])
def edit_func():
    return render_template("edit_profile.html")

@app.route('/edit_profile', methods=["POST"])
def edit_func_post():
    return render_template("edit_profile.html")


@app.route('/orders', methods=["GET"])
def orders_func():
    return render_template("orders.html")

@app.route('/product1', methods=["GET"])
def product1_func_get():
    return render_template("product1_page.html")

@app.route('/product1',methods=["POST"])
def product1_func():
    if request.method == "POST":
        global p1
        global count
        global prod_ID
        global Product_Info_Dict1
        global Dp
        global DictAB
        name = "Black Winter Jacket"
        Dp = Product_Info_Dict1
        price = "$59.99"
        return render_template('product1_page.html')
    
    else:
        return render_template('product1_page.html')

@app.route('/product2', methods=["GET"])
def product2_func_get():
    return render_template("product2_page.html")
 
@app.route('/product2',methods=["POST"])
def product2_func():
    if request.method == "POST":
        global p2
        global count
        global prod_ID
        global Product_Info_Dict2
        global Dp
        global DictAB
        name = "Grey Winter Jacket"
        Dp = Product_Info_Dict2
        price = "$59.99"
        return render_template('product2_page.html')
    
    else:
        return render_template('product2_page.html')

@app.route('/product3', methods=["POST"])
def product3_func():
    if (request.method == "POST"):
        global p3
        global count
        global prod_ID
        global Product_Info_Dict3
        global Dp
        name = "Red Coat"
        Dp = Product_Info_Dict3
        price="$59.99"
        return render_template('product3_page.html')
    else:
        return render_template('product3_page.html')

@app.route('/product4',methods=["POST"])
def product4_func():
    if (request.method == "POST"):
        global p4
        global count
        global prod_ID
        global Product_Info_Dict4
        global Dp
        name = "Hooded Coat"
        Dp = Product_Info_Dict4
        price="$59.99"
        return render_template('product4_page.html')
    else:
        return render_template('product4_page.html')

if __name__=="__main__":
    app.run(debug=True)

