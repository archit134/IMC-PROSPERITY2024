from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string
import numpy as np
from math import floor, sqrt

class Trader:
    
    def run(self, state: TradingState):
        # Only method required. It takes all buy and sell orders for all symbols as an input, and outputs a list of orders to be sent
        print("traderData: " + state.traderData)
        # print("Observations: " + str(state.observations))
        self.traderData = state.traderData
        result = {}
        flag = "AMETHYSTS"
        ema=0
        if self.traderData is None or self.traderData =='':
            self.traderData = "5053;5022;5029;0,0"
        for product in state.order_depths:
            if str(product)=="AMETHYSTS":
            #     order_depth: OrderDepth = state.order_depths[product]
            #     orders: List[Order] = []
            #     acceptable_price = 10000;  # Participant should calculate this value
                
            #     amethyst_position = int(self.traderData.split(",")[1])
            #     # print("Acceptable price : " + str(acceptable_price))
            #     # print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            #     print(f"Keys: {list(state.position.keys())}")
            #     if len(order_depth.sell_orders) != 0:
            #         best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
            #         print('best+ask:'+str(best_ask))
            #         print('ask_amt'+str(best_ask_amount))
            #         if int(best_ask) == (acceptable_price -2):
            #             buyAmount = abs(20 - amethyst_position)
            #             if buyAmount < best_ask_amount:
            #                 print("BUY", str(buyAmount) + "x", best_ask)
            #                 orders.append(Order(product, best_ask, buyAmount)) 
            #             else:
            #                 print("BUY", str(-best_ask_amount) + "x", best_ask)
            #                 orders.append(Order(product, best_ask, -best_ask_amount)) 
            #             amethyst_position = min(amethyst_position + min(buyAmount,-best_ask_amount),20)
        
            #     if len(order_depth.buy_orders) != 0:
            #         best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
            #         print('best+bid:'+str(best_bid))
            #         print('bid_amt'+str(best_bid_amount))
            #         if int(best_bid) >= (acceptable_price + 2):
            #             sellAmount = abs(20 + amethyst_position)
            #             #sellAmount = best_bid_amount
            #             if sellAmount < best_ask_amount:
            #                 print("SELL", str(-sellAmount) + "x", best_bid)
            #                 orders.append(Order(product, best_bid, -sellAmount))
            #             else:
            #                 print("SELL", str(-best_bid_amount) + "x", best_bid)
            #                 orders.append(Order(product, best_bid, -best_bid_amount))
            #             amethyst_position = max(amethyst_position - min(sellAmount,best_bid_amount),-20)
            #         elif int(best_bid) == (acceptable_price):
            #             # sellAmount = floor(min(0.4*amethyst_position,best_bid_amount))
            #             # if sellAmount < best_ask_amount:
            #             #     print("SELL", str(-sellAmount) + "x", best_bid)
            #             #     orders.append(Order(product, best_bid, -sellAmount))
            #             # else:
            #             #     print("SELL", str(-best_ask_amount) + "x", best_bid)
            #             #     orders.append(Order(product, best_bid, -best_bid_amount))
            #             # amethyst_position = max(amethyst_position - min(sellAmount,best_bid_amount),-20)
            #             pass
                pass
                

            elif str(product) =="STARFRUIT":
                #print(f"Starfruit Position: {state.position['PRODUCT2']}")
                order_depth: OrderDepth = state.order_depths[product]
                past_bid_price = float(self.traderData.split(';')[1])
                past_ask_price = float(self.traderData.split(';')[2])
                ema = float(self.traderData.split(';')[0])
                best_ask = 5000
                best_bid = 5000
                sigma3 = 3*2485.07
                position = 0.0
                number_of_stocks_to_trade = 0
                star_position = int(self.traderData.split(';')[3].split(',')[0])
                if len(order_depth.buy_orders) != 0:
                    best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                if len(order_depth.sell_orders) != 0:
                    best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                mp = 0.5*(best_bid + best_ask)
                ema = (mp*0.01998) + (ema*0.998)    #Explain pls
                if best_bid < ema:
                    if(best_bid > past_bid_price):  
                        position = -1*(((abs(best_bid - ema))/sigma3)**2)*20  #idk what is position variable does
                    elif (best_bid < past_bid_price):
                        position = -1*(abs((best_bid-ema)/sigma3)**0.5)*20
                        
                    else:
                        pass
                    number_of_stocks_to_trade = ( round(position) )

                
                elif best_ask > ema:
                    if (best_ask > past_ask_price):
                        position = ((abs(best_ask-ema)/sigma3)**2)*20
                        
                    elif (best_ask < past_ask_price):
                        position = -(((abs(best_ask - ema)/sigma3))**0.5)*20
                    else:
                        pass
                    number_of_stocks_to_trade = (round(position) )  #Very sus, recheck with archit
                #number_of_stocks_to_trade = int(number_of_stocks_to_trade)
                if(number_of_stocks_to_trade>0):
                    best_ask_amount = - best_ask_amount
                    print("BUY", str(min(number_of_stocks_to_trade,best_ask_amount)) + "x", best_ask)
                    orders.append(Order(product, best_ask,min(number_of_stocks_to_trade,abs(best_ask_amount))))
                    star_position = min(star_position + min(number_of_stocks_to_trade,abs(best_ask_amount)),20)
                else:
                    print("SELL", str(-best_bid_amount) + "x", best_bid)
                    orders.append(Order(product, best_bid, min(-best_bid_amount,number_of_stocks_to_trade)))
                    star_position = max(star_position + min(-best_bid_amount,number_of_stocks_to_trade),-20)
                result[product] = orders
            else:
                orders: List[Order] = []
    
            
        traderData = str(ema) + str(';') + str(best_bid) +  str(';') + str(best_ask) + str(';') + str(star_position)+str(',')+ str(0)# + str(amethyst_position)
        # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.      
        conversions = 1
        return result, conversions, traderData
    

    # NOTES:
    # GET SIGMA3 val from archit
    # INCORPORATE POSITION, FINAL POSITION INTO CURRENT CODE
    # GG, text aaron if anything, he prolly sleeping tho
    # lol