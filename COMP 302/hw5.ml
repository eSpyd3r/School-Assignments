(* Question 1 : partition an int list into two lists of equal sum *)
(* TODO: test cases *)
let partition_option_tests : (int list * (int list * int list) option) list = [ 
  ([1; 2; 3;], Some ([1; 2], [3]));
  ([], Some ([], []));
  ([1; 2; 4], None);
]

(* TODO: implement partition *)
let partition (ns : int list) : (int list * int list) =
  let total_sum = sum ns in
  let rec find_partition acc left right remaining =
    match remaining with
    | [] ->
        (* Sum of ns is double of the sums of each partition *)
        if acc * 2 = total_sum then (left, right)
        else 
          raise NoPartitionFound 
    | x::xs ->
        let left' = x :: left in 
        let right' = right in
        try
          find_partition (acc + x) left' right' xs
        with NoPartitionFound ->
          find_partition acc left (x::right) xs
  in
  try find_partition 0 [] [] ns
  with NoPartitionFound ->
    raise NoPartitionFound

(* this function turns the output of partition into a type option *)
(* the tests you write will be tested against this function *)
(* this is meant to allow you to write success and failure tests *)  
let partition_option (ns : int list) : (int list * int list) option =
  try Some (partition ns) with
  | NoPartitionFound -> None


(* Question 2A: find a list of int from distinct tuples that add up to tot *)
(*TODO: test cases *)
let choice_sum_option_tests : ((int * ((int * int) list)) * (int list) option) list = [
  ((6, [(1, 2); (3, 4)]), Some [2; 4]);
  ((1, [(1, 2)]), Some [1]);
  ((0, [(1, 1); (0, 2); (0, 3)]), None);
  ((10, [(0, 5); (0, 5); (0, 5)]), Some [5; 5; 0]);
  ((0, []), Some []);
  ((1, []), None)
]

(* TODO: implement subset_sum_Q2A *)
let choice_sum (n : int) (tuples : (int * int) list) : int list =
  let rec choice_sum_helper n tuples tuple_elements =
    match tuples with
    | [] ->
        if sum tuple_elements = n then tuple_elements
        else
          raise NoSumFound
    | (l,r)::other_tuples ->
        try
          choice_sum_helper n other_tuples (l::tuple_elements)
        with NoSumFound ->
          choice_sum_helper n other_tuples (r::tuple_elements) 
  in 
  try choice_sum_helper n tuples []
  with NoSumFound -> raise NoSumFound

(* this function turns the output of choice_sum into a type option *)
(* the tests you write will be tested against this function *)
(* this is meant to allow you to write success and failure tests *)
let choice_sum_option (n : int) (tuples : (int * int) list) : int list option =
  try Some (choice_sum n tuples) with
  | NoSumFound -> None

(* Question 2B: find a subset of tuple that add up to a given tuple *)
(* TODO: test cases *)
let subset_sum_option_tests : (((int * int) * ((int * int) list)) * ((int * int) list option)) list = [
  (((3, 6), [(1, 2); (2, 4)]), Some [(1, 2); (2, 4)]);
  (((4, 6), [(1, 2); (2, 4)]), None);
  (((0, 0), []), Some []);
  (((1, 1), [(1, 1)]), Some [(1, 1)]);
  (((0, 0), []), Some []);
  (((3, 6), [(1, 2); (2, 3); (2, 4) ]), Some [(1, 2); (2, 4)]);
]

(* TODO: implement subset_sum_Q2B_helper *)
let subset_sum (target: (int * int)) (tuples : (int * int) list) : (int * int) list =
  let rec subset_sum_Q2B_helper target tuples new_tuples_list = 
    match tuples with
    |[] -> 
        if target = (0,0) then new_tuples_list
        else raise NoSubsetFound
    |(l,r)::other_tuples ->
        match target with
        |(x,y) when (x < 0 || y < 0) -> raise NoSubsetFound
        |(x,y) ->
            (* From the hint, there's no need to use sum! Instead, with each tuple in the new list, subtract from target*)
            try subset_sum_Q2B_helper (x-l, y-r) other_tuples ((l,r)::new_tuples_list)
            with NoSubsetFound ->
              subset_sum_Q2B_helper (x,y) other_tuples new_tuples_list
  in
  try subset_sum_Q2B_helper target tuples []
  with NoSubsetFound -> raise NoSubsetFound
  

(* this function turns the output of subset_sum into a type option *)
(* the tests you write will be tested against this function *)        
(* this is meant to allow you to write success and failure tests *)
let subset_sum_option (target : int * int) (tuples : (int * int) list) : (int * int) list option =
  try Some (subset_sum target tuples) with
  | NoSubsetFound -> None
