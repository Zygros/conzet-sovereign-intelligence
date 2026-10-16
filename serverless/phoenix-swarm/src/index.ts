export interface Env {
  SWARM: DurableObjectNamespace;
  SWARM_TOKEN: string;
  ALLOWED_ORIGIN: string;
  MAX_CONCURRENCY?: string;
}
type TaskStatus = "QUEUED" | "RUNNING" | "SUCCEEDED" | "FAILED" | "CANCELLED";
type Task = { id:string; idempotencyKey:string; role:string; input:{operation:"echo"|"sum"; values?:number[]; text?:string}; status:TaskStatus; createdAt:string; updatedAt:string; attempts:number; result?:unknown; error?:string; receiptHash?:string };
type Receipt = { seq:number; taskId:string; event:string; timestamp:string; data:unknown; previousHash:string; hash:string };
const json=(data:unknown,status=200)=>new Response(JSON.stringify(data),{status,headers:{"content-type":"application/json; charset=utf-8","cache-control":"no-store"}});
const hex=(b:ArrayBuffer)=>Array.from(new Uint8Array(b)).map(x=>x.toString(16).padStart(2,"0")).join("");
async function digest(s:string){return hex(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(s)))}
function cors(req:Request,env:Env,resp:Response){const origin=req.headers.get("Origin");const h=new Headers(resp.headers);if(origin && origin===env.ALLOWED_ORIGIN){h.set("Access-Control-Allow-Origin",origin);h.set("Vary","Origin");h.set("Access-Control-Allow-Headers","Authorization,Content-Type,Idempotency-Key");h.set("Access-Control-Allow-Methods","GET,POST,OPTIONS")}return new Response(resp.body,{status:resp.status,headers:h})}
export class SwarmCoordinator {
 state:DurableObjectState; env:Env;
 constructor(state:DurableObjectState,env:Env){this.state=state;this.env=env}
 async fetch(req:Request):Promise<Response>{
  const url=new URL(req.url); const tasks=this.state.storage;
  if(req.method==="GET"&&url.pathname==="/health")return json({ok:true,mode:"LIVE",coordinator:"Durable Object",timestamp:new Date().toISOString()});
  if(req.method==="POST"&&url.pathname==="/tasks"){
   let body:any;try{body=await req.json()}catch{return json({error:"invalid_json"},400)}
   if(!body||!["echo","sum"].includes(body.operation))return json({error:"unsupported_operation"},400);
   if(body.operation==="sum"&&(!Array.isArray(body.values)||body.values.length<1||body.values.length>100||body.values.some((v:unknown)=>typeof v!=="number"||!Number.isFinite(v))))return json({error:"values_must_be_1_to_100_finite_numbers"},400);
   if(body.operation==="echo"&&(typeof body.text!=="string"||body.text.length>2000))return json({error:"text_must_be_string_under_2000_chars"},400);
   const key=req.headers.get("Idempotency-Key");if(!key||key.length>128)return json({error:"idempotency_key_required"},400);
   const idem=await tasks.get<string>("idem:"+key);if(idem){const old=await tasks.get<Task>("task:"+idem);if(old)return json({task:old,idempotentReplay:true})}
   const all=await tasks.get<Task[]>("tasks")||[];const active=all.filter(t=>t.status==="QUEUED"||t.status==="RUNNING").length;const cap=Math.min(10,Math.max(1,Number(this.env.MAX_CONCURRENCY)||3));if(active>=cap)return json({error:"concurrency_limit",limit:cap},429);
   const now=new Date().toISOString();const id=crypto.randomUUID();const task:Task={id,idempotencyKey:key,role:"Phoenix bounded deterministic executor",input:body.operation==="sum"?{operation:"sum",values:body.values}:{operation:"echo",text:body.text},status:"QUEUED",createdAt:now,updatedAt:now,attempts:0};
   all.push(task);await tasks.put("tasks",all);await tasks.put("task:"+id,task);await tasks.put("idem:"+key,id);await this.receipt(task,"DISPATCHED",{mode:"LIVE",operation:body.operation});
   // This first adapter deliberately supports deterministic operations only; no fake model agents.
   task.status="RUNNING";task.attempts=1;task.updatedAt=new Date().toISOString();await tasks.put("task:"+id,task);await this.receipt(task,"EXECUTION_STARTED",{worker:"Durable Object",attempt:1});
   try{task.result=task.input.operation==="sum"?(task.input.values||[]).reduce((a,b)=>a+b,0):task.input.text;task.status="SUCCEEDED";task.updatedAt=new Date().toISOString();const verification=task.input.operation==="sum"?typeof task.result==="number"&&Number.isFinite(task.result):task.result===task.input.text;if(!verification)throw new Error("independent_verification_failed");await this.receipt(task,"VERIFIED",{passed:true,resultType:typeof task.result});}
   catch{task.status="FAILED";task.error="execution_or_verification_failed";task.updatedAt=new Date().toISOString();await this.receipt(task,"FAILED",{reason:task.error})}
   await tasks.put("task:"+id,task);await tasks.put("tasks",all.map(t=>t.id===id?task:t));return json({task,mode:"LIVE",workerType:"deterministic-serverless",externalModelAgent:false},201)
  }
  const m=url.pathname.match(/^\/tasks\/([\w-]+)(?:\/(cancel|receipts|verify))?$/);
  if(m){const id=m[1];let task=await tasks.get<Task>("task:"+id);if(!task)return json({error:"task_not_found"},404);
   if(req.method==="POST"&&m[2]==="cancel"){if(task.status==="SUCCEEDED"||task.status==="FAILED"||task.status==="CANCELLED")return json({task,changed:false});task.status="CANCELLED";task.updatedAt=new Date().toISOString();await tasks.put("task:"+id,task);await tasks.put("tasks",(await tasks.get<Task[]>("tasks")||[]).map(t=>t.id===id?task:t));await this.receipt(task,"CANCELLED",{requested:true});return json({task})}
   if(req.method==="GET"&&m[2]==="receipts")return json({taskId:id,receipts:await tasks.get<Receipt[]>("receipts:"+id)||[]});
   if(req.method==="GET"&&m[2]==="verify"){const rs=await tasks.get<Receipt[]>("receipts:"+id)||[];let prev="0".repeat(64);let valid=true;for(const r of rs){const h=await digest(JSON.stringify({seq:r.seq,taskId:r.taskId,event:r.event,timestamp:r.timestamp,data:r.data,previousHash:r.previousHash}));if(r.previousHash!==prev||r.hash!==h)valid=false;prev=r.hash}return json({taskId:id,valid,receiptCount:rs.length,headHash:prev})}
   if(req.method==="GET"&&!m[2])return json({task})
  }
  return json({error:"not_found"},404)
 }
 async receipt(task:Task,event:string,data:unknown){const key="receipts:"+task.id;const rs=await this.state.storage.get<Receipt[]>(key)||[];const previousHash=rs.length?rs[rs.length-1].hash:"0".repeat(64);const base={seq:rs.length+1,taskId:task.id,event,timestamp:new Date().toISOString(),data,previousHash};rs.push({...base,hash:await digest(JSON.stringify(base))});await this.state.storage.put(key,rs)}
}
export default {async fetch(req:Request,env:Env):Promise<Response>{
 const url=new URL(req.url);const origin=req.headers.get("Origin");if(req.method==="OPTIONS"){if(origin&&origin!==env.ALLOWED_ORIGIN)return json({error:"origin_not_allowed"},403);return cors(req,env,new Response(null,{status:204}))}
 if(origin&&origin!==env.ALLOWED_ORIGIN)return json({error:"origin_not_allowed"},403);
 if(url.pathname==="/health"&&req.method==="GET")return cors(req,env,json({ok:true,mode:"LIVE",coordinator:"Cloudflare Durable Objects"}));
 const auth=req.headers.get("Authorization");if(!env.SWARM_TOKEN||auth!=="Bearer "+env.SWARM_TOKEN)return cors(req,env,json({error:"unauthorized"},401));
 const id=env.SWARM.idFromName("phoenix-global-coordinator-v1");return cors(req,env,await env.SWARM.get(id).fetch(req))
}};
