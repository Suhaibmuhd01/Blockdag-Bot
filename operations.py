"""
Common Operations for BlockDAG Smart Contracts
High-level functions for typical user operations
"""

from contracts import ContractManager
from config import *
import time
import os

class BlockDAGOperations:
    """High-level operations for BlockDAG ecosystem"""
    
    def __init__(self):
        """Initialize operations manager"""
        self.contract_manager = None
        self.setup_complete = False
    
    def initialize(self, private_key, token_abi, presale_abi, mining_abi, wallet_abi):
        """Initialize with private key and contract ABIs"""
        try:
            self.contract_manager = ContractManager(private_key)
            self.contract_manager.setup_contracts(token_abi, presale_abi, mining_abi, wallet_abi)
            self.setup_complete = True
            print("🚀 BlockDAG Operations initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Initialization error: {str(e)}")
            return False
    
    def daily_mobile_mining(self):
        """Perform daily mobile mining claim"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return False
        
        try:
            print("⛏️ Claiming daily mobile mining rewards...")
            
            # Method 1: Try token contract mobile mining
            tx_hash1 = self.contract_manager.token.claim_mobile_mining_reward()
            if tx_hash1:
                print(f"✅ Token mining claim: {tx_hash1}")
            
            # Method 2: Try mining contract
            tx_hash2 = self.contract_manager.mining.claim_mobile_mining()
            if tx_hash2:
                print(f"✅ Mining contract claim: {tx_hash2}")
            
            return tx_hash1 or tx_hash2
            
        except Exception as e:
            print(f"❌ Mobile mining error: {str(e)}")
            return False
    
    def buy_presale_tokens(self, eth_amount):
        """Buy tokens during presale"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return False
        
        try:
            # Check presale status
            presale_info = self.contract_manager.presale.get_presale_info()
            if not presale_info or not presale_info.get('presale_active'):
                print("❌ Presale is not active")
                return False
            
            # Check purchase limits
            if eth_amount < presale_info['min_purchase']:
                print(f"❌ Minimum purchase is {presale_info['min_purchase']} ETH")
                return False
            
            if eth_amount > presale_info['max_purchase']:
                print(f"❌ Maximum purchase is {presale_info['max_purchase']} ETH")
                return False
            
            print(f"💰 Buying presale tokens with {eth_amount} ETH...")
            tx_hash = self.contract_manager.presale.buy_tokens_eth(eth_amount)
            
            if tx_hash:
                print(f"✅ Presale purchase successful: {tx_hash}")
                return tx_hash
            
        except Exception as e:
            print(f"❌ Presale purchase error: {str(e)}")
            return False
    
    def stake_tokens_for_rewards(self, amount):
        """Stake BDAG tokens for rewards"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return False
        
        try:
            address = self.contract_manager.blockchain.account.address
            current_balance = self.contract_manager.token.get_balance(address)
            
            if amount > current_balance:
                print(f"❌ Insufficient balance. You have {current_balance} BDAG")
                return False
            
            print(f"🏦 Staking {amount} BDAG tokens...")
            tx_hash = self.contract_manager.token.stake_tokens(amount)
            
            if tx_hash:
                print(f"✅ Staking successful: {tx_hash}")
                return tx_hash
            
        except Exception as e:
            print(f"❌ Staking error: {str(e)}")
            return False
    
    def claim_all_rewards(self):
        """Claim all available rewards"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return []
        
        results = []
        
        try:
            print("🎁 Claiming all available rewards...")
            
            # 1. Mobile mining rewards
            mobile_tx = self.daily_mobile_mining()
            if mobile_tx:
                results.append(('mobile_mining', mobile_tx))
            
            # 2. Staking rewards
            staking_tx = self.contract_manager.token.claim_staking_rewards()
            if staking_tx:
                results.append(('staking_rewards', staking_tx))
                print(f"✅ Staking rewards claimed: {staking_tx}")
            
            # 3. Hardware miner rewards (if any)
            address = self.contract_manager.blockchain.account.address
            miners = self.contract_manager.mining.get_user_miners(address)
            
            if miners:
                for miner_id in miners:
                    miner_tx = self.contract_manager.mining.claim_miner_rewards(miner_id)
                    if miner_tx:
                        results.append(('miner_rewards', miner_tx))
                        print(f"✅ Miner {miner_id} rewards claimed: {miner_tx}")
            
            print(f"🎉 Claimed {len(results)} reward types successfully!")
            return results
            
        except Exception as e:
            print(f"❌ Reward claiming error: {str(e)}")
            return results
    
    def purchase_hardware_miner(self, miner_type):
        """Purchase hardware miner (X10, X30, X100)"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return False
        
        try:
            print(f"🛒 Purchasing {miner_type} hardware miner...")
            tx_hash = self.contract_manager.mining.purchase_hardware_miner(miner_type)
            
            if tx_hash:
                print(f"✅ Hardware miner purchased: {tx_hash}")
                print("⏳ Miner will need to be activated after shipping simulation")
                return tx_hash
            
        except Exception as e:
            print(f"❌ Miner purchase error: {str(e)}")
            return False
    
    def connect_telegram_wallet(self, telegram_user_id):
        """Connect wallet to Telegram user ID"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return False
        
        try:
            print(f"📱 Connecting wallet to Telegram user {telegram_user_id}...")
            tx_hash = self.contract_manager.wallet.connect_telegram_wallet(telegram_user_id)
            
            if tx_hash:
                print(f"✅ Telegram wallet connected: {tx_hash}")
                return tx_hash
            
        except Exception as e:
            print(f"❌ Telegram connection error: {str(e)}")
            return False
    
    def transfer_tokens(self, to_address, amount):
        """Transfer BDAG tokens to another address"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return False
        
        try:
            address = self.contract_manager.blockchain.account.address
            current_balance = self.contract_manager.token.get_balance(address)
            
            if amount > current_balance:
                print(f"❌ Insufficient balance. You have {current_balance} BDAG")
                return False
            
            print(f"💸 Transferring {amount} BDAG to {to_address}...")
            tx_hash = self.contract_manager.token.transfer(to_address, amount)
            
            if tx_hash:
                print(f"✅ Transfer successful: {tx_hash}")
                
                # Log transaction in wallet contract
                self.contract_manager.wallet.log_transaction(
                    "transfer", amount, to_address, f"Transfer {amount} BDAG"
                )
                return tx_hash
            
        except Exception as e:
            print(f"❌ Transfer error: {str(e)}")
            return False
    
    def get_complete_overview(self):
        """Get complete user overview"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return None
        
        try:
            address = self.contract_manager.blockchain.account.address
            overview = self.contract_manager.get_user_overview(address)
            
            print("\n📊 === USER OVERVIEW ===")
            print(f"💼 Address: {overview['address']}")
            print(f"💰 BDAG Balance: {overview['bdag_balance']:.2f} BDAG")
            print(f"🪙 Token Balance: {overview.get('token_balance', 0):.2f} BDAG")
            
            # Network info
            if overview.get('network_info'):
                info = overview['network_info']
                print(f"🌐 Network: Chain ID {info['chain_id']}, Block {info['latest_block']}")
            
            # Staking info
            if overview.get('staking_info'):
                staking = overview['staking_info']
                print(f"🏦 Staking: {staking['staked_amount']:.2f} BDAG staked")
                print(f"🎁 Rewards: {staking['rewards_earned']:.2f} BDAG earned")
            
            # Mining stats
            if overview.get('mining_stats'):
                mining = overview['mining_stats']
                print(f"⛏️ Mobile Mining: Streak {mining['mobile_streak']}")
                print(f"💎 Total Mined: {mining['total_mined']:.2f} BDAG")
                print(f"🖥️ Active Miners: {mining['active_miners']}")
            
            # Presale info
            if overview.get('presale_purchases'):
                presale = overview['presale_purchases']
                print(f"💰 Presale: {presale['total_tokens_bought']:.2f} BDAG bought")
                print(f"🎁 Referrals: {presale['referral_rewards']:.2f} BDAG rewards")
            
            print("========================\n")
            return overview
            
        except Exception as e:
            print(f"❌ Overview error: {str(e)}")
            return None
    
    def emergency_operations(self):
        """Emergency operations like freezing wallet"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return False
        
        print("🚨 Emergency Operations Menu:")
        print("1. Freeze wallet")
        print("2. Unfreeze wallet")
        print("3. Set daily spending limit")
        
        try:
            choice = input("Enter choice (1-3): ").strip()
            address = self.contract_manager.blockchain.account.address
            
            if choice == "1":
                tx_hash = self.contract_manager.wallet.freeze_wallet(address)
                if tx_hash:
                    print(f"🔒 Wallet frozen: {tx_hash}")
                    return tx_hash
                    
            elif choice == "2":
                tx_hash = self.contract_manager.wallet.unfreeze_wallet(address)
                if tx_hash:
                    print(f"🔓 Wallet unfrozen: {tx_hash}")
                    return tx_hash
                    
            elif choice == "3":
                limit = float(input("Enter daily limit in BDAG: "))
                tx_hash = self.contract_manager.wallet.set_daily_limit(limit)
                if tx_hash:
                    print(f"💳 Daily limit set to {limit} BDAG: {tx_hash}")
                    return tx_hash
            
        except Exception as e:
            print(f"❌ Emergency operation error: {str(e)}")
            return False
    
    def batch_operations(self, operations_list):
        """Execute multiple operations in batch"""
        if not self.setup_complete:
            print("❌ Please initialize first")
            return []
        
        results = []
        print(f"🔄 Executing {len(operations_list)} operations...")
        
        for i, operation in enumerate(operations_list):
            try:
                op_type = operation.get('type')
                op_params = operation.get('params', {})
                
                print(f"📋 Operation {i+1}/{len(operations_list)}: {op_type}")
                
                if op_type == 'mobile_mining':
                    result = self.daily_mobile_mining()
                elif op_type == 'stake':
                    result = self.stake_tokens_for_rewards(op_params['amount'])
                elif op_type == 'transfer':
                    result = self.transfer_tokens(op_params['to'], op_params['amount'])
                elif op_type == 'claim_rewards':
                    result = self.claim_all_rewards()
                else:
                    print(f"❌ Unknown operation type: {op_type}")
                    result = False
                
                results.append({
                    'operation': op_type,
                    'success': bool(result),
                    'result': result
                })
                
                # Small delay between operations
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Batch operation error: {str(e)}")
                results.append({
                    'operation': operation.get('type', 'unknown'),
                    'success': False,
                    'error': str(e)
                })
        
        successful = sum(1 for r in results if r['success'])
        print(f"✅ Batch complete: {successful}/{len(operations_list)} operations successful")
        
        return results