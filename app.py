from flask import *
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask('shop')
app.config['MONGO_URI']='mongodb+srv://youngwonks:85465@cluster0.77pb3.mongodb.net/shop?retryWrites=true&w=majority'
Bootstrap(app)
mongo=PyMongo(app)
app.config['SECRET_KEY'] = "sOmE_rAnDom_woRd"
cart_items=[]
@app.route('/', methods=['GET','POST'])
def note_saver():
    if request.method=='GET':
        documents=mongo.db.AddressbookCollection.find()
        return render_template('page.html',contacts=documents)
    elif request.method=='POST':
        document={}
        for item in request.form:
            document[item]=request.form[item]
        mongo.db.AddressbookCollection.insert_one(document)
        return redirect('/')

@app.route('/add', methods=['GET','POST'])
def cart():
    if request.method == 'GET':
        return render_template('shoppingcart.html')
    elif request.method == 'POST':
        document={}
        for item in request.form:
            document[item]=request.form[item]
        mongo.db.products.insert_one(document)
        return redirect('/')

@app.route('/buy', methods=['GET','POST'])

def buy_product():
    if request.method=='GET':
        session['cart-items']={}
        found_products=mongo.db.products.find()
        return render_template('add_product.html',product=found_products)
    elif request.method =='POST':
        document={}
        for item in request.form:
            if int(request.form[item])!=0:
                document[item]=request.form[item]
        session['cart-items']=document
        return redirect('/checkout')



@app.route("/checkout")
def finalcart():

    total=0

    cart_items=[]

    stored_info=session['cart-items']
    for ID in stored_info:
        print(ID)
        found_item= mongo.db.products.find_one({'_id':ObjectId(ID)})

        found_item['bought']=stored_info[ID]
        found_item['item-total']=float(found_item['Price'])*int(found_item['bought'])
        cart_items.append(found_item)

        total+=found_item["item-total"]
    return render_template("checkout.html",products=cart_items,total=total)

@app.route('/delete/<identity>')
def delete_contact(identity):

    found=mongo.db.products.find_one({'_id':ObjectId(identity)})
    mongo.db.products.remove(found)
    mongo.db.products.insert_one(found)
    return redirect('/buy')

@app.route('/delete')
def delete():
    mongo.db.products.drop()
    return redirect('/')



if __name__ == '__main__':
    app.run(host="https://gentle-journey-73859.herokuapp.com/", debug=True)