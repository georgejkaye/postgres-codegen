open Core

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

type postgres_type = Primitive of postgres_primitive | Composite of string
[@@deriving show]

let postgres_type_of_string s =
  match String.uppercase s with
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
  | _ -> Composite s
