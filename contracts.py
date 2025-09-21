"""
Smart Contract Interaction Classes for BlockDAG Network
Handles all interactions with the 4 deployed smart contracts
"""

from blockchain_manager import BlockDAGManager
from config import *
import json
import time

class SmartContract:
    """Base class for smart contract interactions"""
    
    def __init__(self, contract_address, contract_abi, blockchain_manager):
        self.address = contract_address
        self.abi = contract_abi
        self.blockchain = blockchain_manager
        self.contract = None
        
        if contract_address and contract_abi:
            self.contract = self.blockchain.create_contract(contract_address, contract_abi)
    
    def call_function(self, function_name, *args):
        """Call a read-only contract function"""
        try:
            if not self.contract:
                print("❌ Contract not initialized")
                return None
                
            func = getattr(self.contract.functions, function_name)
            result = func(*args).call()
            return result
            
        except Exception as e:
            print(f"❌ Function call error ({function_name}): {str(e)}")
            return None
    
    def send_transaction(self, function_name, *args, **kwargs):
        """Send a transaction to contract function"""
        try:
            if not self.contract:
                print("❌ Contract not initialized")
                return None
                
            if not self.blockchain.account:
                print("❌ No account setup")
                return None
                
            func = getattr(self.contract.functions, function_name)
            
            # Build transaction with proper value handling
            tx_data = {
                'from': self.blockchain.account.address,
                'gas': kwargs.get('gas', DEFAULT_GAS_LIMIT),
                'gasPrice': kwargs.get('gasPrice', self.blockchain.get_gas_price()),
            }
            
            # Add value if this is a payable function
            if 'value' in kwargs:
                tx_data['value'] = kwargs['value']
            
            transaction = func(*args).build_transaction(tx_data)
            
            # Send transaction
            tx_hash = self.blockchain.send_transaction(transaction)
            return tx_hash
            
        except Exception as e:
            print(f"❌ Transaction error ({function_name}): {str(e)}")
            return None

class BlockDAGToken(SmartContract):
    """BlockDAG Token Contract (ERC-20) Interactions"""
    
    def __init__(self, blockchain_manager, abi=None):
        super().__init__(TOKEN_CONTRACT_ADDRESS, abi, blockchain_manager)
    
    def get_balance(self, address):
        """Get token balance for address"""
        balance = self.call_function('balanceOf', address)
        if balance is not None:
            return balance / 10**18  # Convert from wei to BDAG
        return 0
    
    def get_total_supply(self):
        """Get total token supply"""
        total = self.call_function('totalSupply')
        if total is not None:
            return total / 10**18
        return 0
    
    def transfer(self, to_address, amount):
        """Transfer tokens to address"""
        amount_wei = int(amount * 10**18)
        return self.send_transaction('transfer', to_address, amount_wei)
    
    def approve(self, spender, amount):
        """Approve spender to use tokens"""
        amount_wei = int(amount * 10**18)
        return self.send_transaction('approve', spender, amount_wei)
    
    def get_allowance(self, owner, spender):
        """Get allowance for spender"""
        allowance = self.call_function('allowance', owner, spender)
        if allowance is not None:
            return allowance / 10**18
        return 0
    
    def claim_mobile_mining_reward(self):
        """Claim daily mobile mining reward"""
        return self.send_transaction('claimMobileMiningReward')
    
    def stake_tokens(self, amount):
        """Stake tokens for rewards"""
        amount_wei = int(amount * 10**18)
        return self.send_transaction('stakeTokens', amount_wei)
    
    def unstake_tokens(self, amount):
        """Unstake tokens"""
        amount_wei = int(amount * 10**18)
        return self.send_transaction('unstakeTokens', amount_wei)
    
    def claim_staking_rewards(self):
        """Claim staking rewards"""
        return self.send_transaction('claimStakingRewards')
    
    def get_staking_info(self, address):
        """Get staking information for address"""
        info = self.call_function('stakingInfo', address)
        if info:
            return {
                'staked_amount': info[0] / 10**18,
                'staking_timestamp': info[1],
                'rewards_earned': info[2] / 10**18
            }
        return None

class BlockDAGPresale(SmartContract):
    """BlockDAG Presale Contract Interactions"""
    
    def __init__(self, blockchain_manager, abi=None):
        super().__init__(PRESALE_CONTRACT_ADDRESS, abi, blockchain_manager)
    
    def buy_tokens_eth(self, eth_amount):
        """Buy tokens with ETH"""
        eth_wei = int(eth_amount * 10**18)
        return self.send_transaction('buyTokensETH', value=eth_wei)
    
    def get_presale_info(self):
        """Get presale information"""
        info = self.call_function('getPresaleInfo')
        if info:
            return {
                'current_price': info[0] / 10**18,
                'tokens_sold': info[1] / 10**18,
                'eth_raised': info[2] / 10**18,
                'presale_active': info[3],
                'min_purchase': info[4] / 10**18,
                'max_purchase': info[5] / 10**18
            }
        return None
    
    def get_user_purchases(self, address):
        """Get user purchase information"""
        purchases = self.call_function('userPurchases', address)
        if purchases:
            return {
                'total_eth_spent': purchases[0] / 10**18,
                'total_tokens_bought': purchases[1] / 10**18,
                'referral_rewards': purchases[2] / 10**18,
                'can_claim': purchases[3]
            }
        return None
    
    def claim_tokens(self):
        """Claim purchased tokens after presale ends"""
        return self.send_transaction('claimTokens')
    
    def add_btc_purchase(self, user_address, btc_amount, btc_tx_hash):
        """Admin function: Add BTC purchase"""
        btc_wei = int(btc_amount * 10**18)
        return self.send_transaction('addBTCPurchase', user_address, btc_wei, btc_tx_hash)

class BlockDAGMining(SmartContract):
    """BlockDAG Mining Contract Interactions"""
    
    def __init__(self, blockchain_manager, abi=None):
        super().__init__(MINING_CONTRACT_ADDRESS, abi, blockchain_manager)
    
    def claim_mobile_mining(self):
        """Claim daily mobile mining rewards"""
        return self.send_transaction('claimMobileMining')
    
    def purchase_hardware_miner(self, miner_type):
        """Purchase hardware miner (X10, X30, X100)"""
        prices = {
            'X10': 0.1,   # Example prices in ETH
            'X30': 0.3,
            'X100': 1.0
        }
        
        if miner_type not in prices:
            print("❌ Invalid miner type. Use X10, X30, or X100")
            return None
            
        price_wei = int(prices[miner_type] * 10**18)
        return self.send_transaction('purchaseHardwareMiner', miner_type, value=price_wei)
    
    def activate_miner(self, miner_id):
        """Activate purchased miner"""
        return self.send_transaction('activateMiner', miner_id)
    
    def claim_miner_rewards(self, miner_id):
        """Claim rewards from hardware miner"""
        return self.send_transaction('claimMinerRewards', miner_id)
    
    def get_user_miners(self, address):
        """Get user's miners information"""
        miners = self.call_function('getUserMiners', address)
        return miners
    
    def get_mining_stats(self, address):
        """Get mining statistics for address"""
        stats = self.call_function('getMiningStats', address)
        if stats:
            return {
                'mobile_last_claim': stats[0],
                'mobile_streak': stats[1],
                'total_mined': stats[2] / 10**18,
                'active_miners': stats[3]
            }
        return None

class BlockDAGWallet(SmartContract):
    """BlockDAG Telegram Wallet Contract Interactions"""
    
    def __init__(self, blockchain_manager, abi=None):
        super().__init__(WALLET_CONTRACT_ADDRESS, abi, blockchain_manager)
    
    def connect_telegram_wallet(self, telegram_user_id):
        """Connect wallet to Telegram user ID"""
        return self.send_transaction('connectTelegramWallet', telegram_user_id)
    
    def get_telegram_wallet(self, telegram_user_id):
        """Get wallet address for Telegram user"""
        return self.call_function('getTelegramWallet', telegram_user_id)
    
    def log_transaction(self, tx_type, amount, to_address, description):
        """Log transaction for history tracking"""
        amount_wei = int(amount * 10**18)
        return self.send_transaction('logTransaction', tx_type, amount_wei, to_address, description)
    
    def get_transaction_history(self, address, limit=10):
        """Get transaction history for address"""
        history = self.call_function('getTransactionHistory', address, limit)
        return history
    
    def set_daily_limit(self, limit_amount):
        """Set daily spending limit"""
        limit_wei = int(limit_amount * 10**18)
        return self.send_transaction('setDailyLimit', limit_wei)
    
    def get_daily_limit(self, address):
        """Get daily spending limit"""
        limit = self.call_function('getDailyLimit', address)
        if limit is not None:
            return limit / 10**18
        return 0
    
    def freeze_wallet(self, wallet_address):
        """Freeze wallet for security"""
        return self.send_transaction('freezeWallet', wallet_address)
    
    def unfreeze_wallet(self, wallet_address):
        """Unfreeze wallet"""
        return self.send_transaction('unfreezeWallet', wallet_address)

class ContractManager:
    """Manager for all smart contracts"""
    
    def __init__(self, private_key=None):
        """Initialize all contracts"""
        self.blockchain = BlockDAGManager()
        
        if private_key:
            self.blockchain.setup_account(private_key)
        
        # Initialize contracts (ABIs need to be provided)
        self.token = None
        self.presale = None  
        self.mining = None
        self.wallet = None
    
    def setup_contracts(self, token_abi, presale_abi, mining_abi, wallet_abi):
        """Setup all contracts with their ABIs"""
        self.token = BlockDAGToken(self.blockchain, token_abi)
        self.presale = BlockDAGPresale(self.blockchain, presale_abi)
        self.mining = BlockDAGMining(self.blockchain, mining_abi)
        self.wallet = BlockDAGWallet(self.blockchain, wallet_abi)
        
        print("✅ All contracts initialized successfully!")
    
    def get_user_overview(self, address):
        """Get complete user overview across all contracts"""
        overview = {
            'address': address,
            'bdag_balance': self.blockchain.get_balance(address),
            'network_info': self.blockchain.get_network_info()
        }
        
        if self.token:
            overview['token_balance'] = self.token.get_balance(address)
            overview['staking_info'] = self.token.get_staking_info(address)
        
        if self.presale:
            overview['presale_purchases'] = self.presale.get_user_purchases(address)
        
        if self.mining:
            overview['mining_stats'] = self.mining.get_mining_stats(address)
            overview['miners'] = self.mining.get_user_miners(address)
        
        if self.wallet:
            overview['daily_limit'] = self.wallet.get_daily_limit(address)
        
        return overview