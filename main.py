from fileinput import filename
from pprint import pprint
import csv
import re


def read_csv(file_name):
    with open(file_name) as file:
        rows = csv.reader(file, delimiter=",")
        contact_list = list(rows)
    return contact_list


def get_right_rows(contact_list):
    row_dict = {}
    response = None
    for line in contact_list[1:]:
        name = ' '.join(line[:3])
        name_list = name.strip().split(' ')
        lastname = ''
        firstname = ''
        surname = ''
        if len(name_list) == 3:
            lastname, firstname, surname = name_list
        elif len(name_list) == 2:
            name_list.append('')
            lastname, firstname, surname = name_list
        organization = line[3]
        position = line[4]
        line = ' '.join(line)
        phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]\s?\(?д?о?б?\)?\.?\s?\d?\d?\d?\d?\)?', line)
        if len(phone) > 0:
            phone = phone[0]
            s = [symbol for symbol in phone if symbol.isdigit()]
            if s[0] == '8':
                s[0] = '7'
            phone = f'+{s[0]}({s[1]}{s[2]}{s[3]}){s[4]}{s[5]}{s[6]}-{s[7]}{s[8]}-{s[9]}{s[10]}'
            if len(s) == 15:
                additional = ''.join(s[11:])
                phone += f' доб.{additional}'
        else:
            phone = ''
        email = re.findall(r"\S+@\S+\.\S+", line)
        if len(email) > 0:
            email = email[0]
        else:
            email = ''
        row_list = [lastname, firstname, surname, organization, position, phone, email]
        if lastname in row_dict.keys():
            if firstname != '':
                row_dict[lastname][1] = firstname
            if surname != '':
                row_dict[lastname][2] = surname
            if organization != '':
                row_dict[lastname][3] = organization
            if position != '':
                row_dict[lastname][4] = position
            if phone != '':
                row_dict[lastname][5] = phone
            if email != '':
                row_dict[lastname][6] = email
        else:
            row_dict[lastname] = row_list
        response = [val for val in row_dict.values()]
        response.insert(0, contact_list[0])
    return response


def save_csv(file_name, csv_list):
    with open(file_name, "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(csv_list)


if __name__ == '__main__':
    old_file = 'address_book.csv'
    new_file = 'new_address_book.csv'
    contact_list = read_csv(old_file)
    right_rows = get_right_rows(contact_list)
    for elem in right_rows:
        print(elem)
    save_csv(new_file, right_rows)