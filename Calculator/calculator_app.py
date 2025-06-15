import tkinter as tk

def get_precedence(operation):
    precedence = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "**": 3,
    }
    return precedence.get(operation,0)


def calculater(calculation):

    if len(calculation.split()) < 3:
        return "Invalid input"

    if calculation.endswith("=") :
        calculation = calculation[:-1].strip()


    calculation_list = calculation.split(" ")

    number_list = []
    operation_list = []


    for token in calculation_list:
        

        if token.isdigit():
            number_list.append(token)
        elif token == "(":
            operation_list.append(token)
        elif token == ")":
            while operation_list and operation_list[-1] != "(":
                number_list.append(operation_list.pop())

            operation_list.pop()

        else:
            while operation_list and get_precedence(operation_list[-1]) >= get_precedence(token):
                number_list.append(operation_list.pop())

            operation_list.append(token)


    while operation_list:
        number_list.append(operation_list.pop())
    
    postfix = " ".join(number_list)


    stack = []
    for item in postfix.split():
        if item.isdigit():
            stack.append(int(item))
        else:
            b = stack.pop()
            a = stack.pop()

            if item == "+":
                stack.append(a + b)
            elif item == "-":
                stack.append(a - b)
            elif item == "*":
                stack.append(a * b)
            elif item == "/":
                try: 
                    stack.append(a / b)
                except ZeroDivisionError:
                    return "Can not devide by zero"
                    
            elif item == "^":
                stack.append(pow(a, b))

    return stack.pop()
    




def press(key):
    if key == "C":
        input_var.set("")
        result_var.set("")
    elif key == "=":
        try:
            calculation = input_var.get()
            result = calculater(calculation)
            result_var.set(str(result))
        except Exception as e:
            result_var.set("Error")
    else:
        operations = ["+", "-", "*", "/", "^", "(", ")"]
        if key in operations:
            key = f" {key} "
        input_var.set(input_var.get() + key)


root = tk.Tk()
root.title("Calculater")
root.configure(bg="black")
root.geometry("320x470") 



input_var = tk.StringVar()
result_var = tk.StringVar()

input_label = tk.Label(root, textvariable=input_var, fg="white", bg="black", font=("Arial", 22), anchor="e")
input_label.pack(fill="both", padx=10, pady=5)

result_label = tk.Label(root, textvariable=result_var, fg="gray", bg="black", font=("Arial", 20), anchor="e")
result_label.pack(fill="both", padx=10, pady=5)

buttons = [
    ["C", "^", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", "=", "(", ")"]
]


for row in buttons:
    frame = tk.Frame(root, bg="black")
    frame.pack(expand=True, fill="both")

    for btn in row:
        color = "#ff8833" if btn in ["C", "^", "/", "*", "-", "+", "="] else "#3366cc"
        tk.Button(
            frame,
            text=btn,
            bg=color,
            fg="white",
            font=("Arial", 18),
            relief="ridge",   
            bd=3,               
            command=lambda b=btn: press(b)
        ).pack(side="left", expand=True, fill="both", padx=3, pady=3)

root.mainloop()
