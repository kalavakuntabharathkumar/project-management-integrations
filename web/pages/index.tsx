import {useEffect,useState} from "react";
export default function Home(){const [projects,setProjects]=useState<any[]>([]);
useEffect(()=>{fetch("http://localhost:8000/projects").then(r=>r.json()).then(setProjects).catch(()=>{})},[]);
return <main style={{fontFamily:"system-ui",maxWidth:900,margin:"50px auto"}}><h1>Project Management Suite</h1><p>Projects, tasks, dependencies and integrations</p><h2>Projects</h2><ul>{projects.map(p=><li key={p.id}>{p.name} — {p.owner}</li>)}</ul><h2>Integrations</h2><p>Slack · Google Calendar · Stripe · S3 documents · RabbitMQ</p></main>}
