pragma solidity ^0.4.0;

contract luckyNumber{
    
    uint32 gameType;//游戏类型
    uint gameBet;//该场次下注金额
    address[][] numPlayer;//每个押注号码的玩家集合
    uint32  totalPlayerNum = 0;
    mapping(address=>uint32) betPlayerNumber;//玩家地址=>编号
    mapping(uint32=>address) betPlayerAddress;//玩家编号=>地址
    mapping(uint32=>uint32) playerBetNumber;//玩家编号=>投注数
    address private owner;
    uint32 gameNumber;
    uint bonusMoney;
    uint myMoney;
    constructor()public{
        owner = msg.sender;
    }
    //修饰符
    modifier onlyOwner{
        require(owner == msg.sender);
        _;
    }
    //选择场次
    function setChooseGame(uint32 _num) public onlyOwner returns(bool){
        require(_num==3 || _num== 5 || _num==7);
        gameType = _num;
        if(_num==3){
            gameBet = 0.5 ether;
        }else if(_num==5){
            gameBet = 2 ether;
        }else{
            gameBet = 5 ether;
        }
        numPlayer = new address[][](_num+1);
        return true;
    }
    //下注
    function tBetting(uint32 _betNumber) payable public returns(bool){
        require(_betNumber<=gameType && _betNumber!=0);
        require(msg.value>=gameBet);
        require(betPlayerNumber[msg.sender]==0);
        if(msg.value>gameBet){
            msg.sender.transfer(msg.value-gameBet);
        }
        uint32 nonce;//玩家编号
        nonce = totalPlayerNum+1;
        betPlayerNumber[msg.sender] = nonce;
        betPlayerAddress[nonce] = msg.sender;
        playerBetNumber[nonce]=_betNumber;//记录玩家下注号码
        numPlayer[_betNumber].push(msg.sender);
        totalPlayerNum++;
        return true;
    }
    //获得结果,一分钟调用一次
    function tResult()payable public onlyOwner returns(uint32){
        uint32 result = getNumber();
        bonusMoney = address(this).balance * 82/100;
        myMoney = address(this).balance * 18/100;
        if(numPlayer[result].length==0){
            for(uint32 i=0;i<totalPlayerNum;i++){
                betPlayerAddress[i+1].transfer(bonusMoney/totalPlayerNum);
            }
        }else{
            for(uint j=0;j<numPlayer[result].length;j++){
                numPlayer[result][j].transfer(bonusMoney/numPlayer[result].length);
            } 
        }
        owner.transfer(myMoney);
        for(uint32 k=0;k<totalPlayerNum;k++){
            delete betPlayerNumber[betPlayerAddress[k+1]];
            delete betPlayerAddress[k+1];
            delete playerBetNumber[k+1];
        }
        delete numPlayer;
        numPlayer.length = gameType+1;
        delete totalPlayerNum;
        return result;
    }
    //获得摇出点数
    function getNumber() private returns(uint32){
        uint nonce = 0;
        while(true){
            uint32 random = uint32(keccak256(now, msg.sender,nonce)) % (gameType+1);
            if(random!=0){
                break;
            }
            nonce++;
        }
        gameNumber = random;
        return random;
    }
    //获取合约里的余额
    function getBalance()view public returns(uint){
        return address(this).balance;
    }
    //获取结果点数
    function getGameNum()view public returns(uint32){
        return gameNumber;
    }
    //获取奖池里的金额
    function getbonusMoney()view public returns(uint){
        return bonusMoney;
    }
    // function numPlayerl()view public returns(uint){
    //     return numPlayer[5].length;
    // }
    //获取庄家的分红
    function getMyMoney()view public returns(uint){
        return myMoney;
    }
    // function getOnePlayerAddr()view public returns(address){
    //     return betPlayerAddress[1];
    // } 
}
