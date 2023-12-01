# HW7: Induction

## Question 1: Induction on lists

### Question 1.a

Prove that 
If `a,acc : int` and `ls : int list`, then
`a + sum_tr ls acc = sum_tr ls (a + acc)`

Proof by Induction on ls

Base Case: ls = []

WTS: a + sum_tr [] acc = sum_tr [] (a + acc)

LHS = a + sum_tr [] acc
	= a + acc			--by definition of sum_tr

RHS = sum_tr [] (a + acc)
	= a + acc			--by definition of sum_tr
	= LHS!

########################

Step Case: ls = x :: xs

WTS: a + sum_tr (x :: xs) acc = sum_tr (x :: xs) (a + acc)

IH: a + sum_tr (xs) acc = sum_tr (xs) (a + acc)

LHS = a + sum_tr (x :: xs) acc
	= a + sum_tr xs (x + acc)	--by definition of sum_tr
	= sum_tr (xs) (a + (x + acc)) -- IH

RHS = sum_tr (x :: xs) (a + acc)
	= sum_tr (xs) (x + (a + acc)) -- by deifnition of sum_tr
	= sum_tr (xs) (a + (x + acc)) -- commutative additon
	= LHS

QED



### Question 1.b

Prove that
If `l1,l2 : int list` and `acc : int` then
`sum_tr (l1 @ l2) acc = sum_tr l1 (sum_tr l2 acc)`

Induction on l1.

Base Case: l1 = []

WTS: sum_tr ([] @ l2) acc = sum_tr [] (sum_tr l2 acc)

LHS = sum_tr ([] @ l2) acc
	= sum_tr (l2) acc 		-- by @ definition proven in class

RHS = sum_tr [] (sum_tr l2 acc)
	= sum_tr l2 acc 		-- by definition of sum_tr
	= LHS

########################

Step Case: l1 = x :: xs

WTS: sum_tr (x :: xs @ l2) acc = sum_tr x :: xs (sum_tr l2 acc)
IH: sum_tr (xs @ l2) acc = sum_tr xs (sum_tr l2 acc)

LHS = sum_tr ((x :: xs) @ l2) acc
	= sum_tr (x :: (xs @ l2)) acc 			-- by definition of @
	= sum_tr (xs @ l2) (x + acc) 			-- by definition of sum_tr
	= sum_tr xs (sum_tr l2 (x + acc)) 		-- IH

RHS = sum_tr x :: xs (sum_tr l2 acc)
	= sum_tr xs (x + sum_tr l2 acc) 		-- by definition of sum_tr
	= sum_tr xs (sum_tr l2 (x + acc)) 		-- by Theorem 1
	= LHS

QED.

### Question 1.c

Prove that
If `ls : int list` and `acc : int` then
`acc + sum ls = sum_tr (rev ls) acc`

Induction on ls.

Base Case: ls = []

WTS: acc + sum [] = sum_tr (rev []) acc

LHS = acc + sum []
	= acc + 0				-- by definition of sum
	= acc

RHS = sum_tr (rev []) acc
	= sum_tr ([]) acc		-- by definition of rev
	= acc					-- by definition of sum_tr
	= LHS

###############

Inductive Step: ls = x :: xs

WTS: acc + sum x :: xs = sum_tr (rev x :: xs) acc
IH: acc + sum xs = sum_tr (rev xs) acc

LHS = acc + sum x :: xs
	= acc + (x + sum xs) 					--by definition of sum

RHS = sum_tr (rev x :: xs) acc
	= sum_tr (rev xs @ [x]) acc 			-- by definition of rev 
	= sum_tr(rev xs) (sum_tr([x] acc))		--Theorem 2
	= sum_tr(rev xs) (sum_tr([] (x + acc))) -- by definition of sum_tr
	= sum_tr(rev xs) (x + acc) 				-- by definition of sum_tr
	= (x + acc) + sum xs 					--IH backwards!
	= acc + x + sum xs 						--commutative addition
	= LHS

QED.



## Question 2

Prove that 
If `t : tree` then `height t = height' t`

Induction on t.

Case: t = Empty

WTS: height Empty = height' Empty

LHS = height Empty
	= 0				-- by definition of height

RHS = height' Empty
	= 0				-- by definition of height' 
	= LHS


#############

Case: t = Node (l,r)

WTS: height Node (l,r) = height' Node(l,r)

IH1: height l = height' l
IH2: height r = height' r

LHS = height Node(l,r)
	= 1 + max (height l) (height r)		-- by definition of height
	= 1 + max (height' l) (height r) 	-- IH1
	= 1 + max (height' l) (height' r) 	-- IH2
	= max (height' l + 1) (height' r + 1) -- by definition of Lemma

RHS = height' Node(l,r)
	= max (height' l + 1) (height' r + 1) -- by definition of height'
	= LHS

QED.




## Question 3

Prove that
If `t : int tree` then
`inorder_traversal_1 t = inorder_traversal_2 t []`

Lemma: inorder_traversal_1 t @ acc = inorder_traversal_2 t acc

Induction on t

Case: t = Empty

WTS: inorder_traversal_1 Empty @ acc = inorder_traversal_2 Empty acc

LHS = inorder_traversal_1 Empty @ acc
	= [] @ acc 							-- definition of inorder_traversal_1
	= acc								-- definition of @ seen in class

RHS = inorder_traversal_2 Empty acc
	= acc								-- defiinition of inorder_traversal2
	= LHS

##########

Case: t = Node (l, x, r)

IH1: inorder_traversal_1 l @ acc = inorder_traversal_2 l acc
IH2: inorder_traversal_1 r @ acc = inorder_traversal_2 r acc

WTS: inorder_traversal_1 (Node (l, x, r)) @ acc = inorder_traversal_2 (Node (l, x, r)) acc

LHS = inorder_traversal_1 (Node (l, x, r)) @ acc
	= (inorder_traversal_1 l) @ [x] @ (inorder_traversal_1 r) @ acc --by definition of inorder_traversal_1
	= (inorder_traversal_1 l) @ [x] @ (inorder_traversal_2 r acc)   --by IH2
	= (inorder_traversal_1 l) @ ([x] @ (inorder_traversal_2 r acc)) --by associativity of @
	= (inorder_traversal_1 l) @ (x :: inorder_traversal_2 r acc)	--Definition of @ with a single element list

RHS = inorder_traversal_2 (Node (l, x, r)) acc
	= inorder_traversal_2 l (x :: (inorder_traversal_2 r acc)) 		--by definition of inorder_traversal_2
	= inorder_traversal_1 l @ (x :: (inorder_traversal_2 r acc))    --by IH1 backwards!
	= LHS

Done with Lemma.

Therefore, inorder_traversal_1 t = inorder_traversal_2 t [] holds true given Lemma with acc = []

QED.
