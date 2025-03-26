import socket

def read_menu():
    menoo = {}
    try:
        with open("menu.txt", "r") as file:
            for line in file:
                item, stock = line.strip().split(",")
                menoo[item] = int(stock)
    except:
        print("Erorr: Could not read menu")
        exit(1)
    return menoo

def write_menu(menuu):
    with open("menu.txt", "w") as file:
        for item, stock in menuu.items():
            file.write(f"{item},{stock}\n")

def handle_client(data, addr, serv_sock, menuu, client_ordrs):
    req = data.decode()
    if req.startswith("Connect:"):
        custmr = req.split(":")[1]
        reply = f"Hi, {custmr}! Type 'Order' to place an order or 'Cancel' to modify your order."
        serv_sock.sendto(reply.encode(), addr)
        return custmr
    elif req == "Order":
        reply = "List the items you wanna order, separated by commas."
        serv_sock.sendto(reply.encode(), addr)
    elif req == "Cancel":
        reply = "List the items you wanna cancel, separated by commas."
        serv_sock.sendto(reply.encode(), addr)
    elif req == "Exit":
        reply = "Exit"
        serv_sock.sendto(reply.encode(), addr)
        return None
    elif "," in req:
        if addr not in client_ordrs:
            client_ordrs[addr] = []
        if "Order" in client_ordrs[addr]:
            items = [itm.strip() for itm in req.split(",")]
            success_ordrs = []
            unavailable_itms = []
            for itm in items:
                if itm in menuu and menuu[itm] > 0:
                    success_ordrs.append(itm)
                    menuu[itm] -= 1
                    client_ordrs[addr].append(itm)
                else:
                    unavailable_itms.append(itm)
            rite_menu(menuu)
            reply = f"Ordered: {', '.join(success_ordrs)} | Unavailable: {', '.join(unavailable_itms)}"
            serv_sock.sendto(reply.encode(), addr)
        elif "Cancel" in client_ordrs[addr]:
            items = [itm.strip() for itm in req.split(",")]
            canceled_itms = []
            not_found_itms = []
            for itm in items:
                if itm in client_ordrs[addr]:
                    canceled_itms.append(itm)
                    menuu[itm] += 1
                    client_ordrs[addr].remove(itm)
                else:
                    not_found_itms.append(itm)
            write_menu(menuu)
            reply = f"Canceled: {', '.join(canceled_itms)} | Not Found: {', '.join(not_found_itms)}"
            serv_sock.sendto(reply.encode(), addr)
    else:
        reply = "Invalid input. Use 'Order', 'Cancel', or 'Exit'."
        serv_sock.sendto(reply.encode(), addr)

def start_servr():
    menuu = read_menu()
    client_ordrs = {}
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv_sock.bind(("localhost", 1234))
    while True:
        data, client_addr = serv_sock.recvfrom(1024)
        handle_client(data, client_addr, serv_sock, menuu, client_ordrs)

if __name__ == "__main__":
    start_servr()