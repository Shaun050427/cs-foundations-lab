(function(root){
'use strict';
function rng(seed=42){let s=seed>>>0;return()=>{s=(Math.imul(1664525,s)+1013904223)>>>0;return s/4294967296}}
function shuffled(a,seed=42){const r=rng(seed),b=[...a];for(let i=b.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[b[i],b[j]]=[b[j],b[i]]}return b}
function sorting(input,kind='insertion'){
 if(!Array.isArray(input)||input.length>48||input.some(x=>!Number.isFinite(x)))throw Error('请输入不超过48个有限数字');
 const a=[...input],frames=[];let comparisons=0,writes=0;
 const snap=(message,active=[])=>frames.push({array:[...a],comparisons,writes,message,active});snap('原始输入');
 if(kind==='insertion')for(let i=1;i<a.length;i++){const key=a[i];let j=i-1;snap(`取出索引 ${i} 的值 ${key}`,[i]);while(j>=0){comparisons++;snap(`比较 ${a[j]} 与 ${key}`,[j,i]);if(a[j]<=key)break;a[j+1]=a[j];writes++;snap('向右移动一个元素',[j,j+1]);j--}a[j+1]=key;writes++;snap(`把 ${key} 放入索引 ${j+1}`,[j+1])}
 else if(kind==='merge')for(let width=1;width<a.length;width*=2)for(let lo=0;lo<a.length;lo+=width*2){const mid=Math.min(lo+width,a.length),hi=Math.min(lo+width*2,a.length),left=a.slice(lo,mid),right=a.slice(mid,hi);let i=0,j=0,k=lo;snap(`合并 [${lo},${mid}) 与 [${mid},${hi})`);while(i<left.length||j<right.length){if(i<left.length&&j<right.length){comparisons++;snap('比较两个子序列的头部',[lo+i,mid+j])}a[k]=j>=right.length||(i<left.length&&left[i]<=right[j])?left[i++]:right[j++];writes++;snap(`写入索引 ${k}`,[k++])}}
 else throw Error('未知算法');
 snap('排序完成');return frames;
}
function cacheTrace(addresses,{lines=4,block=4}={}){
 if(!Number.isInteger(lines)||lines<1||lines>64||!Number.isInteger(block)||block<1||block>64)throw Error('非法缓存配置');
 const slots=Array(lines).fill(null),frames=[];let hits=0,misses=0;
 for(const address of addresses){if(!Number.isSafeInteger(address)||address<0)throw Error('地址必须为非负整数');const blockId=Math.floor(address/block),slot=blockId%lines,hit=slots[slot]===blockId;hit?hits++:misses++;slots[slot]=blockId;frames.push({address,blockId,slot,hit,hits,misses,slots:[...slots]})}return frames;
}
const graph=[[1,2],[0,3,4],[0,5],[1,6],[1,6],[2,7],[3,4,7],[5,6]];
function traversal(kind='bfs',start=0,adj=graph){
 if(!['bfs','dfs'].includes(kind)||!Number.isInteger(start)||start<0||start>=adj.length)throw Error('非法遍历配置');
 const pending=[start],seen=new Set([start]),order=[],frames=[];
 while(pending.length){const node=kind==='bfs'?pending.shift():pending.pop();order.push(node);const neighbors=kind==='bfs'?adj[node]:[...adj[node]].reverse();for(const next of neighbors)if(!seen.has(next)){seen.add(next);pending.push(next)}frames.push({node,order:[...order],pending:[...pending],discovered:[...seen]})}return frames;
}
function byte(n){if(!Number.isInteger(n)||n<0||n>255)throw Error('请输入0至255的整数');return{binary:n.toString(2).padStart(8,'0'),unsigned:n,signed:n>=128?n-256:n,hex:n.toString(16).toUpperCase().padStart(2,'0')}}
const api={rng,shuffled,sorting,cacheTrace,traversal,graph,byte};if(typeof module==='object'&&module.exports)module.exports=api;else root.CSLab=api;
})(globalThis);
