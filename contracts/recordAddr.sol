pragma solidity ^0.4.25;

contract recordAddr{
    address [] contractAddr;
    
    //添加地址
    function setAddr(address _addr)public{
        contractAddr.push(_addr);
    }
    //返回所有地址
    function getAll()view public returns(address[]){
        return contractAddr;
    }
}
