(* Question 1: Manhattan Distance *)
(* TODO: Write a good set of tests for distance. *)
let distance_tests = [
  (
    ((0, 0), (0, 0)), (* input: two inputs, each a pair, so we have a pair of pairs *)
    0                 (* output: the distance between (0,0) and (0,0) is 0 *)
  );                    (* end each case with a semicolon *)
                        (* Your test cases go here *)
  (
    ((1, 1), (3, 3)), 
    4
  );
  (
    ((3, 3), (1, 1)), 
    4
  );
  (
    ((-3, -3), (-1, -1)), 
    4
  );
  (
    ((-1, -1), (-3, -3)), 
    4
  );
  (
    ((-1, 2), (-3, 3)), 
    3
  );
  (
    ((-3, 3), (-1, 2)), 
    3
  );
]
;;

(* TODO: Correct this implementation so that it compiles and returns
         the correct answers.
*)
let distance (x1, y1) (x2, y2) = 
  let dx = if x1 > x2 then x1 - x2 else x2 - x1 in (* change in x*)
  let dy = if y1 > y2 then y1 - y2 else y2 - y1 in (* change in y*)
  dx + dy

(* Question 2: Binomial *)
(* TODO: Write your own tests for the binomial function.
         See the provided test for how to write test cases.
         Remember that we assume that  n >= k >= 0; you should not write test cases where this assumption is violated.
*)
let binomial_tests = [
  (* Your test cases go here. Correct this incorrect test case for the function. *)
  ((0, 0), 1);
  ((1, 0), 1);
  ((5, 2), 10); 
  ((4, 3), 4);
  ((3, 3), 1);

]

(* TODO: Correct this implementation so that it compiles and returns
         the correct answers.
*)
let rec factorial (n : int) : int = (* as seen in class*)
  if n <= 1 then 1
  else n * factorial (n - 1)
         
let binomial n k =
  if n < 0 || k < 0 || k > n then 0 (* not needed as mentioned in assignment, but why not*)
  else factorial n / (factorial k * factorial (n - k))
  

(* Question 3: Lucas Numbers *)

(* TODO: Write a good set of tests for lucas_tests. *)
let lucas_tests = [
  ((0), 2);
  ((1), 1);
  ((5), 11);
  ((7), 29);
  
]

(* TODO: Implement a tail-recursive helper lucas_helper. *)
let rec lucas_helper n a b =
  if n = 0 then a
  else if n = 1 then b
  else lucas_helper (n - 1) (b) (a + b) 


(* TODO: Implement lucas by calling lucas_helper. *)
let lucas n =
  lucas_helper n 2 1
