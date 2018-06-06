#*-coding: utf8 -*#
import os
import datetime
from random import *
from colorama import Fore, Back, Style, init
init()

goblin=[400, 40, 0.8] #4 враг
orkArcher=[300, 100, 0.6] #2 враг
orkVarior=[500, 35, 0.9] #1 враг
elfArcher=[250, 130, 0.4] #5 враг
elfVarior=[400, 60, 0.6] #3 враг

inventory=[] #heal=1, boostDamage=2, lightArmor(1.2)=3, middleArmor(1.5)=4, weightyArmor(1.7)=5
me=[0, 0, 0]
gold = 0
raca = 0
name = ""

def startGame():
	global me
	global raca
	global name
	global gold
	global inventory
	os.system("cls")
	print("1)Новая игра\n2)Открыть сохранение\n")
	action = int(input())
	os.system("cls")
	if action == 1:
		name = input("Привет, герой! Как тебя зовут? ")
		raca = int(input("Какой ты расы?(1: Орк, 2: Эльф, 3: Гоблин) "))
		racaString="Оркам" if raca == 1 else "Эльфам" if raca==2 else "Гоблины"
		if raca < 3:
			role=int(input("Кем ты хочешь быть?(1: Лучник, 2: Воин) "))
		if raca==1:
			if role==1:me=list(orkArcher)
			else: me=list(orkVarior)
		elif raca==2:
			if role==1:me=list(elfArcher)
			else:me=list(elfVarior)
		else: me=list(goblin)
		gold = 500
		inventory = []
	else:
		print("0)Вернуться")
		filesAtSaves = []
		if os.path.exists("saves"):
			filesAtSaves = os.listdir("saves")
			if len(filesAtSaves) == 0: 
				print(Fore.RED + "Нет сохранений!" + Style.RESET_ALL)
				os.rmdir("saves")
			else:
				numberOfSaveInMenu = 1
				for file in filesAtSaves:
					print(str(numberOfSaveInMenu) + ")" + file)
					numberOfSaveInMenu+= 1
		else: 
			print(Fore.RED + "Нет сохранений!" + Style.RESET_ALL)
		filenumber = int(input())
		if filenumber == 0 or filenumber > len(filesAtSaves): startGame()
		fileName = filesAtSaves[filenumber - 1]
		file = open('saves/'+fileName, "r")
		content = file.read().split("\n")
		file.close()
		meLine = content[0].replace("[", "").replace("]", "").split(", ")
		inventoryLine = content[1].replace("[", "").replace("]", "").split(", ")
		gold = int(content[2])
		name = content[3]
		me[0] = int(meLine[0])
		me[1] = int(meLine[1])
		me[2] = float(meLine[2])
		for i in range(len(inventoryLine)):
			inventory.append(int(inventoryLine[i]))

def doPurchase(good):
	global gold
	global me
	global hasArmor
	if good ==1: 
		cost=100
	elif good == 2:
		cost = 400
	elif good == 3: 
		cost = 300
	elif good == 4:
		cost = 600
	else: cost = 1200
	if gold < cost:
		print("Недостаточно золота!")
		return False
	inventory.append(good)
	if good == 3: 
		hasArmor = True
		me[2]*=1.2
	elif good == 4: 
		hasArmor = True
		me[2]*=1.5
	elif good == 5: 
		hasArmor = True
		me[2]*=1.7
	gold-=cost
	return True

def sellArmor():
	global inventory
	global gold
	global me
	global hasArmor
	if 3 in inventory: 
		hasArmor = False
		gold+=100
		me[2]/=1.2
		inventory.remove(3)
	elif 4 in inventory:
		hasArmor = False
		gold+=200
		me[2]/=1.5
		inventory.remove(4)
	else:
		hasArmor = False
		gold+=300
		me[2]/=1.7
		inventory.remove(5)

def getInventoryString():
	global inventory
	if len(inventory)==0: return Fore.RED+"Инвентарь пуст.\n"+Style.RESET_ALL
	strInventory="Вещи в инвентаре: \n"
	if 1 in inventory: strInventory+=Fore.GREEN + "целительное зелье(x"+str(inventory.count(1))+")\n"+Style.RESET_ALL
	if 2 in inventory: strInventory+=Fore.RED+ "уселитель урона(x"+str(inventory.count(2))+")\n"+Style.RESET_ALL
	if 3 in inventory: strInventory+=Fore.YELLOW+"лёгкая броня\n"+Style.RESET_ALL
	if 4 in inventory: strInventory+=Fore.CYAN+"средняя броня\n"+Style.RESET_ALL
	if 5 in inventory: strInventory+=Fore.MAGENTA+"тяжёлая броня\n"+Style.RESET_ALL
	return strInventory

def getEnemyMeetString(enemyNumber):
	strEnemy = "Бродя по лесу, ты наткнулся на "
	if enemyNumber == 1: 
		strEnemy+=Fore.RED+"воина орка"+Style.RESET_ALL+".\n"
	elif enemyNumber == 2: 
		strEnemy+=Fore.RED+"лучника орка"+Style.RESET_ALL+".\n"
	elif enemyNumber == 3:
		strEnemy+=Fore.RED+"воина эльфа"+Style.RESET_ALL+".\n"
	elif enemyNumber == 4:
		strEnemy+=Fore.RED+"гоблина"+Style.RESET_ALL+".\n"
	else:
		strEnemy+=Fore.RED+"лучника эльфа"+Style.RESET_ALL+".\n"
	return strEnemy

def getBattleString(enemyNumber):
	strBattle = "Драка с "	
	if enemyNumber == 1: 
		strBattle+=Fore.RED+"воином орком"+Style.RESET_ALL+".\n"
	elif enemyNumber == 2: 
		strBattle+=Fore.RED+"лучником орком"+Style.RESET_ALL+".\n"
	elif enemyNumber == 3:
		strBattle+=Fore.RED+"воином эльфом"+Style.RESET_ALL+".\n"
	elif enemyNumber == 4:
		strBattle+=Fore.RED+"гоблином"+Style.RESET_ALL+".\n"
	else:
		strBattle+=Fore.RED+"лучником эльфом"+Style.RESET_ALL+".\n"
	return strBattle

def getEnemyStats(enemyNumber, enemy):
	strEnemy="Противник: здоровье: "+Fore.RED+str(enemy[0])+Style.RESET_ALL+", "
	strEnemy+="урон: "+Fore.RED+str(enemy[1])+Style.RESET_ALL+", "
	strEnemy+="сопротивляемость урону: "+Fore.YELLOW+str(enemy[2])+Style.RESET_ALL+"."
	return strEnemy

def reset():	
	gold=5000
	if raca==1:
		if role==1:me=list(orkArcher)
		else: me=list(orkVarior)
	elif raca==2:
		if role==1:me=list(elfArcher)
		else:me=list(elfVarior)
	else: me=list(goblin)
	inventory=[] #heal=1, boostDamage=2, lightArmor(1.2)=3, middleArmor(1.5)=4, weightyArmor(1.7)=5

def saveGame():
	global gold
	global me
	global inventory
	global name
	os.system("cls")
	print("0)Отмена\n1)Новое сохранение")
	filesAtRoot = os.listdir()
	hasSaves = "saves" in filesAtRoot
	filesAtSaves = []
	if hasSaves:
		filesAtSaves = os.listdir("saves")
		if len(filesAtSaves) == 0: 
			hasSaves = False
			os.rmdir("saves")
		else:
			os.chdir("saves")
			numberOfSaveInMenu = 2
			for file in filesAtSaves:
				print(str(numberOfSaveInMenu) + ")" + file)
				numberOfSaveInMenu+= 1
	if not hasSaves: 
		print(Fore.RED + "Нет сохранений!" + Style.RESET_ALL)
	action = int(input())
	if action == 0 or action - 2 > len(filesAtSaves): 
		os.chdir("..")
		return		
	elif action == 1:
		if not hasSaves: 
			os.mkdir("saves")
			os.chdir("saves")
		filename = str(datetime.datetime.today().replace(microsecond = 0)).replace(":", "-") + ".txt"
		saveFile = open(filename, "w")
		saveFile.write(str(me) + "\n" + str(inventory) + "\n" + str(gold) + "\n" + name)
		saveFile.close()
	else:
		fileNumber = action - 2
		filename = filesAtSaves[fileNumber]
		saveFile = open(filename, "w")
		saveFile.write(str(me) + "\n" + str(inventory) + "\n" + str(gold) + "\n" + name)
		saveFile.close()
	os.chdir("..")


leaveGame = False
newGame = True
maxHealth = 0
while not leaveGame:
	if newGame:	
		startGame()
		maxHealth = me[0]
	os.system("cls")
	if raca < 3:
		print("Ты находишься в главном здании своей расы, " + Fore.GREEN + name + Style.RESET_ALL + "!")
	else: print("Ты находишься в убежище, " + Fore.GREEN + name + Style.RESET_ALL + "!\n")
	print("Здоровья: " + Fore.GREEN + str(me[0]) + Style.RESET_ALL + ", урон: " + Fore.GREEN + str(me[1]) + Style.RESET_ALL + ", сопротивляемость урону: " + Fore.YELLOW + str("%.2f" % me[2]) + Style.RESET_ALL + ". Золото: " + Fore.YELLOW + str(gold) + Style.RESET_ALL + ".\n")
	print(getInventoryString())
	strAction = "Пойти:\n1)в магазин\n2)в лес\n"
	hasSalve = 1 in inventory
	if hasSalve and me[0] < maxHealth: strAction += "Использовать:\n3)Исцеляющее зелье\n"
	hasBoostDamage = 2 in inventory
	hasArmor = 3 in inventory or 4 in inventory or 5 in inventory
	print(strAction)
	print("4)Сохраниться")
	action = int(input())
	if action == 1:
		good = 1
		while good != 0:
			os.system("cls")
			print(getInventoryString())
			print("Вы находитесь у магазина. Золото: " + Fore.YELLOW + str(gold) + Style.RESET_ALL + "\n")
			market = "Выберите товар:\n1)Целительное зелье("+""+Fore.RED+"+50HP"+""+Style.RESET_ALL+")("+""+Fore.YELLOW+"100 G"+Style.RESET_ALL+""+")\n2)Уселитель урона(x2)("+Fore.YELLOW+"400 G"+Style.RESET_ALL+")\n3)Лёгкая броня("+Fore.YELLOW+"300 G"+Style.RESET_ALL+")\n4)Средняя броня("+Fore.YELLOW+"600 G"+Style.RESET_ALL+")\n5)Тяжёлая броня("+Fore.YELLOW+"1200 G"+Style.RESET_ALL+")\n"
			if 3 in inventory: market+="6)Продать лёгкую броню("+""+Fore.YELLOW+"+100G"+""+Style.RESET_ALL+")\n"
			elif 4 in inventory: market+="6)Продать среднюю броню("+""+Fore.YELLOW+"+200G"+""+Style.RESET_ALL+")\n"
			elif 5 in inventory: market+="6)Продать тяжёлую броню("+""+Fore.YELLOW+"+300G"+""+Style.RESET_ALL+")\n"				
			market+="0)Покинуть магазин\n"
			print(market)
			canDoPurchase = False
			while not canDoPurchase:
				good=int(input())
				if good == 0: 
					newGame = False
					break
				elif hasArmor and good > 2:
					if good == 6:
						sellArmor()
						break
					else:
						print(Fore.RED+"Чтобы купить броню, нужно продать, которая имеется!"+Style.RESET_ALL)
				elif good < 6 and good > 0:
					canDoPurchase = doPurchase(good)
	elif action == 2:
		while True:
			os.system("cls")
			enemyNumber = randrange(1, 6)
			if enemyNumber == 1: enemy = list(orkVarior)
			elif enemyNumber == 2: enemy = list(orkArcher)
			elif enemyNumber == 3: enemy = list(elfVarior)
			elif enemyNumber == 4: enemy = list(goblin)
			else: enemy = list(elfArcher)
			print(getEnemyMeetString(enemyNumber))			
			print(getEnemyStats(enemyNumber, enemy))
			print("Ты: здоровье: " + Fore.GREEN + str(me[0]) + Style.RESET_ALL + ", урон: " + Fore.GREEN + str(me[1]) + Style.RESET_ALL + ", сопротивляемость урону: " + Fore.YELLOW + str(me[2]) + Style.RESET_ALL + ".")
			print(getInventoryString())
			print("Твоё действие:\n1)Начать драку\n2)Продолжить ходить по лесу\n3)Покинуть лес")
			action = int(input())
			if action == 2: continue
			if action == 3: 
				newGame = False
				break								
			battleFinished = False
			boostDamageUsed = False
			dead = False
			while not battleFinished:
				os.system("cls")
				print(getBattleString(enemyNumber))
				print(getEnemyStats(enemyNumber, enemy))
				print("Ты: здоровье: " + Fore.GREEN + str(me[0]) + Style.RESET_ALL + ", урон: " + Fore.GREEN + str(me[1]) + Style.RESET_ALL + ", сопротивляемость урону: " + Fore.YELLOW + str(me[2]) + Style.RESET_ALL + ".")
				print(Fore.RED + "1)Нанести урон противнику" + Style.RESET_ALL)
				if hasSalve and me[0] < maxHealth: print(Fore.YELLOW + "2)Выпить исцеляющее зелье(+50HP)" + Style.RESET_ALL)
				if hasBoostDamage and not boostDamageUsed: print(Fore.GREEN + "3)Увеличить урон(x2)" + Style.RESET_ALL)
				#print(Fore.BLUE + "4)Попытаться убежать" + Style.RESET_ALL)
				action = int(input())
				if action == 1:
					enemy[0] -=int(round(me[1] / enemy[2]))
					if enemy[0] <= 0:
						os.system("cls")
						price = randrange(100, 301)
						gold +=price
						print("Удалось победить вашего врага! У него было с собой "+Fore.YELLOW+str(price)+Style.RESET_ALL+" золота. Теперь у тебя "+str(gold)+" золота\n")
						if boostDamageUsed == True: me[1]/=2
						battleFinished = True
						continue
					me[0] -= int(round(enemy[1] / me[2]))						
					if me[0] <= 0:
						battleFinished = True
						dead = True
				elif action == 2:
					hasSalve = 1 in inventory
					if me[0] == maxHealth or not hasSalve:
						hasSalve = False
						continue
					if me[0]+50 > maxHealth: 
						me[0] = maxHealth
						inventory.remove(1)
					elif me[0]+50 <= maxHealth: 
						me[0]+=50
						inventory.remove(1)
					print("Выпили зелье")
				elif action == 3:
					if boostDamageUsed: continue
					else: 
						me[1]*=2						
						boostDamageUsed = True						
						inventory.remove(2)
						if not(2 in inventory): hasBoostDamage = False
			if dead == False:
				print("1)Продолжить бродить по лесу\n2)Покинуть лес\n")
				action = int(input())
				boostDamageUsed = False
				if action == 1: continue
				else: 
					newGame = False
					break
			else:
				os.system("cls")
				print(Fore.RED+ "Вы умерли!\n"+Style.RESET_ALL)
				action = int(input("1)Начать заного\n2)Выйти из игры\n"))
				if action == 1: 
					newGame = True
					break
				else: exit()
	elif action == 3:
		if me[0] == maxHealth or not(1 in inventory): continue
		if me[0] + 50 >= maxHealth: 
			me[0] = maxHealth
			inventory.remove(1)
		elif me[0] + 50 < maxHealth: 
			me[0]+= 50
			inventory.remove(1)
	elif action == 4:
		saveGame()
		newGame = False