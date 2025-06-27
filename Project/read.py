#Function to read data from the inventory file
def read_inventory():
    """
    Read inventory data from a text file and store it in a dictionary.

    This function opens the 'inventory.txt' file, reads each line, and processes the data to remove newline characters
    and split values by commas. It stores the data in a dictionary with integer keys representing product IDs.

    Parameters:
    -None

    Returns:
    dict: A dictionary where each key is an integer product ID and the value is a list of product attributes
    It contains the ID of the product as the key and a list containing, name, brand, quantity, price and origin of the product.
    """
    #creating empty dictionary to store whole inventory
    d = {}
    prod_id = 1

    #opening the text file in read mode
    file = open("inventory.txt","r")
    data = file.readlines()

    #formatting the data from text file and adding to dictionary with indexes
    for product in data:
        product = product.replace("\n","").split(",")
        d[prod_id] = product
        prod_id = prod_id+1

    #closing the file
    file.close()
    return d