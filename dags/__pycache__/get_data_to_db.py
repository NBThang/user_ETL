from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 10, 1)
}

def fetch_user_data(**context):
    import requests

    data = []
    for _ in range(30):
        url = 'https://randomuser.me/api/'
        response = requests.get(url)

        if response.status_code == 200:
            res = response.json()
            res = res['results'][0]

            # Lấy các trường dữ liệu
            first_name = res['name']['first']
            last_name = res['name']['last']
            name = f"{first_name} {last_name}"
            location = f"{res['location']['street']['number']} {res['location']['street']['name']}"
            city = res['location']['city']
            country = res['location']['country']
            email = res['email']
            phone = res['phone']
            picture = res['picture']['large']

            user_data = {
                'first_name': first_name,
                'last_name': last_name,
                'name': name,
                'location': location,
                'city': city,
                'country': country,
                'email': email,
                'phone': phone,
                'picture': picture
            }

            data.append(user_data)
        else:
            raise Exception(f"API request failed: {response.status_code}")

    # Push danh sách 10 người dùng lên XCom
    context['ti'].xcom_push(key='user_data', value=data)


def insert_to_db(**context):
    import psycopg2
    # Lấy dữ liệu từ XCom
    data = context['ti'].xcom_pull(task_ids='fetch_user', key='user_data')

    # Kết nối PostgreSQL
    conn = psycopg2.connect(
        host= 'host.docker.internal',
        port= 5432,
        dbname= 'user',
        user= 'postgres',
        password= '123456'
    )
    cur = conn.cursor()

    for i in range(30):
        user = data[i]
        
        cur.execute("INSERT INTO users (first_name, last_name, name, location, city, country, email, phone, picture) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (user['first_name'], user['last_name'], user['name'], user['location'], user['city'], user['country'], user['email'], user['phone'], user['picture']))
        conn.commit()

    cur.close()
    conn.close()

with DAG(
    dag_id='put_data_to_db',
    default_args=default_args,
    description='A DAG with two dependent Python tasks',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['example'],
) as dag:

    task_1 = PythonOperator(
        task_id='fetch_user',
        python_callable=fetch_user_data,
    )

    task_2 = PythonOperator(
        task_id='insert_to_db',
        python_callable=insert_to_db,
    )

    task_1 >> task_2