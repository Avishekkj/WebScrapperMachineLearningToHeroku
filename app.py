from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
# from urllib.request import urlopen as uReq
# import pymongo


app = Flask(__name__)

@app.route('/',methods=['GET']) # route to display the home
@cross_origin()
def homePage():
    return render_template("index.html")



@app.route('/review', methods= ['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            flipkartPage = requests.get(flipkart_url)  # reading the webpage
            flipkart_html = bs(flipkartPage.content, "html.parser")  # closing the connection to the web server
            bigboxes = flipkart_html.findAll("div", {"class": "bhgxx2 col-12-12"})  # seacrhing for appropriate tag to redirect to the product link
            del bigboxes[0:3]  # the first 3 members of the list do not contain relevant information, hence deleting them.
            box = bigboxes[0]  # taking the first iteration (for demo)
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']  # extracting the actual product link
            prodRes = requests.get(productLink)  # getting the product page from server
            prod_html = bs(prodRes.text, "html.parser")  # parsing the product page as HTML
            commentboxes = prod_html.find_all('div', {'class': "_3nrCtb"})  # finding the HTML section containing the customer comments
            reviews = []  # initializing an empty list for reviews
            #  iterating over the comment section to get the details of customer and their comments
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p', {'class': '_3LYOAd _3sxSiS'})[0].text

                except:
                    name = 'No Name'

                try:
                    rating = commentbox.div.div.div.div.text

                except:
                    rating = 'No Rating'

                try:
                    commentHead = commentbox.div.div.div.p.text
                except:
                    commentHead = 'No Comment Heading'
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    custComment = comtag[0].div.text
                except:
                    custComment = 'No Customer Comment'

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}  # saving that detail to a dictionary
                reviews.append(mydict)  # appending the comments to the review list
            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'

    else:
        return render_template('index.html')




if __name__ == "__main__":
    app.run(debug=True)
