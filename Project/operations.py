import datetime
import write

#Function to get the data with suitable spacing
def prod_pad(text, length):

    '''
Take the length of the text to be printed and check its length compared to the defined column length.
If the text is shorter adds sufficient whitespace after it.
If the text is longer, cuts the text and trails with '...' to ensure the tabular format isnt broken.

Parameters:
'text'(str) : The product info to be printed.
'length'(int) : The custom defined length of the column.

Returns:
'pad_text'(str) : The string that has the text concatenated with sufficient white space or with trailing '...'.

Example:
print(prod_pad("hello",10), end="")\n
It prints 'hello_____' i.e. hello and 5 whitespaces.
    '''
    
    text = str(text)
    f_text = ""
    c = 1

    #formatting in case of longer texts
    if len(text) > length-1:
        for ch in text:
            
            #slicing the text to fit the column width
            if c > length-4:
                f_text = f_text+"..."
                break
            f_text += ch
            c += 1
            
        pad_text = f_text+" "*(length - len(f_text))

    #formatting in case of preferred text size
    else:
        pad_text =text+" "*(length - len(text))
    
    return pad_text

#Function to validate numeric choice
def validate_choice(input_line, valid_options):
    '''
    Takes the prompt to be printed while asking user for choice checks if the input choice is valid.
    It checks the user input for each element in the valid_options list and loops until a valid option is entered.

    Parameters:
    -'input_line'(str) : Line to print while asking to input a choice
    -'valid_options'(list) : List containing the valid options

    Returns:
    'choice'(int) : The choice that is in the valid_options list

    Example:
    option = validate_choice("Enter a choice: ",[1,2,3])
    It asks the user for choices until a choice available in the list is entered.
    '''
    loop = True

    #Loop to prompt till valid input
    while loop:
        try:
            choice = int(input(input_line))
            #Checking if the input is valid
            if choice in valid_options:
                return choice
            else:
                print("Please enter a valid option.\n")
        except:
            print("Please enter a valid option.\n")

    return choice

#Function to validate ID
def id_validation(d, cart_dict):
    '''
    Prompt the user to input a product ID for selling and validate it against the inventory.
    If the product already exists in the cart, notify the user and restore its quantity to inventory.

    Parameters:
    d (dict): A dictionary containing inventory information with Product IDs as keys.
    Each entry (value) is a list containing:
        - Name (str): The name of the product.
        - Brand (str): The brand of the product.
        - Quantity (str): The available quantity.
        - Price (str): The unit price of the product.
        - Origin (str): The origin of the product.

    cart_dict (dict): A dictionary containing cart information with Product IDs as keys.
    Each entry (value) is a list containing:
        - sell_qty (int): The quantity being sold.
        - free_qty (int): The quantity given for free.
        - total_qty (int): The total quantity being deducted from inventory.

    Returns:
    int: A valid product ID that exists in the inventory.
    '''
    #Taking product ID from user and Validating it
    sell_id = 0
    while sell_id not in d:
        try:
            sell_id = int(input("\nPlease Enter the Product (ID) to Sell:"))
            if sell_id not in d:
                print("Please enter a valid ID from Inventory.")
        except:
            print("Please enter a valid number ID from Inventory.")

    #Notify if the product already exists in the cart
    if sell_id in cart_dict:
        print("Note: " + d[sell_id][0] + " was already in cart. The previous quantity will be replaced.")
        previous_qty = cart_dict[sell_id][2]
        d[sell_id][2] = str(int(d[sell_id][2]) + previous_qty)
        print("The sellable quantity for " + d[sell_id][0] + " is still " + str(d[sell_id][2]) + ".")
    return sell_id

#Function to validate quantity
def qty_validation(d, sell_id):
    """
    Prompt the user to enter a valid quantity of a product to sell and calculate the free quantity based on the offer.

    Parameters:
    d (dict): A dictionary containing product inventory information with product IDs as keys. Each entry should include:
        - 'name' (str): Name of the product.
        - 'brand' (str): Brand of the product.
        - 'quantity' (str): Available quantity in stock.
        - 'price' (str): Price of the product.
        - 'origin' (str): Country of origin.
    sell_id (int): The ID of the product selected for selling.

    Returns:
    list: A list containing:
        - sell_qty (int): The quantity of the product to sell (excluding free items).
        - free_qty (int): The number of free products offered (1 free per 3 sold).
        - total_sell_qty (int): Total quantity including free products.
    """

    #Taking product quantity from user and validating it
    sell_qty = 0
    total_sell_qty = 0
    free_qty = 0

    #Asking for quantity to sell
    while sell_qty == 0:
        try:
            sell_qty = int(input("\nPlease Enter the quantity of " + d[sell_id][0] + " to Sell:"))
            if(sell_qty < 1):
                print("\nThe quantity must be at least 1.")
                sell_qty = 0
            elif(sell_qty > int(d[sell_id][2])):
                print("\nThe product quantity in inventory is not sufficient.\nAvailable Stock: "+d[sell_id][2])
                sell_qty = 0
            else:
                #Calculating number of free products and total products
                free_qty = sell_qty//3
                total_sell_qty = sell_qty + free_qty

                #Checking for sufficient product quantity
                if(total_sell_qty >  int(d[sell_id][2])):
                    print("\nThe product quantity in inventory is not sufficient for free items.\nAvailable Stock: "+d[sell_id][2])

                    #Displaying the highest quantity available to sell
                    recommanded_qty = (int(d[sell_id][2])*3)//4
                    print("[Note:", recommanded_qty, " is the maximum base quantity that can be sold to include free items" + "]")
                    sell_qty = 0
        except:
            print("\nPlease enter a valid quantity number.\n")
            sell_qty = 0
    return [sell_qty, free_qty, total_sell_qty]

#Function to display the inventory
def display_inventory(d, type):
    """
    Display the inventory in a tabular format.

    Parameters:
    d (dict): A dictionary containing product information with product IDs as keys. Each entry should include:
        - 'name' (str): Name of the product.
        - 'brand' (str): Brand of the product.
        - 'quantity' (str): Available quantity in stock.
        - 'price' (str): Price of the product.
        - 'origin' (str): Country of origin.
    type (str): A string that indicates the type of display. It can either be:
        - "sell": Displays the product for sale with adjusted price for selling(200%).
        - "stock": Displays the product price without changes.

    Returns:
    boolean: Always returns `True` after displaying the inventory.
    """
    #defining the tabular format
    print("\n"*2," " * 32, "Inventory\n")
    print("-" * 80)

    #formatting and printing header for the table
    print("ID"+" "*6 + "Name"+" "*16 + "Brand"+" "*8 + "Quantity"+" "*5 + "Price"+" "*5 + "Origin"+" "*5)
    print("-" * 80)

    #iterating through each key-value pair in dictionary
    for key,value in d.items():
        
        #printing the index
        print(prod_pad(key,8), end="")

        #printing the product details
        i = 0
        for each in value:
            if(i == 0):
                #Calling the function prod_pad to ensure equal spacing in each row
                print(prod_pad(each,20), end="")
            elif(i == 1):
                print(prod_pad(each,16), end="")
            elif(i == 2):
                print((prod_pad(int(each),11)), end="")
            elif(i == 3):
                if type == "sell":
                    print(prod_pad(int(each)*2,9), end="")
                elif type == "stock":
                    print(prod_pad(int(each),9), end="")

            elif(i == 4):
                print(each)
            i+=1

    print("-" * 80)
    print("\n\n")
    return True

#Function to display the cart
def display_cart(d, cart_dict):
    """Display the items in the cart and their total cost, including VAT and grand total.

    Parameters:
    d (dict): A dictionary containing product information with product IDs as keys. Each entry should include:
        - 'name' (str): Name of the product.
        - 'brand' (str): Brand of the product.
        - 'quantity' (str): Available quantity in stock.
        - 'price' (str): Price of the product.
        - 'origin' (str): Country of origin.
    cart_dict (dict): A dictionary containing the items added to the cart. Each key is the product ID and its value is a list containing:
        - 'sell_qty' (int): Quantity of the product to be sold.
        - 'free_qty' (int): Quantity of free products.
        - 'total_sell_qty' (int): Total quantity of products including free ones.

    Returns:
    list: A list containing the total cost, VAT, and grand total.
    """
    #Formatting and printing the final cart
    print("\n\n" + "-" * 80)
    print(" " * 32, "Cart")
    print("-" * 80)

    #formatting and printing header for the table
    print("ID"+" "*6 + "Name"+" "*17 + "Rate"+" "*9 + "Quantity"+" "*5 + "Free"+" "*5 + "Amount"+" "*5)
    print("-" * 80)

    total_cost, vat, grand_total = calculate_total(d, cart_dict, "sell")

    #iterating through each key-value pair in dictionary
    for key in cart_dict:
                        
        #printing the index
        print(prod_pad(key, 8), end="")
        
        #Calling the function prod_pad to ensure equal spacing in each row
        print(prod_pad(d[key][0], 21), end="")
        print(prod_pad(int(d[key][3])*2, 15), end="")
        print(prod_pad(cart_dict[key][2], 12), end="")
        print(prod_pad(cart_dict[key][1], 9), end="")
        print(prod_pad(cart_dict[key][0]*int(d[key][3])*2, 16), end="")
        print()

    #More Formatting
    print("-" * 80)
    print("Total: " + str(total_cost))
    print("-" * 80)
    print("\n\n")
    return [total_cost, vat, grand_total]

#Function to display invoice
def display_invoice(d, cart_dict, billing_info):
    """
    Display the invoice for a customer after a purchase, including product details, pricing, and customer information.

    Parameters:
    d (dict): A dictionary containing the product inventory with the following structure:
        - Key: Item ID (int)
        - Value: List containing ['name', 'brand', 'quantity', 'price', 'origin']
    cart_dict (dict): A dictionary representing the cart with Item IDs as keys. Each value should be a list containing:
        - 'sell_qty' (int): Quantity of the product to be sold.
        - 'free_qty' (int): Quantity of free products.
        - 'total_sell_qty' (int): Total quantity of products including free ones.
    billing_info (dict): A dictionary containing customer billing information with the following keys:
        - 'name' (str): Customer's name.
        - 'phone' (str): Customer's phone number.
        - 'total' (float): Total amount before VAT.
        - 'vat' (float): VAT amount.
        - 'grand_total' (float): Total amount including VAT.
        - 'time' (str): The time of the transaction.

    Returns:
    boolean: True if the invoice was displayed successfully.
    """
    #for Invoice Printing
    display_invoice_header(billing_info, "CUSTOMER INVOICE")

    #printing the table
    print("Name: " + billing_info["name"])
    print("Phone no.: " + str(billing_info["phone"]))
    print("-" * 80)
    print("ID"+" "*6 + "Name"+" "*15 + "Brand"+" "*10 + "Price"+" "*5 + "Quantity"+" "*5 + "Free"+" "*5 + "Total"+" "*5)
    print("-" * 80)
    #iterating through each key-value pair in dictionary
    for key in cart_dict:

        #printing the index
        print(prod_pad(key, 8), end="")
        
        #Calling the function prod_pad to ensure equal spacing in each row
        print(prod_pad(d[key][0], 19), end="")
        print(prod_pad(d[key][1], 15), end="")
        print(prod_pad(int(d[key][3])*2, 12), end="")
        print(prod_pad(cart_dict[key][2], 12), end="")
        print(prod_pad(cart_dict[key][1], 9), end="")
        print(prod_pad(cart_dict[key][0]*int(d[key][3])*2, 16), end="")
        print()

    #Printing the footer
    display_invoice_footer(billing_info)

    return True

#Function to get the customer details
def get_customer_details(costs_list):
    """
    Prompt the user to enter customer details (name and phone number) and generate a billing info dictionary.

    Parameters:
    costs_list (list): A list containing the following values:
        - total (float): Total cost of the purchase.
        - vat (float): VAT applied to the total cost.
        - grand_total (float): Total amount including VAT.

    Returns:
    billing_info (dictionary): A dictionary containing customer and billing details with the following keys:
        - 'name' (str): Customer's name.
        - 'phone' (str): Customer's phone number.
        - 'time' (str): The current timestamp when the transaction occurs.
        - 'total' (float): The total amount before VAT.
        - 'vat' (float): The VAT amount.
        - 'grand_total' (float): The total amount including VAT.
    """
    while True:
        try:
            customer_name = input("Enter the name: ")
            customer_phone = str(int(input("Enter the Phone number: ")))
            if len(customer_phone) != 10:
                print("Invalid Phone number.")
                continue
            current_time = str(datetime.datetime.now())

            #Grouping billing and customer details
            billing_info = {
                "name": customer_name,
                "phone": customer_phone,
                "time": current_time,
                "total": costs_list[0],
                "vat": costs_list[1],
                "grand_total": costs_list[2]
            }
            return billing_info
        except:
            print("Invalid input. Please try Again.")

#Function to ask yes/no questions
def ask_yes_no(prompt):
    """
    Prompt the user with a yes/no question and return their response as a boolean value.

    Parameters:
    'prompt' (str): The question or prompt to ask the user.

    Returns:
    boolean: True if the user responds with 'y' or 'yes', False if the user responds with 'n' or 'no'.
    """
    while True:
        #Taking user input
        ans = input(prompt + "(y/n): ").lower()
        if ans in ("y", "yes"):
            return True
        elif ans in ("n", "no"):
            return False
        else:
            print("Invalid Input. Please try again.")

#Function to Checkout
def checkout_loop(d, cart_dict, costs_list):
    """
    Continuously ask the user if they wish to checkout, generate the invoice, and update the inventory.

    Parameters:
    'd' (dict): A dictionary containing product information with product IDs as keys. Each entry should include:
        - 'name' (str): Name of the product.
        - 'brand' (str): Brand of the product.
        - 'quantity' (str): Available quantity in stock.
        - 'price' (str): Price of the product.
        - 'origin' (str): Country of origin.
    'cart_dict' (dict): A dictionary containing the items added to the cart. Each key is the product ID and its value is a list containing:
        - 'sell_qty' (int): Quantity of the product to be sold.
        - 'free_qty' (int): Quantity of free products.
        - 'total_sell_qty' (int): Total quantity of products including free ones.
    'costs_list' (list): A list containing the total cost, VAT, and grand total for the sale.

    Returns:
    boolean: False if the checkout process is completed.
    billing_info (dict): The customer's billing information (name, phone, time, total, vat, grand_total).
    """
    #Loop to check if customer wants to checkout
    billing_info = {}
    while True:

        if ask_yes_no("Does the customer wish to checkout now? "):

            #Loop to generate and display invoice/Bill
            print("\nPlease Fill out the Customer Details:")
            billing_info = get_customer_details(costs_list)

            if display_invoice(d, cart_dict, billing_info):
                #Updating the inventory file
                if write.update_inventory_file(d):
                    print("Inventory file updated.\n")
            return False, billing_info
            
            

        #Asking user if they wist to continue    
        else:
            print("Do you wish to continue selling or exit?")
            print("1. Continue the Sales")
            print("2. Exit")
            ans  = validate_choice("Enter an option: ",(1,2))
            if ans == 1:
                return True, billing_info
            else:

                #Changing back the inventory
                for key in cart_dict:
                    d[key][2] = str(int(d[key][2]) + cart_dict[key][2])
                return False, billing_info
            
#Function to add new product to inventory            
def add_product(d, stock_list):
    """
    Adds a new product to the inventory and logs the restock information.

    Parameters:
        'd' (dict): Inventory dictionary. Keys are item IDs (int), values are lists containing:
            - Name (str)
            - Brand (str)
            - Quantity (str)
            - Price (str)
            - Origin (str)
        'stock_list' (list): A list of lists, where each sub-list contains:
            - Product ID (int)
            - Quantity added (str)
            - Supplier name (str)

    Returns:
        bool: True if the product was added successfully.
              False if the product could not be added.
    """
    print("Please fill new Product details:")
    try:
        #Taking product details
        name = input("Enter the product name: ")
        brand = input("Enter the brand name: ")
        supplier = input("Enter the supplier: ")
        qty = int(input("Enter the initial quantity: "))
        price = int(input("Enter the cost price: "))
        origin = input("Enter the product origin: ")

        #Adding product details to main dictionary
        new_prod_id = 1
        for key in d:
            if key >= new_prod_id:
                new_prod_id = key + 1
        d[new_prod_id] = [name, brand, str(qty), str(price), origin]
         #Adding the new product's stocked quantity to stock list
        stock_list.append([new_prod_id, str(qty), supplier])
        return True
    except:
        print("Invalid input. Please try again.")
        return False

#Function to restock existing product
def restocking_product(d, stock_list):
    """
    Restocks an existing product in the inventory.

    Parameters:
    'd' (dict): Inventory dictionary. Keys are item IDs (int), values are lists containing:
        - Name (str)
        - Brand (str)
        - Quantity (str)
        - Price (str)
        - Origin (str)
    'stock_list' (list): A list of lists, where each sub-list contains:
        - Product ID (int)
        - Quantity added (str)
        - Supplier name (str)

    Returns:
     boolean: True if the product was successfully restocked.
              False if the product couldnt be restocked  
    """
    #Loop for restocking
    restock_loop = True
    while restock_loop == True:
        try:
            #Asking for the id of the product to restock
            restock_id = int(input("Enter the ID of product to restock: "))

            #Validating input product ID
            if restock_id not in d:
                print("ID does not exist in inventory. Please try again.")
                continue
            else:

                supplier = input("Enter the supplier: ")
                #Asking and validating product quantity to restock
                restock_qty = int(input("Enter the quantity to restock: "))
                if restock_qty < 1:
                    print("The quantity must be positive.")
                    continue

                #Updating the quantity in main dictionary
                d[restock_id][2] = str(int(d[restock_id][2]) + restock_qty)
                restock_loop = False
                #Adding the stocked quantity to stock dictionary
                stock_list.append([restock_id, str(restock_qty), supplier])            
                return True   
        except:
            print("Invalid input. Please try again.")
            return False

#Function to display the stock invoice
def display_stock_invoice(d, stock_list, restock_info):
    """
    Displays the stock restocking invoice in tabular format.

    Parameters:
    'd' (dict): The inventory dictionary where keys are product IDs (int), 
    and values are lists containing:
        - name (str)
        - brand (str)
        - quantity (str)
        - price (str)
        - origin (str)

    'stock_list' (list): A list of lists. Each sub-list contains:
        - product ID (int)
        - restocked quantity (str)
        - supplier name (str)

    'restock_info' (dict): A dictionary with restocking details:
        - 'time' (str): Timestamp of restocking
        - 'total' (int): Total cost of restocked items
        - 'vat' (int): VAT applied
        - 'grand_total' (int): Final amount including VAT

    Returns:
        None
    """

    #Printing restock invoice
    display_invoice_header(restock_info, "RESTOCK INVOICE")

    print("ID"+" "*4 + "Name"+" "*12 + "Brand"+" "*10 + "Price"+" "*5 + "Quantity"+" "*5 + "Supplier"+" "*5 + "Total"+" "*5)
    print("-" * 80)
    #Iterating through each key-value pair in dictionary
    
    for item in stock_list:
        #printing the index
        print(prod_pad(str(item[0]), 6), end="")
                            
        #Calling the function prod_pad to ensure equal spacing in each row
        print(prod_pad(d[item[0]][0], 16), end="")
        print(prod_pad(d[item[0]][1], 15), end="")
        print(prod_pad(int(d[item[0]][3]), 12), end="")
        print(prod_pad(str(item[1]), 12), end="")
        print(prod_pad(item[2], 13), end="")
        print(prod_pad(int(item[1])*int(d[item[0]][3]), 16), end="")
        print()
    
    #Printing the footer
    display_invoice_footer(restock_info)

#Function to update file, create invoice and exit to main menu
def restock_and_exit(d, stock_list):
    """
    Handles the finalization process after restocking products.
    Updates the inventory file, calculates totals, and displays the restock invoice.

    Parameters:
    'd' (dict): The inventory dictionary where keys are product IDs (int),
    and values are lists containing:
        - name (str)
        - brand (str)
        - quantity (str)
        - price (str)
        - origin (str)

    'stock_list' (list): A list of lists. Each sub-list contains:
        - product ID (int)
        - restocked quantity (str)
        - supplier name (str)

    Returns:
    dict or boolean: Returns a 'restock_info' dictionary with:
        - 'time' (str)
        - 'total' (int)
        - 'vat' (int)
        - 'grand_total' (int)
        If no items were restocked, returns False.
    """
    if not stock_list:
        return False
    else:
        #Updating inventory file
        write.update_inventory_file(d)

        current_time = str(datetime.datetime.now())

        total_cost, vat, grand_total = calculate_total(d, stock_list, "restock")

        #Grouping billing details
        restock_info = {
            "time": current_time,
            "total": total_cost,
            "vat": vat,
            "grand_total": grand_total
        }

        display_stock_invoice(d, stock_list, restock_info)

        return restock_info
    
# Function to calculate total costs, and taxes
def calculate_total(d, collection, type):
    """
    Calculates the total cost, VAT, and grand total based on the operation type.

    Parameters:
    'd' (dict): The inventory dictionary with product ID as key and a list as value:
        - name (str)
        - brand (str)
        - quantity (str)
        - price (str)
        - origin (str)

    'collection' (list or dict): 
        - If 'type' is 'restock': a list of lists, each containing:
            - product ID (int)
            - restocked quantity (str)
            - supplier (str)
        - If 'type' is 'sell': a dictionary where each key is a product ID (int),
            and value is a list containing:
            - total quantity sold including free items (int)
            - number of free items (int)
            - base sold quantity (int)

    'type' (str): Specifies the calculation mode. Should be either:
        - 'restock'
        - 'sell'

    Returns:
    tuple: A tuple containing:
        - 'total_cost' (int): The total cost before VAT.
        - 'vat' (float): The calculated VAT (13% of total).
        - 'grand_total' (float): The final amount including VAT.
    """
    total_cost = 0
    #Calculating total costs
    if type  == "restock":
        #For restock
        for item in collection:
            total_cost += int(item[1])*int(d[item[0]][3])
    
    elif type == "sell":
        #For sales
        for key in collection:
            total_cost += collection[key][0]*int(d[key][3])*2

    #Calculating VAT and adding to total cost
    vat = total_cost * 0.13
    grand_total = total_cost + vat
    return total_cost, vat, grand_total

#Function to display invoice header
def display_invoice_header(info, type):
    """
    Displays the invoice header with store details and invoice type.

    Parameters:
    'info' (dict): A dictionary containing invoice metadata:
        - 'time' (str): The timestamp of the transaction.

    'type' (str): The title to display for the invoice 
        ('CUSTOMER INVOICE' or 'RESTOCK INVOICE').

    Returns:
        None
    """

    #formatting and printing header for the table
    print("\n"*2 + "-" * 80)
    print(" " * 32 + type + "\n")
    print("-" * 80)
    print("WeCare Store")
    print("Samakushi, Kathmandu, Nepal\n")
    print("Date: " + str(info["time"]))
    print("-" * 80)

#Function to display invoice footer
def display_invoice_footer(info):
    """
    Displays the invoice footer with total, VAT, and grand total amounts.

    Parameters:
    'info' (dict): A dictionary containing financial summary details:
        - 'total' (float): The total amount before tax.
        - 'vat' (float): The value-added tax amount.
        - 'grand_total' (float): The final total including VAT.

    Returns:
        None
    """

    #Printing footer                        
    print("-" * 80)
    print("Total: " + str(info["total"]))
    print("VAT: " + str(info["vat"]))
    print("Grand Total: " + str(info["grand_total"]))
    print("-" * 80)
    print("\n\n")
    
#Main Function for selling products
def sales(d):
    """
    Handles the process of selling products by allowing the user to select items, 
    specify quantities, apply free product offers, and proceed to checkout.

    Parameters:
    'd' (dict): The main inventory dictionary where:
        - Keys are product IDs (int)
        - Values are lists containing product details:
            [name (str), brand (str), quantity (str), price (str), origin (str)]

    Returns:
    'd' (dict): The updated inventory dictionary after the sale.
    'cart_dict' (dict): A dictionary containing sold product information with:
        Keys as product IDs (int), and 
        Values as lists: [billed quantity (int), free quantity (int), total quantity (int)]
    'billing_info' (dict): Dictionary containing customer billing details.

    """
    #dictionary to hold items to sell
    cart_dict = {}
    continue_selling = True

    #Loop to continue selling products
    while continue_selling:
        
        if not display_inventory(d, "sell"):
            print("Could not be displayed. Pleae try again.")
            break

        sell_id = id_validation(d, cart_dict)

        #Dictionary to hold the items to buy
        cart_dict[sell_id] = qty_validation(d, sell_id)

        #Updating the inventory
        d[sell_id][2] = str(int(d[sell_id][2]) - cart_dict[sell_id][2])

        #Informing user about adding the product to cart
        print("\n\n" + str(cart_dict[sell_id][2]) + " of " + d[sell_id][0] + " added to cart.")
        print("Quantity Billed: ",cart_dict[sell_id][0])
        print("Additional Free Quantity: ",cart_dict[sell_id][1])
        
        #Asking user if they want to sell more products
        if ask_yes_no("Do you wish to sell more items? "):
            continue
        else:
            continue_selling = False
        
        #Displaying cart
        costs_list = display_cart(d, cart_dict)
        continue_selling, billing_info = checkout_loop(d, cart_dict, costs_list)

        if not continue_selling:
            #Exiting if the customer is done buying
            return d, cart_dict, billing_info

#Main Function for restocking products.
def restock(d):
    """
    Manages the inventory restocking process by allowing the user to add new products 
    or restock existing ones. Displays the updated stock and generates a restocking invoice.

    Parameters:
    'd' (dict): The main inventory dictionary where:
        - Keys are product IDs (int)
        - Values are lists containing product details:
            [name (str), brand (str), quantity (str), price (str), origin (str)]

    Returns:
    'd' (dict): The updated inventory dictionary after restocking.
    'stock_list' (list): A list of lists representing restocked items:
        Each sublist contains [product ID (int), quantity (str), supplier (str)]
    'restock_info' (dict): Dictionary containing restock invoice details:
        Includes 'time', 'total', 'vat', and 'grand_total'.

    Raises:
        ValueError: If an invalid input is entered when selecting restock options.
    """
    #List to store restocked/new products
    stock_list = []

    #Loop to continue stocking
    continue_stock = True
    while continue_stock == True:

        if not display_inventory(d, "stock"):
            print("Could not be displayed. Pleae try again.")
            break
        
        #Asking user if they want to add new product or restock inventory
        print("\nDo you wish to add product to inventory or restock?")
        print("1. Add new products")
        print("2. Restock product")
        print("3. Create invoice and Exit to menu.")
        stock_choice = int(validate_choice("\nEnter choice: ", (1,2,3)))

        #For adding new product
        if stock_choice == 1:

            if add_product(d, stock_list):
                print("Product added.\n")
            else:
                print("Something went wrong. Please try again.")

        #For restocking old products        
        elif stock_choice == 2:

            if restocking_product(d, stock_list):
                print("Product restocked.\n")
            else:
                print("Something went wrong. Please try again.")

        else:
            continue_stock = False
            restock_info = restock_and_exit(d, stock_list)            

    return d, stock_list, restock_info
