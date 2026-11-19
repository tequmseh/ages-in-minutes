"""Georeference the Wikimedia 'Basin of Mexico 1519' map (CC BY-SA) by town markers and trace the lakes. usage: python3 georef.py <png> """
import sys, json, math, numpy as np, cv2
from PIL import Image
CTRL = {  # name: (pixel x, pixel y in the 1920x2561 file, lon, lat)  town centres, modern coordinates
 "Cuautitlan": (440,570,-99.178,19.671), "Teotihuacan": (1500,613,-98.844,19.692), "Acolman": (1488,848,-98.912,19.636), "Ecatepec": (939,1074,-99.061,19.601),
 "Texcoco": (1417,1114,-98.882,19.512), "Tenayuca": (564,1183,-99.170,19.528), "Huexotla": (1437,1216,-98.885,19.481), "Tepeyacac": (698,1341,-99.118,19.485),
 "Azcapotzalco": (465,1395,-99.186,19.487), "Tlacopan": (483,1477,-99.189,19.459), "Tlatelolco": (633,1466,-99.135,19.452), "Tenochtitlan": (638,1518,-99.132,19.435),
 "Chapultepec": (480,1579,-99.182,19.420), "Mixcoac": (540,1681,-99.187,19.375), "Iztapalapa": (781,1772,-99.056,19.357), "Coyoacan": (579,1783,-99.162,19.350),
 "Ixtapaluca": (1249,1938,-98.883,19.319), "Xochimilco": (869,2213,-99.104,19.257), "Chalco": (1421,2223,-98.897,19.264), "Culhuacan": (701,1855,-99.110,19.336)}
def my(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
def fit(ctrl):
    A=np.array([[x,y,1] for x,y,_,_ in ctrl.values()],float)
    lon=np.array([c[2] for c in ctrl.values()]); Y=np.array([my(c[3]) for c in ctrl.values()])
    px,*_=np.linalg.lstsq(A,lon,rcond=None); py,*_=np.linalg.lstsq(A,Y,rcond=None); return px,py
def to_ll(px,py,x,y):
    lon=px@[x,y,1]; Y=py@[x,y,1]; lat=math.degrees(2*math.atan(math.exp(Y))-math.pi/2); return float(lon),float(lat)
if __name__=="__main__":
    px,py=fit(CTRL)
    for k,(x,y,lo,la) in CTRL.items():
        l2,a2=to_ll(px,py,x,y); print(f"{k:13s} dx {(l2-lo)*105:6.2f} km  dy {(a2-la)*111:6.2f} km")
