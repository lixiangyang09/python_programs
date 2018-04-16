#!/usr/bin/env python
# encoding=utf8


# base_commercial_rate = 0.049
# base_reserve_fund_rate = 0.0325
#
# commercial_total = 880000
# reserve_fund_total = 1200000
#
# total_month = 300

import codecs


def cal_total_rate(total_month, base_rate, discount):
    adjusted_rate = base_rate * (1 - discount) / 12.0
    rate_n = pow(1 + adjusted_rate, total_month)
    total_rate = (rate_n - 1) / (adjusted_rate * rate_n)
    return total_rate


def cal_interest_rate(total_month, base_rate, discount):
    adjusted_rate = base_rate * (1 - discount) / 12.0
    a = 1 - pow(1 + adjusted_rate, total_month)
    b = adjusted_rate
    return a / b


def calculate_monthly_mortgage(total_mortgage, total_month, base_rate, discount):
    # monthly_rate = 1 + base_rate * (1 - discount) / 12.0
    # total_rate = [1.0 / monthly_rate]
    # current_rate = monthly_rate
    # for i in range(1, total_month):
    #     current_rate *= monthly_rate
    #     total_rate.append(total_rate[i - 1] + 1.0 / current_rate)
    # res = total_mortage / total_rate[-1]
    adjusted_rate = base_rate * (1 - discount) / 12.0
    rate_n = pow(1 + adjusted_rate, total_month)
    total_rate = (rate_n - 1) / (adjusted_rate * rate_n)
    return total_mortgage / total_rate


def calculate_monthly_detail(monthly_paid, total_mortage, interest_rate, discount):
    final_monthly_rate = interest_rate * (1 - discount) / 12.0
    current_month_interest = total_mortage * final_monthly_rate
    paid_capital = monthly_paid - current_month_interest
    return paid_capital, current_month_interest


class Loaner:
    def __init__(self, monthly_paid, total_month, total_capital, interest_rate, discount):
        if abs(monthly_paid) < 1e-6:
            self.monthly_paid = calculate_monthly_mortgage(total_capital, total_month, interest_rate, discount)
        else:
            self.monthly_paid = monthly_paid
        self.total_month = total_month
        self.total_capital = total_capital
        self.interest_rate = interest_rate
        self.discount = discount

        self.remain_capital = total_capital
        self.remain_interest = 0
        self.already_paid_capital = 0
        self.already_paid_interest = 0
        self.ind = 0

    def get_next(self, monthly_paid=0):
        if abs(monthly_paid) > 1e-6:
            self.monthly_paid = monthly_paid
        self.ind += 1
        if self.ind > self.total_month:
            print("Exceed max month count.")
            return None
        final_monthly_rate = self.interest_rate * (1 - self.discount) / 12.0
        current_paid_interest = self.remain_capital * final_monthly_rate
        current_paid_capital = self.monthly_paid - current_paid_interest
        self.already_paid_interest += current_paid_interest
        self.already_paid_capital += current_paid_capital

        self.remain_capital -= current_paid_capital

        future_money_index = cal_interest_rate(self.total_month - self.ind, self.interest_rate, self.discount)
        self.remain_interest = future_money_index * self.monthly_paid - self.remain_capital

        return [self.ind, self.monthly_paid, current_paid_capital, current_paid_interest,
                self.already_paid_capital, self.already_paid_interest,
                self.remain_capital, self.remain_interest]


def generate_report(loaner, result_file):
    res = 'index, monthly paid, capital paid, interest paid, capital already paid, ' \
          'interest already paid, capital remaining, interest remaining\n'
    while True:
        monthly_detail = loaner.get_next()
        if not monthly_detail:
            break
        ff = "{:>.2f}"
        for v in monthly_detail[:-1]:
            res += ff.format(v)
            res += ','
        res += '\n'

    with codecs.open(result_file, 'w', 'utf_8_sig') as f:
        f.write(res)


if __name__ == '__main__':
    total_commercial_mortgage = 880000
    total_fund_mortgage = 1200000
    base_rate_commercial = 0.049
    base_rage_fund = 0.0325
    monthly_paid_fund = 4921
    total_months = 300

    commercial_loaner = Loaner(0, total_months, total_commercial_mortgage, base_rate_commercial, -0.05)
    fund_loaner = Loaner(4921, total_months, total_fund_mortgage, base_rage_fund, 0)
    generate_report(commercial_loaner, "commercial_report.csv")
    generate_report(fund_loaner, "fund_report.csv")

