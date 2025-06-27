#Function to update the inventory file
def update_inventory_file(d):
    """
        Update the inventory text file with the current inventory data.

        This function writes the updated inventory data from the dictionary to 'inventory.txt'.
        Each product's information is written as a comma-separated line.

        Parameters:
        d (dict): A dictionary containing inventory information with Product IDs as keys.
            Each entry (value) is a list containing:
                - Name (str): The name of the product.
                - Brand (str): The brand of the product.
                - Quantity (str): The available quantity of the product.
                - Price (str): The price of the product.
                - Origin (str): The origin of the product.

        Returns:
        boolean: 
            - True: If the inventory file is successfully updated.
            - False: If an error occurs during the update process.
        """
    
    try:
        #Opening the inventory in read mode
        update_inventory = open("inventory.txt","w")

        #Rewriting the contents
        for product in d.values():
            line = ",".join(product) + "\n"
            update_inventory.write(line)
        update_inventory.close()
        return True
    
    except:
        return False
    

#Function to generate invoice file for selling items
def generate_sell_invoice(d, cart_dict, billing_info, prod_pad):
    """
    Generate and save a customer invoice text file after a successful sale.

    The invoice includes store details, billing date, customer info, product details, and cost breakdown.

    Parameters:
    d (dict): A dictionary containing inventory information with Product IDs as keys.
    Each entry (value) is a list containing:
        - Name (str): The name of the product.
        - Brand (str): The brand of the product.
        - Quantity (str): The available quantity.
        - Price (str): The unit price of the product.
        - Origin (str): The origin of the product.

    cart_dict (dict): A dictionary of items being purchased with Product IDs as keys.
    Each value is a list containing:
        - Total Sell Quantity (int): The quantity being sold including free units.
        - Free Quantity (int): The number of free units given.
        - Sell Quantity (int): The quantity purchased (excluding free units).

    billing_info (dict): A dictionary containing billing information with the following keys:
        - 'time' (str): Timestamp of the transaction.
        - 'name' (str): Customer's name.
        - 'phone' (str): Customer's phone number.
        - 'total' (float): Total cost before VAT.
        - 'vat' (float): Value-added tax amount.
        - 'grand_total' (float): Final payable amount.

    prod_pad (function): A helper function to format string fields for uniform column width in the invoice.

    Returns:
    str: A confirmation message stating that the invoice file has been created.
    """

    #Creating new invoice file and opening in write mode
    invoice_name = str(billing_info["time"]).replace(":","")+".txt"
    invoice_file = open(invoice_name,"w")

    #Writing the header and formatting to the invoice file
    invoice_file.write("\n"*2 + "-" * 80 + "\n")
    invoice_file.write(" " * 32 + "CUSTOMER INVOICE\n")
    invoice_file.write("-" * 80  + "\n")
    invoice_file.write("WeCare Store\n")
    invoice_file.write("Samakushi, Kathmandu, Nepal\n\n")
    invoice_file.write("Date: " + str(billing_info["time"]) + "\n")
    invoice_file.write("Name: " + billing_info["name"] + "\n")
    invoice_file.write("Phone no.: " + str(billing_info["phone"]) + "\n")
    invoice_file.write("-" * 80 + "\n")
    invoice_file.write("Name"+" "*15 + "Brand"+" "*10 + "Price"+" "*5 + "Quantity"+" "*5 + "Free"+" "*5 + "Total"+" "*5 + "\n")
    invoice_file.write("-" * 80 + "\n")

    #iterating through all the items in cart
    for key in cart_dict:

        #Calling the function prod_pad to ensure equal spacing in each row
        #writing the product details to the file
        invoice_file.write(prod_pad(d[key][0], 19))
        invoice_file.write(prod_pad(d[key][1], 15))
        invoice_file.write(prod_pad(int(d[key][3])*2, 12))
        invoice_file.write(prod_pad(cart_dict[key][2], 12))
        invoice_file.write(prod_pad(cart_dict[key][1], 9))
        invoice_file.write(prod_pad(cart_dict[key][0]*int(d[key][3])*2, 16))
        invoice_file.write("\n")

    #Writing total cost
    invoice_file.write("-" * 80 + "\n")
    invoice_file.write("Total: " + str(billing_info["total"]) + "\n")
    invoice_file.write("VAT: " + str(billing_info["vat"]) + "\n")
    invoice_file.write("Grand Total: " + str(billing_info["grand_total"]) + "\n")
    invoice_file.write("-" * 80 + "\n")
    invoice_file.close()

    return "Invoice file has been created."


#Function to generate invoice file for restocking items
def generate_stock_invoice(d, stock_list, restock_info, prod_pad):
    """
        Generate and save a restock invoice text file after inventory is updated with new stock.

        The invoice includes store details, restock date, item details, supplier information, and total cost.

        Parameters:
        d (dict): A dictionary containing inventory information with Product IDs as keys.
        Each entry (value) is a list containing:
            - Name (str): The name of the product.
            - Brand (str): The brand of the product.
            - Quantity (str): The available quantity.
            - Price (str): The unit price of the product.
            - Origin (str): The origin of the product.

        stock_list (list): A list of lists, where each inner list represents a restocked item and contains:
            - Product ID (int): The ID of the product being restocked.
            - Quantity (int): The quantity of the product added to inventory.
            - Supplier (str): The name of the supplier.

        restock_info (dict): A dictionary containing restocking summary with the following keys:
            - 'time' (str): Timestamp of the restocking event.
            - 'total' (float): Total cost before VAT.
            - 'vat' (float): Value-added tax amount.
            - 'grand_total' (float): Final payable amount.

        prod_pad (function): A helper function to format string fields for uniform column width in the invoice.

        Returns:
        str: A confirmation message stating that the invoice file has been created.
        """
    #Generating restock invoice file
    invoice_name = str(restock_info["time"]).replace(":","")+".txt"
    invoice_file = open(invoice_name,"w")

    #Formatting and printing header for the table
    invoice_file.write("\n"*2 + "-" * 80 + "\n")
    invoice_file.write(" " * 32 + "RESTOCK INVOICE\n")
    invoice_file.write("-" * 80 + "\n")
    invoice_file.write("WeCare Store" + "\n")
    invoice_file.write("Samakushi, Kathmandu, Nepal\n")
    invoice_file.write("Date: " + str(restock_info["time"]) + "\n\n")
    invoice_file.write("-" * 80 + "\n")
    invoice_file.write("Name"+" "*12 + "Brand"+" "*10 + "Price"+" "*5 + "Quantity"+" "*5 + "Supplier"+" "*5 + "Total"+" "*5 + "\n")
    invoice_file.write("-" * 80 + "\n")

    #Iterating through all restocked products
    for item in stock_list:
        
        #Writing product details to the file
        invoice_file.write(prod_pad(d[item[0]][0], 16))
        invoice_file.write(prod_pad(d[item[0]][1], 15))
        invoice_file.write(prod_pad(int(d[item[0]][3]), 12))
        invoice_file.write(prod_pad(item[1], 12))
        invoice_file.write(prod_pad(item[2], 13))
        invoice_file.write(prod_pad(int(item[1])*int(d[item[0]][3]), 16))
        invoice_file.write("\n")

    #Writing total cost/footer
    invoice_file.write("-" * 80 + "\n")
    invoice_file.write("Total: " + str(restock_info["total"]) + "\n")
    invoice_file.write("VAT: " + str(restock_info["vat"]) + "\n")
    invoice_file.write("Grand Total: " + str(restock_info["grand_total"]) + "\n")
    invoice_file.write("-" * 80 + "\n")

    invoice_file.close()

    #Informing user
    return "Invoice file created."