open Core
include Core.Char

let equal_ci c1 c2 = phys_equal (Char.lowercase c1) (Char.lowercase c2)
