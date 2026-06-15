open Core
open Alcotest

let testable_postgres_statement =
  testable Lib.Postgres.Statement.pp_statement (fun a b ->
      Int.equal (Lib.Postgres.Statement.compare_statement a b) 0)
