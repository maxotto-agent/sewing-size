const fs=require('fs');
const html=fs.readFileSync('index.html','utf8');
fs.writeFileSync('/tmp/l.js',html.split('<script>')[1].split('</script>')[0]);
const {compute,DATA}=require('/tmp/l.js');const cm=x=>x*2.54;
const get=(b,r)=>DATA.find(d=>d.brand===b&&d.range.startsWith(r));
let fail=0;const eq=(a,b,n)=>{if(a!==b){fail++;console.log('FAIL',n,a,b)}};
const L=o=>o.text||o.labels.join('/');
const m={hb:cm(38),b:cm(42),w:cm(35),h:cm(46)};
const cc=compute(get('Closet Core','D cup'),m);
eq(L(cc.bust),'14','CC D bust');eq(cc.why,'full bust','CC D rule');
const cb=compute(get('Closet Core','B cup'),m);
eq(cb.why,'high bust','CC B uses high bust');eq(L(cb.hip),'18','CC B hip');
eq(compute(get('Style Arc','Sizes'),{hb:cm(25),b:cm(27),w:cm(20),h:cm(28)}).grade,'Outside this range','small out');
console.log(fail?'FAILED':'all passed');process.exit(fail?1:0)
