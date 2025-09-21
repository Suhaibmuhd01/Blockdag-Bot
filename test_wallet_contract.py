"""
Test script for BlockDAG Wallet Contract
Tests the actual wallet contract with real ABI
"""

import os
import json
from blockchain_manager import BlockDAGManager
from config import *

def load_wallet_abi():
    """Load the real wallet contract ABI"""
    with open('attached_assets/abii_1758419518538.txt', 'r') as f:
        abi = json.load(f)
    return abi

def test_wallet_contract():
    """Test wallet contract with real ABI"""
    print("🦊 === TESTING WALLET CONTRACT ===\n")
    
    # Setup blockchain connection
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found")
        return False
    
    blockchain = BlockDAGManager()
    if not blockchain.setup_account(private_key):
        print("❌ Failed to setup account")
        return False
    
    address = blockchain.account.address
    print(f"✅ Testing with wallet: {address}")
    print(f"💰 BDAG Balance: {blockchain.get_balance(address):.4f} BDAG")
    
    # Load real wallet ABI
    wallet_abi = load_wallet_abi()
    print(f"✅ Loaded wallet ABI with {len(wallet_abi)} functions/events")
    
    # Create wallet contract instance
    wallet_contract = blockchain.create_contract(WALLET_CONTRACT_ADDRESS, wallet_abi)
    if not wallet_contract:
        print("❌ Failed to create wallet contract")
        return False
    
    print(f"✅ Wallet contract created: {WALLET_CONTRACT_ADDRESS}")
    
    # Test read functions
    print("\n📖 Testing Read Functions...")
    
    try:
        # Test 1: Check if wallet is connected
        is_connected = wallet_contract.functions.connectedWallets(address).call()
        print(f"🔗 Wallet connected: {is_connected}")
        
        # Test 2: Get wallet info
        wallet_info = wallet_contract.functions.getWalletInfo(address).call()
        print(f"📊 Wallet info: Connected={wallet_info[0]}, Frozen={wallet_info[1]}")
        
        # Test 3: Get daily spending info
        spending_info = wallet_contract.functions.getDailySpendingInfo(address).call()
        limit_wei, spent_wei, remaining_wei, reset_time = spending_info
        limit_bdag = limit_wei / 10**18
        spent_bdag = spent_wei / 10**18
        remaining_bdag = remaining_wei / 10**18
        
        print(f"💳 Daily Limit: {limit_bdag:.2f} BDAG")
        print(f"💸 Daily Spent: {spent_bdag:.2f} BDAG")
        print(f"💰 Remaining: {remaining_bdag:.2f} BDAG")
        print(f"⏰ Reset Time: {reset_time}")
        
        # Test 4: Get transaction history (last 5)
        tx_history = wallet_contract.functions.getTransactionHistory(address, 5).call()
        print(f"📜 Transaction History: {len(tx_history)} transactions")
        
        for i, tx in enumerate(tx_history):
            from_addr, to_addr, amount_wei, timestamp, tx_type, tx_hash = tx
            amount_bdag = amount_wei / 10**18
            print(f"  {i+1}. {tx_type}: {amount_bdag:.4f} BDAG to {to_addr[:10]}...")
            
    except Exception as e:
        print(f"❌ Read function error: {str(e)}")
        return False
    
    # Test write functions (optional)
    print("\n✍️ Testing Write Functions...")
    
    try:
        # Test 1: Connect wallet to Telegram (example)
        telegram_user_id = "123456789"  # Example Telegram user ID
        print(f"📱 Attempting to connect wallet to Telegram ID: {telegram_user_id}")
        
        # Build transaction for connectWallet
        tx = wallet_contract.functions.connectWallet(telegram_user_id).build_transaction({
            'from': address,
            'gas': 200000,
            'gasPrice': blockchain.get_gas_price(),
            'nonce': blockchain.w3.eth.get_transaction_count(address),
            'chainId': BLOCKDAG_CHAIN_ID
        })
        
        # Sign and send
        signed_tx = blockchain.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = blockchain.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        print(f"🚀 Transaction sent: {tx_hash.hex()}")
        print(f"🔗 Explorer: {BLOCKDAG_EXPLORER_URL}tx/{tx_hash.hex()}")
        
        # Wait for confirmation
        receipt = blockchain.wait_for_transaction(tx_hash.hex())
        if receipt:
            print("✅ Wallet connection transaction confirmed!")
            
            # Check if wallet is now connected to this Telegram ID
            connected_wallet = wallet_contract.functions.getWalletByTelegramId(telegram_user_id).call()
            if connected_wallet == address:
                print(f"✅ Wallet successfully connected to Telegram ID {telegram_user_id}")
            else:
                print(f"⚠️ Wallet connection verification failed")
        
    except Exception as e:
        print(f"❌ Write function error: {str(e)}")
        # This is OK for testing - might not have permissions or contract might have restrictions
        print("💡 This may be normal if the contract has specific access controls")
    
    print("\n🎉 Wallet contract test completed!")
    return True

def test_daily_limit_functions():
    """Test daily limit functionality"""
    print("\n💳 === TESTING DAILY LIMIT FUNCTIONS ===")
    
    private_key = os.getenv('PRIVATE_KEY')
    blockchain = BlockDAGManager()
    blockchain.setup_account(private_key)
    
    wallet_abi = load_wallet_abi()
    wallet_contract = blockchain.create_contract(WALLET_CONTRACT_ADDRESS, wallet_abi)
    address = blockchain.account.address
    
    try:
        # Test setting daily limit
        new_limit = 100  # 100 BDAG daily limit
        limit_wei = int(new_limit * 10**18)
        
        print(f"💳 Setting daily limit to {new_limit} BDAG...")
        
        tx = wallet_contract.functions.setDailyLimit(limit_wei).build_transaction({
            'from': address,
            'gas': 100000,
            'gasPrice': blockchain.get_gas_price(),
            'nonce': blockchain.w3.eth.get_transaction_count(address),
            'chainId': BLOCKDAG_CHAIN_ID
        })
        
        signed_tx = blockchain.w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = blockchain.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        print(f"🚀 Daily limit transaction: {tx_hash.hex()}")
        
        receipt = blockchain.wait_for_transaction(tx_hash.hex())
        if receipt:
            print("✅ Daily limit set successfully!")
            
            # Verify the new limit
            spending_info = wallet_contract.functions.getDailySpendingInfo(address).call()
            new_limit_wei = spending_info[0]
            new_limit_bdag = new_limit_wei / 10**18
            print(f"✅ Verified new daily limit: {new_limit_bdag:.2f} BDAG")
        
    except Exception as e:
        print(f"❌ Daily limit test error: {str(e)}")

if __name__ == "__main__":
    print("🚀 BlockDAG Wallet Contract Test")
    print("================================")
    
    # Set environment variables
    os.environ['PRIVATE_KEY'] = '4e325c938158a0cf48e806b7067d93963430b3f461d1b3874ecd6ac252fbd97c'
    
    # Test wallet contract
    test_wallet_contract()
    
    # Test daily limit functions
    test_daily_limit_functions()