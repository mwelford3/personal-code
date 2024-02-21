/* 
* fizzbuzz.js
* Author: Michael Welford
*/

for (let number = 1; number <= 100; number++){
    // Number is divisible by 3.
    if (number % 3 == 0){
        // Number is also divisible by 5.
        if (number % 5 == 0)
            console.log("FizzBuzz");
        // Only by 3.
        else
            console.log("Fizz");
    }
    
    // Number is divisible only by 5.
    else if (number % 5 == 0)
        console.log("Buzz");
    // Number is not divisible by 3 or 5.
    else
        console.log(number);
}
