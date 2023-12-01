(* Question 1 *)

(* TODO: Write a good set of tests for {!q1a_nat_of_int}. *)
let q1a_nat_of_int_tests : (int * nat) list = [
  (0, Z);
  (5, S (S (S (S (S Z)))));
  (10, S (S (S (S (S (S (S (S (S (S Z))))))))));]

(* TODO:  Implement {!q1a_nat_of_int} using a tail-recursive helper. *)
let rec q1a_nat_of_int (n : int) : nat = 
  let rec nat_of_int_helper acc n =
    if n = 0 then acc
    else nat_of_int_helper (S acc) (n-1)
  in
  if n < 0 then
    failwith "Input Must be non-negative" (* Edge case handling although not graded I imagine*)
  else nat_of_int_helper Z n

(* TODO: Write a good set of tests for {!q1b_int_of_nat}. *)
let q1b_int_of_nat_tests : (nat * int) list = [
  (Z, 0);
  (S (S (S (S (S Z)))), 5);
  (S (S (S (S (S (S (S (S (S (S Z))))))))), 10);]

(* TODO:  Implement {!q1b_int_of_nat} using a tail-recursive helper. *)
let rec q1b_int_of_nat (n : nat) : int = 
  let rec int_of_nat_helper n acc = 
    match n with
    | Z -> acc
    | S remaining -> int_of_nat_helper remaining (acc + 1)
  in 
  int_of_nat_helper n 0

(* TODO: Write a good set of tests for {!q1c_add}. *)
let q1c_add_tests : ((nat * nat) * nat) list = [
  ((S (S (S (S (S Z)))), Z), S (S (S (S (S Z))))); (* 5 + 0 = 5 *)
  ((S (S Z),S (S Z)), S (S (S (S Z))))] (* 2 + 2 = 4*)

(* TODO: Implement {!q1c_add}. *)
let rec q1c_add (n : nat) (m : nat) : nat = 
  match n with
  | Z -> m
  | S remaining -> S (q1c_add remaining m)


(* Question 2 *)

(* TODO: Implement {!q2a_neg}. *)
let q2a_neg (e : exp) : exp = 
  Times (
    Const (-1.0),
    e)

(* TODO: Implement {!q2b_minus}. *)
let q2b_minus (e1 : exp) (e2 : exp) : exp = 
  Plus (e1, q2a_neg e2)

(* TODO: Implement {!q2c_pow}. *)
let q2c_pow (e1 : exp) (p : nat) : exp = 
  let rec q2c_helper e1 p = 
    match p with
    | Z -> Const 1.0
    | S remaining -> Times (e1, q2c_helper e1 remaining)
  in q2c_helper e1 p


(* Question 3 *)

(* TODO: Write a good set of tests for {!eval}. *)
let eval_tests : ((float * exp) * float) list = [
  ((1.0, Plus(Plus(Times(Const 2.0, Var ),Times(Const (-1.0), Var)),Const 10.0 )), 11.0 ); (*2x - x/3 + 10*)
  ((1.0, Plus(Plus(Times(Const 2.0, Var ),Times(Const (-1.0), Div (Var, Const 2.0))),Const 10.0 )), 11.5)] (*2x - x/2 + 10*)

(* TODO: Implement {!eval}. *)
let rec eval (a : float) (e : exp) : float = 
  match e with
  | Const x -> x
  | Var -> a
  | Plus (e1, e2) -> eval a e1 +. eval a e2
  | Times (e1, e2) -> eval a e1 *. eval a e2
  | Div (e1, e2) -> eval a e1 /. eval a e2 


(* Question 4 *)

(* TODO: Write a good set of tests for {!diff_tests}. *)
let diff_tests : (exp * exp) list = [
  (Const 2.0, Const 0.0);  (* Constant 2.0*)
  (Var, Const 1.0); (* Derivative of x *)
  ((Plus (Times (Var, Const 2.0), Const 1.0)), (Plus (Plus (Times (Const 1., Const 2.), Times (Var, Const 0.0)), Const 0.0))); (* Derivative of 2x + 1 is 2 + 0*)
  ((Div (Var, Const 2.0)), (Div (Plus (Times (Const 1., Const 2.), Times(Const (-1.0), Times (Var, Const 0.))), Times (Const 2., Const 2.))));] (* Derivative of x/2 is 2/4 *) 

(* TODO: Implement {!diff}. *)
let rec diff (e : exp) : exp = 
  match e with
  | Const _ -> Const 0.0 (* Derivative of constant *)
  | Var -> Const 1.0 (* Derivative of a standalone variable *)
  | Plus (e1, e2) -> Plus (diff e1, diff e2) (* The Sum rule *)
  | Times (e1, e2) -> Plus (Times (diff e1, e2), Times (e1, diff e2)) (* Product Rule *)
  | Div (e1, e2) -> Div ( Plus (Times (diff e1, e2), Times(Const (-1.0), Times (e1, diff e2))), Times (e2, e2)) (* quotient rule *)
  
