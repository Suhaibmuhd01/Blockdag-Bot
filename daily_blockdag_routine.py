#!/usr/bin/env python3
"""
Daily BlockDAG Routine - Automate your BDAG earnings
Run this script daily to maximize your BlockDAG rewards
"""

import os
from blockdag_integration import BlockDAGIntegration

def main():
    """Daily routine to maximize BDAG earnings"""
    print("🌅 === DAILY BLOCKDAG ROUTINE ===\n")
    
    # Initialize BlockDAG integration
    bdag = BlockDAGIntegration()
    
    # Set your private key (use environment variable for security)
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ Please set PRIVATE_KEY environment variable")
        print("💡 Example: export PRIVATE_KEY='your_private_key_here'")
        return
    
    # Connect wallet
    if not bdag.connect_wallet(private_key):
        print("❌ Failed to connect wallet")
        return
    
    print("✅ Connected to BlockDAG network")
    print(f"💰 Wallet: {bdag.blockchain.account.address}")
    
    # Track daily earnings
    initial_balance = bdag.get_token_balance()
    print(f"🏦 Starting Balance: {initial_balance:.4f} BDAG\n")
    
    # === DAILY EARNING ACTIVITIES ===
    
    # 1. Mobile Mining (20 BDAG daily)
    print("📱 === MOBILE MINING ===")
    try:
        if bdag.perform_mobile_mining():
            print("✅ Mobile mining completed! Earned 20 BDAG")
        else:
            print("⏰ Mobile mining already done today or not available")
    except Exception as e:
        print(f"❌ Mobile mining error: {str(e)}")
    
    # 2. Token Mining 
    print("\n⛏️ === TOKEN MINING ===")
    try:
        if bdag.daily_mine():
            print("✅ Token mining completed!")
        else:
            print("⏰ Token mining already done today or not available")
    except Exception as e:
        print(f"❌ Token mining error: {str(e)}")
    
    # 3. Claim Staking Rewards
    print("\n🎁 === STAKING REWARDS ===")
    try:
        if bdag.claim_staking_rewards():
            print("✅ Staking rewards claimed!")
        else:
            print("💡 No staking rewards available to claim")
    except Exception as e:
        print(f"❌ Staking rewards error: {str(e)}")
    
    # 4. Check if presale tokens can be claimed
    print("\n💰 === PRESALE TOKENS ===")
    try:
        purchase_info = bdag.get_purchase_info()
        if purchase_info and purchase_info['tokens_allocated'] > 0 and not purchase_info['has_claimed']:
            if bdag.claim_presale_tokens():
                print(f"✅ Claimed {purchase_info['tokens_allocated']:.2f} BDAG from presale!")
            else:
                print("⏰ Presale claiming not yet enabled")
        else:
            print("💡 No presale tokens to claim")
    except Exception as e:
        print(f"❌ Presale claim error: {str(e)}")
    
    # === SUMMARY ===
    print("\n📊 === DAILY SUMMARY ===")
    final_balance = bdag.get_token_balance()
    earned_today = final_balance - initial_balance
    
    print(f"🏦 Final Balance: {final_balance:.4f} BDAG")
    print(f"📈 Earned Today: +{earned_today:.4f} BDAG")
    print(f"💵 Estimated Value: ${earned_today * 0.05:.2f} (at $0.05 target)")
    
    # Show complete dashboard
    print("\n🎯 === COMPLETE DASHBOARD ===")
    bdag.get_complete_dashboard()
    
    print("\n🎉 Daily routine completed!")
    print("💡 Run this script daily to maximize your BDAG earnings!")

if __name__ == "__main__":
    main()