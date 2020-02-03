from multiprocessing import Pool,Manager
import os 

def copyFileTask(name,oldFileName,newFileName,queue):
	#print(name)
	fr = open(oldFileName+"\\"+name)
	#print("**********")
	fw = open(newFileName+"\\"+name,"w")
	#print("----------")
	while True:
		content = fr.read()
		if len(content)==0:
			break
		fw.write(content)
		
	fr.close()
	fw.close()
	
	queue.put(name)
	
def main():
	#获取要拷贝的文件夹名字
	oldFileName = input("请输入需要拷贝的文件夹名字：")
	#创建一个文件夹
	newFileName = oldFileName+"-复件"
	#print(newFileName)
	os.mkdir(newFileName)
	#获取old文件夹中的名字
	fileNames = os.listdir(oldFileName)
	#print(fileNames)

	#使用多进程的方式进行拷贝原文夹中的所有文件到新的文件夹中
	pool = Pool(5)
	queue = Manager().Queue()
	
	for name in fileNames:
		pool.apply_async(copyFileTask,args=(name,oldFileName,newFileName,queue))
	num = 0
	allnum = len(fileNames)
	while True:
		queue.get()
		num +=1
		
		copyRate = num/allnum
		print("拷贝的进度是%.2f%%"%(copyRate*100))
		if num == allnum:
			break
	print("已完成你需要拷贝的文件")	
		
	#pool.close()
	#pool.join()
	
if __name__ == "__main__":
	main()
