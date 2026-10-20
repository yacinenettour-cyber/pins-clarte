import sys, subprocess, rendu2 as rendu
from rendu2 import W, H, FPS
i0, i1, sortie = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
p = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-",
    "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-tune","film","-threads","1",sortie], stdin=subprocess.PIPE)
for i in range(i0, i1):
    p.stdin.write(rendu.image(i / FPS).tobytes())
p.stdin.close(); p.wait(); print("ok", sortie)
