# BlockDAG Network Configuration
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# BlockDAG Network Settings
BLOCKDAG_RPC_URL = "https://rpc.primordial.bdagscan.com"
BLOCKDAG_CHAIN_ID = 1043
BLOCKDAG_EXPLORER_URL = "https://primordial.bdagscan.com/"
CURRENCY_SYMBOL = "BDAG"
FAUCET_URL = "https://primordial.bdagscan.com/faucet"

# Contract Addresses (Your deployed contracts)
TOKEN_CONTRACT_ADDRESS = os.getenv('TOKEN_CONTRACT_ADDRESS', '0x62a61cB53761B7C6B0A65f034BD92d839db2a1EB')
PRESALE_CONTRACT_ADDRESS = os.getenv('PRESALE_CONTRACT_ADDRESS', '0xfa2d5f7239aa64eb9564b95d14ad2b2aefe11b03')
MINING_CONTRACT_ADDRESS = os.getenv('MINING_CONTRACT_ADDRESS', '0x45b74a182e44518cb1713f495c8cd8e8e393ba6c')
WALLET_CONTRACT_ADDRESS = os.getenv('WALLET_CONTRACT_ADDRESS', '0xc6f25071cdd6e8cac62733bb776fadbb27ca113a')

# Secrets from environment
PRIVATE_KEY = os.getenv('PRIVATE_KEY', '')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# Gas settings for transactions
DEFAULT_GAS_LIMIT = 300000
DEFAULT_GAS_PRICE = 20000000000  # 20 gwei

# Mining rewards (BDAG per day)
MOBILE_MINING_REWARD = 20  # X1 Miner
X10_MINING_REWARD = 200    # X10 Miner  
X30_MINING_REWARD = 600    # X30 Miner
X100_MINING_REWARD = 2000  # X100 Miner

# Presale settings
PRESALE_PRICE = 0.00164  # $0.00164 per BDAG
MIN_PURCHASE = 15        # $15 minimum
MAX_PURCHASE = 50000     # $50K maximum