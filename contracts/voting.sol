pragma solidity ^0.4.0;

contract Voting{

    struct Candidates{
        bytes32 candidateName;
        uint count;
    }
    struct Person{
        uint weight;
        address consigner;
        uint target;
        bool voted;
    }
    mapping(address=>Person) private Persons;
    Candidates[]private candidateArr;
    address private manager;
    
    /**
     * [setUpVote 创建投票]
     */
    function setUpVote(bytes32[] _candidates)public{
        for(uint i=0;i<_candidates.length;i++){
            candidateArr.push(Candidates({
                candidateName:_candidates[i],
                count:0
            }));
        }
        manager = msg.sender;
    }
    
    /**
     * [setPersonWeight 添加投票群众,仅投票创建人有权添加]
     */
    function setPersonWeight(address person) public{
        require(msg.sender == manager);
        Persons[person].weight = 1;
    }

    /**
     * [beginVote 投票]
     */
    function beginVote(uint id) public{
        Person storage sender =  Persons[msg.sender];
        require(!sender.voted);
        sender.voted = true;
        sender.target = id;
        candidateArr[id].count += sender.weight;
    }
    
    /**
     * [depute 委托他人投票]
     */
    function depute(address to) public{
        Person userInfo = Persons[msg.sender];
        require(!userInfo.voted && userInfo.weight!=0);
        require(to != msg.sender);
        while(Persons[to].consigner != address(0)){
            to = Persons[to].consigner;
            require(to != msg.sender);
        }
        Person storage deputeUserInfo = Persons[to];
        if(deputeUserInfo.voted){
            candidateArr[deputeUserInfo.target].count += userInfo.weight;
        }else{
            deputeUserInfo.weight += userInfo.weight;
        }
        userInfo.voted = true;
        userInfo.consigner = to;
    }

    /**
     * [finishVoting 投票统计]
     */
    function finishVoting() public view returns(string,uint){
        uint totalCount = 0;
        bytes32 candidateName;
        for(uint i=0;i<candidateArr.length;i++){
            if(candidateArr[i].count>totalCount){
                totalCount = candidateArr[i].count;
                candidateName = candidateArr[i].candidateName;
            }
        }
        return (_bytes32ToString(candidateName),totalCount);
    }

    //字节转字符串
    function _bytes32ToString(bytes32 candidateName) private returns(string){
        bytes memory bytesString = new bytes(32);
        uint charCount = 0;
        for (uint j = 0; j < 32; j++) {
            byte char = byte(bytes32(uint(candidateName) * 2 ** (8 * j)));
            if (char != 0) {
                bytesString[charCount] = char;
                charCount++;
            }
        }
        bytes memory bytesStringTrimmed = new bytes(charCount);
        for (j = 0; j < charCount; j++) {
            bytesStringTrimmed[j] = bytesString[j];
        }
        return string(bytesStringTrimmed);
    }

    function getString(string s) pure public returns(string){
        return "hello ihyf";
    }

    
}