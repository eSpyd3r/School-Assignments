(* Question 1: Tree Depth *)
(* TODO: Write a good set of tests for testing your tree depth function. *)
(* For the whole assignment, you only need to write tests for `int tree`s
   etc. However, your functions must still be suitably polymorphic, and the
   grader will check this. *)
let tree_depth_cps_test_cases : (int tree * int) list =
  [ (Empty, 0);
    (Tree (Empty, 10, Empty), 1);
    (Tree (Tree (Empty, 5, Empty), 10, Tree (Empty, 15, Empty)), 2);
    (Tree (Tree (Tree (Empty, 2, Empty), 5, Empty), 10, Tree (Empty, 15, Empty)), 3)(* Your test cases go here *) ]

(* These are the test cases that will actually be graded, but
   you don't have to modify this. Remember that you only need
   to test with the `id` continuation. `insert_test_continuations`
   (defined in the prelude) adds the `id` continuation to each of
   your test cases. *)
let tree_depth_cps_tests : ((int tree * (int -> int)) * int) list =
  insert_test_continuations tree_depth_cps_test_cases

(* An example of Non-CPS function to find depth of a tree: *)
let rec tree_depth t =
  match t with
  | Empty -> 0
  | Tree (l, _, r) -> 1 + max (tree_depth l) (tree_depth r)

(* TODO: Implement a CPS style tree_depth_cps function.*)
let rec tree_depth_cps (t : 'a tree) (return : int -> 'r) : 'r = 
  match t with
  | Empty -> return 0
  | Tree (l, _, r) -> tree_depth_cps l (fun depth_l -> 
      tree_depth_cps r (fun depth_r ->
          maxk (1 + depth_l) (1 + depth_r) return))

(* Question 2(a): Tree Traversal *)
(* TODO: Write a good set of tests for testing your tree traversal function. *)
let traverse_cps_test_cases : (int tree * int list) list = [
  (Empty, []);
  (Tree (Empty, 10, Empty), [10]);
  (Tree (Tree (Empty, 5, Empty), 10, Tree (Empty, 15, Empty)), [10;5;15]);
];;
let traverse_cps_tests : ((int tree * (int list -> int list)) * int list) list =
  insert_test_continuations traverse_cps_test_cases

(* TODO: Implement a CPS style preorder traversal function. *)
let rec traverse_cps (t : 'a tree) (return : 'a list -> 'r) : 'r = 
  match t with
  | Empty -> return []
  | Tree (l, current, r) -> traverse_cps l (fun left ->
      traverse_cps r (fun right ->
          return (current :: left @ right)))

(* Question 2(b): Max Elements in a Tree *)
(* TODO: Write a good set of tests for testing your tree maximum function. *)
let tree_max_cps_test_cases : (int tree * int) list = [
  (Empty, -1);
  (Tree (Tree (Empty, 1, Empty), 4, Tree (Empty, 2, Empty)), 4);
  (Tree (Tree (Empty, 8, Empty), 3, Tree (Empty, 1, Empty)), 8);
];;
let tree_max_cps_tests : ((int tree * (int -> int)) * int) list =
  insert_test_continuations tree_max_cps_test_cases

(* TODO: Implement a CPS style tree maximum function. *)
let rec tree_max_cps (t : int tree) (return : int -> 'r) : 'r = 
  match t with
  | Empty -> return (-1)
  | Tree (l, current, r) -> tree_max_cps l (fun left -> 
      tree_max_cps r (fun right ->
          let max_left_and_right = if left > right then left else right 
          in
          return (if current > max_left_and_right then current else max_left_and_right)))

(* Question 3: Finding Subtrees *)
(* TODO: Write a good set of tests for your finding subtrees function. *)
(* This time we have two continuations.
`insert_test_option_continuations` will automatically
insert the trivial continuations for testing:
fun x -> Some x, and fun () -> None. *)
let find_subtree_cps_test_cases
  : ((int list * int tree) * int tree option) list =
  [ (* Your test cases go here *) 
    (([], Tree (Empty, 15, Empty)), Some (Tree (Empty, 15, Empty)));
    (([10], Empty), None);
    (([10; 5; 3; 1], Tree (Tree (Tree (Empty, 3, Empty), 5, Tree (Empty, 7, Empty)), 10, Tree (Empty, 15, Empty))), None); 
    (([20], Tree (Tree (Empty, 5, Empty), 10, Tree (Empty, 15, Empty))), None); 
    

  ];;
let find_subtree_cps_tests =
  insert_test_option_continuations find_subtree_cps_test_cases

(* TODO: Implement a CPS style finding subtrees function.*)
let rec find_subtree_cps (ps : 'a list) (t : 'a tree) 
    (succeed : 'a tree -> 'r) (fail : unit -> 'r) : 'r =
  match ps, t with
  | [], _ -> succeed t 
  | _, Empty -> fail ()
  | p_start :: p_end, Tree (l, value, r) ->
      if p_start = value then
        find_subtree_cps p_end l succeed (fun () -> find_subtree_cps p_end r succeed fail)
      else find_subtree_cps ps l succeed (fun () -> find_subtree_cps ps r succeed fail)