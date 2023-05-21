import tkinter as tk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Transportation Problem Solver")
        self.geometry("400x500")

        self.lblSupply = tk.Label(self, text="Supply:")
        self.lblSupply.pack()

        self.entrySupply = tk.Entry(self)
        self.entrySupply.pack()

        self.lblDemand = tk.Label(self, text="Demand:")
        self.lblDemand.pack()

        self.entryDemand = tk.Entry(self)
        self.entryDemand.pack()

        self.lblUnitPurchaseCost = tk.Label(self, text="Unit Purchase Cost:")
        self.lblUnitPurchaseCost.pack()

        self.entryUnitPurchaseCost = tk.Entry(self)
        self.entryUnitPurchaseCost.pack()

        self.lblUnitSalePrice = tk.Label(self, text="Unit Sale Price:")
        self.lblUnitSalePrice.pack()

        self.entryUnitSalePrice = tk.Entry(self)
        self.entryUnitSalePrice.pack()

        self.lblTransportCost = tk.Label(self, text="Transport Cost:")
        self.lblTransportCost.pack()

        self.entryTransportCost = tk.Entry(self)
        self.entryTransportCost.pack()

        self.btnSolve = tk.Button(self, text="Solve", command=self.solve_transportation_problem)
        self.btnSolve.pack()

        self.resultText = tk.Text(self, height=15, width=40)
        self.resultText.pack()

    def solve_transportation_problem(self):
        supply_str = self.entrySupply.get()
        demand_str = self.entryDemand.get()
        unit_purchase_cost_str = self.entryUnitPurchaseCost.get()
        unit_sale_price_str = self.entryUnitSalePrice.get()
        transport_cost_str = self.entryTransportCost.get()

        supply_list = [int(supply) for supply in supply_str.split(",")]
        demand_list = [int(demand) for demand in demand_str.split(",")]
        unit_purchase_cost_list = [int(cost) for cost in unit_purchase_cost_str.split(",")]
        unit_sale_price_list = [int(price) for price in unit_sale_price_str.split(",")]

        transport_cost_rows = transport_cost_str.split(";")
        transport_cost_list = []
        for row in transport_cost_rows:
            transport_cost_list.append([int(cost) for cost in row.split(",")])

        result_list, total_revenue, total_profit, total_transport_cost, total_purchase_cost, profit = solve(supply_list, demand_list, unit_purchase_cost_list, unit_sale_price_list, transport_cost_list)

        self.resultText.delete("1.0", tk.END)
        self.resultText.insert(tk.END, "Total revenue: {}\n".format(total_revenue))
        self.resultText.insert(tk.END, "Total profit: {}\n".format(total_profit))
        self.resultText.insert(tk.END, "Total transport cost: {}\n".format(total_transport_cost))
        self.resultText.insert(tk.END, "Total purchase cost: {}\n".format(total_purchase_cost))
        self.resultText.insert(tk.END, "Profit:\n")
        for row in profit:
            self.resultText.insert(tk.END, "{}\n".format(row))
        self.resultText.insert(tk.END, "Solution:\n")
        # Add the solved transportation problem details to the resultText
        for row in result_list:
            self.resultText.insert(tk.END, "{}\n".format(row))

    def run(self):
        self.mainloop()

class SolutionRecord:
    def __init__(self):
        self.k = None
        self.l = None
        self.supply = []
        self.demand = []
        self.result = []


def deep_copy(original):
    if original is None:
        return None

    result = []
    for row in original:
        result.append(row[:])

    return result


def find_largest_element(matrix, supply, demand, result, solution_records):
    largest_element = float("-inf")
    k = -1
    l = -1
    for i in range(len(matrix)):
        if supply[i] > 0:
            for j in range(len(matrix[i])):
                if demand[j] > 0:
                    current_value = matrix[i][j]
                    if current_value > largest_element and supply[i] > 0 and demand[j] > 0:
                        k = i
                        l = j
                        largest_element = current_value

    if supply[k] > demand[l]:
        result[k][l] += demand[l]
        supply[k] -= demand[l]
        demand[l] = 0
    elif supply[k] < demand[l]:
        result[k][l] += supply[k]
        demand[l] -= supply[k]
        supply[k] = 0
    elif supply[k] == demand[l]:
        result[k][l] += supply[k]
        supply[k] = 0
        demand[l] = 0

    record = SolutionRecord()
    record.k = k
    record.l = l
    record.supply = supply.copy()
    record.demand = demand.copy()
    record.result = deep_copy(result)
    solution_records.append(record)

    return largest_element


def calculate_total_profit(buy_cost, sell_cost, transport_cost_list, result_list):
    total_profit = 0
    for i in range(len(result_list) and len(buy_cost)):
        for j in range(len(result_list[i]) and len(sell_cost)):
            profit_value = sell_cost[j] - buy_cost[i] - transport_cost_list[i][j]
            total_profit += profit_value * result_list[i][j]
    return total_profit


def calculate_total_transport_cost(transport_cost_list, result_list):
    total_transport_cost = 0
    for i in range(len(result_list) and len(transport_cost_list)):
        for j in range(len(result_list[i]) and len(transport_cost_list[i])):
            total_transport_cost += transport_cost_list[i][j] * result_list[i][j]
    return total_transport_cost


def calculate_total_purchase_cost(buy_cost, result_list):
    total_purchase_cost = 0
    for i in range(len(result_list) and len(buy_cost)):
        for j in range(len(result_list[i])):
            total_purchase_cost += buy_cost[i] * result_list[i][j]
    return total_purchase_cost


def calculate_total_revenue(sell_cost, result_list):
    total_revenue = 0
    for i in range(len(result_list)):
        for j in range(len(result_list[i]) and len(sell_cost)):
            total_revenue += sell_cost[j] * result_list[i][j]
    return total_revenue


def solve(supply_list, demand_list, buy_cost, sell_cost, transport_cost_list):
    solution_records = []

    not_balanced = sum(supply_list) != sum(demand_list)
    profit = []
    for i in range(len(supply_list)):
        row = []
        for j in range(len(demand_list)):
            profit_value = sell_cost[j] - buy_cost[i] - transport_cost_list[i][j]
            row.append(profit_value)
        profit.append(row)

    if not_balanced:
        result = [[0] * (len(transport_cost_list[0]) + 1) for _ in range(len(transport_cost_list) + 1)]

        for row in profit:
            row.append(0)
        profit.append([0] * (len(demand_list) + 1))
        supply_list.append(sum(demand_list))
        demand_list.append(sum(supply_list) - supply_list[-1])
    else:
        result = [[0] * len(transport_cost_list[0]) for _ in range(len(transport_cost_list))]

    while sum(supply_list) != 0 and sum(demand_list) != 0:
        find_largest_element(profit, supply_list, demand_list, result, solution_records)

    result_list = result
    total_profit = calculate_total_profit(buy_cost, sell_cost, transport_cost_list, result_list)
    total_transport_cost = calculate_total_transport_cost(transport_cost_list, result_list)
    total_purchase_cost = calculate_total_purchase_cost(buy_cost, result_list)
    total_revenue = calculate_total_revenue(sell_cost, result_list)

    return result_list, total_revenue, total_profit, total_transport_cost, total_purchase_cost, profit

if __name__ == "__main__":
    app = Application()
    app.run()


