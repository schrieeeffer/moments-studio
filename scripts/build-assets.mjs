import fs from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve(import.meta.dirname,'../public/assets');
const manifest=[];
for(const file of ['replacement-avatars.json','photo-avatars.json','generated-avatars.json','anime-avatars.json']){
  const rows=JSON.parse(await fs.readFile(path.join(root,file),'utf8'));manifest.push(...rows);
}
manifest.sort((a,b)=>a.id-b.id);
if(manifest.length!==360||manifest.some((a,i)=>a.id!==i||!/^\/assets\/avatars\/\d{3}\.jpg$/.test(a.src)))throw new Error('360 stable JPEG avatar records are required.');
for(const a of manifest)await fs.access(path.join(root,'avatars',path.basename(a.src)));
await fs.writeFile(path.join(root,'avatars.json'),JSON.stringify(manifest));
await fs.copyFile(path.resolve(import.meta.dirname,'../node_modules/jszip/dist/jszip.min.js'),path.join(root,'jszip.min.js'));
const pkg=JSON.parse(await fs.readFile(path.resolve(import.meta.dirname,'../node_modules/jszip/package.json'),'utf8'));
await fs.writeFile(path.join(root,'dependencies.json'),JSON.stringify([{package:'jszip',version:pkg.version,license:pkg.license}],null,2));
console.log(JSON.stringify({avatars:manifest.length,replacement:manifest.filter(a=>a.collection==='replacement').length,photos:manifest.filter(a=>a.license==='Unsplash License').length,generated:manifest.filter(a=>a.generated).length}));
