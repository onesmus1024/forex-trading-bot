import MetaTrader5 as mt5
import math
import  time
from mt5_global.settings import symbol,Model_type,sl
from mt5_global import settings

point = mt5.symbol_info(symbol).point
tp =0.0
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
                    raise Exception("order_close failed, retcode={}".format(result.retcode))
                else:
                    print("order_close done, ",result)
    else:
        print("No orders on at all ",symbol)
        return False
def buy_order(prediction,symbol):
    #close sell position
    #close_position(mt5.ORDER_TYPE_SELL)
    global order_send_count,tp
    price = mt5.symbol_info_tick(symbol).ask
    if not settings.Trade_with_signals:
        sl =mt5.symbol_info_tick(symbol).ask-(prediction-mt5.symbol_info_tick(symbol).ask)
    else:
       
        sl = settings.sl
    symbol_info = mt5.symbol_info(symbol)
        
    if symbol_info is None:
        raise Exception("symbol_info({}}) failed, exit",symbol)
        return 
    
    # if the symbol is unavailable in MarketWatch, add it
    if not symbol_info.visible:
         print(symbol, "is not visible, trying to switch on")
         if not mt5.symbol_select(symbol,True):
                raise Exception("symbol_select({}}) failed, exit",symbol)
                return
    # define request parameters
    request["type"] = mt5.ORDER_TYPE_BUY
    request["price"] = mt5.symbol_info_tick(symbol).ask
    request["sl"] = sl
 

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
            raise Exception("order_send failed, retcode={}".format(result.retcode))
        raise Exception("order_send failed, retcode={}".format(result.retcode))     
    
    print("2. order_send done, ", result)
    print("   opened position with POSITION_TICKET={}".format(result.order))




def sell_order(prediction,symbol):
    #close buy position
    #close_position(mt5.ORDER_TYPE_BUY)

    global order_send_count,tp
    price = mt5.symbol_info_tick(symbol).bid
    if not settings.Trade_with_signals:
        sl =mt5.symbol_info_tick(symbol).bid+(mt5.symbol_info_tick(symbol).bid-prediction)
    else:
        
        sl = settings.sl
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise Exception("symbol_info({}}) failed, exit",symbol)
        return
    if not symbol_info.visible:
        raise Exception("symbol_info({}}) failed, exit",symbol)
        return
    # define request parameters
    request["type"] = mt5.ORDER_TYPE_SELL
    request["price"] = mt5.symbol_info_tick(symbol).bid
    request["sl"] = sl
    

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
            raise Exception("order_send failed, retcode={}".format(result.retcode))
        raise Exception("order_send failed, retcode={}".format(result.retcode))
       
    else:
        print("2. order_send done, ", result)
        print("3. opened position with POSITION_TICKET={}".format(result.order))
    

def change_tp_sl():
    time.sleep(1)
    positions = mt5.positions_get(symbol=symbol)
    if positions:
        levels = 50  # 10 pips
        for position in positions:
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "position": position.ticket,
                "symbol": position.symbol,
            }
            if position.profit > 0:
                if position.type == mt5.ORDER_TYPE_BUY:
                    if not position.sl:
                        if (mt5.symbol_info_tick(symbol).ask-position.price_open) >= levels*point:
                            request['sl'] = position.price_open
                            mt5.order_send(request)
                    else:
                        if position.sl<position.price_open:
                            if (mt5.symbol_info_tick(symbol).ask-position.price_open) >= levels*point:
                                request['sl'] = position.price_open+(levels*point)*0.75
                                mt5.order_send(request)
                        elif (mt5.symbol_info_tick(symbol).ask-position.sl) >= levels*point:
                            request['sl'] = position.sl+(levels*point)*0.75
                            mt5.order_send(request)

                else:
                    if not position.sl:
                        if (position.price_open-mt5.symbol_info_tick(symbol).bid) >= levels*point:
                            request['sl'] = position.price_open
                            mt5.order_send(request)
                    else:
                        if position.sl>position.price_open:
                            if (position.price_open-mt5.symbol_info_tick(symbol).bid) >= levels*point:
                                request['sl'] = position.price_open-(levels*point)*0.75
                                mt5.order_send(request)
                        elif (position.sl-mt5.symbol_info_tick(symbol).bid) >= levels*point:
                            request['sl'] = position.sl-(levels*point)*0.75
                            mt5.order_send(request)

                        