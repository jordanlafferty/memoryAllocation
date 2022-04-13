from random import randint


def createNegativeVal(n):
    x = n * 2
    neg = n - x
    return neg


class physicalMemory:
    def __init__(self, size):
        self.size = size
        self.arr = ['_'] * size
        self.arr[0] = createNegativeVal(size)
        self.allocated = []
        self.numOfHoles = [1]
        self.memoryUtilization = []

    def getAverageMemUtilization(self, requests):
        # gets the average memory utilization by adding the amount of memory used for each request
        # and then dividing it by the number of requests
        avg = 0
        for i in range(len(self.memoryUtilization)):
            avg = self.memoryUtilization[i] / self.size + avg
        avg = avg / requests
        print("Average Memory Utilization is : " + str(avg))

    def getAverageSearchTime(self, requests):
        # gets the average search time by adding the amount of holes looked at
        # and then dividing it by the number of requests
        avg = 0
        for i in range(len(self.numOfHoles)):
            avg = self.numOfHoles[i] + avg
        avg = avg / requests
        print("Average Search Time is : " + str(avg))

    def request(self, requests, fitType):
        # randomly decide if you are going to allocate or deallocate
        # you can only deallocate if the allocated array is not empty
        memoryTotal = 0
        completedRequests = 0
        for i in range(requests):
            completedRequests += 1
            # num decides if you will allocate or deallocate
            num = randint(1, 3)
            # if deallocate was chosen and some memory is allocated
            if num == 1 and self.allocated != []:
                # chooses a random allocated block to deallocate
                block = randint(0, len(self.allocated) - 1)
                blockIndex = self.allocated[block]

                # updates the space of memory used since some of it is being deleted
                memoryTotal = memoryTotal - self.arr[blockIndex]
                self.memoryUtilization.append(memoryTotal)

                # deallocates the block
                self.deallocate(block)

            # will allocate a block
            else:
                # decides what size block to allocate
                allocateNum = randint(1, 8)
                # allocates the block and returns the index, if it can't allocate it returns -1
                # does best fit or worst fit
                if fitType == "best":
                    indexOfAllocation = self.bestFitAllocation(allocateNum)
                else:
                    indexOfAllocation = self.worstFitAllocation(allocateNum)

                if indexOfAllocation == -1:
                    # end program because the memory can not be allocated
                    print("This is the array before the last allocation block failed: " + str(self.arr))

                    # gets average search time and memory utilization since program is ending
                    self.getAverageSearchTime(completedRequests)
                    self.getAverageMemUtilization(completedRequests)
                    return 0
                else:
                    # updates the space of memory used since a block is being added
                    memoryTotal = memoryTotal + allocateNum
                    self.memoryUtilization.append(memoryTotal)
                    # show the memory that has been allocated
                    print(str(allocateNum) + " was allocated, this is the updated array: " + str(self.arr))
                    self.allocated.append(indexOfAllocation)
        self.getAverageSearchTime(requests)
        self.getAverageMemUtilization(requests)

    def deallocate(self, index):
        # gets the index of the block that is going to be deallocated
        blockIndex = self.allocated[index]
        # goes to the index of the block and gets its size
        blockSize = self.arr[blockIndex]
        # makes a negative number to show that there is a whole
        neg = createNegativeVal(blockSize)
        self.arr[blockIndex] = neg
        self.allocated.remove(self.allocated[index])
        print("The block of size " + str(blockSize) + " starting at index " + str(blockIndex) + " was deleted: " + str(
            self.arr))
        self.correctArr()

    def worstFitAllocation(self, blockSize):
        fit = 0
        fitIndex = -1

        # counts how many holes were used for the average search time
        count = 0

        # goes through the memory array to find the largest hole to put the memory block
        for i in range(len(self.arr)):
            if self.arr[i] != '_':
                if self.arr[i] < 0:
                    size = abs(self.arr[i])
                    if size >= blockSize:
                        count += 1
                        if fitIndex == -1 or fit < size:
                            fitIndex = i
                            fit = size
        # adds the number of holes searched in order to get the average at the end
        self.numOfHoles.append(count)

        # ends the program if the block can not be allocated
        if fitIndex == -1:
            print("The last memory request of " + str(blockSize) + " was denied and the program has been ended.")
            return fitIndex
        # actually allocates the memory
        else:
            self.allocate(fitIndex, blockSize)
            return fitIndex

    def bestFitAllocation(self, blockSize):
        fit = 0
        fitIndex = -1

        # counts how many holes were used for the average search time
        count = 0

        # goes through the memory array to find the smallest hole to put the memory block
        for i in range(len(self.arr)):
            if self.arr[i] != '_':
                if self.arr[i] < 0:
                    size = abs(self.arr[i])
                    if size >= blockSize:
                        count += 1
                        # looking if the block is the exact same size as the hole
                        if fit == size:
                            fitIndex = i
                            fit = size
                            break
                        elif fitIndex == -1 or fit > size:
                            fitIndex = i
                            fit = size

        # adds the number of holes searched in order to get the average at the end
        self.numOfHoles.append(count)

        # ends the program if the block can not be allocated
        if fitIndex == -1:
            print("The last memory request of " + str(blockSize) + " was denied and the program has been ended.")
            return fitIndex
        # actually allocates the memory
        else:
            self.allocate(fitIndex, blockSize)
            return fitIndex

    def allocate(self, index, blockSize):
        # changes the index to the block size and marks the rest of the block
        self.arr[index] = blockSize
        for i in range(1, blockSize):
            self.arr[i + index] = '_'

        x = index + blockSize
        y = x
        count = 0
        # if there is leftover space in hole that the block was placed
        # make the leftover space a hole
        if y < len(self.arr):
            if self.arr[y] == '_':
                if x != len(self.arr) - 1 and self.arr[x] == '_':
                    while self.arr[x] == '_' and x < len(self.arr) - 1:
                        count += 1
                        x += 1
                    if x == len(self.arr) - 1:
                        count += 1
                    self.arr[y] = createNegativeVal(count)

    def correctArr(self):
        # goes through the array for memory and fixes the holes
        # ex: if there was a hole of size 1 and a hole of size 2
        # next to each other it would become one hole of size 3
        negIndex = -1
        negVal = 0
        j = 0
        x = 0
        # loops through the array seeing if 2 holes are next to each other,
        # and combine if true
        while j < len(self.arr) - 1:
            if self.arr[j] != '_':
                if self.arr[j] < 0 and x == 0:
                    x = 1
                    negIndex = j
                    negVal = self.arr[j]
                elif x == 1 and self.arr[j] < 0:
                    negVal = negVal + self.arr[j]
                    self.arr[j] = '_'
                else:
                    self.arr[negIndex] = negVal
                    x = 0
            elif j == len(self.arr) - 2:
                self.arr[negIndex] = negVal
                self.arr[j] = '_'
                x = 0
            j += 1
        if self.arr[len(self.arr) - 1] == 0:
            self.arr[len(self.arr) - 1] = '_'


# create the space of memory you want
p = physicalMemory(64)
w = physicalMemory(64)

# format requests ( Number of Requests , type of fit)
# type of fit is either "best" or "worst"
print("This is the BEST FIT")
p.request(50, "best")
print("*\n*\n*\nThis is the WORST FIT")
w.request(50, "worst")
