import sys, glob
from PIL import Image
from rembg import remove, new_session
U="/mnt/user-data/uploads/"
def P(h): return glob.glob(U+h+"-image.*")[0]
# key: (hash, crop|None, mode) mode: cut | full
J={
"V01_helmet":("ac3e1f28",None,"cut"),
"V02_valkyrie":("db9d3bef",None,"cut"),
"V03_alfred_jewel":("6e0fac63",None,"cut"),
"V04_oval_brooch":("f80801a6",None,"cut"),
"V05_silver_bars":("f79d8c23",None,"cut"),
"V05b_dirhams_case":("580548f2",None,"full"),
"V05c_scales":("9cfcee2d",None,"full"),
"V06_gnezdovo_sheet":("810e50c0",None,"cut"),
"V06_pend1":("ff4fcf73",(0,0,0.33,1),"cut"),
"V06_pend2":("ff4fcf73",(0.35,0,0.68,1),"cut"),
"V06_pend3":("ff4fcf73",(0.68,0,1,1),"cut"),
"V07_hist_a":("f4cccf5a",(0,0,0.5,1),"cut"),
"V07_hist_b":("f4cccf5a",(0.5,0,1,1),"cut"),
"V07_hist_single":("aa6aa94f",None,"cut"),
"V07_hist_pair_photo_a":("96509f0c",(0,0,0.5,1),"cut"),
"V07_hist_pair_photo_b":("96509f0c",(0.5,0,1,1),"cut"),
"V08_halfdan_runes":("cac46dfb",None,"full"),
"V09_key_chain":("30baf599",None,"cut"),
"V09_key_lesecq":("043cf27c",None,"cut"),
"V10_lindisfarne_stone":("aa36cef1",None,"cut"),
"V11_gospels_page":("844bb63d",None,"full"),
"V12_oseberg_dig":("8627e9f5",None,"full"),
"V13_oseberg_ship":("2aefbf3c",None,"full"),
"V14_roek_a":("84fdc525",None,"full"),
"V14_roek_b":("b3c38d12",None,"full"),
"V15_u112":("4506b29e",None,"full"),
"V16_cnut_a":("06ab06ee",(0.12,0.05,0.535,0.80),"cut"),
"V16_cnut_b":("06ab06ee",(0.545,0.05,0.97,0.80),"cut"),
"V17_jelling":("6227d258",None,"cut"),
"V18_hvalsey":("b6ae2b8d",None,"full"),
"V19_bayeux":("35a531d7",None,"full"),
"V22_thor_hammer":("23a8d4c9",None,"cut"),
"V20_denier":("70c90fc6",(0.2,0.18,0.88,0.75),"cut"),
}
ses=new_session("isnet-general-use")
for k in (sys.argv[1:] or J):
    h,c,m=J[k]; im=Image.open(P(h)).convert("RGB")
    if c: im=im.crop((int(c[0]*im.width),int(c[1]*im.height),int(c[2]*im.width),int(c[3]*im.height)))
    if m=="full": im.save(f"full/{k}.jpg",quality=95); print(k,"full",im.size); continue
    o=remove(im,session=ses); bb=o.getchannel("A").point(lambda v:255 if v>24 else 0).getbbox(); o=o.crop(bb); o.save(f"cut/{k}.png"); print(k,"cut",o.size,"LOW" if max(o.size)<1000 else "")
