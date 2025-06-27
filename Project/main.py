#importing necessary modules
import read
import write
import operations

#Reading inventory file
d = read.read_inventory()

#Main loop of the program
main_loop = True
while main_loop == True:

    #Main Menu
    print("\n\nWelcome to the System.")
    print("What action do you wish to perform?")
    print("1: Product Sales")
    print("2: Product Purchase/Restock")
    print("3: Exit\n")

    #Taking option choice
    action_option = operations.validate_choice("Enter a choice: ",(1,2,3))

    #For selling products
    if action_option == 1:  

        d, cart_dict, billing_info = operations.sales(d)

        if billing_info:
            #Generating Invoice file
            print(write.generate_sell_invoice(d, cart_dict, billing_info, operations.prod_pad))
        print("Exiting to Main menu.")
            
    #For restocking or stocking new products
    elif action_option == 2:

        d, stock_list, restock_info = operations.restock(d)

        #Checking if the user has restocked
        if not restock_info:
            print("No retock process occured.")
        else:
            #Generating restock invoice
            print(write.generate_stock_invoice(d, stock_list, restock_info, operations.prod_pad))
        print("Exiting to Main  menu.")

    #For closing the system    
    elif action_option == 3:
        print("System Closed. Thank you!")
        main_loop = False
