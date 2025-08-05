### Software Engineering Test Case solution. P1

## Brief description
To solve this task I decided to split the functionality of the emulator to three files: server, client, emulator. I think that this approach is closer to emulating than just 
using server+client, as server should recieve these trades from some clients, as it doesn't generate them.

## Functionality
Client - simple script that receives messages from server using websockets
Server - process that asynchronically recieves and sends trades 
Emulator - reads the .parquet file using pandas (pd.read_parquet), sorts the dataframe using timestamp column. Then, it groups by timestamp, to send the trades asynchronically. For each iteration of sending I compute time diff between the previous and current trade to emulate the trading process as realistically as possible. 


## Another implementation

Please use "alternative_approach" branch. This solution only uses 2 files: server and client.

## Functionality of simpler implementation
Client - simple script that receives messages from server using websockets
Server - combines emulator and server from previous architecture in one implementation. Reads the file, groups the trades using timestamp, sends them asynchronically.

## How to run the code
Before running the code install requirements.txt,
Please run three separate terminals, with corresponding commands(the same order):
python server.py
python client.py
python emulator.py

