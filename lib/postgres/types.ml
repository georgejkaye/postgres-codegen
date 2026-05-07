open Util

type postgres_primitive =
  | Void
  | Text
  | Integer
  | Bigint
  | Decimal
  | Numeric
  | Boolean
  | TimestampWithTimeZone
  | TimestampWithoutTimeZone
  | Interval
  | Daterange
[@@deriving show]

type postgres_type =
  | Primitive of postgres_primitive
  | Composite of string
  | Array of postgres_type
  | Notnull of postgres_type
[@@deriving show]

let rec postgres_type_of_string s =
  let upper_s = String.uppercase s in
  match upper_s with
  | "VOID" -> Primitive Void
  | "TEXT" -> Primitive Text
  | "INTEGER" -> Primitive Integer
  | "BIGINT" -> Primitive Bigint
  | "DECIMAL" -> Primitive Decimal
  | "NUMERIC" -> Primitive Numeric
  | "TIMESTAMP" -> Primitive TimestampWithoutTimeZone
  | "TIMESTAMP WITH TIME ZONE" -> Primitive TimestampWithTimeZone
  | "TIMESTAMP WITHOUT TIME ZONE" -> Primitive TimestampWithoutTimeZone
  | "INTERVAL" -> Primitive Interval
  | "DATERANGE" -> Primitive Daterange
  | "BOOLEAN" -> Primitive Boolean
  | _ -> (
      match String.drop_pattern upper_s "_NOTNULL" with
      | Some s -> Notnull (postgres_type_of_string s)
      | None -> (
          match String.drop_pattern upper_s "[]" with
          | Some s -> Array (postgres_type_of_string s)
          | None -> Composite upper_s))
