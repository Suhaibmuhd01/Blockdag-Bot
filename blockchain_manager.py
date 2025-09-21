"""
BlockDAG Network Blockchain Manager
Handles connection to BlockDAG network and smart contract interactions
"""

from web3 import Web3
try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    geth_poa_middleware = None
import json
import os
from config import *

class BlockDAGManager:
    def __init__(self):
        """Initialize connection to BlockDAG network"""
        self.w3 = None
        self.account = None
        self.connect()
        
    def connect(self):
        """Connect to BlockDAG RPC endpoint"""
        try:
            # Connect to BlockDAG network
            self.w3 = Web3(Web3.HTTPProvider(BLOCKDAG_RPC_URL))
            
            # Add PoA middleware (required for some networks)
            if geth_poa_middleware:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Verify connection
            if self.w3.is_connected():
                print(f"✅ Connected to BlockDAG network (Chain ID: {BLOCKDAG_CHAIN_ID})")
                print(f"🌐 RPC URL: {BLOCKDAG_RPC_URL}")
                return True
            else:
                print("❌ Failed to connect to BlockDAG network")
                return False
                
        except Exception as e:
            print(f"❌ Connection error: {str(e)}")
            return False
    
    def setup_account(self, private_key):
        """Setup account from private key"""
        try:
            if not private_key:
                print("⚠️ No private key provided")
                return False
                
            if not self.w3:
                print("❌ Not connected to network")
                return False
            self.account = self.w3.eth.account.from_key(private_key)
            print(f"✅ Account loaded: {self.account.address}")
            return True
            
        except Exception as e:
            print(f"❌ Account setup error: {str(e)}")
            return False
    
    def get_balance(self, address=None):
        """Get BDAG balance for address"""
        try:
            if not address:
                address = self.account.address if self.account else None
                
            if not address:
                return 0
                
            if not self.w3:
                return 0
            balance_wei = self.w3.eth.get_balance(address)
            balance_bdag = self.w3.from_wei(balance_wei, 'ether')
            return float(balance_bdag)
            
        except Exception as e:
            print(f"❌ Balance check error: {str(e)}")
            return 0
    
    def get_gas_price(self):
        """Get current gas price"""
        try:
            if not self.w3:
                return DEFAULT_GAS_PRICE
            return self.w3.eth.gas_price
        except:
            return DEFAULT_GAS_PRICE
    
    def send_transaction(self, transaction):
        """Send a transaction to the network"""
        try:
            if not self.account:
                print("❌ No account setup")
                return None
                
            if not self.w3:
                print("❌ Not connected to network")
                return None
                
            # Add nonce and gas settings
            transaction['nonce'] = self.w3.eth.get_transaction_count(self.account.address)
            transaction['gas'] = transaction.get('gas', DEFAULT_GAS_LIMIT)
            transaction['gasPrice'] = transaction.get('gasPrice', self.get_gas_price())
            transaction['chainId'] = BLOCKDAG_CHAIN_ID
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.account.key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            print(f"🚀 Transaction sent: {tx_hash.hex()}")
            print(f"🔗 Explorer: {BLOCKDAG_EXPLORER_URL}tx/{tx_hash.hex()}")
            
            return tx_hash.hex()
            
        except Exception as e:
            print(f"❌ Transaction error: {str(e)}")
            return None
    
    def wait_for_transaction(self, tx_hash, timeout=120):
        """Wait for transaction confirmation"""
        try:
            if not self.w3:
                print("❌ Not connected to network")
                return None
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
            
            if receipt and hasattr(receipt, 'status') and receipt.status == 1:
                print(f"✅ Transaction confirmed: {tx_hash}")
                return receipt
            else:
                print(f"❌ Transaction failed: {tx_hash}")
                return None
                
        except Exception as e:
            print(f"❌ Transaction confirmation error: {str(e)}")
            return None
    
    def create_contract(self, address, abi):
        """Create contract instance"""
        try:
            if not address or not abi:
                print("❌ Contract address or ABI missing")
                return None
                
            if not self.w3:
                print("❌ Not connected to network")
                return None
                
            # Convert address to checksum format
            checksum_address = self.w3.to_checksum_address(address)
            contract = self.w3.eth.contract(address=checksum_address, abi=abi)
            return contract
            
        except Exception as e:
            print(f"❌ Contract creation error: {str(e)}")
            return None
    
    def get_network_info(self):
        """Get current network information"""
        try:
            if not self.w3:
                return None
            latest_block = self.w3.eth.get_block('latest')
            chain_id = self.w3.eth.chain_id
            
            info = {
                'chain_id': chain_id,
                'latest_block': latest_block.get('number', 0) if latest_block else 0,
                'block_time': latest_block.get('timestamp', 0) if latest_block else 0,
                'gas_price': self.get_gas_price(),
                'connected': self.w3.is_connected()
            }
            
            return info
            
        except Exception as e:
            print(f"❌ Network info error: {str(e)}")
            return None