
from sys import exit
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

mongo_user = config.get('DB', 'user')
mongodb_pass = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
domain = config.get('DB', 'domain')
# connect to cluster on AtlasDB with connection string
client = MongoClient(f"""mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/?retryWrites=true&w=majority&appName=Cluster0""",
                     server_api=ServerApi('1')
                     )

db = client.web16


def help():
    print("Command help for Help")
    print("Command 'showall' for showing list of all cats")
    print("Command 'name <CatName>' for search cat by his name")
    print("Command 'updateage <CatName>' for upadate cat's age by his name")
    print("Command 'features <CatName>' for upadate cat's features by his name")
    print("Command 'delete <CatName>' for delete cat by his name")
    print("Command 'deleteall' for delete all cats in collection")


# Вивід списка всіх наявних котів
def find_cats():
    result = db.cats.find({})
    for el in result:
        for e, l in el.items():
            print(e, ': ', l)
        print('**'*20)
    return result


# Пошук кота по імені
def find_cat_by_name(name):
    result = db.cats.find_one({"name": name})
    for e, l in result.items():
        print(e, ': ', l)
    print('**'*20)
    return result


# Оновлення віку шуканого кота
def update_cat_age(name):
    age = input(f'Enter new age of {name} >>> ')
    db.cats.update_one({"name": name}, {"$set": {"age": int(age)}})
    result = db.cats.find_one({"name": name})
    return result


# Оновлення властивостей шуканого кота
def update_cat_features(name):
    new_features = input(f'Enter new features of {
                         name}. Use comma for separate features\n>>> ')
    new_features = new_features.split(',')
    features = db.cats.find_one({"name": name})['features']
    features.extend(new_features)
    db.cats.update_one({"name": name}, {"$set": {"features": features}})
    result = db.cats.find_one({"name": name})
    return result


# Видалення шуканого кота
def delete_cat_by_name(name):
    db.cats.delete_one({"name": "barsik"})
    result = db.cats.find_one({"name": "barsik"})
    if not result:
        print(f"Кота на ім'я {name} видалено")
    return result


# Видалення усіх
def delete_all_cats():
    db.cats.delete_many({})
    result = db.cats.find({})
    return result


if __name__ == '__main__':

    COMMANDS = {'name': find_cat_by_name,
                'showall': find_cats,
                'help': help,
                'updateage': update_cat_age,
                'features': update_cat_features,
                'delete': delete_cat_by_name,
                'deleteall': delete_all_cats, }

    while True:
        tag = input(
            "Enter Your command, 'exit' for Quit\n>>> ")

        tag = tag.split()
        if tag[0].lower() == 'exit':
            exit()
        try:
            if len(tag) == 1:
                COMMANDS[tag[0].strip().lower()]()
            elif len(tag) == 2:
                try:
                    COMMANDS[tag[0].strip().lower()](tag[1])
                except AttributeError:
                    print(f"Cat {tag[1]} not exist")
            else:
                raise ValueError
        except:
            print('Unknown command')
