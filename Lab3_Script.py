from sys import argv, exit
import os
from datetime import date
import pandas as pd
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
CUSTOMER_NAME_PATTERN = r"^[\w\s,'.-]+$"


def main():
    sales_csv = get_sales_csv()
    order_dir = create_order_dir(sales_csv)
    process_sales_data(sales_csv, order_dir)




#Path of Sales_data csv file
def get_sales_csv():
    #Check command line params
    if len(argv) > 2:
        print(f"Stop with the arguements now") 
        return
    
    if len(argv) <= 1:
        print("ERROR: CSV file path has not been provided")
    sales_csv = argv[1]

        #Provider param
    print(f"Checking if {sales_csv} is a valid filename")
    if not os.path.isfile(sales_csv):
        print('Error: Invalid Path to sales data CSV file. It wasn\'t found, it was supposed to but it did not work lol')
        return
    
    if not sales_csv.endswith(".csv"):
        print("Extension for csv was not found")
        return
    
    print("Valid extension for csv")
    return sales_csv


def create_order_dir(sales_csv):
    sales_dir = os.path.dirname(os.path.abspath(sales_csv))
    todays_date = date.today().isoformat()
    orders_dir = os.path.join(sales_dir, f'Orders_{todays_date}')
    #Returning orders directory (output)
    if not os.path.isdir(orders_dir):
        os.makedirs(orders_dir)
    return orders_dir

#formatting for price!!!!!!
def price_format(price):
    return "${:,.2f}".format(price)



#Spliting the data individually in order to save it to Excel file
def process_sales_data(sales_csv, orders_dir):
    grouped_sales = pd.read_csv(sales_csv).groupby("ORDER ID") 

    for order_id, orders in grouped_sales:
        new_df = pd.DataFrame(orders, columns=["ORDER DATE", "ITEM NUMBER", "PRODUCT LINE", "PRODUCT CODE", "ITEM QUANTITY", "ITEM PRICE", "STATUS", "CUSTOMER NAME"])
        new_df["TOTAL_PRICE"] = new_df["ITEM QUANTITY"] * new_df["ITEM PRICE"]
        grand_total = "${:,.2f}".format(new_df["TOTAL_PRICE"].sum())
        new_df.sort_values(by='ITEM NUMBER', ascending=True, inplace=True)
        new_df = new_df.append({"TOTAL_PRICE": grand_total}, ignore_index=True)
        export_order_to_excel(order_id, new_df, orders_dir)


#Function for excel sheet order. As defined below.
def export_order_to_excel(order_id, order_df, order_dir):

# Order of Excel sheet
    customer_name = order_df['CUSTOMER NAME'].values[0]
    print(customer_name)
    order_file = f'order-{order_id}.xlsx'
    order_path = os.path.join(order_dir, order_file)
    sheet_name = f'order#{order_id}'
    order_df.to_excel(order_path, index=False, sheet_name=sheet_name)


#calling out the main() function at lasttttttttttttttt!!!!!!!!!!!!!!!!!!!!
main()

