from PIL import Image
img = Image.open(raw_input())
size = img.getbbox()
buf = Image.new("RGB",(size[2],size[3]),"white")
for x in range(0,size[2]):
	for y in range(0,size[3]):
		p = img.getpixel((x,y))
		if(p[0]+p[1]+p[2]<100):
			buf.putpixel((x,y),(0,0,99))
#enhance the image now
del img
def enhance(im):
	dim = im.getbbox()
	temp = Image.new("RGB",(dim[2]*2,dim[3]*2),"white")
	for x in range(0,dim[2]):
		for y in range(0,dim[3]):
			a = im.getpixel((x,y))
			temp.putpixel((2*x,2*y),a)
			temp.putpixel(((2*x)+1,2*y),a)
			temp.putpixel((2*x,(2*y)+1),a)
			temp.putpixel(((2*x)+1,(2*y)+1),a)
	return temp
def trim(im):
	dim = im.getbbox()
	coord = [0,0,0,0] #denoting left-x right-x up-y down-y respectively
	left_start = False
	top_start = False
	detected_black = False
	for y in range(0,dim[3]):
		for x in range(0,dim[2]):
			l = im.getpixel((x,y))
			if(l[0]+l[1]+l[2]<100 and not(detected_black)):
				#detected black for the first time i guess ;p
				detected_black = True
				coord[2] = y
				# im.putpixel((x,y),(255,0,0))
	detected_black = False
	for y in range(0,dim[3]):
		# detected_black = False
		in_y = dim[3] - y -1
		for x in range(0,dim[2]):
			l = im.getpixel((x,in_y))
			# if(l[0]+l[1]+l[2]>100):
			# 	im.putpixel((x,in_y),(50,50,50))
			if(l[0]+l[1]+l[2]<100 and not(detected_black)):
				#detected black for the first time i guess ;p
				detected_black = True
				coord[3] = in_y
				# im.putpixel((x,in_y),(0,255,0))
	detected_black = False
	for x in range(0,dim[2]):
		# detected_black = False
		# in_y = dim[3] - y -1
		for y in range(0,dim[3]):
			l = im.getpixel((x,y))
			if(l[0]+l[1]+l[2]<100 and not(detected_black)):
				#detected black for the first time i guess ;p
				detected_black = True
				coord[1] = x
				# im.putpixel((x,y),(0,0,255))
	detected_black = False
	for x in range(0,dim[2]):
		# detected_black = False
		in_x = dim[2] - x -1
		for y in range(0,dim[3]):
			l = im.getpixel((in_x,y))
			if(l[0]+l[1]+l[2]<100 and not(detected_black)):
				#detected black for the first time i guess ;p
				detected_black = True
				coord[0] = in_x
				# im.putpixel((in_x,y),(255,255,0))
	width = coord[0] - coord[1]
	height = coord[3] - coord[2]
	# print coord
	# quit()
	# im.putpixel((coord[0],coord[2]),(255,0,0))
	# im.putpixel((coord[1],coord[2]),(0,255,0))
	# im.putpixel((coord[0],coord[3]),(0,0,255))
	# im.putpixel((coord[1],coord[3]),(0,0,0))
	# im.show()
	temp = Image.new("RGB",(width,height),"white")
	for x in range(coord[1],coord[0]):
		for y in range(coord[2],coord[3]):
			l = im.getpixel((x,y))
			temp.putpixel((x-coord[1],y-coord[2]),l)
	return temp


buf = enhance(buf)
buf = enhance(buf)
buf = trim(buf)
# buf.show()
#time to detect the character by mapping it onto using bridge method
dim = buf.getbbox()
bridge = []
last_val = 0
first = True
for y in range (0,dim[3]):
	node = 0
	for x in range(0,dim[2]):
		#detect bridge over here
		if(x>1 and buf.getpixel((x-1,y)) != buf.getpixel((x,y))):
			node = node + 1
	if(buf.getpixel((0,y)) == (255,255,255)):
		x = "w"+str(node)
		if(not first):
			#compare to last also
			# print x
			if (bridge[len(bridge)-1] != x):
				bridge.append(x)
		else:
			bridge.append(x)
	else:
		x = "B"+str(node)
		if(not first):
			#compare to last also
			# print x
			if (bridge[len(bridge)-1] != x):
				bridge.append(x)			
		else:
			#dont compare to last just append
			bridge.append(x)

	first = False
# print bridge
bu = ""
for a in range(0,len(bridge)):
	bu = bu+bridge[a]
recom = []
f = open("char.DAT")
datax = f.read()
datax = datax.split("\n")
for i in range(0,len(datax)):
	s = datax[i].split(" ")
	if(s[0] == bu):
		recom.append(s[1])
print recom
if (len(recom) == 0):
	char = raw_input("Gimme a hint please >>>")
	f = open("char.DAT")
	d = f.read()
	d = d+"\n"+bu+" "+char
	f = open("char.DAT",'w')
	f.write(d)
buf = enhance(buf)
buf.show()
