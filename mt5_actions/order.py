import MetaTrader5 as mt5
import  time
from mt5_global.settings import symbol,Model_type,sl
from mt5_global import settings

point = mt5.symbol_info(symbol).point
lot = 0.1
deviation = 20
order_send_count = 0
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "deviation": deviation,
    "magic": 234000,
    "comment": Model_type,
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_FOK,
    }

def check_order():
    global order_send_count
    dic_order = {
        "sell":False,
        "buy":False,
        "ticket":0,
        "type":mt5.ORDER_TYPE_BUY

    }
    # request the list of all orders
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        for position in positions:
            print(position)
            if position.type == mt5.ORDER_TYPE_BUY:
                dic_order["buy"] = True
                dic_order["ticket"] = position.ticket
                dic_order["type"] = mt5.ORDER_TYPE_BUY
            elif position.type == mt5.ORDER_TYPE_SELL:
                dic_order["sell"] = True,
                dic_order["ticket"] = position.ticket
                dic_order["type"] = mt5.ORDER_TYPE_SELL
    else:
        print("No orders on at all "+symbol)
        return dic_order
    print(positions)
    return dic_order
def close_position(type_to_close):
    tick = mt5.symbol_info_tick(symbol)
    
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        for position in positions:
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "position": position.ticket,
                "symbol": position.symbol,
                "volume": position.volume,
                "type": mt5.ORDER_TYPE_BUY if position.type == 1 else mt5.ORDER_TYPE_SELL,
                "price": tick.ask if position.type == 1 else tick.bid,  
                "deviation": 20,
                "magic": 234000,
                "comment": Model_type,
                "type_time": mt5.ORDER_TIME_GTC,
                "type_filling": mt5.ORDER_FILLING_IOC,
            }
            if position.type == type_to_close:
                # send a trading request
                result = mt5.order_send(request)
                if result.retcode != mt5.TRADE_RETCODE_DONE:
                    print("order_close failed, retcode={}".format(result.retcode))
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
                    print("order_close done, ",result)
                    return True
    else:
        print("No orders on at all ",symbol)
        return False
def buy_order(prediction,symbol):
    #close sell position
    close_position(mt5.ORDER_TYPE_SELL)
    global order_send_count
    price = mt5.symbol_info_tick(symbol).ask
    if not settings.Trade_with_signals:
        tp=mt5.symbol_info_tick(symbol).ask+(prediction-mt5.symbol_info_tick(symbol).ask)
        sl =mt5.symbol_info_tick(symbol).ask-(prediction-mt5.symbol_info_tick(symbol).ask)
    else:
        tp=0.0
        sl = settings.sl
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
    request["price"] = mt5.symbol_info_tick(symbol).ask
    request["sl"] = sl
    request["tp"] = tp

    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if (result.retcode not in  [mt5.TRADE_RETCODE_DONE, mt5.TRADE_RETCODE_PLACED]) :
        if result.retcode == mt5.TRADE_RETCODE_REQUOTE and order_send_count <= 4:
            time.sleep(1)
            order_send_count += 1
            buy_order(prediction, symbol)
        else:
            order_send_count = 0
            print("Order Resend Failed",mt5.last_error())
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
    print("   opened position with POSITION_TICKET={}".format(result.order))




def sell_order(prediction,symbol):
    #close buy position
    close_position(mt5.ORDER_TYPE_BUY)
    global order_send_count
    price = mt5.symbol_info_tick(symbol).bid
    if not settings.Trade_with_signals:
        tp=mt5.symbol_info_tick(symbol).bid-(mt5.symbol_info_tick(symbol).bid-prediction)
        sl =mt5.symbol_info_tick(symbol).bid+(mt5.symbol_info_tick(symbol).bid-prediction)
    else:
        tp=0.0
        sl = settings.sl
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
    request["price"] = mt5.symbol_info_tick(symbol).bid
    request["sl"] = sl
    request["tp"] = tp

    # send a trading request
    result = mt5.order_send(request)
    # check the execution result
    print("1. order_send(): by {} {} lots at {} with deviation={} points".format(symbol,lot,price,deviation));
    if (result.retcode not in  [mt5.TRADE_RETCODE_DONE, mt5.TRADE_RETCODE_PLACED]) :

        if result.retcode == mt5.TRADE_RETCODE_REQUOTE and order_send_count <= 4:
            time.sleep(1)
            order_send_count += 1
            buy_order(prediction, symbol)
        else:
            order_send_count = 0
            print("Order Resend Failed",mt5.last_error())
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
    