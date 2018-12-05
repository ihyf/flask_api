pragma solidity ^0.4.0;

contract Play{
    uint private bonus;
    address private owner;
    mapping(bool=>address)private playerBetting;
    address[] odd;
    address[] double;

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
    function betting(bool _guess)payable public{
        require(msg.value>=bonus);
        if(msg.value>bonus){
            msg.sender.transfer(msg.value-bonus);
        }
        if(_guess){
            odd.push(msg.sender);
        }else{
            double.push(msg.sender);
        }
    }

    //获得结果
    function getResult() payable public onlyOwner returns(uint){
        uint total = bonus*2;
        bool result;
        uint number;
        (result,number) = getNumber();
        if(result){
            for(uint i=0;i<odd.length;i++){
                odd[i].transfer(this.balance/odd.length);
            }
        }else{
            for(uint j=0;j<double.length;j++){
                double[j].transfer(this.balance/double.length);
            }
        }
        return number;
    }

    //获得摇出点数
    function getNumber() view private returns(bool,uint){
        uint nonce = 0;
        while(true){
            uint random = uint32(keccak256(now, msg.sender,nonce)) % 7;
            if(random!=0){
                break;
            }
            nonce++;
        }
        if(random%2 ==0){//双
            return (false,random);
        }else{//单
            return (true,random);
        }
    }

}
