from api.models import Politician, Preference
from django.contrib.staticfiles.storage import staticfiles_storage
import os
from django.core.files import File  # you need this somewhere
import urllib

# Loading in politician views
module_dir = os.path.dirname(__file__)  
file_path = os.path.join(module_dir, 'minimal_scrapped_data.txt')   #full path to text.
data_file = open(file_path , 'r')       
data = data_file.read()
fullDict = eval(data)

# Loading in politician names
module_dir = os.path.dirname(__file__)  
file_path = os.path.join(module_dir, 'list_of_names.txt')   #full path to text.
data_file = open(file_path , 'r')       
data = data_file.read()
names = eval(data)

# Loading in politician bios
module_dir = os.path.dirname(__file__)  
file_path = os.path.join(module_dir, 'politician_bios.txt')   #full path to text.
data_file = open(file_path , 'r')       
data = data_file.read()
bios = eval(data)

views = ["criminal justice", "economy taxes", "abortion", "education", "minority support", "immigration", "environment", "lbgtq rights", "womens rights", "health care", "corporations", "national security", "gun control"]

def loadData():
    # for dataSet in data:
    # print(data)
    for politician in names:
        try:
            # Formatting name
            name = politician.lower()
            name = name.replace(" ", "_")
            print(name)
            
            # Getting dict of person
            scrapped_person = fullDict[name]
            # print(scrapped_person)

            # Loading image
            url = 'profile_pics/' + name + '_image.png'
            print(url)
            
            # Checking if user already in db
            try:
                Politician.objects.get(name=politician)
                print('already in \n\n')
                continue
            except Exception as e:
                pass

            # Saving bio
            bio = bios[name]
            print(bio)

            # Getting bio info
            description = bio['bio']

            location = bio['location']

            position = bio['position']

            age = bio['age']
            print("age")
            print(age)
            
            # Creating Preference
            preference = Preference(owner=politician)
            preference.save()

            # Creating Politician 
            new_obj = Politician(name=politician,  biography=description, location=location, position=position, age=age, up_for_election=False, image=url, preference=preference)


            # Looping through
            for view in views:
                key = view.lower()
                key = key.replace(" ", "_")

                # Getting list of statements on view and combining
                statements = scrapped_person[key]

                final_statement = ''
                for statement in statements:
                    final_statement += statement

                # Changing data in modal
                new_obj.__setattr__(key, final_statement)
            
            print(new_obj.abortion)
            print(new_obj.name)
            new_obj.save()
        except Exception as e:
            print(e)
