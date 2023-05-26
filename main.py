# imports
import requests
import sqlite3
import json
from win10toast import ToastNotifier
import webbrowser
#################

url = "https://dog.ceo/api/"

# 1. requests მოდულის ატრიბუტების შემოწმება
def requests_attr_test():
    rest = ('breeds/list/all')
    response = requests.get(url + rest)
    print(response.url)
    print(response.status_code)
    print(response.headers)
    print(response.text)
    
# requests_attr_test()



# 2. json ფაილად შენახვა მონაცემების თავისი ინდენტაციით
def json_write():
    rest = ('breeds/list/all')
    response = requests.get(url + rest)
    result = response.json()
        
    with open("dog_breeds.json", "w") as write_file:
        json.dump(result, write_file, indent=4)

# json_write() 




# 3. გარჩევინებს ძაღლის ჯიშს
def list_of_breeds():
    rest = ('breeds/list/all')
    response = requests.get(url + rest)
    result = response.json()
    breeds = result['message']

    n = []
    for index, Value in enumerate(breeds, 1):
        print(f"{index}. {Value}")
    for each in breeds:
        n.append(each)


    selected_breed = int(input('აირჩიე ჯიში ციფრით: '))
    if selected_breed > len(breeds):
        print('ასეთი ჯიში არ არის!')
    else:        
        return (n[selected_breed - 1])

# list_of_breeds()

# 4. არჩეული ჯიშის რენდომ სურათს ხსნის ბრაუზერში და ასევე აბრუნებს სურათის ლინკს
def get_url(breed):
    rest = (f'breed/{breed}/images/random')
    response = requests.get(url + rest)
    result = response.json()
    json_img_url = result["message"]
    webbrowser.open(f"{json_img_url}")
    return json_img_url
    
    
# get_url(list_of_breeds())

#  4. არჩეული ჯიშის, რენდომ სურათის ბინარულ კოდს იღებს და აბრუნებს
def get_bimg(url):
    resp_img = requests.get(url)
    result_img = resp_img.content
    return result_img

# get_bimg(get_url(list_of_breeds()))


# 5. ქმნის ბაზას
conn = sqlite3.connect('main_db.sqlite')
cur = conn.cursor()

def create_db():
    cur.execute('''CREATE TABLE IF NOT EXISTS breeds
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                breed VARCHAR(50),
                bimg BLOB)''')
    
    conn.commit()
    conn.close()
    
# create_db()

# 6. ინფორმაცია შეაქვს ბაზაში და გამოაქვს შეტყობინება
def insert_info_in_db():
    b_breed = list_of_breeds()
    b_bimg = get_bimg(get_url(b_breed))
    b_items = (b_breed, b_bimg)
    cur.execute("INSERT INTO breeds (breed, bimg) VALUES (?,?)", b_items)

    conn.commit()
    conn.close()
    
    toaster = ToastNotifier()
    toaster.show_toast("Woof Woof...",
                    "ბაზაში ძაღლის ახალი ფოტო დაემატა!",
                    duration=10)


insert_info_in_db()