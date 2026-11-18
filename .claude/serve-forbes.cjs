const http=require('http'),fs=require('fs'),path=require('path');
const root='/Users/katrinayoung/Downloads/forbes-riley-site/dist';
const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4','.svg':'image/svg+xml'};
http.createServer((req,res)=>{let p=decodeURIComponent(req.url.split('?')[0]);if(p.endsWith('/'))p+='index.html';const f=path.join(root,p);
fs.readFile(f,(e,d)=>{if(e){res.writeHead(404);return res.end('nope')}res.writeHead(200,{'Content-Type':types[path.extname(f)]||'application/octet-stream'});res.end(d)})}).listen(8787,()=>console.log('up 8787'));
