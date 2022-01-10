from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account, 
    deploy_mocks, 
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

def deploy_fund_me():
    account = get_account()

    # Two ways to work with other chains/contracts that don't exist on a chain:
    # 1. Forking: work on a forked simulated chain, basically copy an existing
    #   blockchain and brings it into our local computer for us to work on, all
    #   the work on the local chain won't affect the actual blockchain
    # mainnet-forking: powerful when working with smart contracts on mainnet that we
    #   want to test locally, built-in in brownie, pulls from Infura to work with Rinkeby
    # 2. Mocking: deploy a mock/fake priceFeed contract on the ganache local dev chain
    # Mocking is popular in software dev - deploying a fake verison of something and
    #   interacting with it as if it's real (see contracts/test/MockV3Aggregator.sol)

    # If we are on a persistent live network like rinkeby, use the associated address
    #   otherwise if we are on a dev chain, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address # most-recently deployed mock

    fund_me = FundMe.deploy(
        price_feed_address, 
        {"from": account}, # This makes a state change to the blockchain, so we need a "from": account
        publish_source=config["networks"][network.show_active()].get("verify"), # .get() will not raise errors 
                                                                                #   if you forget to include "verify", 
                                                                                #   same as ["verify"]
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()