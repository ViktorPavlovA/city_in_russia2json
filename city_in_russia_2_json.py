import requests
from bs4 import BeautifulSoup
import fake_useragent
import json
import csv
import os
import shutil

class City:
    def __init__(self,link):
        self.link = link
    def get_data(self):
        user_agent_new = fake_useragent.UserAgent().random
        dic_user_agent_new = {'user-agent': user_agent_new}
        responce = requests.get(self.link, dic_user_agent_new).text
        bs = BeautifulSoup(responce, 'html.parser')
        block_city = bs.find_all("td")
        list_with_city = []
        for i in range(1, 3838):  # исключение сюда
            list_with_city.append(block_city[i].text)
        black_list = ["\n","1","2","3","4","5","6","7","8","9","0"]
        for i in range(len(black_list)):
            list_with_city = [d for d in list_with_city if black_list[i] not in d]
        clean_list =[]
        for i in range(1, 2540):
            if i%2==0 or i==0:
                clean_list.append(list_with_city[i])
        clean_list=list(set(clean_list))
        return clean_list

    def save_list(self,clean_list):
        if os.path.exists("data") == True:
            shutil.rmtree("data")
        location_file_csv = "data/data_city.csv"
        location_file_json = "data/data_city.json"
        os.mkdir("data")
        new_dic = {"name_city": clean_list}
        save_json = json.dumps(new_dic)
        with open(location_file_csv, mode="w") as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\r")
            file_writer.writerow(clean_list)
        with open(location_file_json, mode="w",encoding='utf-8') as json_w:
            json.dump(new_dic,json_w,ensure_ascii=False)

    def __del__(self): pass
if __name__ == "__main__":
    link = "https://33tura.ru/goroda-rossii"
    x = City(link)
    clean_list = x.get_data()
    x.save_list(clean_list)

