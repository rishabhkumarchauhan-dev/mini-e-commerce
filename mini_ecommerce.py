products = []
cart = {}

def load_products():
    global products
    products = []
    try:
        f = open("products.txt", "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            line = line.strip()
            if line != "":
                parts = line.split(",")
                if len(parts) == 4:
                    d = {}
                    d["id"] = parts[0]
                    d["name"] = parts[1]
                    d["price"] = int(parts[2])
                    d["stock"] = int(parts[3])
                    products.append(d)
    except:
        products = []

def save_products():
    f = open("products.txt", "w")
    for p in products:
        f.write(p["id"] + "," + p["name"] + "," + str(p["price"]) + "," + str(p["stock"]) + "\n")
    f.close()

def get_next_id():
    if len(products) == 0:
        return "P101"
    maxn = 100
    for p in products:
        num = int(p["id"][1:])
        if num > maxn:
            maxn = num
    return "P" + str(maxn + 1)

def add_product():
    name = input("Enter product name: ")
    price_str = input("Enter price: ")
    stock_str = input("Enter stock: ")
    try:
        price = int(price_str)
        stock = int(stock_str)
        if price <= 0:
            print("Invalid price. Price must be a positive number.")
            return
        pid = get_next_id()
        d = {}
        d["id"] = pid
        d["name"] = name
        d["price"] = price
        d["stock"] = stock
        products.append(d)
        save_products()
        print("Product added. ID: " + pid + " | " + name + " | Price: " + str(price) + " | Stock: " + str(stock))
        if stock == 0:
            print("Warning: " + name + " is out of stock.")
    except:
        print("Invalid input.")

def update_product():
    if len(products) == 0:
        print("No products available.")
        return
    pid = input("Enter product ID to update: ")
    found = False
    for p in products:
        if p["id"] == pid:
            found = True
            print("Current: " + p["name"] + " Price: " + str(p["price"]) + " Stock: " + str(p["stock"]))
            name = input("Enter new name (or press enter to keep): ")
            price_str = input("Enter new price (or press enter to keep): ")
            stock_str = input("Enter new stock (or press enter to keep): ")
            if name != "":
                p["name"] = name
            if price_str != "":
                try:
                    price = int(price_str)
                    if price <= 0:
                        print("Invalid price. Price must be a positive number.")
                        return
                    p["price"] = price
                except:
                    print("Invalid price.")
                    return
            if stock_str != "":
                try:
                    stock = int(stock_str)
                    p["stock"] = stock
                except:
                    print("Invalid stock.")
                    return
            save_products()
            print("Product updated.")
            break
    if found == False:
        print("Product " + pid + " not found.")

def delete_product():
    if len(products) == 0:
        print("No products available.")
        return
    pid = input("Enter product ID to delete: ")
    found = False
    name = ""
    for i in range(len(products)):
        if products[i]["id"] == pid:
            found = True
            name = products[i]["name"]
            del products[i]
            break
    if found:
        save_products()
        print("Product '" + name + "' deleted. Products left: " + str(len(products)))
    else:
        print("Product " + pid + " not found.")

def view_products():
    if len(products) == 0:
        print("No products available.")
        return
    print("ID | Name | Price | Stock")
    for p in products:
        print(p["id"] + " | " + p["name"] + " | " + str(p["price"]) + " | " + str(p["stock"]))

def add_to_cart():
    if len(products) == 0:
        print("No products available.")
        return
    pid = input("Enter product ID: ")
    qty_str = input("Enter quantity: ")
    try:
        qty = int(qty_str)
        if qty <= 0:
            print("Quantity must be positive.")
            return
        found = False
        for p in products:
            if p["id"] == pid:
                found = True
                if qty > p["stock"]:
                    print("Not enough stock. Available: " + str(p["stock"]))
                    return
                if pid in cart:
                    cart[pid] = cart[pid] + qty
                else:
                    cart[pid] = qty
                amount = p["price"] * qty
                print(p["name"] + " x" + str(qty) + " added | Amount: " + str(amount))
                break
        if found == False:
            print("Product " + pid + " not found.")
    except:
        print("Invalid quantity.")

def view_cart():
    if len(cart) == 0:
        print("Cart is empty.")
        return
    print("Cart:")
    total = 0
    for pid in cart:
        for p in products:
            if p["id"] == pid:
                amt = p["price"] * cart[pid]
                total = total + amt
                print(p["name"] + " x" + str(cart[pid]) + " | " + str(amt))
    print("Total: " + str(total))

def checkout():
    if len(cart) == 0:
        print("Cart is empty.")
        return
    total = 0
    stock_msgs = []
    for pid in cart:
        for p in products:
            if p["id"] == pid:
                qty = cart[pid]
                if qty > p["stock"]:
                    print("Not enough stock for " + p["name"])
                    return
                amt = p["price"] * qty
                total = total + amt
                p["stock"] = p["stock"] - qty
                stock_msgs.append(p["name"] + " stock left: " + str(p["stock"]))
    save_products()
    msg = "Order total: " + str(total)
    for s in stock_msgs:
        msg = msg + " | " + s
    print(msg)
    cart.clear()

def main():
    load_products()
    while True:
        print()
        print("===== Mini E-Commerce System =====")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. View Products")
        print("5. Add to Cart")
        print("6. View Cart")
        print("7. Checkout")
        print("8. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            add_product()
        elif choice == "2":
            update_product()
        elif choice == "3":
            delete_product()
        elif choice == "4":
            view_products()
        elif choice == "5":
            add_to_cart()
        elif choice == "6":
            view_cart()
        elif choice == "7":
            checkout()
        elif choice == "8":
            print("Thank you!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
