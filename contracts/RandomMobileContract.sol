pragma solidity ^0.4.22;

contract RandomMobileContract {

    address public owner;
    address[] public participants;
    mapping(address => bytes32) public addressSha3Mmap;
    mapping(address => uint) public addressKeyMap;
    uint maxSeeds;
    uint correctSeeds;
    uint256 daoNumber;

    constructor (uint seeds) public {
        maxSeeds = seeds;
        owner = msg.sender;
        correctSeeds = 0;
    }

    function sendSHA3(bytes32 sha3_hash) public returns (bool) {
        if (addressSha3Mmap[msg.sender] == 0) {
            addressSha3Mmap[msg.sender] = sha3_hash;
            return true;
        }
        return false;
    }

    function evaluate() public {
        require(maxSeeds > 0);
        bytes32 randomNumber = getHash(addressKeyMap[participants[0]]);
        for(uint i = 1; i < participants.length; i++) {
            randomNumber = getHash(addressKeyMap[participants[i]] + uint256(randomNumber));
        }
        daoNumber =  uint256(randomNumber);
    }

    function getDaoRandomNumber() public view returns(uint256) {
        return daoNumber;
    }

    function getHash(uint number) public pure returns(bytes32) {
        return keccak256(abi.encodePacked(number));
    }

    function sendKey(uint key) public returns (bool) {
        if (addressKeyMap[msg.sender] == 0 ) {
            require(addressSha3Mmap[msg.sender] == getHash(key));
            addressKeyMap[msg.sender] = key;
            correctSeeds += 1;

            // Add participant only if valid transaction.
            participants.push(msg.sender);
            if (correctSeeds == maxSeeds) {
                evaluate();
            }
            return true;
        }
        return false;
    }
}
