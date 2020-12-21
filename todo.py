import os
import sys
from datetime import datetime


# =========================================================
def docs():
	helpdocs="""Usage :-
$ ./todo add "todo item"  # Add a new todo
$ ./todo ls               # Show remaining todos
$ ./todo del NUMBER       # Delete a todo
$ ./todo done NUMBER      # Complete a todo
$ ./todo help             # Show usage
$ ./todo report           # Statistics"""
	print(helpdocs)
	return True

# ========================================================
def addTodo():
	
	try:
		todoItems = sys.argv[2:]
		assert len(todoItems)!=0
		with open("todo.txt",'a') as todoFile:
			for todo in todoItems:
				todoFile.write(todo+"\n")
				print("Added todo: \"{}\"".format(todo))
	
	except AssertionError:
		print("Error: Missing todo string. Nothing added!")
	

# ========================================================
def pendingTodo():

	todoItems = []
	todoItemNo = 0

	if(os.path.isfile("todo.txt")):
		with open("todo.txt",'r') as todoFile:
			todoItems = list(reversed(todoFile.readlines()))
			todoItemNo= len(todoItems)
	
	else: print("There are no pending todos!")

	if(todoItemNo>0):
		for todo in todoItems:
				print("[{}] {}".format(todoItemNo,todo),end="")
				todoItemNo-=1
	else : print("There are no pending todos!")



# =======================================================
def deleteTodo():
	
	isDeleted , taskName , todoItemNo = removeTask()

	if(isDeleted): print("Deleted todo #{}".format(todoItemNo))
	elif(todoItemNo==None) : print("Error: Missing NUMBER for deleting todo.")
	else: print("Error: todo #{} does not exist. Nothing deleted.".format(todoItemNo))


# =======================================================
def doneTodo():
	
	isDone , taskName , todoItemNo = removeTask()
	
	if(isDone):
		with open("done.txt",'a+') as todoFile:
			currentDate = datetime.now().date().isoformat()
			todoFile.write("x {} {}".format(currentDate,taskName))
			print("Marked todo #{} as done.".format(todoItemNo))

	elif(todoItemNo==None) : print("Error: Missing NUMBER for marking todo as done.")
	else: print("Error: todo #{} does not exist.".format(todoItemNo))



# ========================================================
def removeTask():
	
	status = False
	taskName = ""
	todoItemNo = None

	try:
		todoItemNo= int(sys.argv[2])
		assert todoItemNo != 0
		with open("todo.txt",'r+') as todoFile:
			todoItems = todoFile.readlines()
			taskName = todoItems[todoItemNo-1]
			# print(task)
			del todoItems[todoItemNo-1]
			todoFile.truncate(0)
			todoFile.flush()
			todoFile.seek(0)
			for todo in todoItems:
				todoFile.write(todo)

			status=True

	except (IndexError,AssertionError,FileNotFoundError) as err:
		pass

	return (status,taskName,todoItemNo)



# ========================================================
def reportTodo():
	with open("todo.txt",'r') as todoFile:
		pendingTodos = len(todoFile.readlines())

	with open("done.txt",'r') as doneFile:
		doneTodos = len(doneFile.readlines())
	currentDate = datetime.now().date().isoformat()
	print("{} Pending : {} Completed : {}".format(currentDate,pendingTodos,doneTodos))


# ========================================================
def cmdSwitcher(cmd):
	cmds = {
		'help'   : docs,
		'add'    : addTodo,
		'ls'     : pendingTodo,
		'del'    : deleteTodo,
		'done'   : doneTodo,
		'report' : reportTodo,
	}

	cmd = cmds.get(cmd,docs)
	return cmd()



if(len(sys.argv)==1): docs()
else: cmdSwitcher(sys.argv[1])


