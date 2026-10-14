"""Check bundled fonts and choose exactly one title family from topic evidence."""
from pathlib import Path
import json
import re
import argparse

TEMPLATE=Path(__file__).resolve().parents[1]
SKILL=TEMPLATE.parents[2]
SPEC=json.loads((TEMPLATE/'references/layout-spec.json').read_text(encoding='utf-8'))

def choose_title(topic,language='zh-CN'):
    if language=='en':
        return {'category':'english_required','font_key':'english_title','reason':'英文H1强制使用用户提供的Playball-Regular，不按中文主题字体分支'}
    human=r'人文|历史|哲学|文学|艺术|考古|文物|文化|博物馆|档案|语言|宗教|伦理|书法|美术|音乐|文献|人类学|humanit|heritage|archaeolog|histor|philosoph|literatur|museum|cultur|linguist|religion|ethic|anthropolog'
    digital=r'计算机|数字|算法|人工智能|机器学习|计算系统|信息技术|computer|digital|algorithm|computing'
    if re.search(human,topic,re.I):
        return {'category':'humanities','font_key':'humanities','reason':'研究主题含人文学科或人文对象；覆盖数字方法关键词'}
    if re.search(digital,topic,re.I):
        return {'category':'computing_without_humanities','font_key':'digital','reason':'计算机／数字研究主题，没有人文对象依据'}
    return {'category':'uncertain','font_key':'humanities','reason':'主题类别难确认，按用户规则优先演示夏行楷'}

def check(topic,language='zh-CN'):
    decision=choose_title(topic,language)
    files={k:SKILL/v for k,v in SPEC['fonts'].items()}
    for key,path in files.items():
        if not path.is_file() or not path.stat().st_size:raise FileNotFoundError(f'{key}: {path}')
    decision['font_path']=str(files[decision['font_key']])
    return {'valid':True,'decision':decision,'fonts':{k:str(v) for k,v in files.items()},'template':str(TEMPLATE)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--topic',default='');p.add_argument('--language',choices=['zh-CN','en'],default='zh-CN');a=p.parse_args()
    print(json.dumps(check(a.topic,a.language),ensure_ascii=False,indent=2))
