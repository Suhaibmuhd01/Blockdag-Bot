"""
Simple test script for BlockDAG smart contract integration
Tests basic functionality with your deployed contracts
"""

import os
from blockchain_manager import BlockDAGManager
from contracts import ContractManager
from config import *

def test_connection():
    """Test connection to BlockDAG network"""
    print("🔗 Testing BlockDAG Network Connection...")
    
    blockchain = BlockDAGManager()
    
    if blockchain.w3 and blockchain.w3.is_connected():
        print("✅ Successfully connected to BlockDAG network")
        
        # Get network info
        info = blockchain.get_network_info()
        if info:
            print(f"📊 Chain ID: {info['chain_id']}")
            print(f"📊 Latest Block: {info['latest_block']}")
            print(f"📊 Gas Price: {info['gas_price']} wei")
        
        return True
    else:
        print("❌ Failed to connect to BlockDAG network")
        return False

def test_account_setup():
    """Test account setup with private key"""
    print("\n🔑 Testing Account Setup...")
    
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return False, None
    
    blockchain = BlockDAGManager()
    success = blockchain.setup_account(private_key)
    
    if success:
        address = blockchain.account.address
        balance = blockchain.get_balance(address)
        print(f"✅ Account loaded: {address}")
        print(f"💰 BDAG Balance: {balance:.4f} BDAG")
        return True, blockchain
    else:
        print("❌ Failed to setup account")
        return False, None

def test_contract_addresses():
    """Test that all contract addresses are set"""
    print("\n📋 Checking Contract Addresses...")
    
    contracts = {
        'Token': TOKEN_CONTRACT_ADDRESS,
        'Presale': PRESALE_CONTRACT_ADDRESS, 
        'Mining': MINING_CONTRACT_ADDRESS,
        'Wallet': WALLET_CONTRACT_ADDRESS
    }
    
    all_set = True
    for name, address in contracts.items():
        if address:
            print(f"✅ {name}: {address}")
        else:
            print(f"❌ {name}: Not set")
            all_set = False
    
    return all_set

def create_minimal_abis():
    """Create minimal ABIs for testing"""
    
    # Minimal Token ABI - just basic ERC20 functions
    token_abi = [
        {
            "inputs": [{"name": "account", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "totalSupply", 
            "outputs": [{"name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "amount", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    
    # Minimal Presale ABI
    presale_abi = [
        {
            "inputs": [],
            "name": "buyTokensETH",
            "outputs": [],
            "stateMutability": "payable",
            "type": "function"
        }
    ]
    
    # Minimal Mining ABI
    mining_abi = [
        {
            "inputs": [],
            "name": "claimMobileMining",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    
    # Minimal Wallet ABI
    wallet_abi = [
        {
            "inputs": [{"name": "telegramUserId", "type": "uint256"}],
            "name": "connectTelegramWallet",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
    
    return token_abi, presale_abi, mining_abi, wallet_abi

def test_contract_calls(blockchain):
    """Test basic contract read calls"""
    print("\n📞 Testing Contract Calls...")
    
    try:
        # Test token contract - check balance
        if TOKEN_CONTRACT_ADDRESS:
            token_abi, _, _, _ = create_minimal_abis()
            token_contract = blockchain.create_contract(TOKEN_CONTRACT_ADDRESS, token_abi)
            
            if token_contract:
                address = blockchain.account.address
                try:
                    balance = token_contract.functions.balanceOf(address).call()
                    balance_bdag = balance / 10**18
                    print(f"✅ Token balance: {balance_bdag:.4f} BDAG")
                except Exception as e:
                    print(f"⚠️ Token balance call failed: {str(e)}")
                
                try:
                    total_supply = token_contract.functions.totalSupply().call()
                    supply_bdag = total_supply / 10**18
                    print(f"✅ Total supply: {supply_bdag:,.0f} BDAG")
                except Exception as e:
                    print(f"⚠️ Total supply call failed: {str(e)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Contract test error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 === BLOCKDAG INTEGRATION TEST ===\n")
    
    # Test 1: Network connection
    if not test_connection():
        return False
    
    # Test 2: Contract addresses
    if not test_contract_addresses():
        print("⚠️ Some contract addresses missing")
    
    # Test 3: Account setup
    success, blockchain = test_account_setup()
    if not success:
        return False
    
    # Test 4: Contract calls
    test_contract_calls(blockchain)
    
    print("\n🎉 Basic integration test completed!")
    print("\n📋 Next Steps:")
    print("1. Get your actual contract ABIs from BlockDAG IDE")
    print("2. Replace minimal ABIs with full contract ABIs")
    print("3. Test specific functions (mining, presale, staking)")
    print("4. Integrate with your Telegram bot")
    
    return True

if __name__ == "__main__":
    main()