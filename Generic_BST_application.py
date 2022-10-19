from Binary_Search_Tree import BSTNode
import names
import random
import uuid

#In this example, we create a BST database called "TreeMap" to organise data of class User
class TreeMap:
    def __init__(self):
        self.tree = None
        self.size = 0

    def __setitem__(self, key, val):
        node = BSTNode.find(self.tree, key)
        #If we don't find the key, create a new node with that key and value
        if node == None:
            self.tree = BSTNode.insert(self.tree, key, val)
            self.tree = self.tree.balance_BST()
            self.size += 1
        #If we do find the key, update the value of that node
        else:
            node.update(val)

    def load_data(self, data, chunkSize = 1000):
        '''Load data (generator) into the database in chunks, then balance the tree after every loaded chunk'''
        #Loop through input data
        while True:
            #Loop each chunk
            for _ in range(chunkSize):
                try:
                    entry = next(data)
                    self[entry.id] = entry
                #If we reach the end of the data, rebalance and break out
                except StopIteration:
                    self.tree = self.tree.balance_BST()
                    return
            #Rebalance the tree after every chunk
            self.tree = self.tree.balance_BST()

    def __getitem__(self, key):
        node = self.tree.find(key)
        return node.val if node != None else None

    def __iter__(self):
        #Create a generator object from the inorder traversal
        return (node for node in self.tree.inorder_traverse())
    
    def __len__(self):
        return self.size

    def display(self):
        return self.tree.display_keys()

class User:
    def __init__(self, id,  name, age):
        self.id = id
        self.name = name
        self.age = age

    @classmethod
    def make_Users(cls, num):
        '''Creates a generator of User objs of size num'''
        for _ in range(num):
            yield cls(uuid.uuid4().int, names.get_first_name(), random.randint(1,101))

    def __str__(self):
        return f'User(id={self.id}, name={self.name}, age={self.age})'
    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, age={self.age})'

#EXAMPLES:

#Create users datapoints
users = User.make_Users(500)

#Innitialize the database
database = TreeMap()
#Load all users into the database
database.load_data(users)

#Create and insert a test user into the database for testing purposes
testUser = User(207700000000, 'Johnny Silverhand', 62)
database[testUser.id] = testUser

print(f'There are {database.size} entries')
print(f'The name of the test user is {database[testUser.id].name}')
