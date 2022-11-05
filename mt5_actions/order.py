import MetaTrader5 as mt5
import  time
from mt5_global.settings import symbol,Model_type


lot = 0.1
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "deviation": deviation,
    "magic": 234000,
    "comment": Model_type,
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
    }

def check_order():
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error())
        quit()
    dic_order = {
        "sell":False,
        "buy":False
    }
    # request the list of all orders
    positions = mt5.positions_get(symbol="EURUSD")
    print(positions,"orders")
    if positions:
        for position in positions:
            print(position)
            if position.type == mt5.ORDER_TYPE_BUY:
                dic_order["buy"] = True
                return dic_order
            elif position.type == mt5.ORDER_TYPE_SELL:
                dic_order["sell"] = True
                return dic_order
    else:
        print("No orders on at all "+symbol)
        return dic_order
def buy_order(prediction,symbol):
    price = mt5.symbol_info_tick(symbol).ask
    sl =price-(prediction-price)
    tp = price+(prediction-price)
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        mt5.shutdown()
        quit()
 
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            mt5.shutdown()
            quit()
    
    # define request parameters
    request["type"] = mt5.ORDER_TYPE_BUY
    request["price"] = price
    request["sl"] = sl
    request["tp"] = tp

    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
    print("2. order_send done, ", result)
    print("3. opened position with POSITION_TICKET={}".format(result.order))


def sell_order(prediction,symbol):

    price = mt5.symbol_info_tick(symbol).bid
    sl =price+(price-prediction)
    tp = price-(price-prediction)
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(symbol, "not found, can not call order_check()")
        
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
        print(symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(symbol,True):
            print("symbol_select({}}) failed, exit",symbol)
            
    
    # define request parameters
    request["type"] = mt5.ORDER_TYPE_SELL
    request["price"] = price
    request["sl"] = sl
    request["tp"] = tp


    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("2. order_send failed, retcode={}".format(result))
        # request the result as a dictionary and display it element by element
        result_dict=result._asdict()
        for field in result_dict.keys():
            print("   {}={}".format(field,result_dict[field]))
            # if this is a trading request structure, display it element by element as well
            if field=="request":
                traderequest_dict=result_dict[field]._asdict()
                for tradereq_filed in traderequest_dict:
                    print("       traderequest: {}={}".format(tradereq_filed,traderequest_dict[tradereq_filed]))
                    
    else:
        print("2. order_send done, ", result)
        print("3. opened position with POSITION_TICKET={}".format(result.order))