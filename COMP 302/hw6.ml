(* SECTION 1 *)

(*  Question 1.1 *)
let repeat (x : 'a) : 'a stream =
  let rec repeat_helper x =
    { head = x; tail = mk_susp (fun () -> repeat_helper x) }
  in repeat_helper x

(* Question 1.2 *)
let rec filter (f : 'a -> bool) (s : 'a stream) : 'a stream = 
  if f s.head then
    { head = s.head; tail = mk_susp (fun () -> filter f (force s.tail)) }
  else
    filter f (force s.tail)

(* Question 1.3 *)
let rec lucas1 = {
  head = 2; 
  tail = Susp (fun () -> lucas2);
}
and lucas2 = {
  head = 1; 
  tail = Susp (fun () ->  zip_with (+)(lucas1) (lucas2));
}

(* Question 1.4 *)
let rec unfold (f : 'a -> 'b * 'a) (seed : 'a) : 'b stream =
  let (value, new_seed) = f seed in
  {
    head = value;
    tail = mk_susp (fun () -> unfold f new_seed)
  }

(* Question 1.5 *)
let unfold_lucas : int stream =  unfold (fun (a, b) -> (a, (b, a + b))) (2, 1)

(* SECTION 2 *)

(* Question 2.1 *)
let rec scale (s1 : int stream) (n : int) : int stream =
  str_map (fun x -> x * n) s1

let rec merge (s1 : 'a stream) (s2 : 'a stream) : 'a stream =
  if s1.head < s2.head then 
    { head = s1.head; tail = mk_susp (fun() -> merge (force s1.tail) s2) }
  else if s1.head > s2.head then 
    { head = s2.head; tail = mk_susp (fun() -> merge s1 (force s2.tail)) }
  else (* s1.head = s2.head *)
    { head = s1.head; tail = mk_susp (fun() -> merge (force s1.tail) (force s2.tail)) }


(* Question 2.2 *)
(* You have to use Susp instead of mk_susp for this one too. *)
let rec s = {
  head = 1;
  tail = Susp (fun () -> merge_three (scale s 2) (scale s 3) (scale s 5))
} 
and merge_three s1 s2 s3 = 
  merge s1 (merge s2 s3)
