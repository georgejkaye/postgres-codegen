open! Core
open Alcotest
module Postgres = Lib.Postgres

let composite () =
  let input = "DROP TYPE test_composite;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Composite
         ~if_exists:false "TEST_COMPOSITE" ~cascade:false)

let composite_if_exists () =
  let input = "DROP TYPE IF EXISTS test_composite;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Composite
         ~if_exists:true "TEST_COMPOSITE" ~cascade:false)

let composite_cascade () =
  let input = "DROP TYPE test_composite CASCADE;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Composite
         ~if_exists:false "TEST_COMPOSITE" ~cascade:true)

let function_ () =
  let input = "DROP FUNCTION test_function;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Function
         ~if_exists:false "TEST_FUNCTION" ~cascade:false)

let function_if_exists () =
  let input = "DROP FUNCTION IF EXISTS test_function;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Function
         ~if_exists:true "TEST_FUNCTION" ~cascade:false)

let function_cascade () =
  let input = "DROP FUNCTION test_function CASCADE;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Function
         ~if_exists:false "TEST_FUNCTION" ~cascade:true)

let domain () =
  let input = "DROP DOMAIN test_domain;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Domain ~if_exists:false
         "TEST_DOMAIN" ~cascade:false)

let domain_if_exists () =
  let input = "DROP DOMAIN IF EXISTS test_domain;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Domain ~if_exists:true
         "TEST_DOMAIN" ~cascade:false)

let domain_cascade () =
  let input = "DROP DOMAIN test_domain CASCADE;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Domain ~if_exists:false
         "TEST_DOMAIN" ~cascade:true)

let view () =
  let input = "DROP VIEW test_view;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.View ~if_exists:false
         "TEST_VIEW" ~cascade:false)

let view_if_exists () =
  let input = "DROP VIEW IF EXISTS test_view;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.View ~if_exists:true
         "TEST_VIEW" ~cascade:false)

let view_cascade () =
  let input = "DROP VIEW test_domain CASCADE;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.View ~if_exists:false
         "TEST_DOMAIN" ~cascade:true)

let lowercase () =
  let input = "drop type if exists test_composite cascade;" in
  Process.test_parser ~input
    ~expected:
      (Postgres.Statement.make_drop Postgres.Object_type.Composite
         ~if_exists:true "TEST_COMPOSITE" ~cascade:true)

let tests =
  ( "Parser.Drop",
    [
      test_case "composite" `Quick composite;
      test_case "composite if exists" `Quick composite_if_exists;
      test_case "composite cascade" `Quick composite_cascade;
      test_case "function" `Quick function_;
      test_case "function if exists" `Quick function_if_exists;
      test_case "function cascade" `Quick function_cascade;
      test_case "domain" `Quick domain;
      test_case "domain if exists" `Quick domain_if_exists;
      test_case "domain cascade" `Quick domain_cascade;
      test_case "view" `Quick view;
      test_case "view if exists" `Quick view_if_exists;
      test_case "view cascade" `Quick view_cascade;
      test_case "lowercase" `Quick lowercase;
    ] )
