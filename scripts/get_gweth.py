from scripts.helpful_scripts import get_account
from brownie import interface,config,network
def main():
    pass

def get_weth():
   """
   Mints weth by depositing eth
   """
   #ABI
   #Address
   account = get_account()
   weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
   tx = weth.deposit({"from":account,"value":0.01 *10 **18})
   tx.wait(1)
   print("Recieved 0.1 eth")
   return tx