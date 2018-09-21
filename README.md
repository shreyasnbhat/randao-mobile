## RANDAO Mobile

#### Prerequisites
- Setup `ganache-cli` and `truffle`.
- Run `pip3 install --user -r requirements.txt` to setup all required packages.
- In the root directory, run `truffle compile`.
- Run `ganache-cli` on `localhost:7545` and then run `truffle migrate` to deploy the smart contracts on `ganache`.
- Run `python3 run.py d 5000` to run the RANDAO app. 

#### The DApp
The `RANDAO` mobile app aims to generate a random number using mobile nodes. Random number generation in inherently important in the encryption, scientific modelling, gambling, lotteries etc. The `DAO(Decentralized Autonomous Organization)` that has been built takes inspiration from the current `RANDAO` implementation used by the `Ethereum` framework.

Currently, a personal blockchain framework called `Ganache` is being used to test out the `smart-contract`. A `flask` based client app has been written to interact with the `smart-contract`.

