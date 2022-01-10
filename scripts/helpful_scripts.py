from brownie import network, config, accounts, MockV3Aggregator

# When working with mainnet-fork, it should create a fake account with
#   100 ETH in it, but it shouldn't deploy a mock because priceFeed contracts
#   already exist on the forked simulated chain
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        # the auto-generated accounts by brownie on a local ganache-cli chain
        return accounts[0]
    else:
        # load account from environment variables
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    # Constructor parameters for MockV3Aggregator
    if len(MockV3Aggregator) <= 0: # MockV3Aggregator is a list of all the mocks we've deployed
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")
