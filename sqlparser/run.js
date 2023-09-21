
// const { Parser } = require('@florajs/sql-parser');
// const parser = new Parser();
// // const ast = parser.parse('SELECT * FROM t');
// const ast = parser.parse('SELECT DISTINCT country_name FROM Beneficiary JOIN Transactions ON Transactions.beneficiary_id = Beneficiary.beneficiary_id WHERE client_id=996720');
// console.log(JSON.stringify(ast, null, 2));

const { Parser } = require('@florajs/sql-parser');
const parser = new Parser();

// 获取命令行参数
const sql_query = process.argv[2];


const ast = parser.parse(sql_query);
console.log(JSON.stringify(ast, null, 2));
