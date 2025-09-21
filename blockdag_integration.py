"""
Complete BlockDAG Integration System
Handles all 4 smart contracts: Token, Presale, Mining, Wallet
"""

import os
import json
import time
from blockchain_manager import BlockDAGManager
from config import *

class BlockDAGIntegration:
    """Complete integration for all BlockDAG contracts"""
    
    def __init__(self):
        self.blockchain = BlockDAGManager()
        self.contracts = {}
        self.abis = {}
        self.setup_contracts()
    
    def setup_contracts(self):
        """Load all contract ABIs and create contract instances"""
        
        # Load ABIs
        abi_files = {
            'token': 'attached_assets/token abi_1758420269516.txt',
            'presale': 'attached_assets/presale abi_1758420269515.txt', 
            'mining': 'attached_assets/mining abi_1758420269514.txt',
            'wallet': 'attached_assets/abii_1758419518538.txt'
        }
        
        # Load each ABI
        for contract_name, file_path in abi_files.items():
            try:
                with open(file_path, 'r') as f:
                    self.abis[contract_name] = json.load(f)
                print(f"✅ Loaded {contract_name} ABI with {len(self.abis[contract_name])} functions/events")
            except Exception as e:
                print(f"❌ Failed to load {contract_name} ABI: {str(e)}")
                return False
        
        # Contract addresses
        contract_addresses = {
            'token': TOKEN_CONTRACT_ADDRESS,
            'presale': PRESALE_CONTRACT_ADDRESS,
            'mining': MINING_CONTRACT_ADDRESS,
            'wallet': WALLET_CONTRACT_ADDRESS
        }
        
        # Create contract instances
        for contract_name, address in contract_addresses.items():
            if contract_name in self.abis:
                contract = self.blockchain.create_contract(address, self.abis[contract_name])
                if contract:
                    self.contracts[contract_name] = contract
                    print(f"✅ {contract_name.title()} contract ready: {address}")
                else:
                    print(f"❌ Failed to create {contract_name} contract")
                    return False
        
        return len(self.contracts) == 4
    
    def connect_wallet(self, private_key):
        """Connect wallet for transactions"""
        return self.blockchain.setup_account(private_key)
    
    # ================================
    # TOKEN CONTRACT FUNCTIONS
    # ================================
    
    def get_token_balance(self, address=None):
        """Get BDAG token balance"""
        if not address:
            address = self.blockchain.account.address
        try:
            balance_wei = self.contracts['token'].functions.balanceOf(address).call()
            return balance_wei / 10**18
        except Exception as e:
            print(f"❌ Token balance error: {str(e)}")
            return 0
    
    def get_token_info(self, address=None):
        """Get comprehensive token account info"""
        if not address:
            address = self.blockchain.account.address
        try:
            # Get token account details
            balance, staked, pending_rewards, next_mining = self.contracts['token'].functions.getAccountInfo(address).call()
            
            return {
                'balance': balance / 10**18,
                'staked': staked / 10**18,
                'pending_rewards': pending_rewards / 10**18,
                'next_mining_time': next_mining,
                'total_supply': self.contracts['token'].functions.totalSupply().call() / 10**18,
                'staking_apy': self.contracts['token'].functions.stakingAPY().call(),
                'mining_rate': self.contracts['token'].functions.miningRewardRate().call() / 10**18
            }
        except Exception as e:
            print(f"❌ Token info error: {str(e)}")
            return None
    
    def stake_tokens(self, amount_bdag):
        """Stake BDAG tokens for rewards"""
        try:
            amount_wei = int(amount_bdag * 10**18)
            address = self.blockchain.account.address
            
            # Check balance
            balance = self.get_token_balance()
            if balance < amount_bdag:
                print(f"❌ Insufficient balance: {balance:.2f} BDAG < {amount_bdag} BDAG")
                return False
            
            # Build transaction
            tx = self.contracts['token'].functions.stake(amount_wei).build_transaction({
                'from': address,
                'gas': 200000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            # Send transaction
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Staking error: {str(e)}")
            return False
    
    def unstake_tokens(self, amount_bdag):
        """Unstake BDAG tokens"""
        try:
            amount_wei = int(amount_bdag * 10**18)
            address = self.blockchain.account.address
            
            tx = self.contracts['token'].functions.unstake(amount_wei).build_transaction({
                'from': address,
                'gas': 200000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Unstaking error: {str(e)}")
            return False
    
    def claim_staking_rewards(self):
        """Claim accumulated staking rewards"""
        try:
            address = self.blockchain.account.address
            
            tx = self.contracts['token'].functions.claimStakingRewards().build_transaction({
                'from': address,
                'gas': 150000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Staking rewards claim error: {str(e)}")
            return False
    
    def daily_mine(self):
        """Perform daily mining"""
        try:
            address = self.blockchain.account.address
            
            # Check if can mine today
            time_until = self.contracts['token'].functions.getTimeUntilNextMining(address).call()
            if time_until > 0:
                hours = time_until // 3600
                minutes = (time_until % 3600) // 60
                print(f"⏰ Must wait {hours}h {minutes}m before next mining")
                return False
            
            tx = self.contracts['token'].functions.mine().build_transaction({
                'from': address,
                'gas': 150000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Mining error: {str(e)}")
            return False
    
    # ================================
    # MINING CONTRACT FUNCTIONS
    # ================================
    
    def get_mining_stats(self, address=None):
        """Get user mining statistics"""
        if not address:
            address = self.blockchain.account.address
        try:
            # Get user mining stats
            total_mined, active_miners, mobile_streak, can_mobile_mine, next_mobile_time = \
                self.contracts['mining'].functions.getUserMiningStats(address).call()
            
            # Get miners list
            miners = self.contracts['mining'].functions.getUserMiners(address).call()
            
            # Get global mining stats
            global_stats = self.contracts['mining'].functions.getMiningStats().call()
            
            return {
                'user_stats': {
                    'total_mined': total_mined / 10**18,
                    'active_miners': active_miners,
                    'mobile_streak': mobile_streak,
                    'can_mobile_mine': can_mobile_mine,
                    'next_mobile_time': next_mobile_time
                },
                'miners': [
                    {
                        'type': miner[0],  # MinerType enum
                        'daily_reward': miner[1] / 10**18,
                        'last_claim': miner[2],
                        'active': miner[3],
                        'purchase_time': miner[4],
                        'total_mined': miner[5] / 10**18
                    } for miner in miners
                ],
                'global_stats': {
                    'total_hardware_miners': global_stats[0],
                    'x10_miners': global_stats[1],
                    'x30_miners': global_stats[2], 
                    'x100_miners': global_stats[3],
                    'contract_balance': global_stats[4] / 10**18
                }
            }
        except Exception as e:
            print(f"❌ Mining stats error: {str(e)}")
            return None
    
    def perform_mobile_mining(self):
        """Perform mobile mining (daily 20 BDAG)"""
        try:
            address = self.blockchain.account.address
            
            # Check if can mine today
            can_mine = self.contracts['mining'].functions.canMineToday(address).call()
            if not can_mine:
                print("⏰ Mobile mining already completed today")
                return False
            
            tx = self.contracts['mining'].functions.performMobileMining().build_transaction({
                'from': address,
                'gas': 200000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Mobile mining error: {str(e)}")
            return False
    
    def purchase_hardware_miner(self, miner_type, eth_amount):
        """Purchase hardware miner (X10=0, X30=1, X100=2)"""
        try:
            address = self.blockchain.account.address
            value_wei = int(eth_amount * 10**18)
            
            tx = self.contracts['mining'].functions.purchaseHardwareMiner(miner_type).build_transaction({
                'from': address,
                'value': value_wei,
                'gas': 300000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Hardware miner purchase error: {str(e)}")
            return False
    
    def claim_mining_rewards(self, miner_id):
        """Claim rewards from hardware miner"""
        try:
            address = self.blockchain.account.address
            
            tx = self.contracts['mining'].functions.claimMiningRewards(miner_id).build_transaction({
                'from': address,
                'gas': 200000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Mining rewards claim error: {str(e)}")
            return False
    
    # ================================
    # PRESALE CONTRACT FUNCTIONS
    # ================================
    
    def get_presale_stats(self):
        """Get presale statistics"""
        try:
            stats = self.contracts['presale'].functions.getPresaleStats().call()
            return {
                'total_raised': stats[0] / 10**18,
                'total_tokens_sold': stats[1] / 10**18,
                'presale_price': stats[2],
                'presale_active': stats[3],
                'claim_enabled': stats[4],
                'time_left': stats[5]
            }
        except Exception as e:
            print(f"❌ Presale stats error: {str(e)}")
            return None
    
    def buy_presale_tokens(self, eth_amount, referrer=None):
        """Buy tokens in presale"""
        try:
            address = self.blockchain.account.address
            value_wei = int(eth_amount * 10**18)
            
            if referrer:
                # Buy with referral
                tx = self.contracts['presale'].functions.buyTokensWithReferral(referrer).build_transaction({
                    'from': address,
                    'value': value_wei,
                    'gas': 300000,
                    'gasPrice': self.blockchain.get_gas_price(),
                    'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                    'chainId': BLOCKDAG_CHAIN_ID
                })
            else:
                # Buy without referral
                tx = self.contracts['presale'].functions.buyTokens().build_transaction({
                    'from': address,
                    'value': value_wei,
                    'gas': 300000,
                    'gasPrice': self.blockchain.get_gas_price(),
                    'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                    'chainId': BLOCKDAG_CHAIN_ID
                })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Presale purchase error: {str(e)}")
            return False
    
    def claim_presale_tokens(self):
        """Claim purchased presale tokens"""
        try:
            address = self.blockchain.account.address
            
            # Check if claim is enabled
            claim_enabled = self.contracts['presale'].functions.claimEnabled().call()
            if not claim_enabled:
                print("❌ Token claiming not yet enabled")
                return False
                
            # Check if already claimed
            claimed = self.contracts['presale'].functions.claimed(address).call()
            if claimed:
                print("❌ Tokens already claimed")
                return False
            
            tx = self.contracts['presale'].functions.claimTokens().build_transaction({
                'from': address,
                'gas': 200000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Presale claim error: {str(e)}")
            return False
    
    def get_purchase_info(self, address=None):
        """Get user's presale purchase information"""
        if not address:
            address = self.blockchain.account.address
        try:
            eth_spent, tokens_allocated, has_claimed, payment_method = \
                self.contracts['presale'].functions.getPurchaseInfo(address).call()
            
            return {
                'eth_spent': eth_spent / 10**18,
                'tokens_allocated': tokens_allocated / 10**18,
                'has_claimed': has_claimed,
                'payment_method': payment_method
            }
        except Exception as e:
            print(f"❌ Purchase info error: {str(e)}")
            return None
    
    # ================================
    # WALLET CONTRACT FUNCTIONS
    # ================================
    
    def connect_telegram_wallet(self, telegram_user_id):
        """Connect wallet to Telegram user ID"""
        try:
            address = self.blockchain.account.address
            
            tx = self.contracts['wallet'].functions.connectWallet(telegram_user_id).build_transaction({
                'from': address,
                'gas': 150000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Telegram wallet connection error: {str(e)}")
            return False
    
    def send_tokens_via_wallet(self, to_address, amount_bdag, tx_type="transfer"):
        """Send tokens through wallet contract"""
        try:
            address = self.blockchain.account.address
            amount_wei = int(amount_bdag * 10**18)
            
            tx = self.contracts['wallet'].functions.sendTokens(to_address, amount_wei, tx_type).build_transaction({
                'from': address,
                'gas': 200000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Wallet send error: {str(e)}")
            return False
    
    def get_wallet_info(self, address=None):
        """Get wallet information"""
        if not address:
            address = self.blockchain.account.address
        try:
            connected, frozen, telegram_id, connection_time = \
                self.contracts['wallet'].functions.getWalletInfo(address).call()
            
            # Get daily spending info
            limit, spent, remaining, reset_time = \
                self.contracts['wallet'].functions.getDailySpendingInfo(address).call()
            
            return {
                'connected': connected,
                'frozen': frozen,
                'telegram_id': telegram_id,
                'connection_time': connection_time,
                'daily_limit': limit / 10**18,
                'daily_spent': spent / 10**18,
                'daily_remaining': remaining / 10**18,
                'reset_time': reset_time
            }
        except Exception as e:
            print(f"❌ Wallet info error: {str(e)}")
            return None
    
    def set_daily_limit(self, limit_bdag):
        """Set daily spending limit"""
        try:
            address = self.blockchain.account.address
            limit_wei = int(limit_bdag * 10**18)
            
            tx = self.contracts['wallet'].functions.setDailyLimit(limit_wei).build_transaction({
                'from': address,
                'gas': 100000,
                'gasPrice': self.blockchain.get_gas_price(),
                'nonce': self.blockchain.w3.eth.get_transaction_count(address),
                'chainId': BLOCKDAG_CHAIN_ID
            })
            
            return self.blockchain.send_transaction(tx)
        except Exception as e:
            print(f"❌ Daily limit error: {str(e)}")
            return False
    
    # ================================
    # COMPREHENSIVE DASHBOARD
    # ================================
    
    def get_complete_dashboard(self, address=None):
        """Get complete user dashboard with all contract data"""
        if not address:
            address = self.blockchain.account.address
        
        print(f"📊 === BLOCKDAG DASHBOARD FOR {address} ===\n")
        
        # Network info
        balance = self.blockchain.get_balance(address)
        print(f"💰 BDAG Balance: {balance:.4f} BDAG")
        print(f"🌐 Network: BlockDAG Primordial (Chain ID: {BLOCKDAG_CHAIN_ID})")
        print(f"🔗 Explorer: {BLOCKDAG_EXPLORER_URL}")
        
        # Token info
        print(f"\n🪙 === TOKEN INFORMATION ===")
        token_info = self.get_token_info(address)
        if token_info:
            print(f"💰 Token Balance: {token_info['balance']:.4f} BDAG")
            print(f"🏦 Staked Amount: {token_info['staked']:.4f} BDAG")
            print(f"🎁 Pending Rewards: {token_info['pending_rewards']:.4f} BDAG")
            print(f"📈 Staking APY: {token_info['staking_apy']}%")
            print(f"⛏️ Mining Rate: {token_info['mining_rate']:.2f} BDAG/day")
            print(f"🏆 Total Supply: {token_info['total_supply']:,.0f} BDAG")
        
        # Mining info
        print(f"\n⛏️ === MINING INFORMATION ===")
        mining_stats = self.get_mining_stats(address)
        if mining_stats:
            user_stats = mining_stats['user_stats']
            print(f"💎 Total Mined: {user_stats['total_mined']:.4f} BDAG")
            print(f"🔧 Active Miners: {user_stats['active_miners']}")
            print(f"📱 Mobile Streak: {user_stats['mobile_streak']} days")
            print(f"✅ Can Mobile Mine: {user_stats['can_mobile_mine']}")
            
            if mining_stats['miners']:
                print(f"\n🔧 Hardware Miners:")
                for i, miner in enumerate(mining_stats['miners']):
                    miner_type = ["X10", "X30", "X100"][miner['type']]
                    print(f"  {i+1}. {miner_type} Miner: {miner['daily_reward']:.2f} BDAG/day (Active: {miner['active']})")
        
        # Presale info
        print(f"\n💰 === PRESALE INFORMATION ===")
        presale_stats = self.get_presale_stats()
        if presale_stats:
            print(f"🎯 Presale Active: {presale_stats['presale_active']}")
            print(f"💰 Total Raised: {presale_stats['total_raised']:.2f} ETH")
            print(f"🪙 Tokens Sold: {presale_stats['total_tokens_sold']:,.0f} BDAG")
            print(f"🎁 Claim Enabled: {presale_stats['claim_enabled']}")
            
            purchase_info = self.get_purchase_info(address)
            if purchase_info and purchase_info['tokens_allocated'] > 0:
                print(f"\n💸 Your Purchase:")
                print(f"  ETH Spent: {purchase_info['eth_spent']:.4f} ETH")
                print(f"  Tokens Allocated: {purchase_info['tokens_allocated']:.2f} BDAG")
                print(f"  Claimed: {purchase_info['has_claimed']}")
        
        # Wallet info  
        print(f"\n🦊 === WALLET INFORMATION ===")
        wallet_info = self.get_wallet_info(address)
        if wallet_info:
            print(f"🔗 Connected: {wallet_info['connected']}")
            print(f"🧊 Frozen: {wallet_info['frozen']}")
            print(f"📱 Telegram ID: {wallet_info['telegram_id']}")
            print(f"💳 Daily Limit: {wallet_info['daily_limit']:.2f} BDAG")
            print(f"💸 Daily Spent: {wallet_info['daily_spent']:.2f} BDAG")
            print(f"💰 Daily Remaining: {wallet_info['daily_remaining']:.2f} BDAG")
        
        print(f"\n🎉 Dashboard complete!")
        return True


# ================================
# EXAMPLE USAGE FUNCTIONS
# ================================

def test_complete_integration():
    """Test all contract integrations"""
    print("🚀 === COMPLETE BLOCKDAG INTEGRATION TEST ===\n")
    
    # Initialize integration
    bdag = BlockDAGIntegration()
    
    # Connect wallet
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print("❌ PRIVATE_KEY not found")
        return False
    
    if not bdag.connect_wallet(private_key):
        print("❌ Failed to connect wallet")
        return False
    
    # Get complete dashboard
    bdag.get_complete_dashboard()
    
    return True

def daily_routine():
    """Perform daily BlockDAG routine"""
    print("🌅 === DAILY BLOCKDAG ROUTINE ===\n")
    
    bdag = BlockDAGIntegration()
    private_key = os.getenv('PRIVATE_KEY')
    
    if not bdag.connect_wallet(private_key):
        print("❌ Failed to connect wallet")
        return False
    
    # 1. Mobile mining (20 BDAG daily)
    print("📱 Attempting mobile mining...")
    if bdag.perform_mobile_mining():
        print("✅ Mobile mining completed! +20 BDAG")
    else:
        print("⏰ Mobile mining not available today")
    
    # 2. Token mining
    print("\n⛏️ Attempting token mining...")
    if bdag.daily_mine():
        print("✅ Token mining completed!")
    else:
        print("⏰ Token mining not available today")
    
    # 3. Claim staking rewards
    print("\n🎁 Claiming staking rewards...")
    if bdag.claim_staking_rewards():
        print("✅ Staking rewards claimed!")
    else:
        print("💡 No staking rewards to claim")
    
    # 4. Show updated dashboard
    print("\n📊 Updated Dashboard:")
    bdag.get_complete_dashboard()
    
    return True

if __name__ == "__main__":
    # Set environment variables for testing
    os.environ['PRIVATE_KEY'] = '4e325c938158a0cf48e806b7067d93963430b3f461d1b3874ecd6ac252fbd97c'
    
    # Test complete integration
    test_complete_integration()