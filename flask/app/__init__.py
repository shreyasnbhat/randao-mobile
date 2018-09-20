from flask import Flask, session
from web3 import Web3, HTTPProvider
import json
from flask_session import Session

# Flask App initialization
app = Flask(__name__)
app.secret_key = 'secret_key'

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

server = Web3(HTTPProvider('http://localhost:7545'))

CONTRACT_ADDRESS = server.toChecksumAddress("0x3eba6ff915ec245a832042fffa63d7a615384836")
DEFAULT_ACCOUNT = server.toChecksumAddress("0xf847465aaC31C383540B56eb2B5a57f2C8192172")

with open('../build/contracts/RandomMobileContract.json') as f:
    voter_contract_data = json.load(f)

CONTRACT_ABI = voter_contract_data['abi']

from app import views
