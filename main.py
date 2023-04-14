from bs4 import BeautifulSoup
from urllib.request import urlopen
from search_id import *
from url_traversal import get_json
import csv
import time
from Weapon import *
import gradio as gr


def main(case_name):
    print("Welcome to SMAB")
    #do a case match
    #case = input("Enter case you want to look at: ")
    #determine which case this is and get the correct url.
    #cases have an id tag associated with them in the url
    #tag_set_community_13 <-- this is that tag number
    #this will be hard coded and will be updated accordinginly
    url = find_case(case_name)
    if(url == "ERROR"):
        print("Case not found!")
    print(url)
    #going through all the links should pass back a list of skin objects
    #eventually we will intialize the list of case objects.
    JSON = []
    NumberOfPages = 14
    for i in range(NumberOfPages):
        JSON.append(get_json(url[:len(url) - 11] + str(i) + url[len(url) - 10:]))
        time.sleep(3)
        i += 1
    #Pipe out to a csv
    f = open("EV.csv", "w+")
    f.close()
    print(len(JSON))
    with open('EV.csv', 'wt') as f:
        csv_writer = csv.writer(f, quoting=csv.QUOTE_ALL)

        csv_writer.writerow(["Gun","skin","condition","stat_track","buy_price","sell_price", "estimated_value"])
        for j in JSON:
            for i in j:
                csv_writer.writerow(i.CSVstructure())
        csv_writer.writerow(["=Sum(F3:F" + str((NumberOfPages * 2 * 10) + 1) + ")"])
    return JSON

def display_items(case_name):
    items = main(case_name)
    header = ["Gun", "Skin", "Condition", "Stat_Track", "Buy_Price", "Sell_Price", "Estimated_Value"]

    # Initialize an empty dictionary to store the last data for each item
    last_data = {}

    # Iterate through items and update the last data for each unique item (identified by Gun and Skin)
    for page in items:
        for item in page:
            item_data = item.CSVstructure()
            item_key = (item_data[0], item_data[1], item_data[2])  # Create a tuple (Gun, Skin) to use as a dictionary key
            last_data[item_key] = item_data

    # Convert the dictionary values to a list of lists
    table_data = [header] + list(last_data.values())

    return table_data

def gradio_app(case_name):
    table_data = display_items(case_name)
    return table_data


iface = gr.Interface(
    fn=display_items,
    inputs=gr.components.Textbox(lines=1, placeholder="Enter case name"),
    outputs=gr.components.Dataframe(),
    title="CSGO Case Items",
    description="Enter the name of the CSGO case to display its items.",
)
iface.launch()
iface.launch()


if __name__ == "__main__":
    main()

