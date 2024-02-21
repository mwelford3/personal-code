const main = function()
{
    console.log("Hello Main");
};

function test(func, value)
{
    func(value);
}

test((x) => {console.log(x*2);}, 5);


let test3 = (x, y)=>{return x < y;};

const readline = require('readline');
let num = readline();

console.log(num);
