from flask import render_template, request, flash, redirect, url_for
from app import *
import random


def bytes32_to_string(x):
    output = x.hex().rstrip("0")
    if len(output) % 2 != 0:
        output = output + '0'
    output = bytes.fromhex(output).decode('utf8')
    return output


@app.route('/', defaults={'account_no': None}, methods=['GET', 'POST'])
@app.route('/account/set/<string:account_no>', methods=['POST'])
def homepage(account_no):
    if request.method == 'GET':
        accounts = [server.toChecksumAddress(i) for i in server.eth.accounts]
        return render_template('homepage.html', accounts=accounts)
    elif request.method == 'POST':
        session['account'] = account_no
        return redirect(url_for('vote'))


@app.route('/vote', methods=['GET'])
def vote():
    if request.method == 'GET':
        randao = server.eth.contract(address=CONTRACT_ADDRESS,
                                     abi=CONTRACT_ABI)

        redirected = session.get('redirect', False)

        if not redirected:
            random_number = random.randint(1, 100)
            print("Random Number", random_number)
            rand_hash = randao.functions.getHash(random_number).call()
            session['seed'] = random_number
            session['hash'] = rand_hash
            randao_gen = session.get('randao', 0) % 10000000000
            return render_template('randao.html', number=random_number, hash=rand_hash, prev_rand=randao_gen)
        else:
            rand_hash = session.get('hash', "".encode('utf-8'))
            seed = session.get('seed', 0)
            return render_template('randao.html', number=seed, hash=rand_hash)


@app.route('/send_sha3', methods=['GET'])
def send_sha3():
    rand_hash = session.get('hash', "".encode('utf-8'))

    randao = server.eth.contract(address=CONTRACT_ADDRESS,
                                 abi=CONTRACT_ABI)

    account = session.get('account', DEFAULT_ACCOUNT)
    tx_hash = randao.functions.sendSHA3(rand_hash).transact({'from': account})
    receipt = server.eth.waitForTransactionReceipt(tx_hash)
    session['redirect'] = True
    return redirect(url_for('vote'))


@app.route('/send_seed', methods=['GET'])
def send_seed():
    seed = session.get('seed', 0)

    randao = server.eth.contract(address=CONTRACT_ADDRESS,
                                 abi=CONTRACT_ABI)

    account = session.get('account', DEFAULT_ACCOUNT)
    tx_hash = randao.functions.sendKey(seed).transact({'from': account})
    receipt = server.eth.waitForTransactionReceipt(tx_hash)
    session['redirect'] = False

    tx_hash = randao.functions.evaluate().transact({'from': account})
    receipt = server.eth.waitForTransactionReceipt(tx_hash)

    result = randao.functions.getDaoRandomNumber().call()
    session['randao'] = result

    return redirect(url_for('vote'))
