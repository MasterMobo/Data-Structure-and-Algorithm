class TreeNode:
    def __init__(self, key, val=None, left=None, right=None):
        self.key = key
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_tuple(cls,arg):
        '''Creates a binary tree from a tuple
            --------------------------------------------------------------------------------------
            Instructions: TreeNode.from_tuple(tree_tuple)
                +tree_tuple: a tuple in the form (left_sub_tree, node_key, right_sub_tree)\n
                +node_key (int): the key of the node\n
                +left_sub_tree and right_sub_tree: either int or tuples in the same form
            Example: TreeNode.from_tuple((3,4,(None,2,6)))'''
            
        #If node has children
        if isinstance(arg, tuple):
            tree = cls(arg[1])
            tree.left = cls.from_tuple(arg[0])
            tree.right = cls.from_tuple(arg[2])
        #If there's no node
        elif arg == None:
            return None
        #If node is leaf
        else:
            return cls(arg)
        return tree
    
    def to_tuple(self):
        '''Convert binary tree into tuple'''

        #If there's no node
        if self == None:
            return None
        #If node is leaf
        if self.right == None and self.left == None:
            return self.key
        #If node has children
        return (TreeNode.to_tuple(self.left), self.key, TreeNode.to_tuple(self.right)) 
    
    def update(self, new_val):
        '''Update the value of the node'''
        self.val = new_val

    def display_keys(self, level=0):
        '''Visualize the binary tree, read from left to right'''

        #If there's no node
        if self == None:
            return
        #If node is leaf
        if self.right == None and self.left == None:
            print('  '*level + str(self.key))
            return
        #If node has children
        TreeNode.display_keys(self.right, level+1)
        print('  '*level + str(self.key))
        TreeNode.display_keys(self.left, level+1)
    
    def inorder_traverse(self):
        '''Returns a list of all nodes objects in the tree in in-order traversal.
           --------------------------------------------------------------------------
           In-order Traversal:
                1.Traverse the left subtree\n
                2.Traverse the current node\n
                3.Traverse the right subtree'''
        if self == None:
            return []
        return (TreeNode.inorder_traverse(self.left)) + [self] + (TreeNode.inorder_traverse(self.right))


    def preorder_traverse(self):
        '''Returns a list of all nodes objects in the tree in pre-order traversal.
           --------------------------------------------------------------------------
           Pre-order Traversal:
                1.Traverse the current node\n
                2.Traverse the left subtree\n
                3.Traverse the right subtree'''

        if self == None:
            return []
        return [self] + (TreeNode.preorder_traverse(self.left)) + (TreeNode.preorder_traverse(self.right))

    
    def postorder_traverse(self):
        '''Returns a list of all nodes objects in the tree in post-order traversal.
           --------------------------------------------------------------------------
           Post-order Traversal:
                1.Traverse the left subtree\n
                2.Traverse the right subtree\n
                3.Traverse the current node'''

        if self == None:
            return []
        return (TreeNode.postorder_traverse(self.left)) + (TreeNode.postorder_traverse(self.right)) + [self]

    def list_keys(self):
        '''Returns a list of all keys in a tree in inorder traversal fashion'''
        return [node.key for node in TreeNode.inorder_traverse(self)]

    def height(self):
        '''Returns the height of the binary tree (the number of nodes along the longest path from the root to the leaf)'''

        if self == None:
            return 0
        return 1 + max(TreeNode.height(self.left), TreeNode.height(self.right)) 
    
    def min_height(self):
        '''Returns the minimum height of the binary tree (the number of nodes along the shortest path from the root to the leaf)'''

        if self == None:
            return 0
        left = TreeNode.min_height(self.left)
        right = TreeNode.min_height(self.right)
        #If either left or right is 0, we dont want to return 1 + min(left, right)
        # just yet because min() would return 0 (which is a None node, doesn't count)
        if left == 0 or right == 0:
            return 1 + left + right
        return 1 + min(left, right)

    def max(self):
        '''Returns the maximum key of a binary tree'''

        if self == None:
            return None
        #Select the maximum value out of this node's key, the left node's key, and the right's (filter out None)
        return max([i for i in [self.key, TreeNode.max(self.left), TreeNode.max(self.right)] if i != None])

    def min(self):
        '''Returns the minimum key of a binary tree'''

        if self == None:
            return None
        #Select the minimum value out of this node's key, the left node's key, and the right's (filter out None)
        return min([i for i in [self.key, TreeNode.min(self.left), TreeNode.min(self.right)] if i != None])

    def size(self):
        '''Returns the total number of nodes in the binary tree'''

        if self == None:
            return 0
        return 1 + TreeNode.size(self.left) + TreeNode.size(self.right)
    
    
    def is_BST(self):
        '''Returns whether the binary tree is a binary search tree
           ------------------------------------------------------------------------
           Binary Search Tree: a binary tree where, for every node:\n
                1.The left subtree only contains keys less than the node's key\n
                2.The right subtree only contains keys greater than the node's key'''
        #If the tree is a BST, the inorder traversal should be an increasing sequence
        #Therefore, we only need to check whether the inorder traversal of the tree is an increasing array or not
        arr = self.list_keys()
        for i in range(1,len(arr)):
            if arr[i-1] > arr[i]:
                return False
        return True
    
    def __str__(self):
        return f'{type(self).__name__}(key={self.key}, val={self.val})'
    def __repr__(self):
        return f'{type(self).__name__}(key={self.key}, val={self.val})'

class BSTNode(TreeNode):
    def __init__(self, *args, **kwargs):
        '''Binary Search Tree: a binary tree where, for every node:\n
                1.The left subtree only contains keys less than the node's key\n
                2.The right subtree only contains keys greater than the node's key'''
        TreeNode.__init__(self, *args, **kwargs)
    
    @classmethod
    def make_balanced_BST_from_keys(cls, lst, lo=0, hi=None):
        '''Creates a balanced binary search tree from a sorted list of (int) keys '''
        #Initialize hi
        if hi == None:
            hi = len(lst) - 1
        
        #Finish condition
        if lo > hi:
            return
        
        #Make the tree, starting from the mid index, partitioning all the way down
        mid = (lo+hi)//2
        tree = BSTNode(lst[mid])
        tree.left = BSTNode.make_balanced_BST_from_keys(lst, lo, mid-1)
        tree.right = BSTNode.make_balanced_BST_from_keys(lst, mid+1, hi)

        return tree
    
    @classmethod
    def make_balanced_BST_from_objs(cls, lst, lo=0, hi=None):
        '''Creates a balanced binary search tree from a list of BSTNode objs'''
        #Initialize hi
        if hi == None:
            hi = len(lst) - 1
        
        #Finish condition
        if lo > hi:
            return
        
        #Make the tree, starting from the mid index, partitioning all the way down
        mid = (lo+hi)//2
        tree = BSTNode(lst[mid].key, lst[mid].val)
        tree.left = BSTNode.make_balanced_BST_from_objs(lst, lo, mid-1)
        tree.right = BSTNode.make_balanced_BST_from_objs(lst, mid+1, hi)

        return tree

    def balance_BST(self):
        '''Returns a balanced BST from an unbalanced BST'''
        #Since we already have a function for making a balanced BST from a sorted list
        #We only need to pass in the inorder traversal of the querried tree to make_balanced_BST
        return BSTNode.make_balanced_BST_from_objs(self.inorder_traverse())

    def find(self, key):
        '''Returns node obj based on key'''
        #If we reach a None node, the key doesn't exist in the tree
        if self == None:
            return None

        #If querried key match the node's key, we've found it!
        if self.key == key:
            return self
        
        #If the querried key is smaller than the current node's key, querried node must be in the left subtree, else, it's in the right subtree.
        if key < self.key:
            return BSTNode.find(self.left, key)
        return BSTNode.find(self.right, key)

    def insert(self, key, val=None):
        '''Correctly inserts a new node within a Binary Search Tree
            ----------------------------------------------------------------
            Instructions: node.insert(key, val=None)
                +node: What node obj to add the new node to 
                +key: The key of the new node
                +val: The value of the new node'''
        
        #If the node is None, it's the correct destination for the new node
        if self == None:
            self = BSTNode(key, val)

        #If the key is smaller than the node's key, keep inserting to the left until hitting a None node
        if key < self.key:
            self.left = BSTNode.insert(self.left, key, val)
        #If the key is bigger than the node's key, keep inserting to the right until hitting a None node
        if key > self.key:
            self.right = BSTNode.insert(self.right,key, val)
        
        return self 

    def is_balanced(self):
        '''Returns whether the Binary Search Tree is balanced
        -----------------------------------------------------
        (Height) Balanced Binary Search Tree: A binary tree in which the height of the left subtree and right subtree of any node does not differ by more than 1'''
        
        def is_balancedUtil(node):
            #Base Case
            if node == None:
                return True
            
            #Calculate the height of ther left and right subtree
            left_height = is_balancedUtil(node.left)
            right_height = is_balancedUtil(node.right)
            
            #If the left/right subtree is not balanced, return False
            if left_height  == False:
                return False
            if right_height == False:
                return False
            
            #Check whether the heights of the two subtrees differ by more than one
            if abs(left_height - right_height) > 1:
                return False
            #If we reach this point, the tree is balanced, return the height of the tree            
            return 1 + max(left_height, right_height)
            
        #One down side of this aproach is it only returns False or the height of the tree,
        #So, we have to create a wrapper function to interpret the height of the tree as "True"
        if is_balancedUtil(self) == False:
            return False
        return True

def main():
    # BINARY TREE TEST CASES:        
    testTree = TreeNode.from_tuple( ((5,12,None),3,(2,7,(None,8,1))) )
    print(testTree.to_tuple())
    testTree.display_keys()
    # testTree.update('This is the new value')
    # print(testTree.inorder_traverse())
    # print(testTree.preorder_traverse())
    # print(testTree.postorder_traverse())
    # print(testTree.height())
    # print(testTree.size())
    # print(testTree.min_height())
    # print(testTree.max())
    # print(testTree.min())
    # print(testTree.is_BST())

    # # BINARY SEARCH TREE TEST CASES:
    # testBST = BSTNode(9)
    # for i in [15,2,12,4,9,5,6,1]:
    #     testBST.insert(i)
    # testBST.display_keys()
    # print(testBST.is_balanced())
    # testBST = testBST.balance_BST()
    # testBST.display_keys()
    # print(testBST.is_balanced())
    # print(testBST.find(12))

if __name__ == "__main__":
    main()