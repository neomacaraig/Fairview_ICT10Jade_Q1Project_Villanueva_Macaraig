from pyscript import document, display

# keep track of items in a list
my_cart = []

def add_to_order(e):
    global my_cart
    
    # get selected drink name and price from dropdown selector
    coffee_dropdown = document.getElementById("coffee")
    selected_index = coffee_dropdown.selectedIndex
    drink_option = coffee_dropdown.options.item(selected_index)
    
    drink_name = drink_option.text.split(" - ")[0]
    drink_price = float(coffee_dropdown.value)
    
    # get price of size
    size_price = 0.0
    size_name = "Tall"
    
    if document.getElementById("grande").checked:
        size_price = float(document.getElementById("grande").value)
        size_name = "Grande"
    elif document.getElementById("venti").checked:
        size_price = float(document.getElementById("venti").value)
        size_name = "Venti"
        
    # drink quantity
    try:
        qty = int(document.getElementById("quantity").value)
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1
        
    # calculate item total
    item_total = (drink_price + size_price) * qty
    
    # add to cart 
    my_cart.append({
        "name": drink_name,
        "size": size_name,
        "qty": qty,
        "total": item_total
    })
    
    display_receipt()

def remove_last_item(e):
    global my_cart
    if my_cart:
        my_cart.pop()  # Removes the last added item from the cart
    display_receipt()

def clear_order(e):
    global my_cart
    my_cart = []
    document.getElementById("show").innerHTML = "Your cart is empty."

def display_receipt():
    if len(my_cart) == 0:
        document.getElementById("show").innerHTML = "Your cart is empty."
        return
        
    receipt_text = ""
    subtotal = 0.0
    
    # receipt and calculate subtotal
    for item in my_cart:
        receipt_text += f"{item['qty']}x {item['name']} ({item['size']}) - ₱{item['total']:.2f}\n"
        subtotal += item['total']
        
    # calculate subtotal, vat (12%), and total amount
    vat = subtotal * 0.12
    total_amount = subtotal + vat
    
    # add the calculations' results to the receipt text
    receipt_text += f"\n--------------------\n"
    receipt_text += f"Subtotal: ₱{subtotal:.2f}\n"
    receipt_text += f"VAT (12%): ₱{vat:.2f}\n"
    receipt_text += f"Total Amount: ₱{total_amount:.2f}"
    
    document.getElementById("show").innerHTML = receipt_text

def checkout(e):
    global my_cart
    if len(my_cart) == 0:
        document.getElementById("show").innerHTML = "Cart is empty! Add items first."
        return
        
    # calculate subtotal, vat, and total amount for the checkout receipt
    subtotal = sum(item['total'] for item in my_cart)
    vat = subtotal * 0.12
    total_amount = subtotal + vat
    
    receipt_summary = "==============================\n"
    receipt_summary += "       Official Receipt       \n"
    receipt_summary += "==============================\n\n"
    receipt_summary += "Status: Paid (Successful)\n"
    receipt_summary += "------------------------------\n"
    
    for item in my_cart:
        receipt_summary += f"{item['qty']}x {item['name']} ({item['size']})\n"
        receipt_summary += f"   Item Total: ₱{item['total']:.2f}\n"
        
    receipt_summary += "------------------------------\n"
    receipt_summary += f"Subtotal    : ₱{subtotal:.2f}\n"
    receipt_summary += f"VAT (12%)   : ₱{vat:.2f}\n"
    receipt_summary += f"Total paid  : ₱{total_amount:.2f}\n"
    receipt_summary += "==============================\n"
    receipt_summary += "   Thank you for your order!  \n"
    receipt_summary += "     Have a nice day!         \n"
    receipt_summary += "=============================="
    
    # display the receipt and clear the cart
    document.getElementById("show").innerHTML = receipt_summary
    my_cart = []