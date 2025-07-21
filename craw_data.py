import requests
import psycopg2

url = 'https://randomuser.me/api/'

response = requests.get(url)

if response.status_code == 200:
    res = response.json()
    
    res = res['results'][0]

    fist_name = res['name']['first']
    last_name = res['name']['last']
    name = fist_name + " " + last_name
    location = str(res['location']['street']['number']) + " " + res['location']['street']['name']
    city = res['location']['city']
    country = res['location']['country']
    email = res['email']
    phone = res['phone']
    picture = res['picture']['large']

    data = {
        'first_name': fist_name,
        'last_name': last_name,
        'name': name,
        'location': location,
        'city': city,
        'country': country,
        'email': email,
        'phone': phone,
        'picture': picture
    }

    conn = psycopg2.connect(
        host= 'localhost',
        port= 5432,
        dbname= 'user',
        user= 'postgres',
        password= '123456'
    )

    cur = conn.cursor()
    cur.execute("INSERT INTO users_tb (first_name, last_name, name, location, city, country, email, phone, picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (data['first_name'], data['last_name'], data['name'], data['location'], data['city'], data['country'], data['email'], data['phone'], data['picture']))
    conn.commit()

    cur.close()
    conn.close()


else:
    print("Failed to retrieve data:", response.status_code)