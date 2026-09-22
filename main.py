from pyscript import document

# keep track of items in a list
my_cart = []

def add_to_order(e):
    global my_cart
    
    coffee_dropdown = document.getElementById("coffee")
    if not coffee_dropdown:
        return

    selected_index = coffee_dropdown.selectedIndex
    drink_option = coffee_dropdown.options.item(selected_index)
    
    drink_name = drink_option.text.split(" - ")[0]
    drink_price = float(coffee_dropdown.value)
    
    size_price = 0.0
    size_name = "Tall"
    
    grande_el = document.getElementById("grande")
    venti_el = document.getElementById("venti")
    
    if grande_el and grande_el.checked:
        size_price = float(grande_el.value)
        size_name = "Grande"
    elif venti_el and venti_el.checked:
        size_price = float(venti_el.value)
        size_name = "Venti"
        
    try:
        qty_el = document.getElementById("quantity")
        qty = int(qty_el.value) if qty_el else 1
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1
        
    item_total = (drink_price + size_price) * qty
    
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
        my_cart.pop()
    display_receipt()

def clear_order(e):
    global my_cart
    my_cart = []
    show_el = document.getElementById("show")
    if show_el:
        show_el.innerHTML = "Your cart is empty."

def display_receipt():
    show_el = document.getElementById("show")
    if not show_el:
        return

    if len(my_cart) == 0:
        show_el.innerHTML = "Your cart is empty."
        return
        
    receipt_text = ""
    subtotal = 0.0
    
    for item in my_cart:
        receipt_text += f"{item['qty']}x {item['name']} ({item['size']}) - ₱{item['total']:.2f}\n"
        subtotal += item['total']
        
    vat = subtotal * 0.12
    total_amount = subtotal + vat
    
    receipt_text += f"\n--------------------\n"
    receipt_text += f"Subtotal: ₱{subtotal:.2f}\n"
    receipt_text += f"VAT (12%): ₱{vat:.2f}\n"
    receipt_text += f"Total Amount: ₱{total_amount:.2f}"
    
    show_el.innerHTML = receipt_text

def checkout(e):
    global my_cart
    show_el = document.getElementById("show")
    if not show_el:
        return

    if len(my_cart) == 0:
        show_el.innerHTML = "Cart is empty! Add items first."
        return
        
    subtotal = sum(item['total'] for item in my_cart)
    vat = subtotal * 0.12
    total_amount = subtotal + vat
    
    receipt_summary = "==============================\n"
    receipt_summary += "         Official Receipt       \n"
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
    
    show_el.innerHTML = receipt_summary
    my_cart = []

def generate_sku(e):
    show_el = document.getElementById('show')
    cat_el = document.getElementById('category_id')
    prod_el = document.getElementById('prod_name_id')
    stock_el = document.getElementById('stock_qty_id')

    if not show_el or not cat_el or not prod_el or not stock_el:
        return

    category_variable = cat_el.value.strip()
    product_name_variable = prod_el.value.strip()
    stock_qty = stock_el.value.strip()

    if not product_name_variable:
        show_el.innerHTML = "Missing Product Name"
        return

    sku_code = f"{category_variable[:3].upper()}-{product_name_variable[:4].upper()}-{stock_qty}"
    show_el.innerHTML = f"SKU: {sku_code}"
