let n = 3;
let op = "";
let num=1

for (let i = 1; i <= n; i++) {
    for (let j = 1; j <= n; j++) {
      op+= num + " ";
      num++;
    
    }

    op += "\n";
}

console.log(op);
