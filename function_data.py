import requests
import urllib
import urllib.parse
import urllib.request
import urllib.response
import urllib.error
import json
##########################################################################
# define a function - url access
# Search general: "https://openlibrary.org/search.json?" [? + title=, author=, q=]
# author specific: "https://openlibrary.org/authors/<olid_id>.json
##########################################################################


# using search API - for general
def get_search_url(identifier, user_input):
    # general format url for search
    base_url = 'https://openlibrary.org/search.json'
    query_search = {identifier: user_input}
    # parsing the url parameter
    search_para = urllib.parse.urlencode(query_search)
    search_url = base_url + "?" + search_para
    # an url will be return
    return search_url
##########################################################################


# getting the output needed from the library
def get_search_data(search_info):
    result = {"title": [], "name": [], "publish_year": [], "pages_num": [], "author_key": [], "cover_i": []}
    for i in search_info:
        if i == "docs":
            docs = search_info[i]
            length = len(docs)
            for j in range(0, length - 1):
                diction = docs[j]
                title = diction.get("title")
                name = diction.get("author_name")
                publish_year = diction.get("first_publish_year")
                pages_num = diction.get("number_of_pages_median")
                author_key = diction.get("author_key")
                cover_i = diction.get("cover_i")
                result["title"].append(title)
                result["name"].append(name)
                result["publish_year"].append(publish_year)
                result["pages_num"].append(pages_num)
                result["author_key"].append(author_key)
                result["cover_i"].append(cover_i)

    # return a dictionary: title, name, publish year, pages, author_key, cover_i
    return result
##########################################################################


# function of getting the search with try/except method.
def safe_get_search(search_url):
    try:
        with urllib.request.urlopen(search_url) as responses:
            search_detail = responses.read().decode()
            search_info = json.loads(search_detail)
        return get_search_data(search_info)
    except urllib.error.HTTPError as e:
        print("Error from server. Error code: ", e.code)
        return None
    except urllib.error.URLError as er:
        print("Failed to reach server. Reason: ", er.reason)
        return None
##########################################################################


# define a function get book cover_i
def get_cover_i(result):
    # result is from get_search_data(search_info)
    # the method call from safe_get_search(search_url)
    # search_url from get_search_url
    # cover_i = []
    id_i = set()
    key = result["cover_i"]
    for i in key:
        if i is not None:
            id_i.add(i)
    cover_i = list(id_i)
    return cover_i
##########################################################################


# define a function get author_olid_id
def get_olid_id(result):
    # result is from get_search_data(search_info)
    # the method call from safe_get_search(search_url)
    # search_url from get_search_url
    # olid_id = []
    olid_set = set()
    key = result["author_key"]
    for i in key:
        if i is not None:
            for j in i:
                olid_set.add(j)
    olid_id = list(olid_set)
    # return a list of author_key (unique)
    return olid_id
##########################################################################


# define a function get author url
# need olid_id
def get_author_url(olid_id):
    author_url = []
    # general format url for author
    base_url = "https://openlibrary.org/authors/ .json"
    if len(olid_id) > 1:
        for i in olid_id:
            author_key = str(i)
            # print(author_key)
            author_url.append(base_url.replace(" ", author_key))
    else:
        author_id = str(olid_id)
        author_key = author_id[2:-2]
        author_url.append(base_url.replace(" ", author_key))
    # a list of url will be return
    return author_url
##########################################################################


def redirect_author_work(olid_id):
    redirect_url = []
    base_url = "https://openlibrary.org/authors/ "
    if len(olid_id) > 1:
        for i in olid_id:
            author_key = str(i)
            redirect_url.append(base_url.replace(" ", author_key))
    else:
        author_id = str(olid_id)
        author_key = author_id[2:-2]
        redirect_url.append(base_url.replace(" ", author_key))

    return redirect_url

##########################################################################
def get_author_bio(author_info):
    data = {'author_id': '', 'bio': '', 'url': ''}
    for i in author_info:
        value = author_info[i]
        if i == "photos":
            data['author_id'] = value[0]
        if i == "bio":
            data['bio'] = value
            if type(value) == dict:
                bio = value["value"]
                data['bio'] = bio
            else:
                data['bio'] = value[0]
        if i == "links":
            for j in value[0]:
                key = value[0]
                if j == "url":
                    data['url'] = key[j]
    # return a dictionary: id, bio, url
    return data
##########################################################################


# function of getting the author with try/except method.
def safe_get_author(author_url):
    try:
        length = len(author_url)
        list_bio = []
        if length > 1:
            # list_bio = []
            count = 0
            while count < length:
                with urllib.request.urlopen(author_url[count]) as responses:
                    author_detail = responses.read().decode()
                    author_info = json.loads(author_detail)
                    bio = get_author_bio(author_info)
                    print(bio)
                    list_bio.append(bio)
                count = count + 1
            # return list_bio
        else:
            author_url = str(author_url)
            author_url = author_url[2:-2]
            with urllib.request.urlopen(author_url) as responses:
                author_detail = responses.read().decode()
                author_info = json.loads(author_detail)
                bio = get_author_bio(author_info)
                list_bio.append(bio)
        # return a list of dictionary: id, bio, url
        return list_bio
    except urllib.error.HTTPError as e:
        print("Error from server. Error code: ", e.code)
        return None
    except urllib.error.URLError as er:
        print("Failed to reach server. Reason: ", er.reason)
        return None
##########################################################################


# base url for cover using Open Library API
# cover_url = "https://covers.openlibrary.org"
#
# define a function - get_book_cover
def get_book_cover(cover_i):
    # base url for cover using Open Library API
    cover_url = "https://covers.openlibrary.org"
    key = "id"
    size = "M"
    book_cover_list = []
    if len(cover_i) > 1:
        for i in cover_i:
            cover_i_size = str(i) + "-" + size
            book_query = " b " + key + " " + cover_i_size
            book_query = book_query.replace(" ", "/")
            url_format = cover_url + book_query + ".jpg?default=false"
            book_cover_list.append(url_format)
    else:
        cover_i_size = str(cover_i) + "-" + size
        book_query = " b " + key + " " + cover_i_size
        book_query = book_query.replace(" ", "/")
        url_format = cover_url + book_query + ".jpg?default=false"
        book_cover_list.append(url_format)
    # extract blank pictures as none
    book_list = []
    for i in book_cover_list:
        url = requests.get(i)
        if url.status_code == 404:
            book_list.append(None)
        else:
            book_list.append(i)
    # list of valid link of NoneType
    return book_list
##########################################################################


# define a function - get_author_cover
# author = {'type' : 'a', 'key': 'olid'/id, 'value': author_key/photo, 'size': size}
def get_author_cover(value):
    # base url for cover using Open Library API
    cover_url = "https://covers.openlibrary.org"
    key = "olid"
    size = "M"
    cover_url_list = []
    if len(value) > 1:
        for i in value:
            val_size = str(i) + "-" + size
            query = " a " + key + " " + val_size
            query = query.replace(" ", "/")
            url_format = cover_url + query + ".jpg?default=false"
            cover_url_list.append(url_format)
    else:
        value = str(value)
        value = value[2:-2]
        val_size = str(value) + "-" + size
        query = " a " + key + " " + val_size
        query = query.replace(" ", "/")
        url_format = cover_url + query + ".jpg?default=false"
        cover_url_list.append(url_format)
    # extract blank pictures as none
    url_list = []
    for i in cover_url_list:
        url = requests.get(i)
        if url.status_code == 404:
            url_list.append(None)
        else:
            url_list.append(i)
    # list of valid link or NoneType
    return url_list
##########################################################################


def get_book_info(result, cover_i, book_cover):
    title = result["title"]
    name = result["name"]
    pub_year = result["publish_year"]
    pages = result["pages_num"]
    c_id = result["cover_i"]
    cover_url = book_cover
    count = 0
    all_list = []
    for i in cover_i:
        index = 0
        for j in c_id:
            if i == j:
                each_list = {"title": title[index], "name": name[index], "pub_year": pub_year[index],
                "pages": pages[index], "cover_url": cover_url[count]}
                all_list.append(each_list)
            index = index + 1
        count = count + 1
    return all_list



##########################################################################

url = get_search_url("author", "Shannon Messenger")
result = safe_get_search(url)
olid = get_olid_id(result)
# author_url = get_author_url(olid)
# print(author_url)
# author_bio = safe_get_author(author_url)
# print(author_bio)
# cover_i = get_cover_i(result)
# book_cover = get_book_cover(cover_i)
# print(book_cover)
# author_cover = get_author_cover(olid)
# print(author_cover)
# # print(len(result["title"]))
# print(len(result["cover_i"]))
# print(result["cover_i"])
# print(result)
# print(get_book_info(result, cover_i, book_cover))

