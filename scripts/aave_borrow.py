from scripts.helpful_scripts import get_account
from brownie import network,config,interface
from scripts.get_gweth import get_weth
from web3 import Web3
amount = Web3.toWei(0.1,'ether')
def main():
    account = get_account()
    erc20_address = config["networks"][networks.show_active()]["weth_token"]
    if network.show_active() in ['mainnet-fork']:
        get_weth()
    lending_pool= get_lending_pool()
    approve_erc20(amount,lending_pool.address,erc20_address,account)
    #approve sending the erc20
    print("depositing ...")
    tx = lending_pool.deposit(erc20_address, amount,account.address,0,{'from':account})
    tx.wait(1)
    print("deposited!")
    borrowable_eth, total_debt = get_borrowable_data(lending_pool,account)
    print('Lets borrow some DAI')
    dai_eth_price_feed = get_asset_price(dai_eth_price_feed = 
      config["networks"][networks.show_active()]["dai_eth_price_feed"])
    amount_dai_to_borrow =(1/dai_eth_price_feed)*(borrowable_eth *0.95)
    #borrowable_eth -> borrowable dai * 95%
    print(f'we are going to borrow {amount_dai_to_borrow} DAI')
    # now we are going to borrow
    dai_adress =  config["networks"][networks.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(dai_adress,Web3.toWei(amount_dai_to_borrow,'ether'),
                                    1,
                                    0,
                                    account.address,
                                    {'from':account})    
    borrow_tx.wait(1)
    print("we Borrowed some Dai")
    get_borrowable_data(lending_pool,account)
    
    repay_all(lending_pool,account,amount)
def repay_all(ending_pool,account,amount):
    approve_erc20(
                  Web3.toWei(amount,'ether'),
                  lending_pool,
                  config["networks"][networks.show_active()]["dai_token"],
                  account.address,
                  {"from":account}
                  )
    repay_tx =lending_pool.repay( config["networks"][networks.show_active()]["dai_token"],
                                 amount,
                                 1,
                                 account.address,
                                  {"from":account})
    repay_tx.wait(1)
    print("repayed!")
def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
   
    converted_latest_price = Web3.fromWei(latest_price,'ether')
    print(f"The Dai/eth price is{web3.fromWei(converted_latest_price,'ether')}")
    return  float(converted_latest_price)




def get_borrowable_data(lending_pool,account):
   (total_colateral_eth,
    total_debt_eth,
    available_borrow_eth, 
    current_liquidation_threshhold,
    ltv,
    health_factor)= lending_pool.getUserAccountData(address)
   available_borrow_eth = Web3.fromWei(available_borrow_eth ,'ether')
   total_colateral_eth = Web3.fromWei(total_colateral_eth,'ether')
   total_debt_eth =Web3.fromWei(total_debt_eth,'ether')
   available_borrow_eth = Web3.fromWei(available_borrow_eth,'ether')
   print(f"You have {total_colateral_eth} deposited")
   print(f"You can {available_borrow_eth} borrowed")
   print(f"You have {total_debt_eth} debt")
   return(float(available_borrow_eth),float(total_debt_eth))
    
def approve_erc20(amount, spender ,erc20_address,account):
    print('Approving erc20 token')
    erc20 = interface.IERC20(erc20_address)
    tx =erc20.approve(spender,amount,{'from': account})
    tx.wait(1)
    print('Approved!')
    return tx
def get_lending_pool():
     #contract Adress
     #ABI
    lending_pool_addressses_provider = interface.ILendingPoolAddressesProvider(config['networks'][networks.show_active()]['lending_pool_addresses_provider'])
    lending_pool_address =  lending_pool_addressses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool