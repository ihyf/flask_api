pragma solidity ^0.4.0;

contract Play{
    uint private bonus;
    address private owner;
    address[] odd;
    address[] double;
    uint32 number;
    //构造函数
    constructor() public{
        bonus = 1 ether;
        owner = msg.sender;
    }

    //修饰符
    modifier onlyOwner{
        require(owner == msg.sender);
        _;
    }

    //下注
    function betting(bool _guess)payable public returns(bool){
        require(msg.value>=bonus);
        if(msg.value>bonus){
            msg.sender.transfer(msg.value-bonus);
        }
        if(_guess){
            odd.push(msg.sender);
        }else{
            double.push(msg.sender);
        }
        return true;
    }

    //获得结果
    function getResult() payable public onlyOwner returns(uint){
        bool result;
        uint number;
        address[] memory champion;
        (result,number) = getNumber();
        if(result){
            champion = odd;
        }else{
           champion = double;
        }
        if(champion.length==0 && result){
            champion = double;
        }else if(champion.length==0 && !result){
            champion = odd;
        }
        for(uint i=0;i<champion.length;i++){
            champion[i].transfer(address(this).balance/champion.length);
        }
        delete champion;
        delete odd;
        delete double;
        return number;
    }
    //获得摇出点数
    function getNumber() view private returns(bool,uint){
        uint nonce = 0;
        while(true){
            uint32 random;
            random = uint32(keccak256(now, msg.sender,nonce)) % 7;
            if(random!=0){
                break;
            }
            nonce++;
        }
        number = random;
        if(random%2 ==0){//双
            return (false,random);
        }else{//单
            return (true,random);
        }
    }
    //获取骰子点数
    function getRandom()view public returns(uint){
        return number;
    }

}
