
#!/usr/bin/python
import Image,time,random,glob,re,os,sys

##$$
train = raw_input("train? (y/n)")
if(train == "y") : train= True
else: train = False
##
fileName = ''.join(sys.argv[1:])
def getNeighbourhood(i,width,height,pixels):
	results = []
	try:
		if(pixels[i+1] != 0): results.append(i+1)
		if(pixels[i-1] != 0): results.append(i-1)
		if(pixels[i-width] != 0): results.append(i-width)
		if(pixels[i+width] != 0): results.append(i+width)
		if(pixels[i-width+1] != 0): results.append(i-width+1)
		if(pixels[i+width+1] != 0): results.append(i+width+1)
		if(pixels[i-width-1] != 0): results.append(i-width-1)
		if(pixels[i+width-1] != 0): results.append(i+width-1)
	except:pass
	return results
now = time.time()
captcha = Image.open(fileName)
(width,height) = captcha.size
pixels = list(captcha.getdata())
i=0
for pixel in pixels:
	if (pixel == 2): pixels[i] = 0
	i+=1
toclean = []
for i in xrange(len(pixels)):
	neighbourhood = getNeighbourhood(i,width,height,pixels)
	if (len(neighbourhood) < 4) : 	pixels[i] = 0

captcha.putdata(pixels)
started=False
lowestY,highestY,count = 0,10000,0
captchas = []
slant = 15
for x in xrange(width):
	hasBlack = False
	for y in xrange(height):
		thisPixel = captcha.getpixel((x,y))
		if(thisPixel != 0):
			if(started == False):
				started=True
				firstX = x
				firstY = y
			else:
				lastX = x
			if(y > lowestY): lowestY = y
			if(y< highestY): highestY = y
			hasBlack = True
	if((hasBlack == False) and (started==True)):
		if((lowestY - highestY) > 4):
			croppingBox = (firstX,highestY,lastX,lowestY)
			newCaptcha = captcha.crop(croppingBox)
			if(train):
				text = raw_input(”char:n”)
				try: os.mkdir(”/home/dbyte/deliciousImages/” + text)
				except:pass
				text__ = “/home/dbyte/deliciousImages/” + text + “/” + str(random.randint(1,100000)) + “-.png”
				newCaptcha.resize((20,30)).save(text__)
				text_ = “/home/dbyte/deliciousImages/” + text + “/” + str(random.randint(1,100000)) + “-.png”
				newCaptcha.resize((20,30)).rotate(slant).save(text_)
				text_ = “/home/dbyte/deliciousImages/” + text + “/” + str(random.randint(1,100000)) + “-.png”
				newCaptcha.resize((20,30)).rotate(360 - slant).save(text_)
				captchas.append(Image.open(text__))
			else:
				#text = str(count)
				#text = “tmp-delicious-” + text + “.png”
				#newCaptcha.save(text)
				captchas.append(newCaptcha.resize((20,30)))

			started=False
			lowestY,highestY = 0,10000
			count +=1
if(train == False):

	imageFolders = os.listdir(”/home/dbyte/deliciousImages/”)
	images =[]
	for imageFolder in imageFolders:
		imageFiles = glob.glob(”/home/dbyte/deliciousImages/” + imageFolder + “/*.png”)
		for imageFile in imageFiles:
			pixels = list(Image.open(imageFile).getdata())
			for i in xrange(len(pixels)):
				if pixels[i] != 0: pixels[i] = 1
			images.append((pixels,imageFolder))

	crackedString = “”
	for captcha in captchas:
		bestSum,bestChar = 0,”"
		captchaPixels = list(captcha.getdata())
		for i in xrange(len(captchaPixels)):
			if captchaPixels[i] != 0: captchaPixels[i] = 1
		for imageAll in images:
			thisSum = 0
			pixels = imageAll[0]
			for i in xrange(len(captchaPixels)):
				try:
					if(captchaPixels[i] == pixels[i]): thisSum+=1
				except: pass
			if(thisSum > bestSum):
				bestSum = thisSum
				bestChar = imageAll[1]
		crackedString += bestChar
	print crackedString
	#print “time taken: ” + str(time.time() - now)
