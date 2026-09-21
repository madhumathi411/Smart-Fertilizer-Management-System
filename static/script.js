let currentData=null;

function showPage(id, step){
  document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  document.getElementById("stepText").textContent=`Step ${step} of 5`;
  window.scrollTo({top:0,behavior:"smooth"});
}

function login(){
  const u=document.getElementById("username").value.trim();
  const p=document.getElementById("password").value.trim();
  if(!u || !p){alert("Please enter username and password.");return;}
  showPage("profilePage",2);
}

function saveProfile(){
  const ids=["farmer_name","farm_name","email","phone"];
  for(const id of ids){
    if(!document.getElementById(id).value.trim()){alert("Please fill all farmer profile details.");return;}
  }
  showPage("dataPage",3);
}

async function analyze(){
  const fields=["farmer_name","farm_name","email","phone","crop","farm_area","moisture","nitrogen","phosphorus","potassium","temperature","humidity"];
  const form=new FormData();
  for(const id of fields) form.append(id,document.getElementById(id).value);
  try{
    const res=await fetch("/analyze",{method:"POST",body:form});
    const data=await res.json();
    if(!res.ok) throw new Error(data.error||"Analysis failed.");
    currentData=data;
    renderAnalysis(data);
    renderRecommendation(data);
    showPage("analysisPage",4);
  }catch(e){alert(e.message);}
}

function renderAnalysis(d){
  const labels=[
    ["Soil Moisture",d.values.moisture+" %",d.status.moisture],
    ["Nitrogen",d.values.nitrogen,d.status.nitrogen],
    ["Phosphorus",d.values.phosphorus,d.status.phosphorus],
    ["Potassium",d.values.potassium,d.status.potassium],
    ["Temperature",d.values.temperature+" °C",d.status.temperature],
    ["Humidity",d.values.humidity+" %",d.status.humidity]
  ];
  document.getElementById("summary").innerHTML=
    `<p><strong>Farmer:</strong> ${d.farmer.name} &nbsp; <strong>Crop:</strong> ${d.crop}</p>
     <div class="status-grid">${labels.map(x=>`<div class="status-card"><strong>${x[0]}</strong>${x[1]}<br>Status: <b>${x[2]}</b></div>`).join("")}</div>`;
}

function renderRecommendation(d){
  const r=d.recommendation;
  document.getElementById("recommendation").innerHTML=
    `<h3>Recommended Fertilizer</h3><p>${r.fertilizer}</p>
     <h3>Recommended Quantity</h3><p>${r.quantity}</p>
     <h3>Application Timing</h3><p>${r.timing}</p>
     <h3>Explanation</h3><p>${r.explanation}</p>`;
}

function downloadReport(){
  if(!currentData)return;
  fetch("/download-report",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(currentData)})
  .then(r=>{if(!r.ok)throw new Error("Report generation failed.");return r.blob();})
  .then(blob=>{
    const url=URL.createObjectURL(blob), a=document.createElement("a");
    a.href=url;a.download="smart_fertilizer_report.txt";a.click();URL.revokeObjectURL(url);
  }).catch(e=>alert(e.message));
}
