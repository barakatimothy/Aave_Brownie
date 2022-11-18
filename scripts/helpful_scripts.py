from brownie import (network,Interfaces,config,accounts,MockAggregatorV3,contract,VRFCoordinator,LinkToken)
from web3 import Web3


decimals=8
startingPrice=200000000
FORKED_BLOCKCHAIN=['mainnet-fork','mainnet-fork-dev']
LOCAL_BLOCKCHAIN=['development','ganache-loacl']

def get_accounts(index=None ,id=None):
     #accounts[0]
     #accounts.add("env")
     #accounts.load("id ")
     if index:
          return accountsp[index]
     if id:
          return accounts.load(id)
     
     if network.show_active() in LOCAL_BLOCKCHAIN:
        return accounts[0]
   
     return accounts.add(config["wallets"]["from_key"])





contract_to_mock = {
     "eth_usd_price_feed":MockAggregatorV3,
     "vrf_coordinator":VRFCoordinatorMock,
     "link_token": LinkToken
}

def get_contratcts(contract_name,):
     """ This function grabs the contract address from brownie config 
        if defined,othherwise it deploys a mock version of the contract ,and 
        returns that contract
        Args:
          contract_name(string)
          return 
          brownie.network.contract.projectContact: The most recently 
          deployed version of this contract
          mockV3Aggreggator[-1]
     """
     contract_type = contract_to_mock[contract_name]
     if network.show_active() in  LOCAL_BLOCKCHAIN:
          if len(contract_type)<=0:
               deploy_mocks()
          contract = contract_type[-1]
     else:
           contract = config['networks'][network.show_active()]
           [contract_name]
           #contract 
           #ABI
           contract = Contract.from_abi(contract_type._name,contract_address,contract_type.abi)
           return contract     
DECIMAL = 8
INITIAL_VALUE =200000000000
def deploy_mocks(decimals = DECIMAL,initial_value =INITIAL_VALUE):
     accounts = get_accounts()
     mock_price_feed = MockAggregatorV3.deploy(decimals,initial_value,{"from":account})
     link_token =LinkToken.deploy({'from':accounts})
     VRFCoordinator.deploy(link_token.address, {'from':accounts})
     print ("depployed")     
def fund_with_link(contract_address,account =None,link_token=None,amount=100000):
     accounts = accounts if account else get_accounts()
     
     link_token = link_token if link_token else get_contratcts("link_token")
     tx = link_token.transfer(contract_address,amount,{'from':account})
     tx.wait(1)
     #link_token_contract= interface.LinkTokenInteface( link_token.address)
     #tx =link_token_contract.transfer(contract_address,amount,{"from":accounts})
     print('fund contract')
     return tx 