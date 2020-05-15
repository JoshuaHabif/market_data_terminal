import requests, config, json, websocket

STR_SECTION = '\n\n------------------------------------------------------------\n\n' 

def financials():

        report = input("\tAs reported (as) or formatted (f)? ").upper()
        if(report == 'AS'):
                report = 'financials-reported'
        elif(report =='F'):
                report = 'financials'
        else:
                exception()

        symbol = input('\tSymbol:').upper()
        stmt = input('\tStatement (bs/ic/cf):').lower()
        freq = input('\tFrequency (a-annual/q-quarterly/t-ttm/y-ytd):').lower()
        if(freq == 'a'):
                freq='annual'
        elif(freq == 'q'):
                freq='quarterly'
        elif(freq == 't'):
                freq='ttm'
        elif(freq == 'y'):
                freq='ytd'
        else:
                exception()
                
        
        response = input('\tSave to file? (Y/N/) ').upper()

        code = 'https://finnhub.io/api/v1/stock/' + report + '?'+\
                'symbol=' + symbol + '&statement=' + stmt + '&freq=' + freq + '&token=' + config.API_KEY
                
        r = requests.get(code)
        json_obj = r.json()
        txt = json.dumps(json_obj, sort_keys=True, indent=4)
                

        if(response == 'N'):
                print(STR_SECTION)
                print(txt)
                
        elif(response == 'Y'):
                file_name = symbol + '_' + stmt + '_' + freq + '.json'
                out = open(config.MISC_OUTPUT_PATH + file_name, 'w')
                out.write(txt)
                out.close()

        else:
                exception()
        return

def tick_data():
        symbol = input('Symbol: ').upper()
        date = input('Date YYYY-MM-DD: ')
        code = 'https://finnhub.io/api/v1/stock/tick?symbol=' +\
                symbol + '&date=' + date + '&token=' + config.API_KEY
        r = requests.get(code)
        if(r != '<Response [200]>'):
                exception()  
        file_name = symbol + '_' + date + '.csv'
        out = open(config.MISC_OUTPUT_PATH + file_name, 'w')
        out.write(r.text)
        out.close()
        return

def tick_stream():
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp("wss://ws.finnhub.io?token={}".format(config.API_KEY),
                on_message = on_message,
                on_error = on_error,
                on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
        streams = int(input('\tEnter number of streams: '))
        for i in range(0,streams):
                symbol = input('\tSymbol: ').upper()
                ws.send('{"type":"subscribe","symbol":"' + symbol + '"}')

def exception():
        print('Error.\nTerminating.\n')
        exit(0)
        return

def terminate():
        print('\nTerminating.\n')
        exit(0)
        return   

def prompt():
        menu_str = STR_SECTION + '''
                \n\tMarket Data Request: 
                \n\t1 -- Tick Data
                \n\t2 -- Live Tick Stream
                \n\t3 -- Financials\n
                \n\n\tResponse (e to terminate): '''

        response = input(menu_str)
        print(STR_SECTION)

        if(response == 'e'):
                terminate()
        elif(response == '1'):
                tick_data()
        elif(response == '2'):
                tick_stream()
        elif(response == '3'):
                financials()
        else:
                exception()

        

if __name__ == "__main__":
   
        prompt()

        print(STR_SECTION + '''\n\nTerminating.\n\n''')

        exit(0)



    

