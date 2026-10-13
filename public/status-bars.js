'use strict';
// Screenshot measurements + one-time AI network sprites. Coordinates: 420 px.
(() => {
  const source={ios:'https://support.apple.com/zh-cn/118203',xiaomi:'https://web.vip.miui.com/page/info/mio/mio/detail?postId=52332496',huawei:'https://consumer.huawei.com/cn/myhuawei-app/',oppo:'https://www.oppo.cn/thread-399423032-1',vivo:'https://bbs.vivo.com/in/thread/161651',honor:'https://club.honor.com/cn/thread-28094158-1-1.html'};
  const styles=[
    {id:'ios-classic',label:'iOS · 简洁',description:'较宽的左右留白、粗体时钟，低电量显示红色。',family:'ios'},
    {id:'ios-percent',label:'iOS · 电量百分比',description:'电池内显示数值，深色电池与反白数字。',family:'ios'},
    {id:'ios-focus',label:'iOS · 专注模式',description:'时钟旁添加月亮，电量百分比显示在电池内。',family:'ios'},
    {id:'miui-dualsim',label:'小米 · 双卡 5G',description:'双卡 5G、蓝牙与静音，圆角胶囊电池。',family:'xiaomi'},
    {id:'hyperos-speed',label:'小米 · 网速与通知',description:'应用通知、两行网速、单卡 5G 与电量数值。',family:'xiaomi'},
    {id:'harmony-clean',label:'华为 · 简洁双卡',description:'Wi-Fi 在双卡信号前，电量数值显示在框内。',family:'huawei'},
    {id:'harmony-speed',label:'华为 · 网速与百分比',description:'两行网速、单卡网络，电量百分比在电池外。',family:'huawei'},
    {id:'coloros-horizontal',label:'ColorOS · 横向电池',description:'5G 与 Wi-Fi，横向电池内显示数值。',family:'oppo'},
    {id:'coloros-vertical',label:'ColorOS · 竖向电池',description:'通知和蓝牙、竖向电池与外置百分比。',family:'oppo'},
    {id:'coloros-ring',label:'ColorOS · 圆环电池',description:'5G 与 Wi-Fi，圆环随电量变化并显示数值。',family:'oppo'},
    {id:'origin-standard',label:'vivo · 外置百分比',description:'4G、带上下行标记的 Wi-Fi、外置百分比。',family:'vivo'},
    {id:'origin-speed',label:'vivo · 网速与静音',description:'静音与两行网速，电池外显示百分比。',family:'vivo'},
    {id:'magic-pure',label:'荣耀 · 纯净模式',description:'仅保留时间、Wi-Fi、移动信号与电量。',family:'honor'},
    {id:'magic-notify',label:'荣耀 · 通知与蓝牙',description:'消息通知、蓝牙与外置百分比。',family:'honor'}
  ].map(s=>({...s,source:source[s.family]}));
  const aliases={'android-stock':'harmony-clean','android-notify':'origin-standard','oneui-standard':'magic-pure','oneui-dnd':'magic-notify'};
  function normalize(id){return styles.some(s=>s.id===id)?id:aliases[id]||'ios-classic';}
  const ink='#171717',images=new Map();let loading;
  function ready(){
    if(!loading)loading=Promise.all([
      ...['ios','xiaomi','xiaomi-single','huawei','huawei-single','oppo','vivo','honor'].map(key=>new Promise((resolve,reject)=>{
        const img=new Image();img.onload=()=>{images.set(key,img);resolve();};img.onerror=()=>reject(new Error('通知栏素材未能载入'));img.src=`/assets/status-bars-v2/${key}.png`;
      })),
      document.fonts.load('650 20px StatusInter','0123456789:'),
      document.fonts.load('550 17px StatusRoboto','0123456789:%'),
      document.fonts.load('700 10px StatusRoboto','0123456789KB/s')
    ]);return loading;
  }
  function text(ctx,s,x,y,size=11,weight=500,color=ink,family='StatusRoboto'){ctx.fillStyle=color;ctx.font=`${weight} ${size}px ${family}, Arial, sans-serif`;ctx.fillText(String(s),x,y);}
  function box(ctx,x,y,w,h,r,color){ctx.fillStyle=color;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();}
  function path(ctx,points,close=false){ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));if(close)ctx.closePath();ctx.stroke();}
  function network(ctx,key,right,y,height){const img=images.get(key);if(!img)throw new Error('通知栏素材尚未就绪');const width=img.width/img.height*height;ctx.drawImage(img,right-width,y,width,height);return right-width;}
  function moon(ctx,x,y,size=11){ctx.save();ctx.beginPath();ctx.arc(x+size/2,y+size/2,size/2,0,2*Math.PI);ctx.clip();ctx.beginPath();ctx.arc(x+size/2,y+size/2,size/2,0,2*Math.PI);ctx.moveTo(x+size*1.37,y+size*.23);ctx.arc(x+size*.81,y+size*.23,size*.56,0,2*Math.PI,true);ctx.fillStyle=ink;ctx.fill('evenodd');ctx.restore();}
  function bluetooth(ctx,x,y){ctx.save();ctx.lineWidth=1.5;path(ctx,[[x+4,y],[x+4,y+14]]);path(ctx,[[x+4,y],[x+9,y+4],[x,y+11]]);path(ctx,[[x+4,y+14],[x+9,y+10],[x,y+3]]);ctx.restore();}
  function muted(ctx,x,y){ctx.save();ctx.fillStyle=ink;ctx.beginPath();ctx.moveTo(x+1,y+11);ctx.quadraticCurveTo(x+3,y+8,x+3,y+4);ctx.quadraticCurveTo(x+6,y,x+9,y+4);ctx.lineTo(x+9,y+8);ctx.lineTo(x+11,y+11);ctx.closePath();ctx.fill();box(ctx,x+4.5,y+12.5,3,1.5,.7,ink);ctx.lineWidth=2;ctx.strokeStyle='#eee';path(ctx,[[x-1,y],[x+12,y+14]]);ctx.lineWidth=1.3;ctx.strokeStyle=ink;path(ctx,[[x-1,y],[x+12,y+14]]);ctx.restore();}
  function notice(ctx,x,y,kind='chat',color=ink){ctx.save();ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=1.35;if(kind==='dots'){[0,4,8].forEach(dx=>{ctx.beginPath();ctx.arc(x+dx,y+5,1,0,Math.PI*2);ctx.fill();});}else if(kind==='app'){box(ctx,x,y,12,12,2.5,color);ctx.strokeStyle='white';path(ctx,[[x+3,y+8],[x+8,y+3],[x+9,y+5],[x+5,y+9]]);}else if(kind==='mail'){ctx.strokeRect(x,y+1,11,8);path(ctx,[[x,y+1],[x+5.5,y+5],[x+11,y+1]]);}else{ctx.beginPath();ctx.roundRect(x,y,11,8,2);ctx.stroke();path(ctx,[[x+3,y+8],[x+3,y+11],[x+6,y+8]]);}ctx.restore();}
  function speed(ctx,x,value='0.12'){text(ctx,value,x,17,7.5,650);text(ctx,'KB/s',x,25,7,600);}
  function battery(ctx,x,y,value,mode='plain',brand='ios'){
    const level=Math.max(1,Math.min(100,Math.round(Number(value)||1))),low=level<=20;
    ctx.save();ctx.lineWidth=1;ctx.strokeStyle=brand==='huawei'||brand==='honor'?'#64676a':'#919395';
    if(mode==='ring'){
      ctx.lineWidth=1.65;ctx.strokeStyle='#aeb0b1';ctx.beginPath();ctx.arc(x+9,y+9,8.1,0,Math.PI*2);ctx.stroke();ctx.strokeStyle=low?'#d85651':ink;ctx.beginPath();ctx.arc(x+9,y+9,8.1,-Math.PI/2,-Math.PI/2+2*Math.PI*level/100);ctx.stroke();ctx.textAlign='center';text(ctx,level,x+9,y+4.5,8.4,650);
    }else if(mode==='vertical'){
      ctx.strokeRect(x,y+2,8.5,14);box(ctx,x+2.5,y,3.5,1.5,.4,'#777');box(ctx,x+1.3,y+3.3+11.4*(1-level/100),5.9,11.4*level/100,.5,low?'#d85651':ink);
    }else{
      const roundness=brand==='xiaomi'?4.3:brand==='vivo'?3:2.8,w=brand==='vivo'?25:27,h=13;
      ctx.beginPath();ctx.roundRect(x,y,w,h,roundness);ctx.stroke();box(ctx,x+w+1.2,y+4.1,1.7,4.8,.65,'#8a8d90');
      if(mode==='inside'){
        box(ctx,x+1.2,y+1.2,w-2.4,h-2.4,Math.max(1,roundness-1),'#b9bbbd');
        const fill=brand==='huawei'||brand==='honor'?'#747779':low?'#d85651':'#292b2d';
        box(ctx,x+1.2,y+1.2,(w-2.4)*level/100,h-2.4,Math.max(1,roundness-1),fill);
        ctx.textAlign='center';text(ctx,level,x+w/2,y+1.15,10.5,700,ink);
        ctx.save();ctx.beginPath();ctx.rect(x+1.2,y+1.2,(w-2.4)*level/100,h-2.4);ctx.clip();text(ctx,level,x+w/2,y+1.15,10.5,700,'#fff');ctx.restore();
      }else box(ctx,x+1.5,y+1.5,(w-3)*level/100,h-3,Math.max(.5,roundness-1.5),low?'#d85651':brand==='ios'?'#353638':'#36383a');
    }ctx.restore();
  }
  function percentage(ctx,value,right,y,size=12){ctx.save();ctx.textAlign='right';text(ctx,value+'%',right,y,size,500);ctx.restore();}
  function draw(ctx,c){
    const id=normalize(c.statusStyle),ios=id.startsWith('ios'),level=Math.max(1,Math.min(100,Math.round(Number(c.battery)||1)));
    ctx.save();ctx.textBaseline='top';ctx.textAlign='left';ctx.fillStyle=ink;ctx.strokeStyle=ink;ctx.lineWidth=1.35;ctx.lineJoin='round';ctx.lineCap='round';
    text(ctx,c.statusTime||'16:38',ios?43:25,ios?15.5:17.5,ios?19.5:16.5,ios?650:550,ink,ios?'StatusInter':'StatusRoboto');
    switch(id){
      case 'ios-classic':network(ctx,'ios',357,19.5,14.8);battery(ctx,367,20,level);break;
      case 'ios-percent':network(ctx,'ios',357,19.5,14.8);battery(ctx,367,20,level,'inside');break;
      case 'ios-focus':moon(ctx,106,22,10);network(ctx,'ios',357,19.5,14.8);battery(ctx,367,20,level,'inside');break;
      case 'miui-dualsim':notice(ctx,78,21,'chat','#429bb3');notice(ctx,96,21,'dots');bluetooth(ctx,250,19);muted(ctx,268,18.5);network(ctx,'xiaomi',363,17,20);battery(ctx,371,21,level,'inside','xiaomi');break;
      case 'hyperos-speed':notice(ctx,78,20.5,'app','#ff9218');notice(ctx,97,21,'mail','#318cac');speed(ctx,278,'78.6');network(ctx,'xiaomi-single',363,17,20);battery(ctx,371,21,level,'inside','xiaomi');break;
      case 'harmony-clean':network(ctx,'huawei',362,20,15);battery(ctx,371,21,level,'inside','huawei');break;
      case 'harmony-speed':speed(ctx,261,'4.2');network(ctx,'huawei-single',336,20,15);percentage(ctx,level,368,21,11);battery(ctx,374,21,level,'plain','huawei');break;
      case 'coloros-horizontal':notice(ctx,78,21,'chat');network(ctx,'oppo',362,17,20);battery(ctx,371,21,level,'inside','oppo');break;
      case 'coloros-vertical':notice(ctx,78,21,'mail');bluetooth(ctx,280,19);network(ctx,'oppo',339,17,20);percentage(ctx,level,383,21,11);battery(ctx,390,18.5,level,'vertical','oppo');break;
      case 'coloros-ring':notice(ctx,78,21,'chat');network(ctx,'oppo',371,17,20);battery(ctx,384,18,level,'ring','oppo');break;
      case 'origin-standard':network(ctx,'vivo',336,17,20);percentage(ctx,level,371,20,12);battery(ctx,376,20.5,level,'plain','vivo');break;
      case 'origin-speed':muted(ctx,243,19);speed(ctx,261,'10.3');network(ctx,'vivo',336,17,20);percentage(ctx,level,371,20,12);battery(ctx,376,20.5,level,'plain','vivo');break;
      case 'magic-pure':network(ctx,'honor',362,20,15);battery(ctx,371,21,level,'inside','honor');break;
      case 'magic-notify':notice(ctx,78,21,'mail');notice(ctx,96,21,'dots');bluetooth(ctx,281,19);network(ctx,'honor',337,20,15);percentage(ctx,level,369,21,11);battery(ctx,375,21,level,'plain','honor');break;
    }ctx.restore();
  }
  function preview(canvas,c){canvas.width=840;canvas.height=100;const ctx=canvas.getContext('2d');ctx.scale(2,2);ctx.fillStyle='#eee';ctx.fillRect(0,0,420,50);draw(ctx,c);}
  window.StatusBars=Object.freeze({styles:Object.freeze(styles.map(Object.freeze)),draw,preview,ready,normalize});
})();
