import os
import sys
from datetime import datetime


# =========================================================
def docs(*args):
	helpdocs="""Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics"""
	print(helpdocs)

# ========================================================
def addTodo(todoItems):

	try:
		assert len(todoItems)!=0 	#handling ./todo add <missingTodoString> exception
		with open("todo.txt",'a') as todoFile:
			for todo in todoItems:
				todoFile.write(todo+"\n")
				print("Added todo: \"{}\"".format(todo))

	
	except AssertionError:
		print("Error: Missing todo string. Nothing added!")

	

# ========================================================
def pendingTodo(*args):

	todoItems = []
	todoItemNo = 0

	if(os.path.isfile("todo.txt")):
		with open("todo.txt",'r') as todoFile:
			todoItems = list(reversed(todoFile.readlines()))
			todoItemNo= len(todoItems)
	
		if(todoItemNo>0):
			for todo in todoItems:
					print("[{}] {}".format(todoItemNo,todo),end="")
					todoItemNo-=1
		else :
			print("There are no pending todos!")

	else :
		print("There are no pending todos!")



# =======================================================
# Handles multiple delete => ./todo del 2 3 4
def deleteTodo(todoItemNoList):

	todoItemNoList = list(map(int ,todoItemNoList))
	todoItemNoList.sort()
	ItemNoOffset = 0	# to get updated todoItemNo 

	if(todoItemNoList==[]):
		print("Error: Missing NUMBER for deleting todo.")
	
	for todoItemNo in todoItemNoList:
		
		if(todoItemNo != 0):
			todoItemNo -= ItemNoOffset
		
		isDeleted , taskName , todoItemNo = removeTask(todoItemNo)

		if(isDeleted):
			print("Deleted todo #{}".format(todoItemNo+ItemNoOffset))
		
		# elif(todoItemNo==None):
		# 	print("Error: Missing NUMBER for deleting todo.")
		
		else:
			print("Error: todo #{} does not exist. Nothing deleted.".format(todoItemNo+ItemNoOffset))

		if(todoItemNo != 0):
			ItemNoOffset += 1

# =======================================================
# args => list of todoItemNo
def doneTodo(todoItemNoList):
	todoItemNoList = list(map(int ,todoItemNoList))
	todoItemNoList.sort()
	ItemNoOffset = 0	# to get updated todoItemNo 

	if(todoItemNoList==[]):
		print("Error: Missing NUMBER for marking todo as done.")

	for todoItemNo in todoItemNoList:
		
		if(todoItemNo != 0):
			todoItemNo -= ItemNoOffset	
		
		isDone , taskName , todoItemNo = removeTask(todoItemNo)
		
		if(isDone):
			with open("done.txt",'a+') as todoFile:
				currentDate = datetime.now().date().isoformat()
				todoFile.write("x {} {}".format(currentDate,taskName))
				print("Marked todo #{} as done.".format(todoItemNo+ItemNoOffset))

		# elif(todoItemNo==None) :
		# 	print("Error: Missing NUMBER for marking todo as done.")
		
		else:
			print("Error: todo #{} does not exist.".format(todoItemNo+ItemNoOffset))

		if(todoItemNo != 0):
			ItemNoOffset += 1


# ========================================================
# args => list of todoItemNo
# Remove a task and return (status,taskName,todoItemNo)
# helper function for deleteTodo() , doneTodo()
def removeTask(todoItemNo):

	status = False
	taskName = ""
	todoItems = ["todo_txt_file"]

	try:
		assert todoItemNo != 0
		with open("todo.txt",'r+') as todoFile:
			todoItems += todoFile.readlines()
			taskName = todoItems[todoItemNo]
			del todoItems[todoItemNo]
			todoFile.truncate(0)
			todoFile.flush()
			todoFile.seek(0)
			for todo in todoItems[1:]:
				todoFile.write(todo)

			status=True

	except (IndexError,AssertionError,FileNotFoundError) as err:
		pass

	return (status,taskName,todoItemNo)




# ========================================================
# output format => YYYY-MM-DD Pending : 5 Completed : 10
def reportTodo(*args):

	pendingTodos = 0
	doneTodos = 0

	try:
		with open("todo.txt",'r') as todoFile:
			pendingTodos = len(todoFile.readlines())
	except FileNotFoundError:
		pass

	try:
		with open("done.txt",'r') as doneFile:
			doneTodos = len(doneFile.readlines())
	except FileNotFoundError:
		pass
	
	currentDate = datetime.now().date().isoformat()
	print("{} Pending : {} Completed : {}".format(currentDate,pendingTodos,doneTodos))


# ========================================================
def cmdSwitcher(args):
	
	cmd,*args = args
	
	cmds = {
		'help'   : docs,
		'add'    : addTodo,
		'ls'     : pendingTodo,
		'del'    : deleteTodo,
		'done'   : doneTodo,
		'report' : reportTodo,
	}

	cmd = cmds.get(cmd,docs)
	return cmd(args)


# ========================================================
# Starting point
if(len(sys.argv)==1): docs()
else: cmdSwitcher(sys.argv[1:])


