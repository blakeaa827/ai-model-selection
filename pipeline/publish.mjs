// Atomic Git data publication. Never log credentials; no force pushes or partial report commits.
import {readFile,writeFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
const repo='blakeaa827/ai-model-selection';
export async function api(path,method='GET',body){
 const token=process.env.GITHUB_TOKEN;
 if(!token)throw Error('GitHub publication token unavailable; staged valid report retained');
 const res=await fetch('https://api.github.com/repos/'+repo+'/'+path,{method,headers:{Authorization:'Bearer '+token,Accept:'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(45000)});
 if(!res.ok)throw Error(`GitHub ${method} ${path.split('?')[0]} HTTP ${res.status}`);
 return res.json();
}
export async function head(){return (await api('branches/main')).commit;}
export async function baseline(sha){
 for(const path of ['latest.json','coverage.json','README.md']){
  const file=await api('contents/'+path+'?ref='+encodeURIComponent(sha));
  if(file.encoding!=='base64')throw Error('Unexpected repository content encoding');
  await writeFile(path,Buffer.from(file.content.replace(/\s/g,''),'base64'));
 }
}
export async function publish(root,parent){
 const d=JSON.parse(await readFile(root+'/latest.json','utf8'));
 const initial=await head();
 if(initial.sha!==parent)throw Error('CONCURRENT_MAIN_CHANGED');
 const validation=JSON.parse(await readFile('run-artifacts/validation.json','utf8'));
 if(validation.status!=='passed')throw Error('Validation has not passed');
 const paths=['latest.json','latest.md','coverage.json','README.md','cost-curve.svg','snapshots/'+d.report_date+'.json'];
 const entries=[];
 for(const path of paths){
  const content=await readFile(root+'/'+path,'utf8');
  if(createHash('sha256').update(content).digest('hex')!==validation.file_hashes_sha256?.[path])throw Error('Validated artifact changed before publication: '+path);
  const blob=await api('git/blobs','POST',{content,encoding:'utf-8'});
  const expected=createHash('sha1').update(Buffer.from('blob '+Buffer.byteLength(content)+'\0')).update(content).digest('hex');
  if(blob.sha!==expected)throw Error('GitHub blob content verification failed');
  entries.push({path,mode:'100644',type:'blob',sha:blob.sha});
 }
 const tree=await api('git/trees','POST',{base_tree:initial.commit.tree.sha,tree:entries});
 const commit=await api('git/commits','POST',{message:'Refresh model selection '+d.report_date+'\n\nVerified public AA configuration records, live canonical routes, complete coverage, marginal costs and conditional subscription guidance. Preserve prior snapshots.',tree:tree.sha,parents:[initial.sha]});
 if((await head()).sha!==parent)throw Error('CONCURRENT_MAIN_CHANGED');
 await api('git/refs/heads/main','PATCH',{sha:commit.sha,force:false});
 const final=await head();
 for(const entry of entries){
  const file=await api('contents/'+entry.path+'?ref=main');
  if(file.sha!==entry.sha)throw Error('Remote report differs after publication: '+entry.path);
 }
 await writeFile('run-artifacts/publication.json',JSON.stringify({status:'published_and_verified',commit:commit.sha,main_commit:final.sha,report_date:d.report_date,files:paths},null,2)+'\n');
 console.log('Published and verified commit '+commit.sha);
 return commit.sha;
}
