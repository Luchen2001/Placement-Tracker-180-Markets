# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests
import csv
import datetime

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    placement_list = []
    with open('placement.csv', 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            placement_list.append(row)
    print(placement_list)

    base_url = 'https://www.asx.com.au/asx/1/share/'
    code = ''
    suffix = '/prices?interval=daily&count=255'
    today = datetime.datetime.today()

    f = open('result.csv', 'w')
    writer = csv.writer(f)
    header = ["Company name",'Placement Date', "Code", "Placement price", "Type", "2 weeks before", "4 weeks before", "3 months before",
              "6 months before",
              "2 weeks after", "4 weeks after", "3 months after", "6 months after"]
    writer.writerow(header)

    for p in placement_list:
        code = p[0]
        price = p[1]
        type = p[3]
        name = p[4]


        date =datetime.datetime.strptime(p[2], '%Y-%m-%d')
        date_2w_b = date - datetime.timedelta(days=14)
        date_4w_b = date - datetime.timedelta(days=28)
        date_3m_b = date - datetime.timedelta(days=84)
        date_6m_b = date - datetime.timedelta(days=168)

        date_2w_a = date + datetime.timedelta(days=14)
        date_4w_a = date + datetime.timedelta(days=28)
        date_3m_a = date + datetime.timedelta(days=84)
        date_6m_a = date + datetime.timedelta(days=168)
        print(date_2w_a)
        print(date_4w_a)
        print(date_3m_a)
        print(date_6m_a)

        date_dict={}
        date_dict['date_2w_b'] = {"date":str(date_2w_b)[:10], "price":'NA'}
        date_dict['date_4w_b'] = {"date":str(date_4w_b)[:10], "price":'NA'}
        date_dict['date_3m_b'] = {"date":str(date_3m_b)[:10], "price":'NA'}
        date_dict['date_6m_b'] = {"date":str(date_6m_b)[:10], "price":'NA'}
        date_dict['date_2w_a'] = {"date": str(date_2w_a)[:10], "price": 'NA'}

        date_dict['date_4w_a'] = {"date": str(date_4w_a)[:10], "price": 'NA'}
        date_dict['date_3m_a'] = {"date": str(date_3m_a)[:10], "price": 'NA'}
        date_dict['date_6m_a'] = {"date": str(date_6m_a)[:10], "price": 'NA'}


        for key in date_dict:
            date_tem = date_dict[key]['date']
            date_tem = datetime.datetime.strptime(date_tem, '%Y-%m-%d')
            if date_tem > today:
                date_dict[key]['price'] = "TBD"

        url = base_url + code + suffix
        print(url)
        r = requests.get(url, timeout=10)
        price_data = r.json()

        data = {}
        if 'data' in price_data.keys():
            data = price_data['data']


        for d in data:
            for key in date_dict.keys():
                if d['close_date'][:10] == date_dict[key]["date"]:
                    #print(date_dict[key]['date'], key, d["close_price"])
                    date_dict[key]['price'] = d["close_price"]
                    print(date_dict)


        deviation = 1
        while (deviation <= 4):
            for key in date_dict.keys():
                if date_dict[key]['price'] == 'NA':
                    old_date = date_dict[key]['date']
                    old_date = datetime.datetime.strptime(old_date, '%Y-%m-%d')
                    new_date = old_date - datetime.timedelta(days=deviation)
                    date_dict[key]['date'] = str(new_date)[:10]
                    for d in data:
                        for key in date_dict.keys():
                            if d['close_date'][:10] == date_dict[key]["date"]:
                                #print(date_dict[key]['date'], key, d["close_price"])
                                date_dict[key]['price'] = d["close_price"]
            deviation = deviation + 1

        deviation = 5
        while (deviation <= 8):
            for key in date_dict.keys():
                if date_dict[key]['price'] == 'NA':
                    old_date = date_dict[key]['date']
                    old_date = datetime.datetime.strptime(old_date, '%Y-%m-%d')
                    new_date = old_date + datetime.timedelta(days=deviation)
                    date_dict[key]['date'] = str(new_date)[:10]
                    for d in data:
                        for key in date_dict.keys():
                            if d['close_date'][:10] == date_dict[key]["date"]:
                                #print(date_dict[key]['date'], key, d["close_price"])
                                date_dict[key]['price'] = d["close_price"]
            deviation = deviation + 1

        row = [name, p[2], code, price, type,
               date_dict['date_2w_b']['price'],
               date_dict['date_4w_b']['price'],
               date_dict['date_3m_b']['price'],
               date_dict['date_6m_b']['price'],
               date_dict['date_2w_a']['price'],
               date_dict['date_4w_a']['price'],
               date_dict['date_3m_a']['price'],
               date_dict['date_6m_a']['price']]
        writer.writerow(row)


        if date_dict['date_2w_b']['price'] != 'NA' and date_dict['date_2w_b']['price'] != 'TBD':
            cg_2w_b = round((float(price) - date_dict['date_2w_b']['price'])/date_dict['date_2w_b']['price']*100, 2)
        else:
            cg_2w_b = 0

        if date_dict['date_4w_b']['price'] != 'NA' and date_dict['date_4w_b']['price'] != 'TBD':
            cg_4w_b = round((float(price) - date_dict['date_4w_b']['price'])/date_dict['date_4w_b']['price']*100, 2)
        else:
            cg_4w_b = 0

        if date_dict['date_3m_b']['price'] != 'NA' and date_dict['date_3m_b']['price'] != 'TBD':
            cg_3m_b = round((float(price) - date_dict['date_3m_b']['price'])/date_dict['date_3m_b']['price']*100, 2)
        else:
            cg_3m_b = 0

        if date_dict['date_6m_b']['price'] != 'NA' and date_dict['date_6m_b']['price'] != 'TBD':
            cg_6m_b = round((float(price) - date_dict['date_6m_b']['price'])/date_dict['date_6m_b']['price']*100, 2)
        else:
            cg_6m_b = 0

        if date_dict['date_2w_a']['price'] != 'NA' and date_dict['date_2w_a']['price'] != 'TBD':
            cg_2w_a = round((float(price) - date_dict['date_2w_a']['price']) / date_dict['date_2w_a']['price'] * 100, 2)
        else:
            cg_2w_a = 0

        if date_dict['date_4w_a']['price'] != 'NA' and date_dict['date_4w_a']['price'] != 'TBD':
            cg_4w_a = round((float(price) - date_dict['date_4w_a']['price']) / date_dict['date_4w_a']['price'] * 100, 2)
        else:
            cg_4w_a = 0

        if date_dict['date_3m_a']['price'] != 'NA' and date_dict['date_3m_a']['price'] != 'TBD':
            cg_3m_a = round((float(price) - date_dict['date_3m_a']['price']) / date_dict['date_3m_a']['price'] * 100, 2)
        else:
            cg_3m_a = 0

        if date_dict['date_6m_a']['price'] != 'NA' and date_dict['date_6m_a']['price'] != 'TBD':
            cg_6m_a = round((float(price) - date_dict['date_6m_a']['price']) / date_dict['date_6m_a']['price'] * 100, 2)
        else:
            cg_6m_a = 0


        row2 = ['', '', '', '','',
                str(cg_2w_b)+ "%",
                str(cg_4w_b) + "%",
                str(cg_3m_b) + "%",
                str(cg_6m_b) + "%",
                str(cg_2w_a) + "%",
                str(cg_4w_a) + "%",
                str(cg_3m_a) + "%",
                str(cg_6m_a) + "%",
                ]
        writer.writerow(row2)

    f.close()
        #df = pd.DataFrame(price_data['data'])
        #df['close_date'] = pd.to_datetime(df.close_date.str[0:10], format='%Y-%m-%d', errors='coerce')

        #print(df['close_date'])
        #print(df['close_price'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
