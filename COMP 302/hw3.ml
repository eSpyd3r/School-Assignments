(* Hi everyone. All of these problems are generally "one-liners" and have slick solutions. They're quite cute to think
   about but are certainly confusing without the appropriate time and experience that you devote towards reasoning about
   this style. Good luck! :-)  *)

(* For example, if you wanted to use the encoding of five in your test cases, you could define: *)
let five : 'b church = fun s z -> s (s (s (s (s z))))
(* and use 'five' like a constant. You could also just use
 'fun z s -> s (s (s (s (s z))))' directly in the test cases too. *)

(* If you define a personal helper function like int_to_church, use it for your test cases, and see things break, you should
   suspect it and consider hard coding the input cases instead *)



(* Question 1a: Church numeral to integer *)
(* TODO: Test cases *)
let to_int_tests : (int church * int) list = [ (one, 1) ; (zero, 0); (five, 5)]
;;

(* TODO: Implement
   Although the input n is of type int church, please do not be confused. This is due to typechecking reasons, and for
   your purposes, you could pretend n is of type 'b church just like in the other problems.
*)
let to_int (n : int church) : int = 
  n (fun x -> x + 1) 0



(* Question 1b: Determine if a church numeral is zero *)
(* TODO: Test cases *)
let is_zero_tests : ('b church * bool) list = [ (one, false); (zero, true)
                                              ]
;;

(* TODO: Implement *)
let is_zero (n : 'b church) : bool = n (fun _ -> false) true (* if false, not zero *)



(* Question 1d: Determine if a church numeral is odd *)
(* TODO: Test cases *)
let is_odd_tests : ('b church * bool) list = [ (one, true); (five, true); 
                                               ((fun s z -> (s (s z))), false)]                                       
;;

let is_odd (n : 'b church) : bool = (* alternating boolean*)
  n not false


(* Question 1e: Add two church numerals *)
(* TODO: Test cases *)
let add_tests : ( ('b church * 'b church) * 'b church) list = [((one, zero), one); 
                                                               ((one, one),(fun s z -> (s (s z)))) ]
;;

let add (n1 : 'b church) (n2 : 'b church) : 'b church =
  fun s z -> n1 s (n2 s z) (* replacing 'z' in n1 with n2 *)



(* Question 1f: Multiply two church numerals *)
(* TODO: Test cases *)
let mult_tests : ( ('b church * 'b church) * 'b church) list = [ ((zero, five), zero); ((one, one), one);
                                                                 ((one, fun s z -> (s (s z))),(fun s z -> (s (s z))))
                                                               ]
;;

let mult (n1 : 'b church) (n2 : 'b church) : 'b church =
  fun s -> n1 (n2 s)



(* Question 2a: Write a function taking an int and a church and returning the int to the power of the church *)
(* TODO: Test cases *)
let int_pow_church_tests : ((int * 'b church) * int) list = 
  [((3, (fun s z -> s (s z))), 9); 
   ((2, zero), 1);
   ((1, one), 1);
   ((0, zero), 1); 
   ((2, fun s z -> (s (s z))), 4);
   ((0, one), 0);
  ]
;;

let int_pow_church (x : int) (n : 'b church) : int =
  n (fun y -> x * y) 1



(* Question 2b: Write a function taking tuple of church and incrementing both values of the tuple of the value of the church *)
(* TODO: Test cases *)
let swap_add_tests : (('b church * 'b church) * ('b church * 'b church)) list = [
  ((zero, one), (one, one));
  ((one, fun s z -> (s (s z))), ((fun s z -> (s (s z))), (fun s z -> s(s (s z))))) ]
;;

let swap_add (t : ('b church * 'b church)) : ('b church * 'b church) =
  let (a,b) = t in (b, (add a b))



(* Question 2c: Write a function computing the nth term of the Fibonacci suite *)
(* TODO: Test cases *)
let fibo_tests : ('a church * 'b church) list = [
  (zero, zero);
  (one, one);
  ((fun s z -> (s (s z))), one); 
]
;;

let fibo (n : 'a church) : 'b church =
  fst (n (fun (a,b) -> (b, add a b)) (zero, one))
