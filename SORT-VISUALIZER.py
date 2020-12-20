import tkinter as tk
import time
import random
from heapq import heapify, heappop

width, height = 1100, 700
buttonW, buttonH = .1, .05
size = 20
vals = [None] * size
bars = [None] * size
sortSpeed = 300
interrupt = False
sorting = False
defaultColor = 'RoyalBlue'
selectColor = 'magenta2'
currTime = 0
mergeQueue = []
quickQueue = []

root = tk.Tk()
root.title("Sorting Visualization")

canvas = tk.Canvas(root, height = height, width = width, bg = 'pale green')
canvas.pack()

def quickAnimation(step, prev = False, idx1 = None, idx2 = None, swapNums = False):
	global interrupt, sorting, quickQueue, sortSpeed, size
	if (not quickQueue and step == 1) or interrupt:
		if prev:
			changeColor(prev[0], defaultColor)
			changeColor(prev[1], defaultColor)
		buttonColor(quick, False)
		interrupt = False
		sorting = False
		quickQueue = []
		return

	# if sortSpeed == 1: # reduce animation lag
	# 	sortSpeed = 30

	if step == 1:
		if prev:
			changeColor(prev[0], defaultColor)
			changeColor(prev[1], defaultColor)

		indices = quickQueue.pop(0)
		idx1 = indices[0]
		idx2 = indices[1]
		swapNums = indices[2]
		changeColor(idx1, selectColor)
		changeColor(idx2, selectColor)
		if size >= 200 and not swapNums: # if large array size then only display swaps
			root.after(0, lambda: quickAnimation(1, (idx1, idx2)))
		else:
			root.after(sortSpeed, lambda: quickAnimation(2, None, idx1, idx2, swapNums))
	elif swapNums:
		swap(idx1, idx2)
		updateScreen()
		changeColor(idx1, selectColor)
		changeColor(idx2, selectColor)
		root.after(sortSpeed, lambda: quickAnimation(1, (idx1, idx2)))
	else:
		root.after(0, lambda: quickAnimation(1, (idx1, idx2)))



def heap(index = None, maxHeap = [], newSort = True, step = 1):
	global interrupt, sorting, vals
	if sorting and newSort: # prevents another sort from being called while running
		return
	elif newSort:
		sorting = True
		buttonColor(heap, True)
		index = size - 1
		maxHeap = [-x for x in vals]
		heapify(maxHeap)
	changeColor(0, defaultColor) if not newSort else False
	if index == -1 or interrupt: # terminates when finished or when interrupted by scale
		interrupt = False
		sorting = False
		buttonColor(heap, False)
		return

	# ALGORITHM #
	if step == 1:
		changeColor(0, selectColor)
		root.after(sortSpeed, lambda: heap(index, maxHeap, False, 2))
	else:
		vals[index] = -heappop(maxHeap)
		vals[:index] = [-x for x in maxHeap]
		updateScreen()
		changeColor(index, selectColor)
		root.after(sortSpeed, lambda: heap(index - 1, maxHeap, False, 1))


def insertion(start = 1, iteration = 0, newSort = True, prev = False): # Insertion Sort
	global interrupt, sorting
	changeColor(prev, defaultColor) if type(prev) == int else None
	if sorting and newSort: # prevents another sort from being called while running
		return
	elif newSort:
		sorting = True
		buttonColor(insertion, True)
	if start == size or interrupt: # terminates when finished or when interrupted by scale
		interrupt = False
		sorting = False
		buttonColor(insertion, False)
		return

	# ALGORITHM # (allows for brief pauses to display selection highlight)
	if iteration % 2 == 0: 
		changeColor(start, selectColor)
		root.after(sortSpeed, lambda: insertion(start, iteration + 1, False)) 
		# pause after initial start selection
	else:
		lowest = 1
		for i in range(start, 0, -1):
			if vals[i] < vals[i - 1]:
				swap(i, i - 1)
				lowest = i - 1
			else:
				lowest = i
				break
		clearRectangles(range(lowest, start + 1))
		for k in range(lowest, start + 1):
			drawRect(k, defaultColor)
		changeColor(lowest, selectColor)
		root.after(sortSpeed, lambda: insertion(start + 1, 0, False, lowest))  
		# pause after start item is swapped as long as it can go
	

	# ALGORITHM # (allows for brief pauses to display selection highlight)
	if iteration % 2 == 0: 
		changeColor(start - 1, defaultColor) if start != 0 else None
		for i in range(start, size):
			if vals[i] < currMin:
				currMin = vals[i]
				minIdx = i
		changeColor(minIdx, selectColor)
		root.after(sortSpeed, lambda: selection(start, False, iteration + 1, currMin, minIdx))
		# pause after minimum item is found in unsorted section
	else:
		clearRectangles([minIdx, start])
		swap(start, minIdx)
		drawRect(start, selectColor)
		drawRect(minIdx, defaultColor)
		root.after(sortSpeed, lambda: selection(start + 1, False))
		# pause after minimum item is swapped with leftmost of unsorted section

def swap(index1, index2):
	vals[index1], vals[index2] = vals[index2], vals[index1]

def changeColor(index, color):
	canvas.itemconfig(bars[index], fill = color, outline = color)

def drawRect(i, color):
	barWidth = (width * 0.9) / size
	startX = width * 0.05
	endY = height * 0.885

	x1 = startX + i * barWidth
	y1 = endY - (vals[i] / (size * 10)) * (.8 * height)
	x2 = x1 + barWidth
	bars[i] = canvas.create_rectangle(x1, y1, x2, endY, fill = color, outline = color, tag = 'rect')

def clearRectangles(lst):
	if not lst:
		canvas.delete('rect')
	else:
		for index in lst:
			canvas.delete(bars[index])

def updateScreen():
	global bars
	clearRectangles(None) # clears all rectangles
	bars = [None] * size
	for i in range(size):
		drawRect(i, defaultColor)		

def randomVals():
	global vals
	random.seed(time.time())
	vals = [None] * size
	for i in range(size):
		vals[i] = random.randint(1, size * 10)
	updateScreen()

def changeSize(newSize):
	global size, interrupt
	interrupt = True if sorting else False
	size = int(newSize)
	randomVals()

def buttonColor(algorithm, pressed):
	index = funcs.index(algorithm)
	buttons[index]['highlightbackground'] = 'snow4' if pressed else 'white'

def slow():
	global sortSpeed
	sortSpeed = 300
	speedButton[0]['highlightbackground'] = 'snow4'
	speedButton[1]['highlightbackground'] = 'white'
	speedButton[2]['highlightbackground'] = 'white'

def medium():
	global sortSpeed
	sortSpeed = 70
	speedButton[0]['highlightbackground'] = 'white'
	speedButton[1]['highlightbackground'] = 'snow4'
	speedButton[2]['highlightbackground'] = 'white'

def fast():
	global sortSpeed
	sortSpeed = 1
	speedButton[0]['highlightbackground'] = 'white'
	speedButton[1]['highlightbackground'] = 'white'
	speedButton[2]['highlightbackground'] = 'snow4'


sorts = ["Heap Sort", "Insertion Sort"]
funcs = [ heap, insertion]
modes = ["Slow", "Medium", "Fast"]
speeds = [slow, medium, fast]
buttons = []
speedButton = []

for i in range(len(sorts)): # button for sorts
	buttons.append(tk.Button(canvas, text = sorts[i], command = funcs[i]))
	buttons[i].place(relx = 0.005 * (i + 1) + buttonW * i, rely = 0.005, relwidth = buttonW, relheight = buttonH)

inputSize = tk.Scale(canvas, from_ = 10, to = 10000, tickinterval = 1000, orient = tk.HORIZONTAL, bg = 'light blue', command = changeSize)
inputSize.place(relx = 0.5 - buttonW * 4.5, rely = 1 - buttonH * 2.1, relwidth = buttonW * 6, relheight = buttonH * 2)
inputSize.set(size)

randomize = tk.Button(canvas, text = 'Reset', command = lambda: changeSize(size))
randomize.place(relx = 1 - buttonW * 1.1, rely = 0.005, relwidth = buttonW, relheight = buttonH)

for i in range(3): # buttons for sort speed
	speedButton.append(tk.Button(canvas, text = modes[i], command = speeds[i]))
	speedButton[i].place(relx = 0.5 + 1.75 * buttonW + buttonW * i, rely = 1 - buttonH * 1.55, relwidth = buttonW, relheight = buttonH)

randomVals()
slow()
root.mainloop()