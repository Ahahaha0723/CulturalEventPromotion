"""Copy USER-DOWNLOADED font files into this extracted module; does not download fonts.
Run: python scripts/install_local_fonts.py <folder containing your original archives>
"""
import json,zipfile,sys,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
if len(sys.argv)!=2:raise SystemExit('用法: python scripts/install_local_fonts.py 路径\到\字体压缩包文件夹')
source=Path(sys.argv[1]); info=json.loads((root/'references/font-manifest.json').read_text('utf8'))
for entry in info['fonts']:
 target=root/entry['file'];target.parent.mkdir(parents=True,exist_ok=True)
 archive=source/entry['source_archive']
 if archive.suffix.lower()=='.ttf':shutil.copy2(archive,target);continue
 with zipfile.ZipFile(archive) as z:
  options=[n for n in z.namelist() if n.endswith('/'+target.name)]
  if len(options)!=1:raise ValueError('没有找到所需字体：'+target.name+' in '+str(archive))
  target.write_bytes(z.read(options[0]))
for family,arc,prefix in [
 ('source-han-serif','09_SourceHanSerifSC.zip',''),
 ('source-han-sans','09_SourceHanSansSC.zip',''),
 ('ma-shan-zheng','Ma_Shan_Zheng,Nunito,Zhi_Mang_Xing.zip','Ma_Shan_Zheng/'),
 ('zhi-mang-xing','Ma_Shan_Zheng,Nunito,Zhi_Mang_Xing.zip','Zhi_Mang_Xing/'),
 ('nunito','Ma_Shan_Zheng,Nunito,Zhi_Mang_Xing.zip','Nunito/')]:
 with zipfile.ZipFile(source/arc) as z:
  name=(prefix+'OFL.txt') if prefix else 'LICENSE.txt'
  data=z.read(name)
  out=root/'fonts'/family/'OFL-LICENSE.txt';out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
# LXGW WenKai full copyright declaration from official OFL, with standard OFL 1.1 terms.
text=(root/'references/LXGW-WenKai-OFL.txt').read_text('utf8')
out=root/'fonts/lxgw-wenkai/OFL.txt';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(text,'utf8')
print('LOCAL FONTS INSTALLED. Run: python scripts/check_fonts.py')
