import networkx as nx
from dataio import *
import random
import string
import rstr
import api

from allpairspy import AllPairs
from faker import Faker

#User PageRank algorithm to resort fields importants based on reference from other fields as 'dependent on'

def resort_fields(field_ref_map):
    # Create blank graph
    D=nx.DiGraph()

    # Feed page link to graph
    D.add_weighted_edges_from(field_ref_map)

    # Print page rank for each pages
    #print (nx.pagerank(D))
    high_rank = dict(sorted(nx.pagerank(D).items(), key=lambda item: item[1], reverse=True))
    return (high_rank)


def build_pairwise_permutation (data):
    permutation = []

    cnt = 0
    for i, pairs in enumerate(AllPairs(data)):
        cnt = cnt + 1
        permutation.append(pairs)
        #print("{:2d}: {}".format(i, pairs))
    return permutation


def reshufle_input (parameters, resorted_fields):
    first = int(list(resorted_fields.keys())[0]) - 1
    new_parameters = [[]]
    new_parameters[0] = parameters[first]
    id = 0
    for k in parameters:
        if id < len(resorted_fields):
            cur = int(list(resorted_fields.keys())[id]) - 1
            if id != 0 and id < len(resorted_fields):
                print (len(resorted_fields))
                new_parameters.append(parameters[cur])
        else:
            new_parameters.append(parameters[id])
        id = id + 1
    return new_parameters

def generate_test_data(rules, rows, fields):
    f = Faker()
    d=[[]]
    d.append([])

    t = {'': '',
    'address': 'f.address()',
    'automotive': 'f.automotive()',
    'android_platform_token': 'f.android_platform_token',
    'ascii_free_email': 'f.ascii_free_email',
    'bban': 'f.bban()',
    'color': 'f.color()',
    'company': 'f.company()',
    'company_email': 'f.company_email()',
    'coordinate': 'f.coordinate()',
    'credit_card_number': 'f.credit_card_number()',
    'credit_card_expire': 'f.credit_card_expire()',
    'credit_card_provider': 'f.credit_card_provider()',
    'credit_card_security_code': 'f.credit_card_security_code()',
    'currency_code': 'f.currency_code()',
    'date': 'f.date()',
    'date_time': 'f.date_time()',
    'day_of_week': 'f.day_of_week()',
    'Empty': '',
    'file_name': 'f.file_name()',
    'first_name': 'f.first_name()',
    'future_date': 'f.future_date()',
    'ios_platform_token': 'f.ios_platform_token()',
    'ipv4': 'f.ipv4()',
    'isbm': 'f.isbm()',
    'job': 'f.job()',
    'language_code': 'f.language_code()',
    'last_name': 'f.last_name()',
    'license_plate': 'f.license_plate()',
    'linux_platform_token': 'f.linux_platform_token()',
    'mac_platform_token': 'f.mac_platform_token()',
    'name': 'f.name()',
    'name_female': 'f.name_female()',
    'name_male': 'f.name_male()',
    'past_datetime': 'f.past_datetime()',
    'phone_number': 'f.phone_number()',
    'prefix': 'f.prefix()',
    'pricetag': 'f.pricetag()',
    'random_int': 'f.random_int()',
    'random_number': 'f.random_number()',
    'RandomString': '',
    'RegExp': '',
    'safe_color_name': 'f.safe_color_name()',
    'ssn': 'f.ssn()',
    'suffix': 'f.suffix()',
    'swift': 'f.swift()',
    'time': 'f.time()',
    'timezone': 'f.timezone()',
    'url': 'f.url()',
    'user_agent': 'f.user_agent()',
    'windows_platform_token': 'f.windows_platform_token()',
    'year': 'f.year()',}

    #for j in range(len(rules)):
    #    d[0].append(rules[j][0])
    for k in range(len(fields)):
        d[0].append(fields[k])
    for i in range(rows):
        if i!=0:
            d.append([])

        for j in range(len(rules)):
            r=rules[j][0]
            r=r.lower()

            a=t.get(r)
            if a!="" and a!=None:

                exec("d[i+1].append("+a+")")
                print (a)
            else:
                print (r)
                if r=='number':
                    d[i+1].append(''.join(random.choices(string.digits, k=7)))
                if r=='randomstring':
                    d[i+1].append(''.join(random.choices(string.ascii_lowercase + string.digits, k=10)))
                if r=='empty':
                    d[i+1].append('')
                if r=='regexp':
                    str = rstr.xeger(r)
                    d[i+1].append(str)

    return d

class WiseTestData:

    api_version="api1"
    rows=1
    excel='TestData.xlsx'
    no_gen="False"
    no_pair="False"
    no_shuffle="False"
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, api_version, rows, excel, no_gen, no_pair, no_shuffle):
        if api_version!="" and api_version!=None:
            self.api_version = api_version
        if rows != "" and rows != None:
            self.rows = rows
        if excel != "" and excel != None:
            self.excel = excel
        if no_gen != "" and no_gen != None:
            self.no_gen = no_gen
        if no_pair != "" and no_pair != None:
            self.no_pair = no_pair
        if no_shuffle != "" and no_shuffle != None:
            self.no_shuffle = no_shuffle

        #print (self.no_shuffle)


    def make_data(self):
        field_names = get_field_names(WiseTestData.excel, 'data')
        if self.no_gen=="False":

            data = generate_test_data(get_test_data_arr (self.excel, 'data', 0), self.rows, field_names)
            #data.insert(0, field_names)
            wb = save_gen_test_data (self.excel, 'generated', data, "a")
        else:
            wb = 'data'

        res=""
        if self.no_shuffle=="False":
            field_ref_map = get_field_ref_map(self.excel, 'ref')
            resorted_fields = resort_fields(field_ref_map)
            if self.no_gen == False:
                skp=0
            else:
                skp=1
            parameters = get_test_data_arr (self.excel, wb, skp)
            new_parameters=reshufle_input(parameters, resorted_fields)

            permutations = build_pairwise_permutation(new_parameters)
            res = save_test_data (self.excel, 'WiseTD', permutations, field_names, resorted_fields, "a")
        #else:
            #new_parameters=parameters
            #print (new_parameters)
        #print("Resulted Pairwise permuations: "+str(permutations))
        #print("Result rows#: "+str(len(permutations)))

        return res

#Uncomment and parametrize to use in IDE and comment #import api string to stop using API mode
#runer = WiseTestData ("api", 4, 'TestData.xlsx', "False", "False", "False")
#runer.make_data()