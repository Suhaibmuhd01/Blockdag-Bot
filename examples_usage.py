"""
BlockDAG Integration Examples
Comprehensive examples of how to use all contract functions
"""

import os
from blockdag_integration import BlockDAGIntegration

def example_token_operations():
    """Examples of token contract operations"""
    print("🪙 === TOKEN OPERATIONS EXAMPLES ===\n")
    
    bdag = BlockDAGIntegration()
    private_key = os.getenv('PRIVATE_KEY')
    bdag.connect_wallet(private_key)
    
    # Check token balance
    balance = bdag.get_token_balance()
    print(f"💰 Current Balance: {balance:.4f} BDAG")
    
    # Get comprehensive token info
    token_info = bdag.get_token_info()
    if token_info:
        print(f"🏦 Staked Amount: {token_info['staked']:.4f} BDAG")
        print(f"🎁 Pending Rewards: {token_info['pending_rewards']:.4f} BDAG")
        print(f"📈 Staking APY: {token_info['staking_apy']}%")
    
    # Stake tokens (example: 100 BDAG)
    if balance >= 100:
        print(f"\n💼 Staking 100 BDAG...")
        if bdag.stake_tokens(100):
            print("✅ Successfully staked 100 BDAG!")
        else:
            print("❌ Staking failed")
    
    # Daily mining
    print(f"\n⛏️ Attempting daily mining...")
    if bdag.daily_mine():
        print("✅ Daily mining completed!")
    else:
        print("⏰ Mining not available today")

def example_mining_operations():
    """Examples of mining contract operations"""
    print("\n⛏️ === MINING OPERATIONS EXAMPLES ===\n")
    
    bdag = BlockDAGIntegration()
    private_key = os.getenv('PRIVATE_KEY')
    bdag.connect_wallet(private_key)
    
    # Get mining statistics
    mining_stats = bdag.get_mining_stats()
    if mining_stats:
        user_stats = mining_stats['user_stats']
        print(f"💎 Total Mined: {user_stats['total_mined']:.4f} BDAG")
        print(f"🔧 Active Miners: {user_stats['active_miners']}")
        print(f"📱 Mobile Streak: {user_stats['mobile_streak']} days")
        print(f"✅ Can Mobile Mine: {user_stats['can_mobile_mine']}")
    
    # Mobile mining (daily 20 BDAG)
    print(f"\n📱 Attempting mobile mining...")
    if bdag.perform_mobile_mining():
        print("✅ Mobile mining completed! +20 BDAG")
    else:
        print("⏰ Mobile mining not available today")
    
    # Purchase hardware miner example (X10 miner for ~$400)
    # Uncomment to actually purchase:
    # if bdag.purchase_hardware_miner(0, 0.1):  # MinerType.X10, 0.1 ETH
    #     print("✅ X10 miner purchased!")

def example_presale_operations():
    """Examples of presale contract operations"""
    print("\n💰 === PRESALE OPERATIONS EXAMPLES ===\n")
    
    bdag = BlockDAGIntegration()
    private_key = os.getenv('PRIVATE_KEY')
    bdag.connect_wallet(private_key)
    
    # Get presale statistics
    presale_stats = bdag.get_presale_stats()
    if presale_stats:
        print(f"🎯 Presale Active: {presale_stats['presale_active']}")
        print(f"💰 Total Raised: {presale_stats['total_raised']:.2f} ETH")
        print(f"🪙 Tokens Sold: {presale_stats['total_tokens_sold']:,.0f} BDAG")
        print(f"🎁 Claim Enabled: {presale_stats['claim_enabled']}")
    
    # Get your purchase info
    purchase_info = bdag.get_purchase_info()
    if purchase_info:
        print(f"\n💸 Your Purchases:")
        print(f"ETH Spent: {purchase_info['eth_spent']:.4f} ETH")
        print(f"Tokens Allocated: {purchase_info['tokens_allocated']:.2f} BDAG")
        print(f"Has Claimed: {purchase_info['has_claimed']}")
    
    # Buy presale tokens example (0.01 ETH)
    # Uncomment to actually purchase:
    # if bdag.buy_presale_tokens(0.01):
    #     print("✅ Presale tokens purchased!")
    
    # Claim presale tokens
    if bdag.claim_presale_tokens():
        print("✅ Presale tokens claimed!")
    else:
        print("💡 No presale tokens to claim or claiming not enabled")

def example_wallet_operations():
    """Examples of wallet contract operations"""
    print("\n🦊 === WALLET OPERATIONS EXAMPLES ===\n")
    
    bdag = BlockDAGIntegration()
    private_key = os.getenv('PRIVATE_KEY')
    bdag.connect_wallet(private_key)
    
    # Get wallet information
    wallet_info = bdag.get_wallet_info()
    if wallet_info:
        print(f"🔗 Connected: {wallet_info['connected']}")
        print(f"🧊 Frozen: {wallet_info['frozen']}")
        print(f"📱 Telegram ID: {wallet_info['telegram_id']}")
        print(f"💳 Daily Limit: {wallet_info['daily_limit']:.2f} BDAG")
        print(f"💰 Daily Remaining: {wallet_info['daily_remaining']:.2f} BDAG")
    
    # Connect to Telegram example
    # if bdag.connect_telegram_wallet("123456789"):
    #     print("✅ Wallet connected to Telegram!")
    
    # Set daily spending limit (100 BDAG)
    # if bdag.set_daily_limit(100):
    #     print("✅ Daily limit set to 100 BDAG!")
    
    # Send tokens through wallet
    # recipient = "0x742d35Cc6ab4a3c3a4f01d9E8E9fd8F9e3A3b3A3"
    # if bdag.send_tokens_via_wallet(recipient, 10, "transfer"):
    #     print("✅ Sent 10 BDAG through wallet!")

def complete_dashboard_example():
    """Show complete dashboard with all information"""
    print("\n📊 === COMPLETE DASHBOARD EXAMPLE ===\n")
    
    bdag = BlockDAGIntegration()
    private_key = os.getenv('PRIVATE_KEY')
    
    if bdag.connect_wallet(private_key):
        # This shows everything: token info, mining stats, presale info, wallet info
        bdag.get_complete_dashboard()
    else:
        print("❌ Failed to connect wallet")

def investment_strategy_example():
    """Example investment strategy using BlockDAG contracts"""
    print("\n🎯 === INVESTMENT STRATEGY EXAMPLE ===\n")
    
    bdag = BlockDAGIntegration()
    private_key = os.getenv('PRIVATE_KEY')
    bdag.connect_wallet(private_key)
    
    print("💡 Recommended BlockDAG Investment Strategy:")
    print("1. 📱 Daily mobile mining: +20 BDAG/day (FREE)")
    print("2. ⛏️ Daily token mining: Additional BDAG")
    print("3. 🏦 Stake tokens for 12% APY passive income")
    print("4. 🔧 Buy hardware miners for higher daily rewards")
    print("5. 💰 Participate in presale if still active")
    
    current_balance = bdag.get_token_balance()
    print(f"\n📊 Current Portfolio:")
    print(f"💰 BDAG Balance: {current_balance:.4f}")
    
    # Calculate potential daily earnings
    mining_stats = bdag.get_mining_stats()
    daily_potential = 20  # Mobile mining base
    
    if mining_stats and mining_stats['miners']:
        for miner in mining_stats['miners']:
            if miner['active']:
                daily_potential += miner['daily_reward']
    
    print(f"📈 Daily Earning Potential: {daily_potential:.2f} BDAG")
    print(f"📅 Monthly Potential: {daily_potential * 30:.2f} BDAG")
    print(f"🎯 Value at $0.05 target: ${daily_potential * 30 * 0.05:.2f}/month")

def main():
    """Run all examples"""
    print("🚀 === BLOCKDAG INTEGRATION EXAMPLES ===\n")
    
    # Set your private key for examples
    os.environ['PRIVATE_KEY'] = '4e325c938158a0cf48e806b7067d93963430b3f461d1b3874ecd6ac252fbd97c'
    
    try:
        # Run example functions
        example_token_operations()
        example_mining_operations() 
        example_presale_operations()
        example_wallet_operations()
        complete_dashboard_example()
        investment_strategy_example()
        
    except Exception as e:
        print(f"❌ Error running examples: {str(e)}")
        print("💡 Some functions may not work if contracts have access restrictions")
    
    print("\n🎉 All examples completed!")
    print("💡 Uncomment the transaction examples to actually execute them")

if __name__ == "__main__":
    main()