"""Create a new tonal background or load an already edited source-pack background."""
from pathlib import Path

def rgb(hex_color):
    value=hex_color.lstrip('#')
    if len(value)!=6:raise ValueError('Palette colors must be #RRGGBB')
    return tuple(int(value[i:i+2],16) for i in (0,2,4))

def luminance(color):
    vals=[c/255 for c in color]
    vals=[c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4 for c in vals]
    return sum(c*w for c,w in zip(vals,(0.2126,0.7152,0.0722)))

def contrast(a,b):
    x,y=sorted((luminance(a),luminance(b)))
    return (y+0.05)/(x+0.05)

def build(visual,spec):
    from PIL import Image,ImageDraw
    palette=visual.get('palette',spec['default_palette'])
    colors={key:rgb(palette[key]) for key in ('background_top','background_bottom','ink','line')}
    if all(colors[key]==(255,255,255) for key in ('background_top','background_bottom')):
        raise ValueError('Pure-white academic background is prohibited')
    w,h=spec['canvas']['width'],spec['canvas']['height']
    mode=visual.get('background_mode','tonal_gradient')
    if mode=='tonal_gradient':
        image=Image.new('RGB',(w,h));draw=ImageDraw.Draw(image)
        top,bottom=colors['background_top'],colors['background_bottom']
        for y in range(h):
            t=y/(h-1)
            color=tuple(round(a*(1-t)+b*t) for a,b in zip(top,bottom))
            draw.line((0,y,w-1,y),fill=color)
    elif mode=='prepared_blurred_image':
        if not visual.get('source_image') or not visual.get('image_edit_record'):
            raise ValueError('A prepared background requires original source and image-edit evidence')
        path=Path(visual['prepared_background'])
        if not path.is_absolute():raise ValueError('Prepared background path must be absolute')
        with Image.open(path) as asset:
            if asset.size!=(w,h):raise ValueError('Prepared background must already be 2400x3000')
            image=asset.convert('RGB')
    else:raise ValueError(f'Unsupported background mode: {mode}')
    return image,palette,{'mode':mode,'palette':palette,'basis':visual.get('palette_basis'),
                         'source_image':visual.get('source_image'),'prepared_background':visual.get('prepared_background')}

def region_contrast(image,bbox,ink):
    # Channel extrema give conservative luminance bounds over ALL region pixels,
    # not a few points. Mixed dark/light imagery crossing ink luminance fails.
    box=tuple(int(c) for c in bbox)
    extrema=image.crop(box).getextrema()
    low=tuple(v[0] for v in extrema);high=tuple(v[1] for v in extrema)
    li=luminance(ink)
    if luminance(low)<=li<=luminance(high):return 1.0
    return min(contrast(ink,low),contrast(ink,high))
