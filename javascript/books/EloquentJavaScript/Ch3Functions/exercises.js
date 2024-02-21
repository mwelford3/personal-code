// Question 1
function minimum(x, y)
{
    if (x < y)
        return x;
    else
        return y;
};

console.log(minimum(20, 10));

// Question 2
function even_odd(num)
{
    if (num < 0)
        num = -num;
    if (num == 0)
        console.log('even');
    else if (num == 1)
        console.log('odd');
    else
        even_odd(num - 2); 
};

even_odd(50);
even_odd(75);
even_odd(-1);


// Question 3
function countBs(s)
{
    let count = countChar(s, 'B');

    return count;
};

function countChar(s, ch)
{
    let count = 0;
    
    for (let i = 0; i < s.length; i++)
    {
        if (s[i] == ch)
            count++;
    }

    return count;
};

console.log(countBs('BaB'));
console.log(countChar('Apple', 'p'));
