open Alcotest
open Core
module Postgres = Lib.Postgres

let testable_postgres_type =
  testable Postgres.Types.pp_postgres_type (fun a b ->
      Int.equal (Postgres.Types.compare_postgres_type a b) 0)

let test_postgres_type_of_string input expected =
  check testable_postgres_type
    [%string "testable_postgres_type_of_string_%{input}"] expected
    (Postgres.Types.postgres_type_of_string input);
  check testable_postgres_type
    [%string "testable_postgres_type_of_string_%{input}"] expected
    (Postgres.Types.postgres_type_of_string (String.uppercase input));
  check testable_postgres_type
    [%string "testable_postgres_type_of_string_%{input}"] expected
    (Postgres.Types.postgres_type_of_string (String.lowercase input))

let void () =
  test_postgres_type_of_string "void"
    (Postgres.Types.Primitive Postgres.Types.Void)

let text () =
  test_postgres_type_of_string "text"
    (Postgres.Types.Primitive Postgres.Types.Text)

let integer () =
  test_postgres_type_of_string "integer"
    (Postgres.Types.Primitive Postgres.Types.Integer)

let bigint () =
  test_postgres_type_of_string "bigint"
    (Postgres.Types.Primitive Postgres.Types.Bigint)

let decimal () =
  test_postgres_type_of_string "decimal"
    (Postgres.Types.Primitive Postgres.Types.Decimal)

let numeric () =
  test_postgres_type_of_string "numeric"
    (Postgres.Types.Primitive Postgres.Types.Numeric)

let timestamp () =
  test_postgres_type_of_string "timestamp"
    (Postgres.Types.Primitive Postgres.Types.TimestampWithoutTimeZone)

let timestamp_with_time_zone () =
  test_postgres_type_of_string "timestamp with time zone"
    (Postgres.Types.Primitive Postgres.Types.TimestampWithTimeZone)

let timestamp_without_time_zone () =
  test_postgres_type_of_string "timestamp without time zone"
    (Postgres.Types.Primitive Postgres.Types.TimestampWithoutTimeZone)

let interval () =
  test_postgres_type_of_string "interval"
    (Postgres.Types.Primitive Postgres.Types.Interval)

let daterange () =
  test_postgres_type_of_string "daterange"
    (Postgres.Types.Primitive Postgres.Types.Daterange)

let boolean () =
  test_postgres_type_of_string "boolean"
    (Postgres.Types.Primitive Postgres.Types.Boolean)

let setof_primitive () =
  test_postgres_type_of_string "setof text"
    (Postgres.Types.Setof (Postgres.Types.Primitive Postgres.Types.Text))

let setof_composite () =
  test_postgres_type_of_string "setof test_composite"
    (Postgres.Types.Setof (Postgres.Types.Composite "TEST_COMPOSITE"))

let setof_array () =
  test_postgres_type_of_string "setof text[]"
    (Postgres.Types.Setof
       (Postgres.Types.Array (Postgres.Types.Primitive Postgres.Types.Text)))

let setof_notnull () =
  test_postgres_type_of_string "setof text_notnull"
    (Postgres.Types.Setof
       (Postgres.Types.Notnull (Postgres.Types.Primitive Postgres.Types.Text)))

let notnull_primitive () =
  test_postgres_type_of_string "text_notnull"
    (Postgres.Types.Notnull (Postgres.Types.Primitive Postgres.Types.Text))

let notnull_composite () =
  test_postgres_type_of_string "test_composite_notnull"
    (Postgres.Types.Notnull (Postgres.Types.Composite "TEST_COMPOSITE"))

let array_primitive () =
  test_postgres_type_of_string "text[]"
    (Postgres.Types.Array (Postgres.Types.Primitive Postgres.Types.Text))

let array_composite () =
  test_postgres_type_of_string "test_composite[]"
    (Postgres.Types.Array (Postgres.Types.Composite "TEST_COMPOSITE"))

let array_notnull_primitive () =
  test_postgres_type_of_string "text_notnull[]"
    (Postgres.Types.Array
       (Postgres.Types.Notnull (Postgres.Types.Primitive Postgres.Types.Text)))

let array_notnull_composite () =
  test_postgres_type_of_string "test_composite_notnull[]"
    (Postgres.Types.Array
       (Postgres.Types.Notnull (Postgres.Types.Composite "TEST_COMOSITE")))

let tests =
  ( "Postgres.Types",
    [
      test_case "void" `Quick void;
      test_case "text" `Quick text;
      test_case "integer" `Quick integer;
      test_case "bigint" `Quick bigint;
      test_case "decimal" `Quick decimal;
      test_case "numeric" `Quick numeric;
      test_case "timestamp" `Quick timestamp;
      test_case "timestamp with time zone" `Quick timestamp_with_time_zone;
      test_case "timestamp without time zone" `Quick timestamp_without_time_zone;
      test_case "interval" `Quick interval;
      test_case "daterange" `Quick daterange;
      test_case "boolean" `Quick boolean;
      test_case "setof text" `Quick setof_primitive;
      test_case "setof test_composite" `Quick setof_composite;
      test_case "setof text[]" `Quick setof_array;
      test_case "setof text_notnull" `Quick setof_notnull;
      test_case "text_notnull" `Quick notnull_primitive;
      test_case "test_composite_notnull" `Quick notnull_composite;
      test_case "test_composite_notnull" `Quick notnull_composite;
      test_case "text[]" `Quick array_primitive;
      test_case "test_composite[]" `Quick array_composite;
      test_case "text_notnull[]" `Quick array_notnull_primitive;
      test_case "test_composite_notnull[]" `Quick array_notnull_composite;
    ] )
