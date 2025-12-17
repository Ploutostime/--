// WebSocket chat client example
(function(){
	console.log('chat client loaded');
	function uuidv4(){ return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g,function(c){var r=Math.random()*16|0,v=c=='x'?r:(r&0x3|0x8);return v.toString(16);}); }
	const userId = uuidv4();
	const wsUrl = (location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host + '/ws/' + userId;
	let ws;

	// build UI
	const panel = document.createElement('div');
	panel.style.position = 'fixed';
	panel.style.right = '20px';
	panel.style.bottom = '20px';
	panel.style.width = '320px';
	panel.style.maxHeight = '60vh';
	panel.style.background = 'rgba(255,255,255,0.95)';
	panel.style.border = '1px solid #ddd';
	panel.style.borderRadius = '8px';
	panel.style.boxShadow = '0 6px 20px rgba(0,0,0,0.15)';
	panel.style.display = 'flex';
	panel.style.flexDirection = 'column';
	panel.style.overflow = 'hidden';
	panel.style.zIndex = 9999;

	const header = document.createElement('div'); header.textContent='Chat'; header.style.padding='8px'; header.style.fontWeight='600'; header.style.borderBottom='1px solid #eee'; panel.appendChild(header);
	const log = document.createElement('div'); log.style.flex='1'; log.style.padding='8px'; log.style.overflowY='auto'; panel.appendChild(log);
	const form = document.createElement('div'); form.style.display='flex'; form.style.padding='8px';
	const input = document.createElement('input'); input.style.flex='1'; input.style.padding='8px'; input.placeholder='说点什么...';
	const btn = document.createElement('button'); btn.textContent='发送'; btn.style.marginLeft='6px';
	form.appendChild(input); form.appendChild(btn); panel.appendChild(form);
	document.body.appendChild(panel);

	function appendMessage(role, text){
		const d = document.createElement('div');
		d.style.marginBottom='8px';
		d.innerHTML = '<b>'+role+':</b> '+(text||'');
		log.appendChild(d); log.scrollTop = log.scrollHeight;
	}

	function connect(){
		try{
			ws = new WebSocket(wsUrl);
			ws.onopen = ()=>{ appendMessage('system','WS connected as '+userId); };
			ws.onmessage = (e)=>{ try{ const p=JSON.parse(e.data); appendMessage('assistant', p.answer || e.data); }catch(err){ appendMessage('assistant', e.data); }};
			ws.onclose = ()=>{ appendMessage('system','WS closed'); setTimeout(connect,3000); };
			ws.onerror = (err)=>{ console.error(err); };
		}catch(err){ console.error('ws connect error', err); }
	}

	btn.addEventListener('click', ()=>{
		const v = input.value.trim(); if(!v) return;
		appendMessage('you', v);
		const payload = JSON.stringify({text: v, persona: 'agri_expert'});
		if(ws && ws.readyState === WebSocket.OPEN){ ws.send(payload); }
		else { appendMessage('system','WS not connected, will try in background'); }
		input.value = '';
	});

	connect();
})();
