import requests
from flask import Flask, render_template, request, url_for
import function_data as function


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index_final.html", tittle="Searching For Books")


@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        identifier = request.form.get("identifier")
        search_url = function.get_search_url(identifier=identifier, user_input=user_input)
        search_data = function.safe_get_search(search_url=search_url)
        cover_i = function.get_cover_i(result=search_data)
        book_cover_url = function.get_book_cover(cover_i=cover_i)
        book_info = function.get_book_info(result=search_data, cover_i=cover_i, book_cover=book_cover_url)
        return render_template("results_final.html", user_input=user_input, search_url=search_url,
                               search_data=search_data, book_cover_url=book_cover_url, book_info=book_info)
    else:
        return "Error: was expecting a POST request", 400



@app.route("/author")
def author():
    return render_template("author_final.html", title= "Searching author releated")


@app.route("/authors", methods=["GET", "POST"])
def authors():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        identifier = request.form.get("identifier")
        search_url = function.get_search_url(identifier=identifier, user_input=user_input)
        search_data = function.safe_get_search(search_url=search_url)
        olid_id = function.get_olid_id(result=search_data)
        redirect_url = function.redirect_author_work(olid_id=olid_id)
        author_url = function.get_author_url(olid_id=olid_id)
        author_bio = function.safe_get_author(author_url=author_url)
        author_cover_url = function.get_author_cover(value=olid_id)
        return render_template("authors_final.html", identifier=identifier, user_input=user_input,
                               search_url=search_url, search_data=search_data, author_cover_url=author_cover_url,
                               author_bio=author_bio, redirect_url=redirect_url)
    else:
        return "Error: was expecting a POST request", 400



if __name__ == "__main__":
    app.run(debug=True)
