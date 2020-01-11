# -*- coding:utf-8 -*-

from datetime import datetime, timedelta
from decimal import Decimal
from flask_restful import reqparse
from flask_restful import Resource
import json

import db


class AbchinaRmbGoldInterest(Resource):
    def get(self):
        session = db.DBSession()
        try:
            buy_order = session.query(db.BuyBankOrder).first()
            bank_info_list = session.query(db.BankInfo).all()

            result_data_list = []
            last_show_time = datetime.strptime('2000-01-01', '%Y-%m-%d')
            for bank_info in bank_info_list:
                rmb_gold_update_beijing_time = bank_info.rmb_gold_update_beijing_time
                # 展示间隔时间12小时
                if rmb_gold_update_beijing_time - last_show_time >= timedelta(hours=12):
                    last_show_time = rmb_gold_update_beijing_time
                    time = rmb_gold_update_beijing_time.strftime('%Y-%m-%d %H:%M')

                    hold_days = Decimal((rmb_gold_update_beijing_time - buy_order.time).days)
                    # 年化利率 = （卖出价格 - 买入价格） / 买入价格 / （持有天数 / 365天）
                    annual_interest_rate = str((bank_info.rmb_gold_customer_sell - buy_order.price) / buy_order.price /
                                               (hold_days / 365))

                    buy_time_str = buy_order.time.strftime('%Y-%m-%d')
                    sell_time_str = buy_order.sell_bank_order.time.strftime('%Y-%m-%d')
                    annual_interest_rate_key = buy_time_str + '--' + sell_time_str
                    result_data_list.append({
                        'time': time,
                        annual_interest_rate_key: annual_interest_rate,
                    })

            return result_data_list
        finally:
            session.close()


class FundInterest(Resource):

    parser_fund = reqparse.RequestParser()
    parser_fund.add_argument('fund_name', type=str, required=True, help='fund_name cannot be blank! For example: yhfund')
    parser_fund.add_argument('fund_code', type=str, required=True, help='fund_code cannot be blank! For example: 000286')

    def get(self):
        fund_query_argument = FundInterest.parser_fund.parse_args()

        session = db.DBSession()
        try:
            buy_fund_order_list = session.query(db.BuyFundOrder).filter_by(fund_name=fund_query_argument['fund_name'])\
                .filter_by(fund_code=fund_query_argument['fund_code']).order_by(db.BuyFundOrder.time).all()
            fund_info_list = session.query(db.FundInfo).filter_by(fund_name=fund_query_argument['fund_name'])\
                .filter_by(fund_code=fund_query_argument['fund_code'])\
                .filter(db.FundInfo.time > buy_fund_order_list[0].time).all()

            result_data_list = []
            for fund_info in fund_info_list:
                this_day_result = {'time': fund_info.time.strftime('%Y-%m-%d')}
                for buy_fund_order in buy_fund_order_list:
                    if buy_fund_order.time >= fund_info.time:
                        continue
                    spread_money = buy_fund_order.quantity * (fund_info.LJJZ - buy_fund_order.LJJZ)

                    hold_days = (fund_info.time - buy_fund_order.time).days

                    redemption_rate = Decimal(0)
                    redemption_rule_list = json.loads(buy_fund_order.redemption_rule)
                    for redemption_rule in redemption_rule_list:
                        redemption_rule_section = list(redemption_rule.values())[0]
                        if redemption_rule_section['start'] <= hold_days < redemption_rule_section['end']:
                            redemption_rate = Decimal(list(redemption_rule.keys())[0])
                            break
                    sell_value = buy_fund_order.quantity * fund_info.IOPV
                    redemption_money = sell_value * redemption_rate
                    hold_days_decimal = Decimal(hold_days)

                    # 年化利率 = 差价 / 买入价格 / （持有天数 / 365天）
                    # 差价 = 买入份数 * （累计净值卖出 - 累计净值买入） - 买入手续费 - 赎回手续费
                    # 赎回手续费 = 当前价值 * 赎回费率 / （赎回费率 + 1）
                    # 赎回手续费 = 当前价值 * 赎回费率 ！！！ 招商银行使用这种方式计算得到赎回手续费而不是上一行的方式
                    # 当前价值 = 买入份数 * 单位净值
                    # 赎回费率 = X（持有天数）
                    annual_interest_rate = str((spread_money - buy_fund_order.charge - redemption_money) /
                                               buy_fund_order.total_money / (hold_days_decimal / 365))
                    buy_fund_time_str = buy_fund_order.time.strftime('%Y-%m-%d')
                    this_day_result[buy_fund_time_str + "买入"] = annual_interest_rate

                result_data_list.append(this_day_result)

            return result_data_list
        finally:
            session.close()
