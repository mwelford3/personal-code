/*
* Title: chessboard.js
* Author: Michael Welford
*/

let line = '# # # #';
let size = 4;
for (let i = 0; i < size; i++)
{
    if (i%2 == 0)
        console.log(' ' + line);
    else
        console.log(line);
}
