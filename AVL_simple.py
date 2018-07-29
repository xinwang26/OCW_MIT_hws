class node():
    """unit of the AVL tree"""
    def __init__(self,key,left =None,right=None,parent = None):
        ### seems no need to set parent separately?
        self.key = key ### transition itself have defined comparisons
        self.left = left###need to be a key
        self.right = right
        self.parent = parent
        self.height = -1
    def __repr__(self):
        selfstr = str(self.key) if self.key !=None else "NA"
        leftstr = str(self.left.key) if self.left !=None else "NA"
        rightstr = str(self.right.key) if self.right !=None else "NA"
        parentstr = str(self.parent.key) if self.parent !=None else "NA"
        heightstr = str(self.height)
        return "<self@{self} left:{left} right:{right} parent:{parent} height:{height}>".format(
            self = selfstr,
            left = leftstr,
            right = rightstr,
            parent = parentstr,
            height = heightstr
            )

class BST():
    """Implement balanced Binary search Tree -- no need to AVL since only need to find the smallest"""
    def __init__(self,root=None):
        self.root = root
        self.nodelist = []
        self.nodelist = []
    def leftrotate(self,x = None):
        #print("leftrotate")
        #print("rotating node root:"+ str(self.root.key) + " and left" + str(self.root.right.key))
        x = self.root if x == None else x
        y = x.right
        P = x.parent  #nullable
        A = x.left  #nullable
        B = y.left  #nullable
        C = y.right #nullable but B& C cannot be both null because y need to be higher than A
        #print("rotate root :"+str(x.key))
        #print("rotate root right :"+str(y.key))
        if x == self.root:
            self.root = y
        y.parent = P
        if P != None and P.right == x: P.right = y
        if P != None and P.left == x: P.left =y
        x.right = B
        if B != None: B.parent = x
        y.left = x
        x.parent = y
        self.updateheight(x,onelevelup = True)
        #print("afterrotate:")
        #print(self.nodelist)
    def rightrotate(self,x =  None):
        #print("rightrotate")
        #print("rotating node root:"+ str(self.root.key) + " and left" + str(self.root.left.key))
        x = self.root if x == None else x
        y = x.left
        P = x.parent  #nullable
        A = x.right  #nullable
        B = y.right  #nullable
        C = y.left #nullable but B& C cannot be both null because y need to be higher than A
        #print("rotate root :"+str(x.key))
        #print("rotate root right :"+str(y.key))
        if x == self.root:
            self.root = y
        y.parent = P
        if P != None and P.right == x: P.right = y
        if P != None and P.left == x: P.left =y
        x.left = B
        if B != None: B.parent = x
        y.right = x
        x.parent = y
        self.updateheight(x,onelevelup = True)
        #print("afterrotate:")
        #print(self.nodelist)
    def updateheight(self,node,onelevelup = False):
        #node.height =  0 for insert and -1 for remove
        #print("updateheight")
        node = node.parent if onelevelup == False else node
        while node != None:
            if node.right ==None and node.left != None:
                node.height = node.left.height +1
            elif node.left ==None and node.right != None:
                node.height = node.right.height +1
            elif node.left!= None and node.right!=None:
                node.height = max(node.left.height,node.right.height)+1
            else:
                node.height = 0
            node = node.parent
        #print("afterupdateheight:")
        #print(self.nodelist)

    def rebalance(self,currentnode):
        while currentnode != None:
            temproot = currentnode.parent
            if temproot == None: return
            currentnode = currentnode.parent
            leftsubheight = temproot.left.height if temproot.left != None else 0
            righsubtheight = temproot.right.height if temproot.right != None else 0
            #print("rebalance at "+str(temproot.key)+"with left = "+str(leftsubheight)+" and right = "+str(righsubtheight))
            #print(self.nodelist)
            #print("left height "+str(leftsubheight)+" right height "+str(righsubtheight))
            if  leftsubheight - righsubtheight > 1:
                outheight = temproot.left.left.height if temproot.left.left != None else 0
                inheight = temproot.left.right.height if temproot.left.right != None else 0
                if outheight >= inheight: #outside
                    self.rightrotate(temproot)
                else:#inside
                    self.leftrotate(temproot.left)
                    self.rightrotate(temproot)
            elif leftsubheight - righsubtheight < -1:
                outheight = temproot.right.right.height if temproot.right.right != None else 0
                inheight = temproot.right.left.height if temproot.right.left != None else 0
                if outheight >= inheight: #outside
                    self.leftrotate(temproot)
                else:#inside
                    self.rightrotate(temproot.right)
                    self.leftrotate(temproot)

    def insert(self,newnode):
        #print([(node.key,node.height) for node in self.nodelist])
        #print("inserting"+str(newnode.key))
        self.nodelist.append(newnode)
        newnode.height =0
        if self.root == None:
            self.root = newnode
        else:
            currentnode = self.root
            #print("go"+str(currentnode.key))
            while currentnode != None:
                #print("go"+str(currentnode.key))
                if newnode.key < currentnode.key:
                    if currentnode.left == None:
                        currentnode.left = newnode
                        newnode.parent = currentnode
                        if currentnode.right == None:
                            self.updateheight(currentnode.left)
                        self.rebalance(currentnode.left)
                        # self.updateheightsize()
                        return
                    else:
                        currentnode = currentnode.left
                else:
                    if currentnode.right == None:
                        currentnode.right = newnode
                        newnode.parent = currentnode
                        if currentnode.left == None:
                            self.updateheight(currentnode.right)
                        self.rebalance(currentnode.right)
                        # self.updateheightsize()
                        return
                    else:
                        currentnode = currentnode.right
        # print("inserting "+str(newnode))
        # print(tree.nodelist)
        #print (newnode)
    def min(self):
        if self.root == None:
            print("nothing in the tree")
            return None
        a = self.root
        while a.left != None:
            a = a.left
        #print(a)
        return a, self.nodelist.index(a)
    def removemin(self,key = None):
        if self.root == None or self.nodelist == []:
            print("nothing left in the tree!")
            return None
        key = self.min()[0].key if key == None else key
        print("removing" + str(key))
        #print([node.key for node in self.nodelist])
        i = [node.key for node in self.nodelist].index(key)
        y = self.nodelist[i] #the smallest
        x = y.parent #could be none
        z = y.right #y has no left because it is smallest, y.right could be none
        self.nodelist.remove(y)
        if x != None:
            x.left = z
            if z != None: z.parent = x
        else: #when y is root
            if y.right == None:
                self.root = None
                return None
            z.parent = None
            self.root = y.right
        #self.updateheight(y)  ##blocked these because not much improvment for find min and remove
        #self.rebalance(y)
        # self.updateheightsize()
        return y
    def pop(self):
        temp =  self.min()[0]
        temp.height = -1
        self.removemin()

        return temp
    def __len__(self):
        return len(self.nodelist)

if __name__ == "__main__":
    tree = BST()
    # a = node(15)
    # print(a)
    tree.insert(node(15))
    tree.insert(node(13))
    tree.insert(node(9))
    tree.insert(node(12))
    tree.insert(node(10))
    tree.insert(node(12.5))
    tree.insert(node(20))
    tree.insert(node(16))
    tree.insert(node(18))
    #print(tree.nodelist)
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    tree.removemin()
    #print(tree.min())
    print(tree.nodelist)
    # print(tree.min())
    # tree.removemin()
    # print(tree.nodelist)
    # print(tree.min())
    # tree.removemin()
    # print(tree.nodelist)
    # print(tree.min())
