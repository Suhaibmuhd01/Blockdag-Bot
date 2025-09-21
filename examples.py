"""
Example Usage and Testing Functions for BlockDAG Smart Contracts
Shows how to use the smart contract integration
"""

import os
import json
from operations import BlockDAGOperations
from config import *

def example_contract_abis():
    """
    Example contract ABIs - Replace these with your actual ABIs
    These are simplified examples showing the structure
    """
    
    # Simplified Token ABI example
    token_abi = [
        {
            "inputs": [{"name": "account", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "inputs": [],
            "name": "totalSupply", 
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function"
        },
        {
            "inputs": [
                {"name": "to", "type": "address"},
                {"name": "amount", "type": "uint256"}
            ],
            "name": "transfer",
            "outputs": [{"name": "", "type": "bool"}],
            "type": "function"
        },
        {
            "inputs": [],
            "name": "claimMobileMiningReward",
            "outputs": [],
            "type": "function"
        }
    ]
    
    # Simplified Presale ABI example
    presale_abi = [
        {
            "inputs": [],
            "name": "buyTokensETH",
            "outputs": [],
            "payable": True,
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getPresaleInfo",
            "outputs": [
                {"name": "price", "type": "uint256"},
                {"name": "tokensSold", "type": "uint256"},
                {"name": "ethRaised", "type": "uint256"},
                {"name": "active", "type": "bool"}
            ],
            "type": "function"
        }
    ]
    
    # Add minimal ABIs for mining and wallet contracts
    mining_abi = [
        {
            "inputs": [],
            "name": "claimMobileMining",
            "outputs": [],
            "type": "function"
        }
    ]
    
    wallet_abi = [
        {
            "inputs": [{"name": "telegramUserId", "type": "uint256"}],
            "name": "connectTelegramWallet",
            "outputs": [],
            "type": "function"
        }
    ]
    
    return token_abi, presale_abi, mining_abi, wallet_abi

def setup_environment():
    """Setup environment variables and configuration"""
    print("🔧 Setting up BlockDAG environment...")
    
    # Check if contract addresses are set
    if not TOKEN_CONTRACT_ADDRESS:
        print("⚠️ TOKEN_CONTRACT_ADDRESS not set in environment")
        print("Please set your contract addresses in the environment variables")
        return False
    
    print(f"✅ Token Contract: {TOKEN_CONTRACT_ADDRESS}")
    print(f"✅ Presale Contract: {PRESALE_CONTRACT_ADDRESS}")  
    print(f"✅ Mining Contract: {MINING_CONTRACT_ADDRESS}")
    print(f"✅ Wallet Contract: {WALLET_CONTRACT_ADDRESS}")
    print(f"✅ Network: {BLOCKDAG_RPC_URL}")
    
    return True

def test_basic_connection():
    """Test basic blockchain connection"""
    print("\n🔗 Testing BlockDAG Network Connection...")
    
    from blockchain_manager import BlockDAGManager
    
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

def example_daily_routine():
    """Example of daily routine operations"""
    print("\n🌅 === DAILY ROUTINE EXAMPLE ===")
    
    # Initialize operations
    operations = BlockDAGOperations()
    
    # Note: You need to provide your actual private key and ABIs
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        print("💡 Use the ask_secrets tool to securely add your private key")
        return False
    
    # Get example ABIs (replace with your actual ABIs)
    token_abi, presale_abi, mining_abi, wallet_abi = example_contract_abis()
    
    # Initialize contracts
    if not operations.initialize(private_key, token_abi, presale_abi, mining_abi, wallet_abi):
        return False
    
    print("\n1️⃣ Checking account overview...")
    overview = operations.get_complete_overview()
    
    print("\n2️⃣ Claiming daily mobile mining...")
    mining_result = operations.daily_mobile_mining()
    
    print("\n3️⃣ Claiming all available rewards...")
    rewards = operations.claim_all_rewards()
    
    print("\n4️⃣ Updated overview after claims...")
    final_overview = operations.get_complete_overview()
    
    return True

def example_presale_purchase():
    """Example of purchasing tokens during presale"""
    print("\n💰 === PRESALE PURCHASE EXAMPLE ===")
    
    operations = BlockDAGOperations()
    
    # Setup (same as daily routine)
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return False
    
    token_abi, presale_abi, mining_abi, wallet_abi = example_contract_abis()
    
    if not operations.initialize(private_key, token_abi, presale_abi, mining_abi, wallet_abi):
        return False
    
    # Check presale status
    print("📊 Checking presale information...")
    presale_info = operations.contract_manager.presale.get_presale_info()
    if presale_info:
        print(f"💵 Current Price: ${presale_info['current_price']}")
        print(f"🎯 Tokens Sold: {presale_info['tokens_sold']}")
        print(f"💰 ETH Raised: {presale_info['eth_raised']}")
        print(f"🟢 Active: {presale_info['presale_active']}")
    
    # Example purchase (use small amount for testing)
    eth_amount = 0.01  # 0.01 ETH for testing
    print(f"\n💳 Attempting to buy tokens with {eth_amount} ETH...")
    
    purchase_result = operations.buy_presale_tokens(eth_amount)
    if purchase_result:
        print("✅ Presale purchase successful!")
    
    return True

def example_staking_operations():
    """Example of staking operations"""
    print("\n🏦 === STAKING OPERATIONS EXAMPLE ===")
    
    operations = BlockDAGOperations()
    
    # Setup
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return False
    
    token_abi, presale_abi, mining_abi, wallet_abi = example_contract_abis()
    
    if not operations.initialize(private_key, token_abi, presale_abi, mining_abi, wallet_abi):
        return False
    
    address = operations.contract_manager.blockchain.account.address
    
    # Check current balance
    balance = operations.contract_manager.token.get_balance(address)
    print(f"💰 Current BDAG balance: {balance}")
    
    if balance > 100:  # Only stake if we have more than 100 BDAG
        stake_amount = 50  # Stake 50 BDAG
        
        print(f"🏦 Staking {stake_amount} BDAG...")
        stake_result = operations.stake_tokens_for_rewards(stake_amount)
        
        if stake_result:
            print("✅ Staking successful!")
            
            # Check staking info
            staking_info = operations.contract_manager.token.get_staking_info(address)
            if staking_info:
                print(f"📊 Staked Amount: {staking_info['staked_amount']} BDAG")
                print(f"🎁 Rewards Earned: {staking_info['rewards_earned']} BDAG")
    else:
        print("⚠️ Insufficient balance for staking example")
    
    return True

def example_hardware_mining():
    """Example of hardware mining operations"""
    print("\n⛏️ === HARDWARE MINING EXAMPLE ===")
    
    operations = BlockDAGOperations()
    
    # Setup
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return False
    
    token_abi, presale_abi, mining_abi, wallet_abi = example_contract_abis()
    
    if not operations.initialize(private_key, token_abi, presale_abi, mining_abi, wallet_abi):
        return False
    
    # Check current miners
    address = operations.contract_manager.blockchain.account.address
    miners = operations.contract_manager.mining.get_user_miners(address)
    
    print(f"🖥️ Current miners: {miners}")
    
    # Example: Purchase X10 miner (cheapest option)
    print("🛒 Purchasing X10 hardware miner...")
    purchase_result = operations.purchase_hardware_miner("X10")
    
    if purchase_result:
        print("✅ X10 miner purchased successfully!")
        print("⏳ Miner will need activation after shipping simulation")
    
    return True

def example_telegram_integration():
    """Example of Telegram wallet integration"""
    print("\n📱 === TELEGRAM INTEGRATION EXAMPLE ===")
    
    operations = BlockDAGOperations()
    
    # Setup
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return False
    
    token_abi, presale_abi, mining_abi, wallet_abi = example_contract_abis()
    
    if not operations.initialize(private_key, token_abi, presale_abi, mining_abi, wallet_abi):
        return False
    
    # Example Telegram user ID
    telegram_user_id = 123456789
    
    print(f"📱 Connecting wallet to Telegram user {telegram_user_id}...")
    connection_result = operations.connect_telegram_wallet(telegram_user_id)
    
    if connection_result:
        print("✅ Telegram wallet connected successfully!")
        
        # Check connection
        wallet_address = operations.contract_manager.wallet.get_telegram_wallet(telegram_user_id)
        if wallet_address:
            print(f"💼 Connected wallet: {wallet_address}")
    
    return True

def example_batch_operations():
    """Example of batch operations"""
    print("\n🔄 === BATCH OPERATIONS EXAMPLE ===")
    
    operations = BlockDAGOperations()
    
    # Setup
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found in environment")
        return False
    
    token_abi, presale_abi, mining_abi, wallet_abi = example_contract_abis()
    
    if not operations.initialize(private_key, token_abi, presale_abi, mining_abi, wallet_abi):
        return False
    
    # Define batch operations
    batch_ops = [
        {'type': 'mobile_mining'},
        {'type': 'claim_rewards'},
        {'type': 'stake', 'params': {'amount': 10}}
    ]
    
    print("🔄 Executing batch operations...")
    results = operations.batch_operations(batch_ops)
    
    # Show results
    for result in results:
        status = "✅" if result['success'] else "❌"
        print(f"{status} {result['operation']}: {result.get('result', result.get('error', 'No result'))}")
    
    return True

def run_all_examples():
    """Run all examples"""
    print("🚀 === BLOCKDAG SMART CONTRACT EXAMPLES ===\n")
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        return False
    
    # Test connection
    if not test_basic_connection():
        print("❌ Connection test failed")
        return False
    
    print("\n" + "="*50)
    print("📋 Available Examples:")
    print("1. Daily Routine (mobile mining + rewards)")
    print("2. Presale Purchase")
    print("3. Staking Operations")
    print("4. Hardware Mining")
    print("5. Telegram Integration")
    print("6. Batch Operations")
    print("7. Run All Examples")
    
    try:
        choice = input("\nEnter choice (1-7): ").strip()
        
        if choice == "1":
            return example_daily_routine()
        elif choice == "2":
            return example_presale_purchase()
        elif choice == "3":
            return example_staking_operations()
        elif choice == "4":
            return example_hardware_mining()
        elif choice == "5":
            return example_telegram_integration()
        elif choice == "6":
            return example_batch_operations()
        elif choice == "7":
            # Run all examples
            examples = [
                example_daily_routine,
                example_presale_purchase,
                example_staking_operations,
                example_hardware_mining,
                example_telegram_integration,
                example_batch_operations
            ]
            
            for i, example in enumerate(examples):
                print(f"\n{'='*20} EXAMPLE {i+1} {'='*20}")
                try:
                    example()
                except Exception as e:
                    print(f"❌ Example {i+1} error: {str(e)}")
            
            return True
        else:
            print("❌ Invalid choice")
            return False
            
    except KeyboardInterrupt:
        print("\n👋 Examples interrupted by user")
        return False
    except Exception as e:
        print(f"❌ Examples error: {str(e)}")
        return False

if __name__ == "__main__":
    """
    Main execution - You need to:
    1. Set your private key using the ask_secrets tool
    2. Set your contract addresses in environment variables
    3. Replace example ABIs with your actual contract ABIs
    4. Run the examples
    """
    
    print("📚 BlockDAG Smart Contract Integration Examples")
    print("⚠️ Before running:")
    print("1. Set PRIVATE_KEY using ask_secrets tool")
    print("2. Set contract addresses in environment variables")
    print("3. Replace example ABIs with your actual contract ABIs")
    print("4. Make sure you have test BDAG tokens in your wallet")
    
    proceed = input("\nReady to proceed? (y/n): ").strip().lower()
    if proceed == 'y':
        run_all_examples()
    else:
        print("👋 Setup your environment first, then run the examples!")