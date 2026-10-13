from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
subjects=[
 'Chinese adult woman, 24, short black bob, candid smile, loose blue shirt, standing by a riverside railing',
 'Chinese adult man, 27, round glasses, slightly messy short hair, white T-shirt, eating at a tiny noodle shop',
 'Chinese adult woman, 31, shoulder-length dark curls, natural freckles, cream cardigan, apartment window',
 'Chinese adult man, 35, closely cropped hair, lightly sun-tanned skin, dark denim jacket, brick street corner',
 'Chinese adult woman, 28, ponytail, sporty sweatshirt, quiet hiking trail, candid side profile',
 'Chinese adult man, 42, salt-and-pepper hair, linen shirt, seated in a leafy courtyard',
 'Chinese adult woman, 36, wire-frame glasses, tied hair, striped shirt, browsing a bookshop',
 'Chinese adult man, 23, longer fringe, forest-green sweater, station platform',
 'Chinese adult woman, 45, soft smile lines, short wavy hair, red scarf, autumn park',
 'Chinese adult man, 55, graying temples, light jacket, quiet morning tea stall',
 'Chinese adult woman, 22, straight black hair, oversized checked shirt, warm dorm-style room',
 'Chinese adult man, 29, stubble, thick eyebrows, workwear jacket, rainy alley, cropped candid portrait',
 'Chinese adult woman, 33, shoulder-length hair, black cardigan, cafe mirror selfie without a visible camera blocking the face',
 'Chinese adult man, 26, shaved head, subtle dimples, athletic shirt, outdoor basketball court',
 'Chinese adult woman, 30, swept-back hair, natural skin texture, cotton top, seaside breeze',
 'Chinese adult man, 38, narrow oval face, rectangular spectacles, brown sweater, home kitchen',
 'Chinese adult woman, 26, curly short hair, cheerful candid expression, denim shirt, flower market',
 'Chinese adult man, 32, side-parted hair, beige jacket, cafe doorway, off-center waist-up snapshot',
 'Chinese adult woman, 41, warm tan skin, loose linen blouse, bamboo grove, side-view portrait',
 'Chinese adult man, 61, silver hair, relaxed smile, blue polo, fishing dock at sunrise',
 'Chinese adult woman, 25, chin-length black hair, headphones around neck, dark hoodie, evening bus stop',
 'Chinese adult man, 24, tousled hair, dark round glasses, orange knit cap, mountain campsite',
 'Chinese adult woman, 34, soft round face, tied bun, khaki coat, drizzly neighborhood street',
 'Chinese adult man, 46, short salt-and-pepper beard, pale blue shirt, sunny balcony with plants',
 'Chinese adult woman, 58, cropped gray hair, kind smile, purple wool sweater, village courtyard',
 'Chinese adult man, 31, straight dark hair, striped navy T-shirt, candid coastal walk',
 'Chinese adult woman, 29, dark hair in a loose braid, round glasses, white shirt, antique bookstore',
 'Chinese adult man, 36, broad face, clean-shaven, olive shirt, shaded forest bench',
 'Chinese adult woman, 23, black ponytail, casual plaid jacket, vending-machine light at night',
 'Chinese adult man, 28, slight mustache, black windbreaker, city rooftop at dusk',
 'Chinese adult woman, 39, swept side fringe, pale blue blouse, resting by a sunny kitchen window',
 'Chinese adult man, 51, graying curls, oval glasses, cardigan, reading in a quiet apartment',
 'Chinese adult woman, 27, short pixie haircut, brown jacket, bicycle repair shop, laughing candidly',
 'Chinese adult man, 34, thick black hair, navy overshirt, misty lakeside, contemplative side profile',
 'Chinese adult woman, 44, low bun, tiny silver stud earrings, olive knitwear, wooden cafe interior',
 'Chinese adult man, 25, soft round face, baseball cap backwards, loose gray sweatshirt, casual outdoor snapshot',
 'Chinese adult woman, 32, straight shoulder-length hair, simple white cotton dress, leafy park bench',
 'Chinese adult man, 40, angular face, fine smile lines, rust-colored shirt, warm book-filled study',
 'Chinese adult woman, 60, short black-and-gray hair, blue cardigan, seaside promenade',
 'Chinese adult man, 30, wavy black hair, slim black glasses, canvas jacket, old apartment stairwell'
]
camera=[
 'ordinary smartphone snapshot, eye-level and slightly off-center, soft overcast light',
 'warm indoor phone photography, informal close-up with slight film grain',
 '35mm documentary photo, environmental portrait, sunlight and deep shadows',
 'older compact digital camera look, modest grain, natural slightly imperfect framing',
 'soft-window-light photo, relaxed three-quarter composition, unretouched skin',
 'street photography, candid chest-up crop, subtle background motion and rich contrast',
 'natural backlit photo, casual composition with background context, muted warm colors',
 'evening smartphone photo, realistic low-light texture, cool and warm mixed illumination'
]
illustrations=[
 ('二次元','watercolor school-life illustration','original adult woman with short black hair reading by a rainy window, blue-gray washed pigments and paper texture'),
 ('二次元','1990s cel animation','original adult man with wind-tossed hair on a city rooftop, bold cel shadows and dusty warm colors'),
 ('二次元','monochrome ink manga','original adult woman wearing round glasses, thoughtful side-view portrait, fine pen lines and sparse screentones'),
 ('二次元','soft gouache character illustration','original adult man in a cream sweater holding a small dog, brushy pastel textures'),
 ('二次元','Chinese ink fantasy illustration','original adult woman in a simple flowing robe under bamboo shadows, restrained ink and pale jade wash'),
 ('二次元','crisp urban graphic novel','original adult man with short hair in a rainy neon street, angular expressive linework'),
 ('二次元','colored pencil anime portrait','original adult woman with a ponytail and blue scarf, rough pencil hatching and warm paper'),
 ('二次元','storybook character painting','original adult man tending plants on a small balcony, loose earthy painted shapes'),
 ('二次元','retro shojo illustration','original adult woman with dark wavy hair and a quiet smile, delicate ink and softly textured colors'),
 ('二次元','dark atmospheric animation still','original adult man leaning on a train-window frame at night, restrained teal-orange lighting'),
 ('二次元','light line-and-wash illustration','original adult woman eating an orange at a kitchen table, tiny everyday scene and clean white space'),
 ('二次元','expressive charcoal character sketch','original adult man looking upward with a scarf, smudged graphite and a few rusty color accents'),
 ('二次元','gentle watercolor animation still','original adult woman walking beside an autumn lake, soft edges and long daylight shadows'),
 ('二次元','bold flat cel character portrait','original adult man in an olive jacket under a railway sign, broad shadows and saturated limited palette'),
 ('二次元','detailed fantasy novel cover illustration','original adult woman with braided black hair holding a lantern, moonlit blue tones, no cover text'),
 ('二次元','vintage pen illustration','original adult man playing guitar in a tiny apartment, brown ink hatching and faded ochre wash'),
 ('二次元','pastel chalk anime portrait','original adult woman in a red knit hat surrounded by winter light, visible chalk grain'),
 ('二次元','stylized cinematic animation still','original adult man riding a bicycle through a sunlit tree-lined street, expressive perspective'),
 ('二次元','loose oil-brush character painting','original adult woman with a short haircut in a cafe, thick textured brush strokes and muted colors'),
 ('二次元','delicate botanical character illustration','original adult man with glasses surrounded by green leaves, natural ink linework and watercolor'),
 ('手绘插画','thick oil painting','a small fishing boat near a rocky coastline at dusk, visible impasto and muted violet sea'),
 ('手绘插画','rice-paper ink painting','a single bamboo branch and a tiny bird, flowing ink strokes and generous cream paper'),
 ('手绘插画','gouache storybook painting','a sleepy red fox curled beside a mossy tree, organic brush texture'),
 ('手绘插画','graphite still-life drawing','a ceramic mug and a worn book on a wooden desk, soft pencil shading'),
 ('手绘插画','wax crayon drawing','a tabby cat curled on a windowsill beside orange curtains, thick cheerful crayon marks'),
 ('手绘插画','handmade linocut print','a fish swimming between aquatic leaves, irregular deep-blue carved lines'),
 ('手绘插画','botanical watercolor','an iris flower with translucent blue petals and soft green leaves on paper'),
 ('手绘插画','expressive palette-knife seascape','a bright turquoise wave meeting dark rocks, thick textured paint'),
 ('手绘插画','soft pastel interior drawing','a quiet sunlit room with a sofa, book stack, and small potted plant'),
 ('手绘插画','torn-paper collage','a misty woodland with a tiny cabin, tactile layered paper edges'),
 ('手绘插画','handmade clay miniature photography','a tiny gray rabbit figurine resting beside a ceramic mushroom, actual clay texture'),
 ('手绘插画','needle-felt sculpture photography','a small woolen sleeping corgi on a linen cloth, realistic fiber texture'),
 ('手绘插画','traditional brush ink drawing','a running horse in a few expressive ink strokes, pale rice paper'),
 ('手绘插画','travel watercolor sketch','a little old street shop with plants at its doorway, fine line-and-wash, no legible shop text'),
 ('手绘插画','chalk landscape drawing','early orange sunlight behind a blue mountain range, powdery chalk grain'),
 ('手绘插画','children-book watercolor','a small hedgehog asleep under fallen leaves, soft handmade pigment'),
 ('手绘插画','cyanotype botanical print','a fern silhouette on richly textured indigo photographic paper'),
 ('手绘插画','colored pencil still life','a green pear and an amber glass bottle on a soft fabric surface'),
 ('手绘插画','embroidered textile art photography','a mountain meadow stitched on coarse linen, visible thread and tactile texture'),
 ('手绘插画','vintage etching illustration','a vinyl player and a houseplant, delicate crosshatching on warm aged paper')
]
rows=[]
for i,subject in enumerate(subjects):
    style=camera[(i*3+i//8)%len(camera)]
    prompt=f'Use case: photorealistic-natural. Asset type: one square social-media avatar. Create a candid photo of one fictional {subject}. Style: {style}. Keep a recognizable subject within a square crop, but vary natural framing rather than centering a passport headshot. Real pores, ordinary expression, natural clothing and everyday surroundings. Not a real named person. No beauty-filter plastic skin, no studio backdrop, no logos, no written text, no border, no collage, no watermark. A believable personal profile picture, not an advertisement.'
    rows.append({'id':i,'category':'写真人像','style':style,'prompt':prompt})
for i,(category,medium,subject) in enumerate(illustrations,40):
    prompt=f'Use case: illustration-story. Asset type: one square social-media avatar. Subject: {subject}. Medium: {medium}. Use this specific medium authentically, with its own line weights, textures, composition and lighting. One finished image, no avatar sheet, no contact sheet, no generic flat vector mascot. Original fictional adult characters or original non-human scene, no existing copyrighted character. Square composition; readable at small size. No lettering, watermark or decorative border.'
    rows.append({'id':i,'category':category,'style':medium,'prompt':prompt})
assert len(rows)==80 and len({r['prompt'] for r in rows})==80
dest=root/'source-assets/avatar-replacement';dest.mkdir(parents=True,exist_ok=True)
(dest/'ai-plan.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Planned 80 distinct avatar prompts')
