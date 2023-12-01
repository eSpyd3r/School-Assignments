(* SECTION 1: Laziness *)

(* Question 1a *)

let rec lazy_insert (v : 'a) (l : 'a lazy_list) : 'a lazy_list =
  match l with
  |LNil -> LCons (v, mk_susp (fun () -> LNil))
  |LCons (x, tail) ->
      if v <= x then LCons (v, mk_susp (fun () -> l))
      else LCons (x, mk_susp (fun () -> lazy_insert v (force (tail))))

(* Question 1b *)

let lazy_ins_sort (l : 'a lazy_list) : 'a lazy_list =
  let rec go (l : 'a lazy_list) (acc : 'a lazy_list) : 'a lazy_list =
    match l, acc with
    |LNil, _ -> acc
    |LCons (x, tail), LNil -> go (force (tail)) (LCons (x, mk_susp (fun () -> LNil)))
    |LCons (x, tail), LCons (accX, accTail) -> go (force (tail)) (lazy_insert x acc)
        
  in go l LNil

(* SECTION 2 : Backtracking *)

(* Question 2a *)

let rec tree_sum (t : int tree) (n : int) : int list =
  match t with
  |Empty -> if n = 0 then [] else raise NoTreeSum
  |Tree (Empty, value, Empty) -> if value = n then [value] else raise NoTreeSum
  |Tree (l, value, r) -> 
      value :: (try tree_sum (l) (n - value) with
          | NoTreeSum -> tree_sum (r) (n - value)) 
              
    


(* Section 3 : References *)

(* Question 3a *)
let ( *= ) (x : int ref) (n : int) : int = 
  x := !x * n; !x

(* Question 3b *)
let make_piggybank () : piggybank =
  let funds = ref 0 in
  let broken = ref false in
  let bal () = if !broken then raise BrokenPiggybank else !funds in
  let add n = if !broken then raise BrokenPiggybank else funds := !funds + n in
  let break () =
    if !broken then raise BrokenPiggybank
    else broken := true; !funds in
  {get_balance = bal; add_to_piggybank = add; break_piggybank = break}

