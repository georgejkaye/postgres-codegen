open Alcotest
open Core
open Lib

let testable_postgres_object =
  testable Postgres.Object.pp_postgres_object (fun a b ->
      Int.equal (Postgres.Object.compare_postgres_object a b) 0)
